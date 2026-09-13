// ===================================
// CPU Scheduler - Scheduling Algorithms
// ===================================

class CPUScheduler {
    constructor(processManager) {
        this.processManager = processManager;
        this.algorithm = 'RR'; // Default: Round Robin
        this.timeQuantum = 20; // For Round Robin
        this.currentTime = 0;
        this.readyQueue = [];
        this.ganttChart = [];
        this.isRunning = false;
        this.cpuCores = 4; // Simulate 4 CPU cores
        this.coreStates = Array(this.cpuCores).fill(null); // null = idle, pid = running
    }

    // ===================================
    // Scheduling Algorithms
    // ===================================

    // Round Robin (RR)
    scheduleRoundRobin() {
        if (this.readyQueue.length === 0) return null;

        // Get next process from queue
        const process = this.readyQueue.shift();

        // Execute for time quantum or until completion
        const executeTime = Math.min(this.timeQuantum, process.remainingTime);

        this.executeProcess(process, executeTime);

        // If not finished, add back to queue
        if (process.remainingTime > 0) {
            this.readyQueue.push(process);
        } else {
            this.processManager.terminateProcess(process.pid);
        }

        return process;
    }

    // First-Come-First-Served (FCFS)
    scheduleFCFS() {
        if (this.readyQueue.length === 0) return null;

        // Sort by arrival time
        this.readyQueue.sort((a, b) => a.arrivalTime - b.arrivalTime);

        const process = this.readyQueue.shift();
        this.executeProcess(process, process.remainingTime);
        this.processManager.terminateProcess(process.pid);

        return process;
    }

    // Shortest Job First (SJF)
    scheduleSJF() {
        if (this.readyQueue.length === 0) return null;

        // Sort by remaining time (shortest first)
        this.readyQueue.sort((a, b) => a.remainingTime - b.remainingTime);

        const process = this.readyQueue.shift();
        this.executeProcess(process, process.remainingTime);
        this.processManager.terminateProcess(process.pid);

        return process;
    }

    // Shortest Remaining Time First (SRTF) - Preemptive SJF
    scheduleSRTF() {
        if (this.readyQueue.length === 0) return null;

        // Sort by remaining time
        this.readyQueue.sort((a, b) => a.remainingTime - b.remainingTime);

        const process = this.readyQueue.shift();

        // Execute for 1 time unit (preemptive)
        this.executeProcess(process, 1);

        if (process.remainingTime > 0) {
            this.readyQueue.push(process);
        } else {
            this.processManager.terminateProcess(process.pid);
        }

        return process;
    }

    // Priority Scheduling (Non-preemptive)
    schedulePriority() {
        if (this.readyQueue.length === 0) return null;

        // Sort by priority (higher number = higher priority)
        this.readyQueue.sort((a, b) => b.priority - a.priority);

        const process = this.readyQueue.shift();
        this.executeProcess(process, process.remainingTime);
        this.processManager.terminateProcess(process.pid);

        return process;
    }

    // Priority Scheduling (Preemptive)
    schedulePriorityPreemptive() {
        if (this.readyQueue.length === 0) return null;

        // Sort by priority
        this.readyQueue.sort((a, b) => b.priority - a.priority);

        const process = this.readyQueue.shift();

        // Execute for 1 time unit
        this.executeProcess(process, 1);

        if (process.remainingTime > 0) {
            this.readyQueue.push(process);
        } else {
            this.processManager.terminateProcess(process.pid);
        }

        return process;
    }

    // Multilevel Queue Scheduling
    scheduleMultilevelQueue() {
        // Three queues: System (priority 8-10), Interactive (4-7), Batch (1-3)
        const systemQueue = this.readyQueue.filter(p => p.priority >= 8);
        const interactiveQueue = this.readyQueue.filter(p => p.priority >= 4 && p.priority < 8);
        const batchQueue = this.readyQueue.filter(p => p.priority < 4);

        let process = null;

        // System queue has highest priority
        if (systemQueue.length > 0) {
            process = systemQueue.shift();
            this.readyQueue = this.readyQueue.filter(p => p.pid !== process.pid);
        } else if (interactiveQueue.length > 0) {
            process = interactiveQueue.shift();
            this.readyQueue = this.readyQueue.filter(p => p.pid !== process.pid);
        } else if (batchQueue.length > 0) {
            process = batchQueue.shift();
            this.readyQueue = this.readyQueue.filter(p => p.pid !== process.pid);
        }

        if (process) {
            const executeTime = Math.min(this.timeQuantum, process.remainingTime);
            this.executeProcess(process, executeTime);

            if (process.remainingTime > 0) {
                this.readyQueue.push(process);
            } else {
                this.processManager.terminateProcess(process.pid);
            }
        }

        return process;
    }

    // ===================================
    // Core Scheduling Logic
    // ===================================

