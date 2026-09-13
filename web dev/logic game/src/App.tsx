import { useState } from 'react';
import { CodeEditor } from './components/CodeEditor';
import { MemoryVisualizer } from './components/MemoryVisualizer';
import { GameCanvas } from './components/GameCanvas';
import { DialogueOverlay } from './components/DialogueOverlay';
import { useGameStore } from './store/gameStore';
import { Play, RefreshCw, StepForward, ChevronRight, CheckCircle, Users, Loader, Terminal, Cpu } from 'lucide-react';

function App() {
    const {
        code, setCode, runCode, reset, stepForward, isRunning,
        currentLevel, isLevelComplete, nextLevel,
        isMultiplayer, isSearching, connectedPeers, toggleMultiplayer
    } = useGameStore();

    const [isTerminalOpen, setIsTerminalOpen] = useState(true);
    const [isMemoryOpen, setIsMemoryOpen] = useState(true);

    // Toggle handlers
    const toggleTerminal = () => setIsTerminalOpen(!isTerminalOpen);
    const toggleMemory = () => setIsMemoryOpen(!isMemoryOpen);

    return (
        <div className="w-screen h-screen bg-black text-white overflow-hidden relative font-mono">
            {/* Fullscreen Game Canvas */}
            <div className="absolute inset-0 z-0">
                <GameCanvas />
            </div>

            {/* Overlay: Vignette & Scanlines */}
            <div className="absolute inset-0 pointer-events-none z-10 bg-[radial-gradient(circle_at_center,transparent_0%,rgba(0,0,0,0.6)_100%)]"></div>
            <div className="absolute inset-0 pointer-events-none z-10 opacity-10 bg-[url('https://media.istockphoto.com/id/1364368143/vector/scanlines-grid-overlay-background.jpg?s=612x612&w=0&k=20&c=EaM7a9mXyJjJ_k_k_k_k_k_k_k_k_k_k_k_k_k_k_k_k=')] bg-repeat"></div>

            {/* Top HUD */}
            <div className="absolute top-0 left-0 right-0 p-4 flex justify-between items-start z-20 pointer-events-none">
                {/* Level Info */}
                <div className="glass-panel p-4 rounded-br-2xl border-l-4 border-cyan-500 pointer-events-auto backdrop-blur-md bg-black/60 max-w-md animate-in slide-in-from-top-10 duration-500">
                    <h2 className="text-2xl font-bold text-cyan-400 flex items-center gap-3">
                        <span className="bg-cyan-900/80 border border-cyan-500/50 text-cyan-200 text-xs px-2 py-1 rounded font-mono tracking-wider">SECTOR {currentLevel.id}</span>
                        {currentLevel.title}
                    </h2>
                    <p className="text-gray-300 text-sm mt-2 leading-relaxed border-t border-gray-700/50 pt-2">{currentLevel.description}</p>
                    <div className="mt-3 flex items-center gap-2 text-xs text-yellow-400 bg-yellow-900/20 px-3 py-1.5 rounded border border-yellow-700/30">
                        <span className="font-bold">MISSION HINT:</span> {currentLevel.hint}
                    </div>
                </div>

                {/* Status & Multiplayer */}
                <div className="flex flex-col items-end gap-2 pointer-events-auto">
                    <button
                        onClick={toggleMultiplayer}
                        className={`flex items-center gap-2 px-4 py-2 rounded-bl-xl border-r-4 transition-all duration-300 backdrop-blur-md ${isMultiplayer
                            ? 'bg-purple-900/80 border-purple-500 text-purple-100 shadow-[0_0_20px_rgba(168,85,247,0.4)]'
                            : 'bg-gray-900/80 border-gray-600 text-gray-400 hover:bg-gray-800/80'}`}
                    >
                        {isSearching ? <Loader size={16} className="animate-spin" /> : <Users size={16} />}
                        <span className="font-bold tracking-wide">{isSearching ? 'SCANNING...' : isMultiplayer ? `LINKED (${connectedPeers.length})` : 'OFFLINE'}</span>
                    </button>

                    <div className="flex gap-2">
                        <button
                            onClick={toggleTerminal}
                            className={`p-2 rounded border border-gray-700/50 backdrop-blur-md transition-all ${isTerminalOpen ? 'bg-cyan-900/50 text-cyan-400' : 'bg-gray-900/50 text-gray-500 hover:text-white'}`}
                            title="Toggle Terminal"
                        >
                            <Terminal size={20} />
                        </button>
                        <button
                            onClick={toggleMemory}
                            className={`p-2 rounded border border-gray-700/50 backdrop-blur-md transition-all ${isMemoryOpen ? 'bg-green-900/50 text-green-400' : 'bg-gray-900/50 text-gray-500 hover:text-white'}`}
                            title="Toggle Memory"
                        >
                            <Cpu size={20} />
                        </button>
                    </div>
                </div>
            </div>

            {/* Floating Terminal (Code Editor) */}
            <div className={`absolute bottom-8 left-8 z-30 transition-all duration-500 transform ${isTerminalOpen ? 'translate-y-0 opacity-100' : 'translate-y-20 opacity-0 pointer-events-none'}`}>
                <div className="glass-panel w-[600px] h-[400px] flex flex-col rounded-xl border border-cyan-500/30 shadow-[0_0_30px_rgba(6,182,212,0.15)] bg-black/80 backdrop-blur-xl overflow-hidden">
                    {/* Terminal Header */}
                    <div className="bg-gray-900/90 p-2 flex items-center justify-between border-b border-gray-700/50">
                        <div className="flex items-center gap-2 text-cyan-400 text-xs font-bold tracking-widest px-2">
                            <Terminal size={14} />
                            <span>TERMINAL_UPLINK_V1.0</span>
                        </div>
                        <div className="flex items-center gap-1">
                            <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/50"></div>
                            <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/50"></div>
                            <div className="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/50"></div>
                        </div>
                    </div>

                    {/* Editor Area */}
                    <div className="flex-1 relative bg-black/50">
                        <CodeEditor code={code} onChange={setCode} />
                    </div>

                    {/* Controls */}
                    <div className="p-3 bg-gray-900/90 border-t border-gray-700/50 flex gap-3">
                        <button
                            onClick={runCode}
                            disabled={isRunning}
                            className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-cyan-700 hover:bg-cyan-600 text-white rounded text-sm font-bold transition-all shadow-[0_0_15px_rgba(6,182,212,0.3)] disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <Play size={16} /> EXECUTE
                        </button>
                        <button
                            onClick={stepForward}
                            disabled={!isRunning}
                            className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded text-sm font-bold transition-all border border-gray-600 disabled:opacity-50"
                        >
                            <StepForward size={16} />
                        </button>
                        <button
                            onClick={reset}
                            className="px-4 py-2 bg-red-900/50 hover:bg-red-800/50 text-red-200 rounded text-sm font-bold transition-all border border-red-800/30"
                        >
                            <RefreshCw size={16} />
                        </button>
                    </div>
                </div>
            </div>

            {/* Floating Memory Visualizer */}
            <div className={`absolute top-24 right-8 z-30 transition-all duration-500 transform ${isMemoryOpen ? 'translate-x-0 opacity-100' : 'translate-x-20 opacity-0 pointer-events-none'}`}>
                <div className="glass-panel w-[300px] rounded-xl border border-green-500/30 shadow-[0_0_30px_rgba(34,197,94,0.15)] bg-black/80 backdrop-blur-xl overflow-hidden">
                    <div className="bg-gray-900/90 p-2 border-b border-gray-700/50 flex items-center gap-2 text-green-400 text-xs font-bold tracking-widest px-3">
                        <Cpu size={14} />
                        <span>SYSTEM_MEMORY</span>
                    </div>
                    <div className="p-0">
                        <MemoryVisualizer />
                    </div>
                </div>
            </div>

            {/* Dialogue Overlay (Center Bottom) */}
            <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2 z-40 w-full max-w-2xl pointer-events-none">
                <div className="pointer-events-auto">
                    <DialogueOverlay
                        characterName="System AI"
                        text={currentLevel.hint}
                    />
                </div>
            </div>

            {/* Level Complete Overlay */}
            {isLevelComplete && (
                <div className="absolute inset-0 bg-black/80 backdrop-blur-md flex flex-col items-center justify-center z-50 animate-in fade-in duration-500">
                    <div className="bg-gray-900/90 border-2 border-cyan-500 p-10 rounded-3xl shadow-[0_0_100px_rgba(6,182,212,0.5)] flex flex-col items-center text-center max-w-lg transform scale-100 animate-in zoom-in-95 duration-300 relative overflow-hidden">
                        <div className="absolute inset-0 bg-[url('https://media.istockphoto.com/id/1364368143/vector/scanlines-grid-overlay-background.jpg?s=612x612&w=0&k=20&c=EaM7a9mXyJjJ_k_k_k_k_k_k_k_k_k_k_k_k_k_k_k_k=')] opacity-10 pointer-events-none"></div>
                        <CheckCircle size={80} className="text-cyan-400 mb-6 drop-shadow-[0_0_20px_rgba(34,211,238,0.8)] animate-bounce" />
                        <h2 className="text-4xl font-black text-white mb-2 tracking-tighter uppercase italic">Sector Cleared</h2>
                        <p className="text-cyan-200 mb-8 font-mono text-sm">System stabilized. Uplink established. Proceeding to next sector.</p>
                        <button
                            onClick={nextLevel}
                            className="group relative flex items-center gap-3 px-10 py-4 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl font-bold transition-all transform hover:scale-105 shadow-[0_0_30px_rgba(6,182,212,0.4)] overflow-hidden"
                        >
                            <span className="relative z-10">INITIALIZE NEXT SECTOR</span>
                            <ChevronRight size={24} className="relative z-10 group-hover:translate-x-1 transition-transform" />
                            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;
