"""
Voice Commands Handler for ROOMie
Parses and executes voice commands from users
"""
import re
from logger import setup_logger

logger = setup_logger("voice_commands")

# Command patterns
COMMAND_PATTERNS = {
    "change_personality": r"(?:change|switch|set)\s+(?:personality|mood|to)\s+(?:to\s+)?(\w+)",
    "show_stats": r"(?:show|display|open)\s+(?:my\s+)?(?:stats|statistics|analytics|dashboard)",
    "clear_conversation": r"(?:clear|delete|remove)\s+(?:conversation|chat|history)",
    "export_history": r"(?:export|download|save)\s+(?:my\s+)?(?:history|conversation|chat)",
    "stop_listening": r"(?:stop|pause)\s+listening",
    "start_listening": r"(?:start|resume)\s+listening",
    "help": r"(?:help|what can you do|commands)",
    "greeting": r"(?:hello|hi|hey)\s+roomie",
    "open_game_center": r"(?:open|start|play|show)\s+(?:the\s+)?(?:game|games|arcade)(?:\s+center)?",
    "open_goals": r"(?:open|show|view)\s+(?:my\s+)?(?:goals|targets|objectives)",
    "open_analytics": r"(?:open|show|view)\s+(?:my\s+)?(?:stats|statistics|analytics|dashboard)",
    "start_game_rapid_fire": r"(?:start|play)\s+(?:rapid\s+fire|guessing\s+game)",
    "start_game_charades": r"(?:start|play)\s+(?:emotion\s+)?charades",
    "start_game_focus": r"(?:start|begin)\s+(?:focus\s+quest|focus\s+mode)",
    "stop_game": r"(?:stop|quit|end|finish)\s+(?:the\s+)?game",
    "explain_analytics": r"(?:explain|analyze|tell\s+me\s+about)\s+(?:my\s+)?(?:stats|statistics|analytics|data|mood|feelings)",
    "add_goal": r"(?:add|new|create)\s+(?:goal|target|objective)\s+(.+)",
    "complete_goal": r"(?:complete|finish|done|check\s+off)\s+(?:goal|target|objective)\s+(.+)",
    "open_generic": r"(?:open|show|view)\s+(settings|emotions|calibration|game\s+center|goals|analytics)",
    "close_generic": r"(?:close|hide)\s+(settings|emotions|calibration|game\s+center|goals|analytics)",
}

# Personality mappings
PERSONALITY_MAP = {
    "cheerful": "cheerful",
    "happy": "cheerful",
    "energetic": "cheerful",
    "sad": "low",
    "low": "low",
    "calm": "low",
    "neutral": "neutral",
    "normal": "neutral",
    "balanced": "neutral",
    "stressed": "stressed",
    "anxious": "stressed",
    "angry": "angry",
    "mad": "angry",
}

