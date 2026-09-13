import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';

const app = express();
app.use(cors());

const httpServer = createServer(app);
const io = new Server(httpServer, {
    cors: {
        origin: "http://localhost:5173", // Vite default port
        methods: ["GET", "POST"]
    }
});

interface Player {
    id: string;
    x: number;
    y: number;
    level: number;
}

const players: Record<string, Player> = {};

io.on('connection', (socket) => {
    console.log('User connected:', socket.id);

    // Initialize player
    players[socket.id] = {
        id: socket.id,
        x: 0,
        y: 0,
        level: 1
    };

    // Send current players to new player
    socket.emit('currentPlayers', players);

    // Broadcast new player to others
    socket.broadcast.emit('newPlayer', players[socket.id]);

    socket.on('disconnect', () => {
        console.log('User disconnected:', socket.id);
        delete players[socket.id];
        io.emit('playerDisconnected', socket.id);
    });

    socket.on('playerMovement', (movementData) => {
        if (players[socket.id]) {
            players[socket.id].x = movementData.x;
            players[socket.id].y = movementData.y;
            // Broadcast movement to other players
            socket.broadcast.emit('playerMoved', players[socket.id]);
        }
    });

    socket.on('levelUpdate', (levelData) => {
        if (players[socket.id]) {
            players[socket.id].level = levelData.level;
            socket.broadcast.emit('playerLevelUpdate', { id: socket.id, level: levelData.level });
        }
    });
});

const PORT = process.env.PORT || 3000;

httpServer.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
