"""
WebSocket handler for real-time communication with ROOMie frontend
"""
from flask_socketio import SocketIO, emit
from flask import request
import asyncio
from logger import setup_logger
from emotion_detector import get_cached_emotion, BackgroundEmotionMonitor
from ai_core import generate_response
from tts_output import speak_async, cleanup_audio_file
from conversation_memory import memory
from mood_manager import update_mood
from main import choose_personality
from config import Config
import time

logger = setup_logger("websocket")

# Global emotion monitor
emotion_monitor = None

def init_socketio(app):
    """Initialize SocketIO with Flask app"""
    socketio = SocketIO(
        app, 
        cors_allowed_origins="*",
        # async_mode='threading',  # Let it auto-detect (prefer eventlet)
        logger=True,
        engineio_logger=False
    )
    
    # Store user sessions and processing flags
    user_sessions = {}
    processing_flags = {} # sid -> bool (True = keep processing, False = stop)

    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        logger.info(f"Client connected: {request.sid}")
        emit('connected', {'message': 'Connected to ROOMii backend'})
        
        # Start background emotion monitoring
        global emotion_monitor
        if emotion_monitor is None:
            emotion_monitor = BackgroundEmotionMonitor(interval=2.0)
            emotion_monitor.start()

    @socketio.on('restore_session')
    def handle_restore_session(data):
        """Handle session restoration from local storage"""
        user_id = data.get('user_id')
        username = data.get('username')
        
        if user_id and username:
            # In a real app, we would verify a token here.
            # For now, we trust the client's stored ID/username match.
            user_sessions[request.sid] = user_id
            logger.info(f"Session restored for user: {username} (ID: {user_id})")
            
            # Update emotion monitor with user ID
            global emotion_monitor
            if emotion_monitor:
                emotion_monitor.set_user_id(user_id)

            emit('login_success', {'user_id': user_id, 'username': username})
            
            # Send history immediately
            history = asyncio.run(memory.get_recent_conversations(user_id, 20))
            emit('conversation_history', {'history': history})
            
            # Trigger proactive greeting
            socketio.start_background_task(send_proactive_greeting, user_id, username, request.sid)

    @socketio.on('stop_response')
    def handle_stop_response():
        """Handle request to stop current processing"""
        if request.sid in processing_flags:
            processing_flags[request.sid] = False
            logger.info(f"Stopping processing for session {request.sid}")

    @socketio.on('auth_signup')
    def handle_signup(data):
        """Handle user signup"""
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            emit('auth_error', {'message': 'Username and password required'})
            return
            
        user_id = asyncio.run(memory.create_user(username, password))
        if user_id:
            user_sessions[request.sid] = user_id
            logger.info(f"User signed up: {username} (ID: {user_id})")
            
            # Update emotion monitor with user ID
            global emotion_monitor
            if emotion_monitor:
                emotion_monitor.set_user_id(user_id)

            emit('login_success', {'user_id': user_id, 'username': username})
            # Send history immediately
            history = asyncio.run(memory.get_recent_conversations(user_id, 20))
            emit('conversation_history', {'history': history})
            
            # Trigger proactive greeting
            socketio.start_background_task(send_proactive_greeting, user_id, username, request.sid)
        else:
            emit('auth_error', {'message': 'Username already exists'})

    @socketio.on('auth_login')
    def handle_login(data):
        """Handle user login"""
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            emit('auth_error', {'message': 'Username and password required'})
            return

        user_id = asyncio.run(memory.verify_user(username, password))
        if user_id:
            user_sessions[request.sid] = user_id
            logger.info(f"User logged in: {username} (ID: {user_id})")
            
            # Update emotion monitor with user ID
            global emotion_monitor
            if emotion_monitor:
                emotion_monitor.set_user_id(user_id)

            emit('login_success', {'user_id': user_id, 'username': username})
            # Send history immediately
            history = asyncio.run(memory.get_recent_conversations(user_id, 20))
            emit('conversation_history', {'history': history})
            
            # Trigger proactive greeting
            socketio.start_background_task(send_proactive_greeting, user_id, username, request.sid)
        else:
            emit('auth_error', {'message': 'Invalid username or password'})

    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        if request.sid in user_sessions:
            del user_sessions[request.sid]
        if request.sid in processing_flags:
            del processing_flags[request.sid]
        
        # Stop emotion monitor if no users left (or just stop it for safety in single-user mode)
        global emotion_monitor
        if emotion_monitor:
            emotion_monitor.stop()
            emotion_monitor = None
            
        logger.info(f"Client disconnected: {request.sid}")
    
    @socketio.on('get_emotion')
    def handle_get_emotion():
        """Send current cached emotion"""
        emotion, confidence = get_cached_emotion()
        emit('emotion_update', {
            'emotion': emotion,
            'confidence': float(confidence),
            'timestamp': time.time()
        })
    
    @socketio.on('send_message')
    def handle_message(data):
        """Handle incoming user message"""
        try:
            # Set processing flag to True for this new request
            processing_flags[request.sid] = True
            
            user_message = data.get('message', '').strip()
            if not user_message:
                emit('error', {'message': 'Empty message received'})
                return
            
            user_id = user_sessions.get(request.sid)
            if not user_id:
                emit('error', {'message': 'User not logged in'})
                return

            # --- Check for Commands (Text/Voice) ---
            from voice_commands import voice_handler
            command_data = voice_handler.parse_command(user_message)
            
            if command_data['confidence'] >= 0.7:
                logger.info(f"Command detected in message: {user_message}")
                result = voice_handler.execute_command(command_data)
                
                # --- Handle Special Backend Actions ---
                action = result.get('action')
                
                if action == 'explain_analytics':
                    # Fetch analytics and generate explanation
                    from analytics import analytics_engine
                    summary = asyncio.run(analytics_engine.get_emotion_summary(user_id, days=7))
                    
                    prompt = f"""
                    You are ROOMii. The user asked you to explain their analytics.
                    Here is the data:
                    - Dominant Emotion: {summary.get('dominant_emotion', 'unknown')}
                    - Mood Score: {summary.get('mood_score', 50)}/100
                    - Total Interactions: {summary.get('total_records', 0)}
                    
                    Task: Give a friendly, encouraging summary of how they've been feeling.
                    Keep it under 3 sentences.
                    """
                    
                    response = client.chat.completions.create(
                        model=Config.AI_MODEL,
                        messages=[{"role": "system", "content": prompt}],
                        temperature=0.7,
                        max_tokens=150
                    )
                    explanation = response.choices[0].message.content.strip()
                    
                    # Send explanation as a message
                    emit('message_response', {
                        'text': explanation,
                        'sender': 'bot',
                        'personality': 'Analyst'
                    })
                    
                    # Generate audio
                    socketio.start_background_task(
                        generate_and_send_audio,
                        explanation,
                        "neutral",
                        request.sid
                    )
                    
                    # Also open the dashboard
                    emit('command_response', {
                        'success': True, 
                        'message': 'Here is your analysis.', 
                        'action': 'show_analytics'
                    })
                    return

                elif action == 'add_goal':
                    goal_text = result['data'].get('text')
                    from goals_manager import goals_manager
                    asyncio.run(goals_manager.add_goal(user_id, goal_text))
                    emit('goal_added', {'description': goal_text})
                    
                elif action == 'complete_goal':
                    goal_text = result['data'].get('text')
                    from goals_manager import goals_manager
                    success = asyncio.run(goals_manager.complete_goal(user_id, goal_text))
                    if success:
                        emit('command_response', {
                            'success': True,
                            'message': f"Goal completed: {goal_text}",
                            'action': 'goal_completed'
                        })
                    else:
                        emit('command_response', {
                            'success': False,
                            'message': f"Goal not found: {goal_text}",
                            'is_message': True
                        })
                    return

                elif action == 'stop_game':
                    from games_manager import game_engine
                    game_engine.end_game(user_id)
                    emit('command_response', {
                        'success': True,
                        'message': "Game stopped.",
                        'action': 'game_stopped'
                    })
                    return
                
                # --------------------------------------

                emit('command_response', result)
                return  # Stop processing, don't send to AI
            # ---------------------------------------

            logger.info(f"Received message from user {user_id}: {user_message}")
            
            # Check cancellation
            if not processing_flags.get(request.sid, True):
                logger.info("Processing cancelled by user")
                return

            # Get current emotion from face
            face_emotion, face_confidence = get_cached_emotion()
            
            # Analyze voice tone from text
            from voice_tone_analyzer import analyze_voice_tone, combine_emotions
            voice_emotion, voice_confidence = analyze_voice_tone(text=user_message)
            
            # Combine face and voice emotions
            emotion, confidence = combine_emotions(
                face_emotion, face_confidence,
                voice_emotion, voice_confidence
            )
            
            logger.info(f"Combined emotion: {emotion} (face: {face_emotion}, voice: {voice_emotion})")
            
            sentiment = "neutral"  # TODO: Add sentiment analysis
            
            mood_state, _ = update_mood(emotion, sentiment)
            combined_mood = mood_state["combined_mood"]
            
            # Choose personality
            persona = choose_personality(combined_mood)
            
            # Get conversation context
            context = asyncio.run(memory.get_context_for_ai(
                user_id, 
                max_messages=Config.CONVERSATION_CONTEXT_LENGTH
            ))
            
            # Check cancellation before expensive generation
            if not processing_flags.get(request.sid, True):
                logger.info("Processing cancelled before generation")
                return

            # Fetch analytics context
            analytics_context = ""
            try:
                from analytics import analytics_engine
                summary = asyncio.run(analytics_engine.get_emotion_summary(user_id, days=7))
                
                if summary:
                    analytics_context = f"""
                    User's 7-day Emotion Summary:
                    - Dominant Emotion: {summary.get('dominant_emotion', 'unknown')}
                    - Mood Score: {summary.get('mood_score', 50)}/100
                    - Total Interactions: {summary.get('total_records', 0)}
                    - Emotion Distribution: {summary.get('emotion_distribution', {})}
                    """
            except Exception as e:
                logger.error(f"Failed to fetch analytics context: {e}")

            # Generate AI response
            response_text = generate_response(
                user_message,
                emotion,
                sentiment,
                history=context,
                personality=combined_mood,
                analytics_context=analytics_context
            )
            
            # Check for goal detection tag
            import re
            goal_match = re.search(r'\[GOAL_DETECTED:\s*(.*?)\]', response_text)
            if goal_match:
                new_goal = goal_match.group(1).strip()
                # Remove tag from response
                response_text = response_text.replace(goal_match.group(0), "").strip()
                
                # Add goal automatically
                from goals_manager import goals_manager
                asyncio.run(goals_manager.add_goal(user_id, new_goal))
                logger.info(f"Auto-detected and added goal: {new_goal}")
                
                # Notify frontend
                emit('goal_added', {'description': new_goal})
            
            # Check cancellation before sending
            if not processing_flags.get(request.sid, True):
                logger.info("Processing cancelled before sending response")
                return

            # Send text response immediately
            emit('message_response', {
                'text': response_text,
                'emotion': emotion,
                'mood': combined_mood,
                'personality': persona['name']
            })
            
            # Generate audio in background
            socketio.start_background_task(
                generate_and_send_audio,
                response_text,
                persona['tone'],
                request.sid
            )
            
            # Store conversation (async)
            asyncio.run(memory.add_conversation(
                user_id,
                user_message,
                response_text,
                emotion,
                sentiment,
                combined_mood
            ))
            
            # Store emotion record
            asyncio.run(memory.add_emotion_record(
                user_id,
                emotion,
                confidence,
                combined_mood
            ))
            
        except Exception as e:
            logger.error(f"Message handling error: {e}")
            emit('error', {'message': 'Failed to process message'})
    
    @socketio.on('voice_command')
    def handle_voice_command(data):
        """Handle voice command from user"""
        try:
            from voice_commands import voice_handler
            
            text = data.get('text', '').strip()
            if not text:
                emit('command_response', {
                    'success': False,
                    'message': 'No command text received'
                })
                return
            
            logger.info(f"Processing voice command: {text}")
            
            # Parse command
            command_data = voice_handler.parse_command(text)
            
            # Execute if confidence is high enough
            if command_data['confidence'] >= 0.7:
                result = voice_handler.execute_command(command_data)
                emit('command_response', result)
                logger.info(f"Command executed: {result['action']}")
            else:
                # Not a command, treat as normal message
                emit('command_response', {
                    'success': False,
                    'message': 'Not a recognized command',
                    'is_message': True
                })
        
        except Exception as e:
            logger.error(f"Voice command error: {e}")
            emit('command_response', {
                'success': False,
                'message': 'Failed to process command'
            })
    
    def generate_and_send_audio(text, tone, sid):
        """Background task to generate and send audio"""
        try:
            # Check cancellation before expensive audio generation
            if not processing_flags.get(sid, True):
                logger.info("Audio generation cancelled")
                return

            # Generate audio
            audio_path = asyncio.run(speak_async(text, tone))
            
            # Check cancellation before sending
            if not processing_flags.get(sid, True):
                logger.info("Audio sending cancelled")
                cleanup_audio_file(audio_path)
                return

            if audio_path:
                # Send audio URL
                socketio.emit('audio_ready', {
                    'audio_url': f"/{audio_path}"
                }, room=sid)
                
                # Schedule cleanup
                socketio.sleep(Config.AUDIO_CLEANUP_DELAY)
                cleanup_audio_file(audio_path)
        except Exception as e:
            logger.error(f"Audio generation error: {e}")
    
    @socketio.on('get_conversation_history')
    def handle_get_history(data):
        """Send conversation history"""
        try:
            user_id = user_sessions.get(request.sid)
            if not user_id:
                return
                
            limit = data.get('limit', 20)
            history = asyncio.run(memory.get_recent_conversations(user_id, limit))
            emit('conversation_history', {'history': history})
        except Exception as e:
            logger.error(f"History retrieval error: {e}")
            emit('error', {'message': 'Failed to retrieve history'})
    
    @socketio.on('get_emotion_history')
    def handle_get_emotion_history(data):
        """Send emotion history"""
        try:
            user_id = user_sessions.get(request.sid)
            if not user_id:
                return

            hours = data.get('hours', 24)
            history = asyncio.run(memory.get_emotion_history(user_id, hours))
            emit('emotion_history', {'history': history})
        except Exception as e:
            logger.error(f"Emotion history retrieval error: {e}")
            emit('error', {'message': 'Failed to retrieve emotion history'})

    @socketio.on('clear_history')
    def handle_clear_history():
        """Clear user history"""
        try:
            user_id = user_sessions.get(request.sid)
            if not user_id:
                emit('error', {'message': 'User not logged in'})
                return

            asyncio.run(memory.clear_user_history(user_id))
            emit('history_cleared', {'message': 'Chat history cleared'})
            logger.info(f"History cleared for user {user_id}")
        except Exception as e:
            logger.error(f"History clear error: {e}")
            emit('error', {'message': 'Failed to clear history'})
    
    @socketio.on('get_analytics')
    def handle_get_analytics(data):
        """Send analytics data"""
        try:
            user_id = user_sessions.get(request.sid)
            if not user_id:
                emit('error', {'message': 'User not logged in'})
                return
                
            from analytics import analytics_engine
            
            days = data.get('days', 7)
            
            # Get all analytics data for this user
            summary = asyncio.run(analytics_engine.get_emotion_summary(user_id, days))
            calendar = asyncio.run(analytics_engine.get_mood_calendar(user_id, 30))
            insights = asyncio.run(analytics_engine.generate_insights(user_id))
            trends = asyncio.run(analytics_engine.get_emotion_trends(user_id, days))
            
            emit('analytics_data', {
                'summary': summary,
                'calendar': calendar,
                'insights': insights,
                'trends': trends
            })
            
            logger.info(f"Analytics data sent for user {user_id} ({days} days)")
        except Exception as e:
            logger.error(f"Analytics retrieval error: {e}")
            emit('error', {'message': 'Failed to retrieve analytics'})
    
    @socketio.on('save_calibration_sample')
    def handle_save_calibration_sample(data):
        """Save a calibration sample for user"""
        try:
            user_id = user_sessions.get(request.sid)
            if not user_id:
                emit('error', {'message': 'User not logged in'})
                return
            
            from emotion_calibration import calibrator
            import base64
            
            emotion = data.get('emotion')
            frame_data_b64 = data.get('frame_data')
            
            if not emotion or not frame_data_b64:
                emit('error', {'message': 'Missing emotion or frame data'})
                return
            
            # Decode base64 frame data
            frame_data = base64.b64decode(frame_data_b64)
            
            # Save calibration sample
            success = asyncio.run(calibrator.save_calibration_sample(user_id, emotion, frame_data))
            
            if success:
                emit('calibration_sample_saved', {'emotion': emotion})
                logger.info(f"Calibration sample saved for user {user_id}, emotion: {emotion}")
            else:
                emit('error', {'message': 'Failed to save calibration sample'})
                
        except Exception as e:
            logger.error(f"Calibration sample save error: {e}")
            emit('error', {'message': 'Failed to save calibration sample'})
    
    @socketio.on('check_calibration')
    def handle_check_calibration():
        """Check if user has calibration data"""
        try:
            user_id = user_sessions.get(request.sid)
            if not user_id:
                emit('error', {'message': 'User not logged in'})
                return
            
            from emotion_calibration import calibrator
            
            has_calibration = asyncio.run(calibrator.has_calibration(user_id))
            emit('calibration_status', {'has_calibration': has_calibration})
            
        except Exception as e:
            logger.error(f"Check calibration error: {e}")
            emit('error', {'message': 'Failed to check calibration'})
    
    @socketio.on('clear_calibration')
    def handle_clear_calibration():
        """Clear user's calibration data"""
        try:
            user_id = user_sessions.get(request.sid)
            if not user_id:
                emit('error', {'message': 'User not logged in'})
                return
            
            from emotion_calibration import calibrator
            
            asyncio.run(calibrator.clear_calibration(user_id))
            emit('calibration_cleared', {'message': 'Calibration data cleared'})
            logger.info(f"Calibration cleared for user {user_id}")
            
        except Exception as e:
            logger.error(f"Clear calibration error: {e}")
            emit('error', {'message': 'Failed to clear calibration'})
    
    @socketio.on('start_monitoring')
    def handle_start_monitoring():
        """Start background emotion monitoring"""
        global emotion_monitor
        if emotion_monitor:
            emotion_monitor.start()
        else:
            emotion_monitor = BackgroundEmotionMonitor(interval=2.0)
            emotion_monitor.start()
        
        # Ensure user_id is set if logged in
        user_id = user_sessions.get(request.sid)
        if user_id and emotion_monitor:
            emotion_monitor.set_user_id(user_id)
            
        logger.info("Resumed emotion monitoring")

    @socketio.on('stop_monitoring')
    def handle_stop_monitoring():
        """Stop background emotion monitoring"""
        global emotion_monitor
        if emotion_monitor:
            emotion_monitor.stop()
            # We need to re-initialize it next time because stop() kills the thread
            emotion_monitor = None 
        logger.info("Stopped emotion monitoring")

    @socketio.on('add_goal')
    def handle_add_goal(data):
        """Add a new user goal"""
        try:
            user_id = user_sessions.get(request.sid)
            if not user_id:
                emit('error', {'message': 'User not logged in'})
                return
            
            description = data.get('description')
            if not description:
                return
            
            from goals_manager import goals_manager
            asyncio.run(goals_manager.add_goal(user_id, description))
            emit('goal_added', {'description': description})
            logger.info(f"Goal added for user {user_id}: {description}")
            
        except Exception as e:
            logger.error(f"Add goal error: {e}")
            emit('error', {'message': 'Failed to add goal'})

    @socketio.on('get_goals')
    def handle_get_goals():
        """Get user goals"""
        try:
            user_id = user_sessions.get(request.sid)
            if not user_id:
                return
            
            from goals_manager import goals_manager
            goals = asyncio.run(goals_manager.get_active_goals(user_id))
            emit('user_goals', {'goals': goals})
            
        except Exception as e:
            logger.error(f"Get goals error: {e}")

    # Track active background loops to prevent duplicates
    active_checkin_loops = {} # user_id -> bool

    class ProactiveManager:
        def __init__(self):
            self.last_interaction = {} # user_id -> timestamp
            self.greeting_sent = {} # user_id -> bool (per session/day)
            
        def can_interact(self, user_id, cooldown=120):
            """Check if enough time has passed since last proactive message"""
            last = self.last_interaction.get(user_id, 0)
            return (time.time() - last) > cooldown
            
        def mark_interaction(self, user_id):
            self.last_interaction[user_id] = time.time()
            
        def has_greeted(self, user_id):
            return self.greeting_sent.get(user_id, False)
            
        def set_greeted(self, user_id):
            self.greeting_sent[user_id] = True

    proactive_manager = ProactiveManager()

    def send_proactive_greeting(user_id, username, sid):
        """Generate and send a proactive greeting"""
        try:
            # 1. Check if we already greeted this user recently or in this session
            if proactive_manager.has_greeted(user_id):
                logger.info(f"Skipping greeting for {username}, already greeted.")
                # Ensure loop is running though
                if user_id not in active_checkin_loops:
                    socketio.start_background_task(goal_checkin_loop, user_id, username, sid)
                return

            # 2. Check cooldown just in case
            if not proactive_manager.can_interact(user_id, cooldown=60):
                return

            from goals_manager import goals_manager
            from ai_core import generate_proactive_greeting
            
            # 3. Send "Intro/Normal" greeting first
            # We don't fetch goals for the FIRST greeting to keep it simple/introductory
            greeting_text = f"Welcome back, {username}! I'm ready to help you achieve your goals today."
            
            # Send text
            socketio.emit('message_response', {
                'text': greeting_text,
                'sender': 'bot',
                'personality': 'Friend'
            }, room=sid)
            
            # Generate audio
            socketio.start_background_task(
                generate_and_send_audio,
                greeting_text,
                "cheerful", 
                sid
            )
            
            # Mark as greeted and interacted
            proactive_manager.set_greeted(user_id)
            proactive_manager.mark_interaction(user_id)
            
            # Store in history
            asyncio.run(memory.add_conversation(
                user_id,
                "[Proactive Greeting]",
                greeting_text,
                "neutral",
                "neutral",
                "Friend"
            ))
            
            # 4. Start the goal check-in loop (if not already running)
            if user_id not in active_checkin_loops:
                socketio.start_background_task(goal_checkin_loop, user_id, username, sid)
            
        except Exception as e:
            logger.error(f"Proactive greeting error: {e}")

    def goal_checkin_loop(user_id, username, sid):
        """Background loop to check in on goals randomly"""
        import random
        from goals_manager import goals_manager
        
        if user_id in active_checkin_loops:
            logger.info(f"Goal check-in loop already active for {user_id}")
            return

        active_checkin_loops[user_id] = True
        logger.info(f"Starting goal check-in loop for user {user_id}")
        
        try:
            while sid in user_sessions: # Only run while user is connected
                # Wait for a random interval (Minimum 2 mins = 120s)
                wait_time = random.randint(120, 300) 
                socketio.sleep(wait_time)
                
                if sid not in user_sessions:
                    break
                
                # Check cooldown (ensure 2 mins since ANY proactive message)
                if not proactive_manager.can_interact(user_id, cooldown=120):
                    continue

                # Check for next unasked goal
                goal = asyncio.run(goals_manager.get_next_goal_to_ask(user_id))
                
                if goal:
                    goal_desc = goal['description']
                    logger.info(f"Triggering check-in for goal: {goal_desc}")
                    
                    # Generate check-in message
                    prompt = f"""
                    You are ROOMii. The user is {username}.
                    Goal to check: "{goal_desc}".
                    
                    Task: Ask the user specifically about this goal.
                    - Be motivating but direct.
                    - Ask if they've made progress today.
                    - Keep it short (1-2 sentences).
                    """
                    
                    response = client.chat.completions.create(
                        model=Config.AI_MODEL,
                        messages=[{"role": "system", "content": prompt}],
                        temperature=0.9,
                        max_tokens=100
                    )
                    message_text = response.choices[0].message.content.strip()
                    
                    # Send message
                    socketio.emit('message_response', {
                        'text': message_text,
                        'sender': 'bot',
                        'personality': 'Motivator'
                    }, room=sid)
                    
                    # Generate audio
                    socketio.start_background_task(
                        generate_and_send_audio,
                        message_text,
                        "cheerful",
                        sid
                    )
                    
                    # Mark interaction
                    proactive_manager.mark_interaction(user_id)
                    
                    # Mark as asked
                    asyncio.run(goals_manager.mark_goal_asked(goal['id']))
                    
                    # Store in history
                    asyncio.run(memory.add_conversation(
                        user_id,
                        f"[Goal Check-in: {goal_desc}]",
                        message_text,
                        "neutral",
                        "neutral",
                        "Motivator"
                    ))
                else:
                    logger.debug("No unasked goals found for today.")
                    socketio.sleep(300) # Wait 5 mins before checking again
                    
        except Exception as e:
            logger.error(f"Goal check-in loop error: {e}")
        finally:
            if user_id in active_checkin_loops:
                del active_checkin_loops[user_id]
            logger.info(f"Goal check-in loop stopped for {user_id}")



    # --- Game Events ---
    @socketio.on('start_game')
    def handle_start_game(data):
        try:
            user_id = user_sessions.get(request.sid)
            if not user_id: return
            
            game_type = data.get('game_type')
            from games_manager import game_engine
            
            success, result = game_engine.start_game(user_id, game_type)
            if success:
                emit('game_started', {'game_type': game_type, 'state': result})
                logger.info(f"Game started: {game_type} for user {user_id}")
            else:
                emit('error', {'message': result})
        except Exception as e:
            logger.error(f"Start game error: {e}")

    @socketio.on('game_action')
    def handle_game_action(data):
        try:
            user_id = user_sessions.get(request.sid)
            if not user_id: return
            
            action = data.get('action')
            payload = data.get('data', {})
            from games_manager import game_engine
            
            success, result = game_engine.process_action(user_id, action, payload)
            if success:
                emit('game_update', result)
            else:
                emit('error', {'message': result})
        except Exception as e:
            logger.error(f"Game action error: {e}")

    @socketio.on('end_game')
    def handle_end_game():
        try:
            user_id = user_sessions.get(request.sid)
            if not user_id: return
            
            from games_manager import game_engine
            result = game_engine.end_game(user_id)
            emit('game_ended', result)
            logger.info(f"Game ended for user {user_id}")
        except Exception as e:
            logger.error(f"End game error: {e}")

    return socketio

