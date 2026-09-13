import React, { useState, useEffect } from 'react';
import { MessageCircle, X } from 'lucide-react';

interface DialogueProps {
    characterName: string;
    text: string;
    onComplete?: () => void;
}

export const DialogueOverlay: React.FC<DialogueProps> = ({ characterName, text, onComplete }) => {
    const [displayedText, setDisplayedText] = useState('');
    const [index, setIndex] = useState(0);

    useEffect(() => {
        if (index < text.length) {
            const timer = setTimeout(() => {
                setDisplayedText((prev) => prev + text[index]);
                setIndex((prev) => prev + 1);
            }, 30); // Typing speed
            return () => clearTimeout(timer);
        }
    }, [index, text]);

    return (
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 w-3/4 max-w-2xl bg-black/80 backdrop-blur-md border border-cyan-500/30 rounded-xl p-6 shadow-2xl animate-in slide-in-from-bottom-10 fade-in duration-300 z-50">
            <div className="flex items-start gap-4">
                <div className="w-16 h-16 bg-cyan-900/50 rounded-full flex items-center justify-center border border-cyan-500/50 shrink-0">
                    <MessageCircle className="text-cyan-400" size={32} />
                </div>
                <div className="flex-1">
                    <h3 className="text-cyan-400 font-bold text-lg mb-1">{characterName}</h3>
                    <p className="text-gray-200 text-lg leading-relaxed font-mono">
                        {displayedText}
                        <span className="animate-pulse inline-block w-2 h-5 bg-cyan-500 ml-1 align-middle"></span>
                    </p>
                </div>
                {index >= text.length && (
                    <button
                        onClick={onComplete}
                        className="text-gray-400 hover:text-white transition-colors"
                    >
                        <X size={24} />
                    </button>
                )}
            </div>
        </div>
    );
};
