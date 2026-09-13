// ===================================
// 3D Visualizer - OS Component Visualization
// ===================================

class Visualizer3D {
    constructor(scene, osEngine) {
        this.scene = scene;
        this.os = osEngine;
        this.visualizations = {};

        // Visualization settings
        this.settings = {
            processSize: 0.3,
            coreSpacing: 2,
            memoryBlockSize: 0.1,
            updateInterval: 100
        };

        this.init();
    }

    init() {
        this.createCPUVisualization();
        this.createMemoryVisualization();
        this.createFileSystemVisualization();

        // Start update loop
        setInterval(() => this.update(), this.settings.updateInterval);
    }

    // ===================================
    // CPU & Process Visualization
    // ===================================

    createCPUVisualization() {
        const cpuGroup = new THREE.Group();
        cpuGroup.name = 'CPU';

        // Create CPU cores
        const cores = [];
        for (let i = 0; i < 4; i++) {
            const coreGeometry = new THREE.BoxGeometry(1, 1, 0.2);
            const coreMaterial = new THREE.MeshStandardMaterial({
                color: 0x00d4ff,
                emissive: 0x00d4ff,
                emissiveIntensity: 0.3,
                metalness: 0.8,
                roughness: 0.2
            });

            const core = new THREE.Mesh(coreGeometry, coreMaterial);
            core.position.set((i - 1.5) * this.settings.coreSpacing, 0, 0);
            core.userData = { coreIndex: i, process: null };

            cores.push(core);
            cpuGroup.add(core);

            // Add core label
            const label = this.createTextSprite(`Core ${i}`, 0.3);
            label.position.set(0, -0.8, 0);
            core.add(label);
        }

        this.visualizations.cpuCores = cores;
        this.visualizations.cpuGroup = cpuGroup;

        // Position CPU group in scene (will be placed on front screen)
        cpuGroup.position.set(0, 2, -7.5);
        this.scene.add(cpuGroup);

        // Create process visualization area
        this.visualizations.processes = new Map();
    }

    updateCPUVisualization() {
        const coreStates = this.os.scheduler.getCoreStates();
        const readyQueue = this.os.scheduler.getReadyQueue();

        // Update cores
        coreStates.forEach((coreState, index) => {
            const core = this.visualizations.cpuCores[index];

            if (coreState.process) {
                // Core is busy
                core.material.color.setHex(0x00ff00);
                core.material.emissive.setHex(0x00ff00);
                core.material.emissiveIntensity = 0.5;

                // Show process on core
                this.visualizeProcessOnCore(coreState.process, index);
            } else {
                // Core is idle
                core.material.color.setHex(0x00d4ff);
                core.material.emissive.setHex(0x00d4ff);
                core.material.emissiveIntensity = 0.2;
            }
        });

        // Visualize ready queue
        this.visualizeReadyQueue(readyQueue);
    }

    visualizeProcessOnCore(process, coreIndex) {
        const core = this.visualizations.cpuCores[coreIndex];

        // Remove old process visualization
        const oldProcess = core.children.find(c => c.userData.isProcess);
        if (oldProcess) {
            core.remove(oldProcess);
        }

        // Create process sphere
        const processGeometry = new THREE.SphereGeometry(this.settings.processSize, 16, 16);
        const processMaterial = new THREE.MeshStandardMaterial({
            color: process.color,
            emissive: process.color,
            emissiveIntensity: 0.5
        });

        const processMesh = new THREE.Mesh(processGeometry, processMaterial);
        processMesh.position.set(0, 0.8, 0);
        processMesh.userData = { isProcess: true, pid: process.pid };

        core.add(processMesh);

        // Animate
        processMesh.rotation.y += 0.05;
    }

    visualizeReadyQueue(queue) {
        // Show processes waiting in queue
        // This would be displayed on a separate area
    }

    // ===================================
    // Memory Visualization
    // ===================================

    createMemoryVisualization() {
        const memoryGroup = new THREE.Group();
        memoryGroup.name = 'Memory';

        // Create memory grid
        const gridSize = 32; // 32x32 grid
        const blocks = [];

        for (let x = 0; x < gridSize; x++) {
            for (let y = 0; y < gridSize; y++) {
                const blockGeometry = new THREE.BoxGeometry(
                    this.settings.memoryBlockSize,
                    this.settings.memoryBlockSize,
                    0.05
                );
                const blockMaterial = new THREE.MeshStandardMaterial({
                    color: 0x333333,
                    emissive: 0x111111,
                    emissiveIntensity: 0.1
                });

                const block = new THREE.Mesh(blockGeometry, blockMaterial);
                block.position.set(
                    (x - gridSize / 2) * this.settings.memoryBlockSize * 1.1,
                    (y - gridSize / 2) * this.settings.memoryBlockSize * 1.1,
                    0
                );
                block.userData = { frame: x * gridSize + y, pid: null };

                blocks.push(block);
                memoryGroup.add(block);
            }
        }

        this.visualizations.memoryBlocks = blocks;
        this.visualizations.memoryGroup = memoryGroup;

        // Position memory group (will be on left screen)
        memoryGroup.position.set(-7.5, 0, 0);
        memoryGroup.rotation.y = Math.PI / 2;
        this.scene.add(memoryGroup);
    }

