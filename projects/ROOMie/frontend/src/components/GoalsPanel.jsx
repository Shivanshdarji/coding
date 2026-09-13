import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export default function GoalsPanel({ socket, isOpen, onClose }) {
    const [goals, setGoals] = useState([]);
    const [newGoal, setNewGoal] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        if (isOpen && socket) {
            setIsLoading(true);
            socket.emit('get_goals');

            const handleGoals = (data) => {
                setGoals(data.goals || []);
                setIsLoading(false);
            };

            const handleGoalAdded = (data) => {
                setGoals(prev => [...prev, data.description]);
                setNewGoal("");
            };

            socket.on('user_goals', handleGoals);
            socket.on('goal_added', handleGoalAdded);

            return () => {
                socket.off('user_goals', handleGoals);
                socket.off('goal_added', handleGoalAdded);
            };
        }
    }, [isOpen, socket]);

    const handleAddGoal = (e) => {
        e.preventDefault();
        if (!newGoal.trim() || !socket) return;

        socket.emit('add_goal', { description: newGoal.trim() });
    };

    if (!isOpen) return null;

    return (
        <div className="calibration-overlay">
            <motion.div
                className="calibration-modal"
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
            >
                <div className="calibration-header">
                    <h2>🎯 Your Goals</h2>
                    <button className="close-btn" onClick={onClose}>×</button>
                </div>

                <div className="calibration-content" style={{ alignItems: 'stretch', textAlign: 'left' }}>
                    <p className="instruction">
                        Tell ROOMii what you want to achieve. I'll help you stay on track!
                    </p>

                    <form onSubmit={handleAddGoal} style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
                        <input
                            type="text"
                            value={newGoal}
                            onChange={(e) => setNewGoal(e.target.value)}
                            placeholder="e.g., Crack Google, Learn React, Run 5k..."
                            className="chat-input"
                            style={{ flex: 1 }}
                            autoFocus
                        />
                        <button type="submit" className="btn accent" disabled={!newGoal.trim()}>
                            Add
                        </button>
                    </form>

                    <div className="goals-list" style={{ maxHeight: '300px', overflowY: 'auto' }}>
                        {isLoading ? (
                            <div className="loading-state">Loading goals...</div>
                        ) : goals.length === 0 ? (
                            <div className="empty-state">
                                <span style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🌱</span>
                                <p>No goals set yet. Start small!</p>
                            </div>
                        ) : (
                            <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                {goals.map((goal, index) => (
                                    <motion.li
                                        key={index}
                                        initial={{ opacity: 0, x: -10 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        style={{
                                            background: 'rgba(255,255,255,0.05)',
                                            padding: '1rem',
                                            borderRadius: '8px',
                                            borderLeft: '3px solid var(--accent)',
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: '0.5rem'
                                        }}
                                    >
                                        <span>📌</span>
                                        <span style={{ fontSize: '1.1rem' }}>{goal}</span>
                                    </motion.li>
                                ))}
                            </ul>
                        )}
                    </div>
                </div>
            </motion.div>
        </div>
    );
}
