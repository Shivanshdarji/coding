import { create } from 'zustand';
import { CEvaluator, ExecutionStep } from '../engine/CEvaluator';
import { levels, Level } from '../data/levels';

import { io, Socket } from 'socket.io-client';

interface GameState {
    code: string;
    output: string[];
    variables: Record<string, any>;
    steps: ExecutionStep[];
    currentStepIndex: number;
    isRunning: boolean;
    error: string | null;

    // Level State
    currentLevelId: number;
    currentLevel: Level;
    isLevelComplete: boolean;

    // Multiplayer State
    isMultiplayer: boolean;
    isSearching: boolean;
    connectedPeers: string[];
    socket: Socket | null;

    setCode: (code: string) => void;
    runCode: () => void;
    stepForward: () => void;
    stepBackward: () => void;
    reset: () => void;
    nextLevel: () => void;
    toggleMultiplayer: () => void;
}

const evaluator = new CEvaluator();

export const useGameStore = create<GameState>((set, get) => ({
    code: levels[0].initialCode,
    output: [],
    variables: {},
    steps: [],
    currentStepIndex: 0,
    isRunning: false,
    error: null,

    currentLevelId: 1,
    currentLevel: levels[0],
    isLevelComplete: false,

    isMultiplayer: false,
    isSearching: false,
    connectedPeers: [],
    socket: null,

    setCode: (code) => set({ code }),

    runCode: () => {
        const { code, currentLevel } = get();
        try {
            const steps = evaluator.evaluate(code);
            set({
                steps,
                currentStepIndex: 0,
                isRunning: true,
                error: null,
                output: [],
                variables: {}
            });

            if (steps.length > 0) {
                const lastStep = steps[steps.length - 1];
                set({
                    variables: lastStep.variables,
                    output: lastStep.output
                });

                // Check Win Condition
                if (currentLevel.validate(lastStep.output, lastStep.variables)) {
                    set({ isLevelComplete: true });
                    // Notify server of level completion
                    get().socket?.emit('levelUpdate', { level: currentLevel.id + 1 });
                }
            }
        } catch (e: any) {
            set({ error: e.message, isRunning: false });
        }
    },

    stepForward: () => {
        const { steps, currentStepIndex } = get();
        if (currentStepIndex < steps.length - 1) {
            const nextIndex = currentStepIndex + 1;
            const step = steps[nextIndex];
            set({
                currentStepIndex: nextIndex,
                variables: step.variables,
                output: step.output
            });
        } else {
            set({ isRunning: false });
        }
    },

    stepBackward: () => {
        const { steps, currentStepIndex } = get();
        if (currentStepIndex > 0) {
            const prevIndex = currentStepIndex - 1;
            const step = steps[prevIndex];
            set({
                currentStepIndex: prevIndex,
                variables: step.variables,
                output: step.output
            });
        }
    },

    reset: () => {
        set({
            output: [],
            variables: {},
            steps: [],
            currentStepIndex: 0,
            isRunning: false,
            error: null,
            isLevelComplete: false
        });
    },

    nextLevel: () => {
        const { currentLevelId } = get();
        const nextId = currentLevelId + 1;
        const nextLevel = levels.find(l => l.id === nextId);

        if (nextLevel) {
            set({
                currentLevelId: nextId,
                currentLevel: nextLevel,
                code: nextLevel.initialCode,
                isLevelComplete: false,
                output: [],
                variables: {},
                steps: [],
                error: null
            });
        }
    },

    toggleMultiplayer: () => {
        const { isMultiplayer, socket } = get();
        if (isMultiplayer) {
            socket?.disconnect();
            set({ isMultiplayer: false, connectedPeers: [], socket: null });
        } else {
            set({ isSearching: true });

            const newSocket = io('/', {
                path: '/socket.io',
                reconnection: true,
            });

            newSocket.on('connect', () => {
                console.log('Connected to server');
                set({ isSearching: false, isMultiplayer: true, socket: newSocket });
            });

            newSocket.on('currentPlayers', (players: Record<string, any>) => {
                const peers = Object.keys(players).filter(id => id !== newSocket.id);
                set({ connectedPeers: peers });
            });

            newSocket.on('newPlayer', (player: any) => {
                set(state => ({ connectedPeers: [...state.connectedPeers, player.id] }));
            });

            newSocket.on('playerDisconnected', (id: string) => {
                set(state => ({ connectedPeers: state.connectedPeers.filter(peerId => peerId !== id) }));
            });
        }
    }
}));
