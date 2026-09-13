import React, { useEffect, useRef } from 'react';
import Phaser from 'phaser';
import { config } from '../game/config';

export const GameCanvas: React.FC = () => {
    const gameRef = useRef<Phaser.Game | null>(null);

    useEffect(() => {
        if (!gameRef.current) {
            gameRef.current = new Phaser.Game(config);
        }

        return () => {
            gameRef.current?.destroy(true);
            gameRef.current = null;
        };
    }, []);

    return <div id="game-container" className="w-full h-full" />;
};
