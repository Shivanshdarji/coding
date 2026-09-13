from openai import OpenAI
from personality import PERSONALITIES, current_persona
import random
from config import Config
from logger import setup_logger
from typing import AsyncGenerator, List, Dict

logger = setup_logger("ai_core")
client = OpenAI(api_key=Config.OPENAI_API_KEY)

def generate_response(
    user_text: str, 
    emotion: str, 
    sentiment: str, 
    history: List[Dict] = None,
    personality: str = None,
    analytics_context: str = None
) -> str:
    """Generate AI response (non-streaming version for compatibility)"""
    if history is None:
        history = []
    
    if personality is None:
        personality = current_persona
        
    persona = PERSONALITIES.get(personality, PERSONALITIES["neutral"])
    
    prompt = f"""
    You are ROOMii, an emotionally intelligent AI roommate and friend.
    Your personality: {personality} — {persona['style']}.
    Speaking style: {persona['prompt_tone']}
    
    The user's detected emotion is {emotion}, and their voice sentiment is {sentiment}.
    
    **Analytics Context:**
    {analytics_context if analytics_context else "No analytics data available at this time."}
    
    Your goal: respond in a friendly, natural, and emotionally aware way.
    If the user asks about their feelings, mood trends, or emotional history, USE the Analytics Context above to give a specific, data-backed answer.
    
    Keep your tone conversational, not robotic.
    Never repeat exact phrasing — sound like a genuine friend who listens and cares.
    Keep responses concise (2-3 sentences max) unless the user asks for more detail.
    
    **Goal Tracking Instructions:**
    1. If the user explicitly mentions a NEW goal or achievement (e.g., "I want to learn Python", "I ran 5k today"), 
       append this tag at the very end of your response: `[GOAL_DETECTED: <short description>]`.
    2. Occasionally (randomly), if the conversation is casual, ask a small question about their known goals to keep them on track.
    """

    # Build chat history
    chat_history = [{"role": "system", "content": prompt}]
    
    # Add conversation context
    for msg in history[-Config.CONVERSATION_CONTEXT_LENGTH:]:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if content:
            chat_history.append({"role": role, "content": content})
    
    # Add current message
    chat_history.append({"role": "user", "content": user_text})

    try:
        response = client.chat.completions.create(
            model=Config.AI_MODEL,
            messages=chat_history,
            temperature=Config.AI_TEMPERATURE,
            max_tokens=Config.AI_MAX_TOKENS
        )
        
        reply = response.choices[0].message.content.strip()
        logger.info(f"AI response generated: {reply[:50]}...")
        return reply
        
    except Exception as e:
        logger.error(f"AI generation error: {e}")
        return "I'm having trouble thinking right now. Can you try again?"


def generate_proactive_greeting(
    username: str,
    goals: List[str],
    personality: str = None
) -> str:
    """Generate a proactive greeting (mixed: 30% goal-oriented, 70% casual)"""
    if personality is None:
        personality = current_persona
        
    persona = PERSONALITIES.get(personality, PERSONALITIES["neutral"])
    
    # 30% chance to ask about goals, 70% chance for casual greeting
    is_goal_oriented = random.random() < 0.3 and bool(goals)
    
    goals_text = ", ".join(goals) if goals else "general self-improvement"
    
    if is_goal_oriented:
        prompt = f"""
        You are ROOMii, an emotionally intelligent AI roommate.
        Your personality: {personality} — {persona['style']}.
        The user is {username}. Their current goals are: {goals_text}.
        
        Your goal: Start a conversation proactively about their goals.
        1. Greet them warmly.
        2. Ask a specific question about one of their goals (e.g., "Did you work on [Goal] today?").
        3. Be encouraging but keep it short.
        """
    else:
        prompt = f"""
        You are ROOMii, an emotionally intelligent AI roommate.
        Your personality: {personality} — {persona['style']}.
        The user is {username}.
        
        Your goal: Start a casual, friendly conversation.
        1. Greet them warmly (e.g., "Hey, how's it going?", "Good to see you!").
        2. Ask about their day or mood.
        3. Do NOT mention their goals this time. Keep it light.
        """
    
    try:
        response = client.chat.completions.create(
            model=Config.AI_MODEL,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.9, # Higher temperature for variety
            max_tokens=100
        )
        
        reply = response.choices[0].message.content.strip()
        logger.info(f"Proactive greeting generated ({'Goal' if is_goal_oriented else 'Casual'}): {reply[:50]}...")
        return reply
        
    except Exception as e:
        logger.error(f"Proactive greeting error: {e}")
        return f"Hey {username}, hope you're having a great day!"


async def generate_response_stream(
    user_text: str,
    emotion: str,
    sentiment: str,
    history: List[Dict] = None,
    personality: str = None,
    analytics_context: str = None
) -> AsyncGenerator[str, None]:
    """Generate AI response with streaming"""
    if history is None:
        history = []
    
    if personality is None:
        personality = current_persona
        
    persona = PERSONALITIES.get(personality, PERSONALITIES["neutral"])
    
    prompt = f"""
    You are ROOMii, an emotionally intelligent AI roommate and friend.
    Your personality: {personality} — {persona['style']}.
    Speaking style: {persona['prompt_tone']}
    
    The user's detected emotion is {emotion}, and their voice sentiment is {sentiment}.
    
    **Analytics Context:**
    {analytics_context if analytics_context else "No analytics data available at this time."}
    
    Your goal: respond in a friendly, natural, and emotionally aware way.
    If the user asks about their feelings, mood trends, or emotional history, USE the Analytics Context above to give a specific, data-backed answer.
    
    Keep your tone conversational, not robotic.
    Never repeat exact phrasing — sound like a genuine friend who listens and cares.
    Keep responses concise (2-3 sentences max) unless the user asks for more detail.
    """

    # Build chat history
    chat_history = [{"role": "system", "content": prompt}]
    
    # Add conversation context
    for msg in history[-Config.CONVERSATION_CONTEXT_LENGTH:]:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if content:
            chat_history.append({"role": role, "content": content})
    
    # Add current message
    chat_history.append({"role": "user", "content": user_text})

    try:
        stream = client.chat.completions.create(
            model=Config.AI_MODEL,
            messages=chat_history,
            temperature=Config.AI_TEMPERATURE,
            max_tokens=Config.AI_MAX_TOKENS,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                
    except Exception as e:
        logger.error(f"AI streaming error: {e}")
        yield "I'm having trouble thinking right now. Can you try again?"



