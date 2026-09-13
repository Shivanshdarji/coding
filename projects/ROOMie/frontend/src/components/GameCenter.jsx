import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// --- Game Components (Defined Outside to prevent re-renders) ---

const RapidFireOverlay = ({ state, displayTime, sendAction }) => (
    <div className="game-overlay rapid-fire">
        <div className="game-header-glass">
            <h2>🔥 Rapid Fire Guessing</h2>
            <div className="timer-glass" style={{ animation: displayTime <= 10 ? 'pulse-red 1s infinite' : 'none' }}>
                {displayTime}s
            </div>
        </div>
        <div className="game-content-glass">
            <div className="ai-question">
                <h3>ROOMii asks:</h3>
                <p>"{state.question}"</p>
            </div>
            <div className="user-controls-grid">
                <button className="btn glass-btn" onClick={() => sendAction('answer', { answer: 'yes' })}>Yes</button>
                <button className="btn glass-btn" onClick={() => sendAction('answer', { answer: 'no' })}>No</button>
                <button className="btn glass-btn" onClick={() => sendAction('answer', { answer: 'maybe' })}>Maybe</button>
                <button className="btn glass-btn success" onClick={() => sendAction('answer', { answer: 'correct' })}>That's it!</button>
            </div>
            <p className="hint">🎤 Tip: You can just say "Yes", "No", or "That's it!"</p>
        </div>
    </div>
);

const CharadesOverlay = ({ state, sendAction }) => (
    <div className="game-overlay charades">
        <div className="game-header-glass">
            <h2>🎭 Emotion Charades</h2>
            <div className="score-glass">Score: {state.score}</div>
        </div>
        <div className="game-content-glass">
            <div className="target-emotion">
                <h3>Show me:</h3>
                <div className="emotion-big">{state.target?.toUpperCase()}</div>
            </div>
            <div className="camera-preview">
                <button className="btn accent large" onClick={() => sendAction('check_emotion', { emotion: 'happy' })}>
                    I'm doing it! (Simulate)
                </button>
                <p className="hint">📸 Face the camera and show the emotion!</p>
            </div>
        </div>
    </div>
);

const FocusQuestOverlay = ({ state, displayTime, sendAction }) => (
    <div className="game-overlay focus-quest">
        <div className="game-header-glass">
            <h2>⚔️ Focus Quest</h2>
        </div>
        <div className="game-content-glass center">
            <div className="timer-big-glass">
                {Math.floor(displayTime / 60)}:{(displayTime % 60).toString().padStart(2, '0')}
            </div>
            <p>Stay focused! I'm watching over you.</p>
            <button className="btn danger" onClick={() => sendAction('stop')}>Abandon Quest</button>
        </div>
    </div>
);