class VoiceCommandHandler:
    """Handles voice command parsing and execution"""
    
    def __init__(self):
        self.enabled = True
    
    def parse_command(self, text: str) -> dict:
        """
        Parse text to detect voice commands
        
        Returns:
            dict with 'command', 'params', and 'confidence'
        """
        text = text.lower().strip()
        
        # Check if text starts with "roomie" (activation word)
        has_activation = text.startswith("roomie") or "hey roomie" in text
        
        # Remove activation word for parsing
        clean_text = re.sub(r"^(?:hey\s+)?roomie[,\s]+", "", text)
        
        for command_name, pattern in COMMAND_PATTERNS.items():
            match = re.search(pattern, clean_text, re.IGNORECASE)
            if match:
                result = {
                    "command": command_name,
                    "params": {},
                    "confidence": 1.0 if has_activation else 0.7,
                    "original_text": text
                }
                
                # Extract parameters based on command type
                if command_name == "change_personality":
                    personality = match.group(1).lower()
                    mapped_personality = PERSONALITY_MAP.get(personality, "neutral")
                    result["params"]["personality"] = mapped_personality
                elif command_name in ["add_goal", "complete_goal"]:
                    result["params"]["text"] = match.group(1).strip()
                elif command_name in ["open_generic", "close_generic"]:
                    result["params"]["target"] = match.group(1).strip().lower()
                
                logger.info(f"Detected command: {command_name} with params: {result['params']}")
                return result
        
        # No command detected
        return {
            "command": None,
            "params": {},
            "confidence": 0.0,
            "original_text": text
        }
    
    def execute_command(self, command_data: dict) -> dict:
        """
        Execute a parsed command
        
        Returns:
            dict with 'success', 'message', and 'action'
        """
        command = command_data.get("command")
        params = command_data.get("params", {})
        
        if not command:
            return {
                "success": False,
                "message": "No command detected",
                "action": None
            }
        
        # Execute based on command type
        if command == "change_personality":
            personality = params.get("personality", "neutral")
            return {
                "success": True,
                "message": f"Switching to {personality} personality",
                "action": "change_personality",
                "data": {"personality": personality}
            }
        
        elif command == "show_stats":
            return {
                "success": True,
                "message": "Opening analytics dashboard",
                "action": "show_analytics",
                "data": {}
            }
        
        elif command == "clear_conversation":
            return {
                "success": True,
                "message": "Clearing conversation history",
                "action": "clear_conversation",
                "data": {}
            }
        
        elif command == "export_history":
            return {
                "success": True,
                "message": "Exporting conversation history",
                "action": "export_history",
                "data": {}
            }
        
        elif command == "stop_listening":
            self.enabled = False
            return {
                "success": True,
                "message": "Stopped listening for voice commands",
                "action": "toggle_listening",
                "data": {"enabled": False}
            }
        
        elif command == "start_listening":
            self.enabled = True
            return {
                "success": True,
                "message": "Resumed listening for voice commands",
                "action": "toggle_listening",
                "data": {"enabled": True}
            }
        
        elif command == "help":
            return {
                "success": True,
                "message": self.get_help_text(),
                "action": "show_help",
                "data": {}
            }
        
        elif command == "greeting":
            return {
                "success": True,
                "message": "Hello! How can I help you today?",
                "action": "greeting",
                "data": {}
            }
        
        elif command == "open_game_center":
            return {
                "success": True,
                "message": "Opening Game Center...",
                "action": "open_game_center",
                "data": {}
            }

        elif command == "open_goals":
            return {
                "success": True,
                "message": "Opening your goals...",
                "action": "open_goals",
                "data": {}
            }

        elif command == "open_analytics":
            return {
                "success": True,
                "message": "Opening analytics dashboard...",
                "action": "show_analytics",
                "data": {}
            }

        elif command == "start_game_rapid_fire":
            return {
                "success": True,
                "message": "Starting Rapid Fire Guessing!",
                "action": "start_game",
                "data": {"game": "rapid_fire"}
            }

        elif command == "start_game_charades":
            return {
                "success": True,
                "message": "Let's play Emotion Charades!",
                "action": "start_game",
                "data": {"game": "charades"}
            }

        elif command == "start_game_focus":
            return {
                "success": True,
                "message": "Starting Focus Quest. Good luck!",
                "action": "start_game",
                "data": {"game": "focus_quest"}
            }

        elif command == "stop_game":
            return {
                "success": True,
                "message": "Stopping current game.",
                "action": "stop_game",
                "data": {}
            }

        elif command == "explain_analytics":
            return {
                "success": True,
                "message": "Analyzing your data...",
                "action": "explain_analytics",
                "data": {}
            }

        elif command == "add_goal":
            text = params.get("text", "")
            return {
                "success": True,
                "message": f"Adding goal: {text}",
                "action": "add_goal",
                "data": {"text": text}
            }

        elif command == "complete_goal":
            text = params.get("text", "")
            return {
                "success": True,
                "message": f"Completing goal: {text}",
                "action": "complete_goal",
                "data": {"text": text}
            }

        elif command == "open_generic":
            target = params.get("target", "").replace(" ", "_")
            return {
                "success": True,
                "message": f"Opening {target.replace('_', ' ')}",
                "action": f"open_{target}",
                "data": {}
            }

        elif command == "close_generic":
            target = params.get("target", "").replace(" ", "_")
            return {
                "success": True,
                "message": f"Closing {target.replace('_', ' ')}",
                "action": f"close_{target}",
                "data": {}
            }
        
        return {
            "success": False,
            "message": f"Unknown command: {command}",
            "action": None
        }
    
    def get_help_text(self) -> str:
        """Get help text for available commands"""
        return """
🎤 Available Voice Commands:

• "ROOMie, change personality to [cheerful/calm/neutral]"
• "ROOMie, show my stats"
• "ROOMie, clear conversation"
• "ROOMie, export history"
• "ROOMie, stop listening"
• "ROOMie, help"

Just say "ROOMie" followed by your command!
        """.strip()

# Global instance
voice_handler = VoiceCommandHandler()
