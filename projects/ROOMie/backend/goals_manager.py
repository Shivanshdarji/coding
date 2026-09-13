"""
Goals and Activity Management for ROOMie
Handles user goals, daily activity logging, and productivity tracking.
"""
import aiosqlite
from datetime import datetime
from typing import List, Dict, Optional
from logger import setup_logger

logger = setup_logger("goals_manager")

class GoalsManager:
    def __init__(self, db_path: str = "roomie_data.db"):
        self.db_path = db_path

    async def add_goal(self, user_id: int, description: str, category: str = "general"):
        """Add a new long-term goal"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO user_goals (user_id, description, category) VALUES (?, ?, ?)",
                (user_id, description, category)
            )
            await db.commit()
        logger.info(f"Added goal for user {user_id}: {description}")

    async def get_active_goals(self, user_id: int) -> List[str]:
        """Get list of active goal descriptions"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT description FROM user_goals WHERE user_id = ? AND is_active = 1",
                (user_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [row['description'] for row in rows]

    async def get_next_goal_to_ask(self, user_id: int) -> Optional[Dict]:
        """Get the next goal that hasn't been asked about recently"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            # Select goals that haven't been asked today, ordered by last_asked_at (oldest first)
            async with db.execute(
                """SELECT id, description FROM user_goals 
                   WHERE user_id = ? AND is_active = 1 
                   AND (last_asked_at IS NULL OR date(last_asked_at) != date('now'))
                   ORDER BY last_asked_at ASC LIMIT 1""",
                (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def mark_goal_asked(self, goal_id: int):
        """Update the last_asked_at timestamp for a goal"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE user_goals SET last_asked_at = CURRENT_TIMESTAMP WHERE id = ?",
                (goal_id,)
            )
            await db.commit()
        logger.info(f"Marked goal {goal_id} as asked")

    async def complete_goal(self, user_id: int, description: str) -> bool:
        """Mark a goal as completed (inactive) by description"""
        async with aiosqlite.connect(self.db_path) as db:
            # Find the goal first to ensure it exists and belongs to user
            async with db.execute(
                "SELECT id FROM user_goals WHERE user_id = ? AND description LIKE ? AND is_active = 1",
                (user_id, f"%{description}%")
            ) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return False
                
                goal_id = row[0]
                
            await db.execute(
                "UPDATE user_goals SET is_active = 0 WHERE id = ?",
                (goal_id,)
            )
            await db.commit()
            logger.info(f"Completed goal {goal_id} for user {user_id}")
            return True

    async def log_activity(self, user_id: int, description: str, status: str, notes: str = "", score: int = 0):
        """Log a daily activity"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT INTO activity_logs (user_id, date, activity_description, status, notes, productivity_score)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (user_id, date_str, description, status, notes, score)
            )
            await db.commit()
        logger.info(f"Logged activity for user {user_id}: {description} ({status})")

    async def get_daily_summary(self, user_id: int, date: str = None) -> List[Dict]:
        """Get activities for a specific date"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
            
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM activity_logs WHERE user_id = ? AND date = ?",
                (user_id, date)
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def has_logged_today(self, user_id: int) -> bool:
        """Check if user has logged any activity today"""
        date = datetime.now().strftime("%Y-%m-%d")
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT COUNT(*) FROM activity_logs WHERE user_id = ? AND date = ?",
                (user_id, date)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] > 0

# Global instance
goals_manager = GoalsManager()
