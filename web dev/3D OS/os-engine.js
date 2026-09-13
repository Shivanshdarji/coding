// ===================================
// OS Engine - Main Operating System Core
// ===================================

class OSEngine {
    constructor() {
        // Core Subsystems
        this.processManager = new ProcessManager();
        this.scheduler = new CPUScheduler(this.processManager);
        this.memoryManager = new MemoryManager();
        this.fileSystem = new FileSystem();

        // System State
        this.isRunning = false;
        this.bootTime = null;
        this.uptime = 0;
        this.tickInterval = null;
        this.tickRate = 100; // ms per tick

        // System Statistics
        this.stats = {
            totalProcesses: 0,
            totalMemoryAllocated: 0,
            totalFilesCreated: 0,
            cpuUtilization: 0,
            memoryUtilization: 0,
            diskUtilization: 0
        };

        console.log('[OSEngine] Initialized');
    }

    // ===================================
    // System Boot & Shutdown
    // ===================================

    boot() {
        console.log('[OSEngine] Booting system...');

        this.bootTime = Date.now();
        this.isRunning = true;

        // Initialize demo data
        this.initializeSystem();

        // Start scheduler
        this.scheduler.start();

        // Start system tick
        this.startTick();

        console.log('[OSEngine] System booted successfully');

        return true;
    }

    shutdown() {
        console.log('[OSEngine] Shutting down...');

        this.isRunning = false;
        this.scheduler.stop();

        if (this.tickInterval) {
            clearInterval(this.tickInterval);
        }

        console.log('[OSEngine] System shutdown complete');
    }

    initializeSystem() {
        // Create demo processes
        this.processManager.createDemoProcesses();

        // Allocate memory for processes
        this.processManager.getAllProcesses().forEach(process => {
            this.memoryManager.allocateMemory(process.pid, process.memorySize);
        });

        // Create demo file system
        this.fileSystem.createDemoFiles();

        console.log('[OSEngine] System initialized with demo data');
    }

    // ===================================
    // System Tick (Simulation Loop)
    // ===================================

    startTick() {
        this.tickInterval = setInterval(() => {
            this.tick();
        }, this.tickRate);
    }

    tick() {
        if (!this.isRunning) return;

        // Update uptime
        this.uptime = Date.now() - this.bootTime;

        // Run scheduler
        const scheduledProcess = this.scheduler.schedule();

        // Process I/O requests
        this.fileSystem.ioScheduler.schedule();

        // Update statistics
        this.updateStatistics();

        // Randomly create new processes (simulate workload)
        if (Math.random() < 0.05) { // 5% chance per tick
            this.createRandomProcess();
        }

        // Randomly terminate completed processes
        this.cleanupTerminatedProcesses();
    }

    createRandomProcess() {
        const names = ['task', 'worker', 'service', 'daemon', 'job'];
        const name = names[Math.floor(Math.random() * names.length)] + Math.floor(Math.random() * 1000);
        const priority = Math.floor(Math.random() * 10) + 1;
        const burstTime = Math.floor(Math.random() * 200) + 50;

        const process = this.processManager.createProcess(name, priority, burstTime);
        this.memoryManager.allocateMemory(process.pid, process.memorySize);

        this.stats.totalProcesses++;
    }

    cleanupTerminatedProcesses() {
        const terminated = this.processManager.getProcessesByState('terminated');

        terminated.forEach(process => {
            // Keep for a while for statistics, then remove
            if (Date.now() - process.completionTime > 10000) {
                this.memoryManager.deallocateMemory(process.pid);
                this.processManager.processes.delete(process.pid);
            }
        });
    }

    updateStatistics() {
        const procStats = this.processManager.getStatistics();
        const memStats = this.memoryManager.getStatistics();
        const fsStats = this.fileSystem.getStatistics();
        const schedStats = this.scheduler.getStatistics();

        this.stats = {
            ...this.stats,
            ...procStats,
            cpuUtilization: schedStats.cpuUtilization,
            memoryUtilization: memStats.usagePercent,
            diskUtilization: fsStats.usagePercent,
            uptime: this.uptime
        };
    }

