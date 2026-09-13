// ===================================
// Process Manager - Process & Thread Management
// ===================================

class ProcessManager {
    constructor() {
        this.processes = new Map(); // pid -> Process
        this.nextPID = 1;
        this.currentProcess = null;
        this.processStates = {
            NEW: 'new',
            READY: 'ready',
            RUNNING: 'running',
            WAITING: 'waiting',
            TERMINATED: 'terminated'
        };
    }

    // ===================================
    // Process Control Block (PCB)
    // ===================================

    createPCB(name, priority = 5, burstTime = 100, arrivalTime = 0) {
        const pcb = {
            pid: this.nextPID++,
            name: name,
            state: this.processStates.NEW,
            priority: priority,

            // CPU Scheduling Info
            burstTime: burstTime,          // Total CPU time needed
            remainingTime: burstTime,       // Time left to execute
            arrivalTime: arrivalTime,       // When process arrived
            startTime: null,                // When first executed
            completionTime: null,           // When finished
            waitingTime: 0,                 // Time spent waiting
            turnaroundTime: 0,              // Total time in system
            responseTime: null,             // Time to first response

            // Memory Info
            memorySize: Math.floor(Math.random() * 1024) + 256, // KB
            memoryStart: null,
            memoryEnd: null,
            pageTable: [],

            // Process Hierarchy
            parentPID: null,
            childrenPIDs: [],

            // Thread Info
            threads: [],

            // I/O Info
            ioQueue: [],

            // File Descriptors
            openFiles: [],

            // Registers (simulated)
            registers: {
                pc: 0,      // Program counter
                sp: 0,      // Stack pointer
                ax: 0,      // Accumulator
                bx: 0,
                cx: 0,
                dx: 0
            },

            // Statistics
            contextSwitches: 0,
            cpuUsage: 0,

            // Visual Properties
            color: this.generateColor(),
            position: { x: 0, y: 0, z: 0 }
        };

        return pcb;
    }

    // ===================================
    // Process Operations
    // ===================================

    createProcess(name, priority = 5, burstTime = null, parentPID = null) {
        // Random burst time if not specified (10-200 time units)
        if (burstTime === null) {
            burstTime = Math.floor(Math.random() * 190) + 10;
        }

        const pcb = this.createPCB(name, priority, burstTime, Date.now());
        pcb.parentPID = parentPID;

        // Add to parent's children if parent exists
        if (parentPID && this.processes.has(parentPID)) {
            this.processes.get(parentPID).childrenPIDs.push(pcb.pid);
        }

        this.processes.set(pcb.pid, pcb);
        pcb.state = this.processStates.READY;

        console.log(`[ProcessManager] Created process ${pcb.pid}: ${name} (burst: ${burstTime}, priority: ${priority})`);

        return pcb;
    }

    terminateProcess(pid) {
        const process = this.processes.get(pid);
        if (!process) return false;

        // Terminate all child processes first
        process.childrenPIDs.forEach(childPID => {
            this.terminateProcess(childPID);
        });

        process.state = this.processStates.TERMINATED;
        process.completionTime = Date.now();
        process.turnaroundTime = process.completionTime - process.arrivalTime;

        console.log(`[ProcessManager] Terminated process ${pid}: ${process.name}`);

        // Remove from parent's children list
        if (process.parentPID && this.processes.has(process.parentPID)) {
            const parent = this.processes.get(process.parentPID);
            parent.childrenPIDs = parent.childrenPIDs.filter(id => id !== pid);
        }

        return true;
    }

    getProcess(pid) {
        return this.processes.get(pid);
    }

    getAllProcesses() {
        return Array.from(this.processes.values());
    }

    getProcessesByState(state) {
        return this.getAllProcesses().filter(p => p.state === state);
    }

    // ===================================
    // Context Switching
    // ===================================

    contextSwitch(fromPID, toPID) {
        if (fromPID) {
            const fromProcess = this.processes.get(fromPID);
            if (fromProcess && fromProcess.state === this.processStates.RUNNING) {
                // Save state
                fromProcess.state = this.processStates.READY;
                fromProcess.contextSwitches++;
            }
        }

        if (toPID) {
            const toProcess = this.processes.get(toPID);
            if (toProcess) {
                // Restore state
                toProcess.state = this.processStates.RUNNING;
                toProcess.contextSwitches++;

                if (toProcess.startTime === null) {
                    toProcess.startTime = Date.now();
                    toProcess.responseTime = toProcess.startTime - toProcess.arrivalTime;
                }

                this.currentProcess = toProcess;
                return toProcess;
            }
        }

        this.currentProcess = null;
        return null;
    }

    // ===================================
    // Thread Management
    // ===================================

    createThread(pid, name) {
        const process = this.processes.get(pid);
        if (!process) return null;

        const thread = {
            tid: process.threads.length + 1,
            name: name,
            state: this.processStates.READY,
            registers: { pc: 0, sp: 0 },
            stack: []
        };

        process.threads.push(thread);
        return thread;
    }

    // ===================================
    // Utilities
    // ===================================

    generateColor() {
        const hue = Math.floor(Math.random() * 360);
        return `hsl(${hue}, 70%, 60%)`;
    }

    // ===================================
    // Statistics
    // ===================================

    getStatistics() {
        const processes = this.getAllProcesses();
        const terminated = this.getProcessesByState(this.processStates.TERMINATED);

        let totalWaitingTime = 0;
        let totalTurnaroundTime = 0;
        let totalResponseTime = 0;
        let count = 0;

        terminated.forEach(p => {
            if (p.completionTime) {
                totalWaitingTime += p.waitingTime;
                totalTurnaroundTime += p.turnaroundTime;
                if (p.responseTime !== null) {
                    totalResponseTime += p.responseTime;
                }
                count++;
            }
        });

        return {
            totalProcesses: processes.length,
            running: this.getProcessesByState(this.processStates.RUNNING).length,
            ready: this.getProcessesByState(this.processStates.READY).length,
            waiting: this.getProcessesByState(this.processStates.WAITING).length,
            terminated: terminated.length,
            avgWaitingTime: count > 0 ? totalWaitingTime / count : 0,
            avgTurnaroundTime: count > 0 ? totalTurnaroundTime / count : 0,
            avgResponseTime: count > 0 ? totalResponseTime / count : 0
        };
    }

    // ===================================
    // Demo Process Creation
    // ===================================

    createDemoProcesses() {
        // System processes
        this.createProcess('init', 10, 500);
        this.createProcess('systemd', 9, 300);

        // User processes
        const shellPID = this.createProcess('bash', 5, 200);
        this.createProcess('ls', 3, 50, shellPID);
        this.createProcess('grep', 3, 80, shellPID);

        // Applications
        this.createProcess('chrome', 4, 400);
        this.createProcess('vscode', 4, 350);
        this.createProcess('spotify', 2, 250);

        // Background tasks
        this.createProcess('cron', 1, 100);
        this.createProcess('sshd', 6, 150);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProcessManager;
}
