import Phaser from 'phaser';

export class MainScene extends Phaser.Scene {
    private player!: Phaser.GameObjects.Rectangle;
    private cursors?: Phaser.Types.Input.Keyboard.CursorKeys;

    constructor() {
        super({ key: 'MainScene' });
    }

    preload() {
        // Load assets here
    }

    create() {
        // Create Map (Placeholder Grid)
        const gridSize = 40;
        for (let x = 0; x < this.scale.width; x += gridSize) {
            this.add.line(0, 0, x, 0, x, this.scale.height, 0x333333).setOrigin(0);
        }
        for (let y = 0; y < this.scale.height; y += gridSize) {
            this.add.line(0, 0, 0, y, this.scale.width, y, 0x333333).setOrigin(0);
        }

        // Create Player
        this.player = this.add.rectangle(400, 300, 32, 32, 0x00ffff);
        this.physics.add.existing(this.player);

        // Controls
        if (this.input.keyboard) {
            this.cursors = this.input.keyboard.createCursorKeys();
        }

        // Add Text
        this.add.text(16, 16, 'Use Arrow Keys to Move', {
            fontSize: '18px',
            color: '#ffffff'
        });
    }

    update() {
        const speed = 200;
        const body = this.player.body as Phaser.Physics.Arcade.Body;

        if (this.cursors) {
            body.setVelocity(0);

            if (this.cursors.left.isDown) {
                body.setVelocityX(-speed);
            } else if (this.cursors.right.isDown) {
                body.setVelocityX(speed);
            }

            if (this.cursors.up.isDown) {
                body.setVelocityY(-speed);
            } else if (this.cursors.down.isDown) {
                body.setVelocityY(speed);
            }
        }
    }
}
