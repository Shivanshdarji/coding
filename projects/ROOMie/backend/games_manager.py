import asyncio
import time
import random
from config import Config
from openai import OpenAI

client = OpenAI(api_key=Config.OPENAI_API_KEY)

class GameEngine:
    def __init__(self):
        self.active_game = None # { type, state, data, user_id }
        self.games = {
            "rapid_fire": RapidFireGame(),
            "charades": CharadesGame(),
            "focus_quest": FocusQuestGame()
        }

    def start_game(self, user_id, game_type, **kwargs):
        if game_type not in self.games:
            return False, "Game not found"
        
        self.active_game = self.games[game_type]
        return self.active_game.start(user_id, **kwargs)

    def end_game(self, user_id):
        if self.active_game:
            result = self.active_game.end()
            self.active_game = None
            return result
        return None

    def process_action(self, user_id, action, data):
        if self.active_game:
            return self.active_game.process_action(user_id, action, data)
        return None, "No active game"

    def get_state(self):
        if self.active_game:
            return self.active_game.get_state()
        return None

class RapidFireGame:
    def __init__(self):
        self.is_active = False
        self.start_time = 0
        self.questions_asked = 0
        self.history = []
        self.current_question = ""
        
    def start(self, user_id, **kwargs):
        self.is_active = True
        self.start_time = time.time()
        self.questions_asked = 0
        self.history = []
        self.current_question = "Is it a living thing?" # Initial question
        return True, {
            "message": "Think of an object! I have 2 minutes to guess it.",
            "question": self.current_question,
            "timer": 120
        }

    def process_action(self, user_id, action, data):
        if not self.is_active:
            return False, "Game not active"

        # Check timer
        elapsed = time.time() - self.start_time
        if elapsed > 120:
            return self.end(winner="user")

        if action == "answer":
            answer = data.get("answer", "").lower() # yes, no, maybe, correct
            self.history.append({"q": self.current_question, "a": answer})
            
            if "correct" in answer or "you win" in answer or "yes that's it" in answer:
                return self.end(winner="ai")
            
            # Generate next question
            self.current_question = self._generate_next_question()
            self.questions_asked += 1
            
            return True, {
                "question": self.current_question,
                "time_left": 120 - int(elapsed)
            }
            
        return False, "Invalid action"

    def _generate_next_question(self):
        prompt = f"""
        You are playing 20 Questions. You are the guesser.
        History: {self.history}
        
        Task: Ask the next YES/NO question to narrow down the object.
        - If you are confident, guess the object (e.g., "Is it a toaster?").
        - Keep it short.
        """
        try:
            response = client.chat.completions.create(
                model=Config.AI_MODEL,
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7,
                max_tokens=50
            )
            return response.choices[0].message.content.strip()
        except:
            return "Is it bigger than a breadbox?"

    def end(self, winner="user"):
        self.is_active = False
        msg = "I win! 🎉" if winner == "ai" else "You win! 🏆 Time's up!"
        return True, {"game_over": True, "winner": winner, "message": msg}
        
    def get_state(self):
        if not self.is_active: return None
        return {
            "type": "rapid_fire",
            "question": self.current_question,
            "time_left": 120 - int(time.time() - self.start_time)
        }

class CharadesGame:
    def __init__(self):
        self.is_active = False
        self.target_emotion = ""
        self.score = 0
        
    def start(self, user_id, **kwargs):
        self.is_active = True
        self.score = 0
        self.target_emotion = self._get_random_emotion()
        return True, {
            "message": f"Show me: {self.target_emotion.upper()}!",
            "target": self.target_emotion,
            "score": 0
        }

    def process_action(self, user_id, action, data):
        if not self.is_active: return False, "Game not active"
        
        if action == "check_emotion":
            detected = data.get("emotion")
            if detected == self.target_emotion:
                self.score += 1
                self.target_emotion = self._get_random_emotion()
                return True, {
                    "correct": True,
                    "message": "Correct! Next one...",
                    "target": self.target_emotion,
                    "score": self.score
                }
            return True, {"correct": False}
            
        return False, "Invalid action"

    def _get_random_emotion(self):
        return random.choice(['happy', 'sad', 'angry', 'surprise', 'fear', 'neutral'])

    def end(self):
        self.is_active = False
        return True, {"game_over": True, "final_score": self.score}

    def get_state(self):
        return {"type": "charades", "target": self.target_emotion, "score": self.score}

class FocusQuestGame:
    def __init__(self):
        self.is_active = False
        self.start_time = 0
        self.duration = 25 * 60 # 25 mins
        
    def start(self, user_id, duration=25, **kwargs):
        self.is_active = True
        self.start_time = time.time()
        self.duration = duration * 60
        return True, {
            "message": "Focus Quest Started! Good luck.",
            "duration": self.duration
        }

    def process_action(self, user_id, action, data):
        if action == "stop":
            return self.end()
        return False, "Invalid action"

    def end(self):
        self.is_active = False
        elapsed = int(time.time() - self.start_time)
        return True, {"game_over": True, "message": f"Quest Complete! Focused for {elapsed//60} mins."}

    def get_state(self):
        return {"type": "focus_quest", "time_left": self.duration - (time.time() - self.start_time)}

# Global instance
game_engine = GameEngine()