    executeProcess(process, time) {
        // Update process state
        process.remainingTime -= time;
        process.cpuUsage += time;

        // Record in Gantt chart
        this.ganttChart.push({
            pid: process.pid,
            name: process.name,
            start: this.currentTime,
            end: this.currentTime + time,
            color: process.color
        });

        this.currentTime += time;

        // Update waiting time for other processes
        this.readyQueue.forEach(p => {
            if (p.pid !== process.pid) {
                p.waitingTime += time;
            }
        });
    }

    schedule() {
        // Add ready processes to queue
        const readyProcesses = this.processManager.getProcessesByState('ready');
        readyProcesses.forEach(p => {
            if (!this.readyQueue.find(qp => qp.pid === p.pid)) {
                this.readyQueue.push(p);
            }
        });

        if (this.readyQueue.length === 0) return null;

        // Execute scheduling algorithm
        let process = null;

        switch (this.algorithm) {
            case 'RR':
                process = this.scheduleRoundRobin();
                break;
            case 'FCFS':
                process = this.scheduleFCFS();
                break;
            case 'SJF':
                process = this.scheduleSJF();
                break;
            case 'SRTF':
                process = this.scheduleSRTF();
                break;
            case 'PRIORITY':
                process = this.schedulePriority();
                break;
            case 'PRIORITY_PREEMPTIVE':
                process = this.schedulePriorityPreemptive();
                break;
            case 'MULTILEVEL':
                process = this.scheduleMultilevelQueue();
                break;
            default:
                process = this.scheduleRoundRobin();
        }

        return process;
    }

    // ===================================
    // Multi-Core Scheduling
    // ===================================

    scheduleMultiCore() {
        // Schedule processes on available cores
        for (let core = 0; core < this.cpuCores; core++) {
            if (this.coreStates[core] === null && this.readyQueue.length > 0) {
                const process = this.schedule();
                if (process) {
                    this.coreStates[core] = process.pid;
                }
            }
        }
    }

    // ===================================
    // Algorithm Management
    // ===================================

    setAlgorithm(algorithm) {
        const validAlgorithms = ['RR', 'FCFS', 'SJF', 'SRTF', 'PRIORITY', 'PRIORITY_PREEMPTIVE', 'MULTILEVEL'];
        if (validAlgorithms.includes(algorithm)) {
            this.algorithm = algorithm;
            console.log(`[Scheduler] Algorithm changed to: ${algorithm}`);
            return true;
        }
        return false;
    }

    setTimeQuantum(quantum) {
        this.timeQuantum = quantum;
        console.log(`[Scheduler] Time quantum set to: ${quantum}`);
    }

    // ===================================
    // Simulation Control
    // ===================================

    start() {
        this.isRunning = true;
        console.log('[Scheduler] Started');
    }

    stop() {
        this.isRunning = false;
        console.log('[Scheduler] Stopped');
    }

    reset() {
        this.currentTime = 0;
        this.readyQueue = [];
        this.ganttChart = [];
        this.coreStates = Array(this.cpuCores).fill(null);
        console.log('[Scheduler] Reset');
    }

    // ===================================
    // Statistics & Visualization
    // ===================================

    getGanttChart() {
        return this.ganttChart;
    }

    getReadyQueue() {
        return this.readyQueue;
    }

    getCoreStates() {
        return this.coreStates.map((pid, index) => ({
            core: index,
            pid: pid,
            process: pid ? this.processManager.getProcess(pid) : null
        }));
    }

    getAlgorithmInfo() {
        const info = {
            'RR': 'Round Robin - Each process gets equal time quantum',
            'FCFS': 'First-Come-First-Served - Processes executed in arrival order',
            'SJF': 'Shortest Job First - Shortest burst time first (non-preemptive)',
            'SRTF': 'Shortest Remaining Time First - Preemptive SJF',
            'PRIORITY': 'Priority Scheduling - Higher priority first (non-preemptive)',
            'PRIORITY_PREEMPTIVE': 'Priority Scheduling - Preemptive version',
            'MULTILEVEL': 'Multilevel Queue - System, Interactive, Batch queues'
        };
        return info[this.algorithm] || 'Unknown algorithm';
    }

    getStatistics() {
        const stats = this.processManager.getStatistics();
        return {
            ...stats,
            algorithm: this.algorithm,
            timeQuantum: this.timeQuantum,
            currentTime: this.currentTime,
            queueLength: this.readyQueue.length,
            ganttChartLength: this.ganttChart.length,
            cpuUtilization: this.calculateCPUUtilization()
        };
    }

    calculateCPUUtilization() {
        if (this.currentTime === 0) return 0;

        let busyTime = 0;
        this.ganttChart.forEach(entry => {
            busyTime += (entry.end - entry.start);
        });

        return (busyTime / (this.currentTime * this.cpuCores)) * 100;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CPUScheduler;
}