    // ===================================
    // System Calls (User Interface)
    // ===================================

    // Process Management
    exec(name, priority, burstTime) {
        const process = this.processManager.createProcess(name, priority, burstTime);
        if (process) {
            this.memoryManager.allocateMemory(process.pid, process.memorySize);
            return process.pid;
        }
        return null;
    }

    kill(pid) {
        const success = this.processManager.terminateProcess(pid);
        if (success) {
            this.memoryManager.deallocateMemory(pid);
        }
        return success;
    }

    ps() {
        return this.processManager.getAllProcesses();
    }

    top() {
        return this.processManager.getStatistics();
    }

    // Memory Management
    malloc(pid, size) {
        return this.memoryManager.allocateMemory(pid, size);
    }

    free(pid) {
        return this.memoryManager.deallocateMemory(pid);
    }

    meminfo() {
        return this.memoryManager.getStatistics();
    }

    // File System
    touch(filename, content) {
        return this.fileSystem.createFile(filename, content);
    }

    mkdir(dirname) {
        return this.fileSystem.createDirectory(dirname);
    }

    rm(inodeNumber) {
        return this.fileSystem.deleteFile(inodeNumber);
    }

    cat(inodeNumber) {
        return this.fileSystem.readFile(inodeNumber);
    }

    echo(inodeNumber, content) {
        return this.fileSystem.writeFile(inodeNumber, content);
    }

    ls(path) {
        return this.fileSystem.listDirectory(path);
    }

    cd(path) {
        return this.fileSystem.changeDirectory(path);
    }

    pwd() {
        return this.fileSystem.getPath(this.fileSystem.currentDirectory);
    }

    df() {
        return this.fileSystem.getStatistics();
    }

    // Scheduler Control
    sched(algorithm) {
        return this.scheduler.setAlgorithm(algorithm);
    }

    quantum(value) {
        this.scheduler.setTimeQuantum(value);
    }

    // ===================================
    // System Information
    // ===================================

    getSystemInfo() {
        return {
            uptime: this.uptime,
            bootTime: this.bootTime,
            isRunning: this.isRunning,
            tickRate: this.tickRate,
            processes: this.processManager.getStatistics(),
            memory: this.memoryManager.getStatistics(),
            disk: this.fileSystem.getStatistics(),
            scheduler: this.scheduler.getStatistics()
        };
    }

    getStatistics() {
        return this.stats;
    }

    // ===================================
    // Help System
    // ===================================

    help() {
        return {
            'Process Management': {
                'exec(name, priority, burstTime)': 'Create new process',
                'kill(pid)': 'Terminate process',
                'ps()': 'List all processes',
                'top()': 'Process statistics'
            },
            'Memory Management': {
                'malloc(pid, size)': 'Allocate memory',
                'free(pid)': 'Free memory',
                'meminfo()': 'Memory statistics'
            },
            'File System': {
                'touch(filename, content)': 'Create file',
                'mkdir(dirname)': 'Create directory',
                'rm(inode)': 'Delete file',
                'cat(inode)': 'Read file',
                'echo(inode, content)': 'Write file',
                'ls(path)': 'List directory',
                'cd(path)': 'Change directory',
                'pwd()': 'Print working directory',
                'df()': 'Disk statistics'
            },
            'Scheduler': {
                'sched(algorithm)': 'Set scheduling algorithm (RR, FCFS, SJF, SRTF, PRIORITY, MULTILEVEL)',
                'quantum(value)': 'Set time quantum for Round Robin'
            },
            'System': {
                'help()': 'Show this help',
                'getSystemInfo()': 'Get system information',
                'getStatistics()': 'Get system statistics'
            }
        };
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OSEngine;
}
