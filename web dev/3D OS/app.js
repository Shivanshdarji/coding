// ===================================
// 3D OS - Main Application with OS Engine
// ===================================

class ThreeDOS {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.screens = {};
        this.osEngine = null;
        this.visualizer = null;
        this.controls = null;

        this.init();
    }

    init() {
        this.setupScene();
        this.createScreens();
        this.setupLighting();
        this.setupControls();
        this.setupEventListeners();
        this.startClock();

        // Initialize OS Engine
        this.initializeOS();

        this.hideLoading();
        this.animate();
    }

    initializeOS() {
        console.log('[3D OS] Initializing OS Engine...');

        // Create OS Engine
        this.osEngine = new OSEngine();
        this.osEngine.boot();

        // Create 3D Visualizer
        this.visualizer = new Visualizer3D(this.scene, this.osEngine);

        // Make OS accessible globally for terminal
        window.os = this.osEngine;

        console.log('[3D OS] OS Engine initialized');
        console.log('[3D OS] Type "os.help()" in console for available commands');

        // Update UI with OS stats
        this.startStatsUpdate();
    }

    setupScene() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0a0e27);
        this.scene.fog = new THREE.Fog(0x0a0e27, 10, 50);

        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.camera.position.set(0, 0, 0);

        const canvas = document.getElementById('canvas3d');
        this.renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);

        this.createStarfield();
    }

    createStarfield() {
        const starsGeometry = new THREE.BufferGeometry();
        const starsMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 0.1, transparent: true, opacity: 0.8 });
        const starsVertices = [];
        for (let i = 0; i < 10000; i++) {
            starsVertices.push((Math.random() - 0.5) * 2000, (Math.random() - 0.5) * 2000, (Math.random() - 0.5) * 2000);
        }
        starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
        this.scene.add(new THREE.Points(starsGeometry, starsMaterial));
    }

    createScreens() {
        const screenDistance = 8, screenWidth = 12, screenHeight = 7;

        this.createScreen('front', { position: [0, 0, -screenDistance], rotation: [0, 0, 0], size: [screenWidth, screenHeight], color: 0x1a1f3a });
        this.createScreen('left', { position: [-screenDistance, 0, 0], rotation: [0, Math.PI / 2, 0], size: [screenWidth, screenHeight], color: 0x1a2f3a });
        this.createScreen('right', { position: [screenDistance, 0, 0], rotation: [0, -Math.PI / 2, 0], size: [screenWidth, screenHeight], color: 0x2a1f3a });
        this.createScreen('back', { position: [0, 0, screenDistance], rotation: [0, Math.PI, 0], size: [screenWidth, screenHeight], color: 0x1a3a2f });
        this.createScreen('top', { position: [0, screenDistance * 0.8, 0], rotation: [Math.PI / 2, 0, 0], size: [screenWidth, screenHeight], color: 0x3a1f1a });
        this.createScreen('bottom', { position: [0, -screenDistance * 0.8, 0], rotation: [-Math.PI / 2, 0, 0], size: [screenWidth, screenHeight], color: 0x1a1a3a });
    }

    createScreen(name, config) {
        const geometry = new THREE.PlaneGeometry(config.size[0], config.size[1]);
        const canvas = document.createElement('canvas');
        canvas.width = 1920;
        canvas.height = 1080;
        const ctx = canvas.getContext('2d');

        this.renderScreenContent(ctx, name);

        const texture = new THREE.CanvasTexture(canvas);
        texture.minFilter = THREE.LinearFilter;
        texture.magFilter = THREE.LinearFilter;

        const material = new THREE.MeshStandardMaterial({ map: texture, emissive: config.color, emissiveIntensity: 0.2, side: THREE.DoubleSide });
        const screen = new THREE.Mesh(geometry, material);
        screen.position.set(...config.position);
        screen.rotation.set(...config.rotation);
        screen.userData = { name, canvas, ctx };

        const glowGeometry = new THREE.PlaneGeometry(config.size[0] + 0.2, config.size[1] + 0.2);
        const glowMaterial = new THREE.MeshBasicMaterial({ color: 0x00d4ff, transparent: true, opacity: 0.1, side: THREE.DoubleSide });
        const glow = new THREE.Mesh(glowGeometry, glowMaterial);
        glow.position.z = -0.01;
        screen.add(glow);

        this.scene.add(screen);
        this.screens[name] = screen;
    }

    renderScreenContent(ctx, screenName) {
        ctx.fillStyle = '#0d1117';
        ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        ctx.strokeStyle = '#00d4ff';
        ctx.lineWidth = 4;
        ctx.strokeRect(10, 10, ctx.canvas.width - 20, ctx.canvas.height - 20);

        ctx.fillStyle = 'rgba(0, 212, 255, 0.1)';
        ctx.fillRect(10, 10, ctx.canvas.width - 20, 60);
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 40px Segoe UI';

        const titles = { front: '⚡ CPU & Scheduler', left: '🧠 Memory Manager', right: '📁 File System', back: '📊 System Monitor', top: '🌳 Process Tree', bottom: '💻 Terminal' };
        ctx.fillText(titles[screenName] || 'Screen', 40, 55);

        if (this.osEngine) {
            ctx.font = '30px Segoe UI';
            ctx.fillStyle = '#ffffff';
            const stats = this.osEngine.getStatistics();

            if (screenName === 'front') {
                const schedStats = this.osEngine.scheduler.getStatistics();
                ctx.fillText(`Algorithm: ${schedStats.algorithm}`, 60, 150);
                ctx.fillText(`CPU Utilization: ${schedStats.cpuUtilization.toFixed(1)}%`, 60, 200);
                ctx.fillText(`Ready Queue: ${schedStats.queueLength}`, 60, 250);
                ctx.fillStyle = '#00d4ff';
                ctx.font = 'bold 35px Segoe UI';
                ctx.fillText('Look around to see 3D CPU cores!', 60, 700);
            } else if (screenName === 'left') {
                const memStats = this.osEngine.memoryManager.getStatistics();
                ctx.fillText(`Total Memory: ${memStats.total} MB`, 60, 150);
                ctx.fillText(`Used: ${memStats.used.toFixed(1)} MB (${memStats.usagePercent.toFixed(1)}%)`, 60, 200);
                ctx.fillText(`Page Faults: ${memStats.pageFaults}`, 60, 250);
                ctx.fillText(`Hit Ratio: ${(memStats.hitRatio * 100).toFixed(1)}%`, 60, 300);
            } else if (screenName === 'right') {
                const fsStats = this.osEngine.fileSystem.getStatistics();
                ctx.fillText(`Total Space: ${fsStats.totalSpace} MB`, 60, 150);
                ctx.fillText(`Used: ${fsStats.usedSpace.toFixed(1)} MB`, 60, 200);
                ctx.fillText(`Files Created: ${fsStats.filesCreated}`, 60, 250);
            } else if (screenName === 'back') {
                ctx.fillText(`Uptime: ${Math.floor(stats.uptime / 1000)}s`, 60, 150);
                ctx.fillText(`CPU: ${stats.cpuUtilization.toFixed(1)}%`, 60, 220);
                ctx.fillText(`Memory: ${stats.memoryUtilization.toFixed(1)}%`, 60, 290);
                ctx.fillText(`Disk: ${stats.diskUtilization.toFixed(1)}%`, 60, 360);
                ctx.fillText(`Processes: ${stats.totalProcesses}`, 60, 430);
            } else if (screenName === 'top') {
                const processes = this.osEngine.processManager.getAllProcesses().slice(0, 12);
                ctx.font = '28px Consolas';
                processes.forEach((proc, i) => {
                    const y = 120 + (i * 60);
                    ctx.fillText(`[${proc.pid}] ${proc.name} - ${proc.state}`, 60, y);
                });
            } else if (screenName === 'bottom') {
                ctx.font = '28px Consolas';
                ctx.fillStyle = '#00ff00';
                const lines = [
                    '3D OS Terminal v1.0.0',
                    '',
                    'Open browser console (F12) to interact',
                    '',
                    'Commands:',
                    '  os.help()         - Show all commands',
                    '  os.ps()           - List processes',
                    '  os.exec(name, pri, burst) - Create process',
                    '  os.kill(pid)      - Terminate process',
                    '  os.meminfo()      - Memory stats',
                    '  os.ls()           - List files',
                    '  os.sched("RR")    - Set scheduler',
                    '',
                    'System is running! Watch the 3D visualizations!'
                ];
                lines.forEach((line, i) => ctx.fillText(line, 40, 120 + (i * 45)));
            }
        }
    }

    setupControls() {
        this.controls = { mouseDown: false, mouseX: 0, mouseY: 0, rotationX: 0, rotationY: 0, targetRotationX: 0, targetRotationY: 0 };
    }

    setupEventListeners() {
        const canvas = document.getElementById('canvas3d');
        canvas.addEventListener('mousedown', (e) => { this.controls.mouseDown = true; this.controls.mouseX = e.clientX; this.controls.mouseY = e.clientY; });
        canvas.addEventListener('mousemove', (e) => {
            if (!this.controls.mouseDown) return;
            this.controls.targetRotationY -= (e.clientX - this.controls.mouseX) * 0.005;
            this.controls.targetRotationX -= (e.clientY - this.controls.mouseY) * 0.005;
            this.controls.targetRotationX = Math.max(-Math.PI / 2, Math.min(Math.PI / 2, this.controls.targetRotationX));
            this.controls.mouseX = e.clientX;
            this.controls.mouseY = e.clientY;
        });
        canvas.addEventListener('mouseup', () => { this.controls.mouseDown = false; });

        document.querySelectorAll('.screen-btn').forEach(btn => btn.addEventListener('click', () => this.focusScreen(btn.dataset.screen)));
        window.addEventListener('resize', () => { this.camera.aspect = window.innerWidth / window.innerHeight; this.camera.updateProjectionMatrix(); this.renderer.setSize(window.innerWidth, window.innerHeight); });
        document.getElementById('fullscreen-btn').addEventListener('click', () => { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); });
    }

    focusScreen(screenName) {
        document.querySelectorAll('.screen-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelector(`[data-screen="${screenName}"]`).classList.add('active');
        const rotations = { front: { x: 0, y: 0 }, left: { x: 0, y: -Math.PI / 2 }, right: { x: 0, y: Math.PI / 2 }, back: { x: 0, y: Math.PI }, top: { x: Math.PI / 3, y: 0 }, bottom: { x: -Math.PI / 3, y: 0 } };
        const target = rotations[screenName] || { x: 0, y: 0 };
        this.controls.targetRotationX = target.x;
        this.controls.targetRotationY = target.y;
    }

    setupLighting() {
        this.scene.add(new THREE.AmbientLight(0xffffff, 0.5));
        Object.values(this.screens).forEach(screen => {
            const light = new THREE.PointLight(0x00d4ff, 1, 15);
            light.position.copy(screen.position);
            this.scene.add(light);
        });
    }

    startClock() {
        const updateTime = () => document.getElementById('current-time').textContent = new Date().toLocaleTimeString('en-US', { hour12: false });
        updateTime();
        setInterval(updateTime, 1000);
    }

    startStatsUpdate() {
        setInterval(() => {
            if (!this.osEngine || !this.osEngine.isRunning) return;
            Object.values(this.screens).forEach(screen => {
                this.renderScreenContent(screen.userData.ctx, screen.userData.name);
                screen.material.map.needsUpdate = true;
            });
        }, 1000);
    }

    hideLoading() {
        setTimeout(() => document.getElementById('loading-screen').classList.add('hidden'), 2000);
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        this.controls.rotationX += (this.controls.targetRotationX - this.controls.rotationX) * 0.1;
        this.controls.rotationY += (this.controls.targetRotationY - this.controls.rotationY) * 0.1;
        this.camera.rotation.order = 'YXZ';
        this.camera.rotation.x = this.controls.rotationX;
        this.camera.rotation.y = this.controls.rotationY;
        this.renderer.render(this.scene, this.camera);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    const os = new ThreeDOS();
    window.threeDOS = os;
    console.log('%c3D OS Loaded!', 'color: #00d4ff; font-size: 20px; font-weight: bold;');
    console.log('%cType os.help() for available commands', 'color: #00ff00; font-size: 14px;');
});
