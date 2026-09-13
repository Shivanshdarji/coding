import React from 'react';
import { useGameStore } from '../store/gameStore';
import { VariableValue } from '../engine/CEvaluator';

export const MemoryVisualizer: React.FC = () => {
    const { variables, output, error } = useGameStore();

    return (
        <div className="flex flex-col h-full bg-gray-900 border-l border-gray-700 p-4 w-80">
            <h2 className="text-lg font-bold text-cyan-400 mb-4">Memory & Output</h2>

            {/* Variables Section */}
            <div className="mb-6">
                <h3 className="text-sm font-semibold text-gray-400 mb-2 uppercase tracking-wider">Stack Variables</h3>
                <div className="space-y-2">
                    {Object.entries(variables).length === 0 ? (
                        <div className="text-gray-600 italic text-sm">No variables</div>
                    ) : (
                        Object.entries(variables).map(([name, data]: [string, VariableValue]) => (
                            <div key={name} className="bg-gray-800 p-2 rounded border border-gray-700 flex justify-between items-center">
                                <span className="font-mono text-yellow-400">{name}</span>
                                <div className="flex items-center gap-2">
                                    <span className="text-xs text-gray-500">{data.type}</span>
                                    <span className="font-mono text-white font-bold">{String(data.value)}</span>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>

            {/* Output Section */}
            <div className="flex-1 flex flex-col min-h-0">
                <h3 className="text-sm font-semibold text-gray-400 mb-2 uppercase tracking-wider">Console Output</h3>
                <div className="bg-black rounded p-2 font-mono text-sm text-gray-300 flex-1 overflow-y-auto border border-gray-700">
                    {output.map((line, i) => (
                        <div key={i}>{line}</div>
                    ))}
                    {output.length === 0 && !error && <span className="text-gray-600 italic">Ready...</span>}
                    {error && <div className="text-red-500 font-bold">Error: {error}</div>}
                </div>
            </div>
        </div>
    );
};