export default function GameCenter({ socket, isOpen, onClose, activeGoals = [] }) {
    const [activeGame, setActiveGame] = useState(null); // 'rapid_fire', 'charades', 'focus_quest'
    const [gameState, setGameState] = useState(null);
    const [gameMessage, setGameMessage] = useState("");
    const [activeTab, setActiveTab] = useState('arcade'); // 'goals' or 'arcade'

    // Continuous Timer Logic
    const [displayTime, setDisplayTime] = useState(0);
    const timerRef = useRef(null);

    useEffect(() => {
        if (!socket) return;

        socket.on('game_started', (data) => {
            setActiveGame(data.game_type);
            setGameState(data.state);
            setGameMessage(data.state.message);

            // Sync timer
            if (data.state.time_left) {
                setDisplayTime(data.state.time_left);
            } else if (data.state.timer) {
                setDisplayTime(data.state.timer);
            }
        });

        socket.on('game_update', (data) => {
            setGameState(prev => ({ ...prev, ...data }));
            if (data.message) setGameMessage(data.message);

            // Sync timer occasionally or on specific events if needed
            if (data.time_left !== undefined) {
                // Only hard sync if drift is large (>2s) to avoid jumping
                if (Math.abs(displayTime - data.time_left) > 2) {
                    setDisplayTime(data.time_left);
                }
            }

            if (data.game_over) {
                setTimeout(() => {
                    setActiveGame(null);
                    setGameState(null);
                    setGameMessage("");
                }, 5000); // Close after 5s
            }
        });

        socket.on('game_ended', (data) => {
            setGameMessage(data.message);
            setTimeout(() => {
                setActiveGame(null);
                setGameState(null);
                setGameMessage("");
            }, 3000);
        });

        return () => {
            socket.off('game_started');
            socket.off('game_update');
            socket.off('game_ended');
        };
    }, [socket, displayTime]);

    // Frontend Timer Tick
    useEffect(() => {
        if (activeGame === 'rapid_fire' || activeGame === 'focus_quest') {
            timerRef.current = setInterval(() => {
                setDisplayTime(prev => Math.max(0, prev - 1));
            }, 1000);
        } else {
            clearInterval(timerRef.current);
        }
        return () => clearInterval(timerRef.current);
    }, [activeGame]);

    const startGame = (type) => {
        socket.emit('start_game', { game_type: type });
    };

    const sendAction = (action, data = {}) => {
        socket.emit('game_action', { action, data });
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <motion.div
                    className="game-center-modal-glass"
                    initial={{ opacity: 0, scale: 0.95, x: "-50%", y: "-45%" }}
                    animate={{ opacity: 1, scale: 1, x: "-50%", y: "-50%" }}
                    exit={{ opacity: 0, scale: 0.95, x: "-50%", y: "-45%" }}
                    transition={{ type: "spring", damping: 25, stiffness: 300 }}
                >
                    <div className="modal-header">
                        <h2>🎮 Game Center</h2>
                        <button className="close-btn" onClick={onClose}>✕</button>
                    </div>

                    {!activeGame ? (
                        <div className="game-hub">
                            {/* Tabs */}
                            <div className="game-tabs">
                                <button
                                    className={`tab-btn ${activeTab === 'arcade' ? 'active' : ''}`}
                                    onClick={() => setActiveTab('arcade')}
                                >
                                    🕹️ Arcade
                                </button>
                                <button
                                    className={`tab-btn ${activeTab === 'goals' ? 'active' : ''}`}
                                    onClick={() => setActiveTab('goals')}
                                >
                                    🎯 Goals
                                </button>
                            </div>

                            {/* Tab Content */}
                            <div className="tab-content">
                                {activeTab === 'arcade' && (
                                    <motion.div
                                        className="game-grid"
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                    >
                                        <div className="game-card glass-card-hover" onClick={() => startGame('rapid_fire')}>
                                            <div className="icon-glow">🔥</div>
                                            <div className="card-info">
                                                <h4>Rapid Fire</h4>
                                                <p>I guess your object in 2 mins!</p>
                                            </div>
                                        </div>
                                        <div className="game-card glass-card-hover" onClick={() => startGame('charades')}>
                                            <div className="icon-glow">🎭</div>
                                            <div className="card-info">
                                                <h4>Charades</h4>
                                                <p>Act out emotions for points.</p>
                                            </div>
                                        </div>
                                    </motion.div>
                                )}

                                {activeTab === 'goals' && (
                                    <motion.div
                                        className="game-grid"
                                        initial={{ opacity: 0, x: 20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                    >
                                        <div className="game-card glass-card-hover" onClick={() => startGame('focus_quest')}>
                                            <div className="icon-glow">⚔️</div>
                                            <div className="card-info">
                                                <h4>Focus Quest</h4>
                                                <p>Gamified productivity timer.</p>
                                            </div>
                                        </div>
                                        <div className="game-card disabled">
                                            <div className="icon-glow">🧠</div>
                                            <div className="card-info">
                                                <h4>Quiz Master</h4>
                                                <p>Coming soon based on your goals!</p>
                                            </div>
                                        </div>
                                    </motion.div>
                                )}
                            </div>
                        </div>
                    ) : (
                        <div className="active-game-container">
                            {gameMessage && <div className="game-message-toast">{gameMessage}</div>}
                            {activeGame === 'rapid_fire' && <RapidFireOverlay state={gameState} displayTime={displayTime} sendAction={sendAction} />}
                            {activeGame === 'charades' && <CharadesOverlay state={gameState} sendAction={sendAction} />}
                            {activeGame === 'focus_quest' && <FocusQuestOverlay state={gameState} displayTime={displayTime} sendAction={sendAction} />}
                        </div>
                    )}
                </motion.div>
            )}
        </AnimatePresence>
    );
}