    updateMemoryVisualization() {
        const memoryMap = this.os.memoryManager.getMemoryMap();

        memoryMap.forEach((frame, index) => {
            if (index < this.visualizations.memoryBlocks.length) {
                const block = this.visualizations.memoryBlocks[index];

                if (frame.isFree) {
                    // Free memory - dark
                    block.material.color.setHex(0x333333);
                    block.material.emissive.setHex(0x111111);
                } else {
                    // Allocated memory - colored by process
                    const process = this.os.processManager.getProcess(frame.pid);
                    if (process) {
                        const color = new THREE.Color(process.color);
                        block.material.color.copy(color);
                        block.material.emissive.copy(color);
                        block.material.emissiveIntensity = 0.3;
                    }
                }
            }
        });
    }

    // ===================================
    // File System Visualization
    // ===================================

    createFileSystemVisualization() {
        const fsGroup = new THREE.Group();
        fsGroup.name = 'FileSystem';

        this.visualizations.fsGroup = fsGroup;
        this.visualizations.fileNodes = new Map();

        // Position file system group (will be on right screen)
        fsGroup.position.set(7.5, 0, 0);
        fsGroup.rotation.y = -Math.PI / 2;
        this.scene.add(fsGroup);

        // Initial tree creation
        this.updateFileSystemVisualization();
    }

    updateFileSystemVisualization() {
        // Clear existing visualization
        this.visualizations.fsGroup.children = [];
        this.visualizations.fileNodes.clear();

        // Build tree from root
        this.visualizeDirectory(this.os.fileSystem.root, 0, 0, 0);
    }

    visualizeDirectory(inode, x, y, depth) {
        // Create directory node
        const nodeGeometry = new THREE.SphereGeometry(0.2, 16, 16);
        const nodeMaterial = new THREE.MeshStandardMaterial({
            color: inode.type === 'directory' ? 0xffbe0b : 0x00d4ff,
            emissive: inode.type === 'directory' ? 0xffbe0b : 0x00d4ff,
            emissiveIntensity: 0.3
        });

        const node = new THREE.Mesh(nodeGeometry, nodeMaterial);
        node.position.set(x, y, depth);
        node.userData = { inode: inode.number };

        this.visualizations.fsGroup.add(node);
        this.visualizations.fileNodes.set(inode.number, node);

        // Add label
        const label = this.createTextSprite(inode.name, 0.2);
        label.position.set(0, -0.4, 0);
        node.add(label);

        // Visualize children
        if (inode.children) {
            let childIndex = 0;
            const childSpacing = 1;
            const childrenCount = inode.children.size;

            inode.children.forEach((childInodeNum) => {
                const childInode = this.os.fileSystem.inodes.get(childInodeNum);
                if (childInode) {
                    const childX = x + (childIndex - childrenCount / 2) * childSpacing;
                    const childY = y - 1.5;

                    // Draw connection line
                    const lineMaterial = new THREE.LineBasicMaterial({ color: 0x666666 });
                    const lineGeometry = new THREE.BufferGeometry().setFromPoints([
                        new THREE.Vector3(x, y, depth),
                        new THREE.Vector3(childX, childY, depth)
                    ]);
                    const line = new THREE.Line(lineGeometry, lineMaterial);
                    this.visualizations.fsGroup.add(line);

                    this.visualizeDirectory(childInode, childX, childY, depth);
                    childIndex++;
                }
            });
        }
    }

    // ===================================
    // Utilities
    // ===================================

    createTextSprite(text, size = 0.5) {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = 256;
        canvas.height = 64;

        context.fillStyle = '#ffffff';
        context.font = 'bold 32px Arial';
        context.textAlign = 'center';
        context.fillText(text, 128, 40);

        const texture = new THREE.CanvasTexture(canvas);
        const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
        const sprite = new THREE.Sprite(spriteMaterial);
        sprite.scale.set(size * 2, size * 0.5, 1);

        return sprite;
    }

    update() {
        if (!this.os.isRunning) return;

        this.updateCPUVisualization();
        this.updateMemoryVisualization();

        // Update file system less frequently
        if (Math.random() < 0.1) {
            this.updateFileSystemVisualization();
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Visualizer3D;
}
