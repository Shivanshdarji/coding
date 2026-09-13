import Phaser from 'phaser';

export class IsometricScene extends Phaser.Scene {
    private player!: Phaser.GameObjects.Container;
    private cursors?: Phaser.Types.Input.Keyboard.CursorKeys;
    private mapGroup!: Phaser.GameObjects.Group;
    private grid: number[][] = [];
    private readonly TILE_WIDTH = 64;
    private readonly TILE_HEIGHT = 32;

    constructor() {
        super({ key: 'IsometricScene' });
    }

    preload() {
        // Create procedural textures for tiles
        const graphics = this.make.graphics({ x: 0, y: 0 }, false);

        // Grass Tile
        graphics.fillStyle(0x4caf50);
        graphics.beginPath();
        graphics.moveTo(32, 0);
        graphics.lineTo(64, 16);
        graphics.lineTo(32, 32);
        graphics.lineTo(0, 16);
        graphics.closePath();
        graphics.fill();
        graphics.lineStyle(1, 0x388e3c);
        graphics.strokePath();
        graphics.generateTexture('grass', 64, 32);

        // Water Tile
        graphics.clear();
        graphics.fillStyle(0x2196f3);
        graphics.beginPath();
        graphics.moveTo(32, 0);
        graphics.lineTo(64, 16);
        graphics.lineTo(32, 32);
        graphics.lineTo(0, 16);
        graphics.closePath();
        graphics.fill();
        graphics.lineStyle(1, 0x1976d2);
        graphics.strokePath();
        graphics.generateTexture('water', 64, 32);

        // Player (Diamond)
        graphics.clear();
        graphics.fillStyle(0xffeb3b);
        graphics.beginPath();
        graphics.moveTo(16, 0);
        graphics.lineTo(32, 16);
        graphics.lineTo(16, 32);
        graphics.lineTo(0, 16);
        graphics.closePath();
        graphics.fill();
        graphics.generateTexture('player', 32, 32);
    }

    create() {
        this.mapGroup = this.add.group();

        // Generate a 10x10 grid
        const size = 10;
        for (let y = 0; y < size; y++) {
            this.grid[y] = [];
            for (let x = 0; x < size; x++) {
                // Simple map generation: Water on edges
                const isWater = x === 0 || x === size - 1 || y === 0 || y === size - 1;
                this.grid[y][x] = isWater ? 1 : 0;

                const tx = (x - y) * (this.TILE_WIDTH / 2);
                const ty = (x + y) * (this.TILE_HEIGHT / 2);

                const tile = this.add.image(400 + tx, 100 + ty, isWater ? 'water' : 'grass');
                tile.setDepth(ty); // Simple depth sorting
                this.mapGroup.add(tile);
            }
        }

        // Player Setup
        const startX = 2;
        const startY = 2;
        const px = (startX - startY) * (this.TILE_WIDTH / 2);
        const py = (startX + startY) * (this.TILE_HEIGHT / 2);

        const playerSprite = this.add.image(0, -16, 'player');
        this.player = this.add.container(400 + px, 100 + py, [playerSprite]);
        this.player.setDepth(100 + py + 1);
        this.player.setData('gridX', startX);
        this.player.setData('gridY', startY);

        if (this.input.keyboard) {
            this.cursors = this.input.keyboard.createCursorKeys();
        }

        // Camera
        this.cameras.main.zoom = 1.2;

        // Input handling
        this.input.keyboard?.on('keydown-LEFT', () => this.movePlayer(-1, 0));
        this.input.keyboard?.on('keydown-RIGHT', () => this.movePlayer(1, 0));
        this.input.keyboard?.on('keydown-UP', () => this.movePlayer(0, -1));
        this.input.keyboard?.on('keydown-DOWN', () => this.movePlayer(0, 1));
    }

    update() {
        // Movement handled by events
    }

    public movePlayer(dx: number, dy: number) {
        if (!this.player) return;

        const currentX = this.player.getData('gridX');
        const currentY = this.player.getData('gridY');
        const newX = currentX + dx;
        const newY = currentY + dy;

        // Check bounds and collision
        if (newX >= 0 && newX < 10 && newY >= 0 && newY < 10) {
            if (this.grid[newY][newX] === 0) { // 0 is walkable (grass)
                this.player.setData('gridX', newX);
                this.player.setData('gridY', newY);

                const tx = (newX - newY) * (this.TILE_WIDTH / 2);
                const ty = (newX + newY) * (this.TILE_HEIGHT / 2);

                this.tweens.add({
                    targets: this.player,
                    x: 400 + tx,
                    y: 100 + ty,
                    duration: 200,
                    onUpdate: () => {
                        this.player.setDepth(100 + this.player.y);
                    }
                });
            }
        }
    }
}
