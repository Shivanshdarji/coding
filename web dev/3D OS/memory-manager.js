// ===================================
// Memory Manager - Virtual Memory & Paging
// ===================================

class MemoryManager {
    constructor() {
        // Physical Memory Configuration
        this.totalMemory = 16 * 1024; // 16 GB in MB
        this.pageSize = 4; // 4 MB per page
        this.totalPages = this.totalMemory / this.pageSize;

        // Memory Structures
        this.physicalMemory = new Array(this.totalPages).fill(null);
        this.freeFrames = Array.from({ length: this.totalPages }, (_, i) => i);
        this.allocatedFrames = new Map(); // pid -> [frame indices]

        // Page Tables (per process)
        this.pageTables = new Map(); // pid -> page table

        // Page Replacement
        this.pageReplacementAlgorithm = 'LRU'; // LRU, FIFO, OPTIMAL
        this.pageAccessHistory = []; // For LRU
        this.pageQueue = []; // For FIFO

        // Statistics
        this.pageFaults = 0;
        this.pageHits = 0;
        this.swapOuts = 0;
        this.swapIns = 0;

        // Allocation Algorithm
        this.allocationAlgorithm = 'FIRST_FIT'; // FIRST_FIT, BEST_FIT, WORST_FIT

        // Fragmentation tracking
        this.externalFragmentation = 0;
        this.internalFragmentation = 0;
    }

    // ===================================
    // Memory Allocation
    // ===================================

    allocateMemory(pid, size) {
        const pagesNeeded = Math.ceil(size / this.pageSize);

        if (pagesNeeded > this.freeFrames.length) {
            console.error(`[MemoryManager] Not enough memory for process ${pid}`);
            return false;
        }

        let allocatedFrames = [];

        switch (this.allocationAlgorithm) {
            case 'FIRST_FIT':
                allocatedFrames = this.firstFit(pagesNeeded);
                break;
            case 'BEST_FIT':
                allocatedFrames = this.bestFit(pagesNeeded);
                break;
            case 'WORST_FIT':
                allocatedFrames = this.worstFit(pagesNeeded);
                break;
        }

        if (allocatedFrames.length < pagesNeeded) {
            return false;
        }

        // Allocate frames
        allocatedFrames.forEach(frame => {
            this.physicalMemory[frame] = pid;
            this.freeFrames = this.freeFrames.filter(f => f !== frame);
        });

        // Store allocation
        if (!this.allocatedFrames.has(pid)) {
            this.allocatedFrames.set(pid, []);
        }
        this.allocatedFrames.get(pid).push(...allocatedFrames);

        // Create page table
        this.createPageTable(pid, pagesNeeded);

        // Calculate internal fragmentation
        const actualUsed = size;
        const allocated = pagesNeeded * this.pageSize;
        this.internalFragmentation += (allocated - actualUsed);

        console.log(`[MemoryManager] Allocated ${pagesNeeded} pages (${size}MB) for process ${pid}`);

        return true;
    }

    // First Fit Algorithm
    firstFit(pagesNeeded) {
        return this.freeFrames.slice(0, pagesNeeded);
    }

    // Best Fit Algorithm
    bestFit(pagesNeeded) {
        // Find smallest contiguous block that fits
        let bestStart = -1;
        let bestSize = Infinity;

        let currentStart = -1;
        let currentSize = 0;

        for (let i = 0; i < this.totalPages; i++) {
            if (this.freeFrames.includes(i)) {
                if (currentStart === -1) currentStart = i;
                currentSize++;
            } else {
                if (currentSize >= pagesNeeded && currentSize < bestSize) {
                    bestStart = currentStart;
                    bestSize = currentSize;
                }
                currentStart = -1;
                currentSize = 0;
            }
        }

        // Check last block
        if (currentSize >= pagesNeeded && currentSize < bestSize) {
            bestStart = currentStart;
            bestSize = currentSize;
        }

        if (bestStart !== -1) {
            return this.freeFrames.filter(f => f >= bestStart && f < bestStart + pagesNeeded);
        }

        return this.freeFrames.slice(0, pagesNeeded);
    }

    // Worst Fit Algorithm
    worstFit(pagesNeeded) {
        // Find largest contiguous block
        let worstStart = -1;
        let worstSize = 0;

        let currentStart = -1;
        let currentSize = 0;

        for (let i = 0; i < this.totalPages; i++) {
            if (this.freeFrames.includes(i)) {
                if (currentStart === -1) currentStart = i;
                currentSize++;
            } else {
                if (currentSize > worstSize) {
                    worstStart = currentStart;
                    worstSize = currentSize;
                }
                currentStart = -1;
                currentSize = 0;
            }
        }

        // Check last block
        if (currentSize > worstSize) {
            worstStart = currentStart;
            worstSize = currentSize;
        }

        if (worstStart !== -1) {
            return this.freeFrames.filter(f => f >= worstStart && f < worstStart + pagesNeeded);
        }

        return this.freeFrames.slice(0, pagesNeeded);
    }

    deallocateMemory(pid) {
        const frames = this.allocatedFrames.get(pid);
        if (!frames) return false;

        // Free all frames
        frames.forEach(frame => {
            this.physicalMemory[frame] = null;
            this.freeFrames.push(frame);
        });

        this.freeFrames.sort((a, b) => a - b);

        // Remove allocation
        this.allocatedFrames.delete(pid);
        this.pageTables.delete(pid);

        console.log(`[MemoryManager] Deallocated memory for process ${pid}`);

        return true;
    }

    // ===================================
    // Paging & Page Tables
    // ===================================

    createPageTable(pid, numPages) {
        const pageTable = [];
        const frames = this.allocatedFrames.get(pid);

        for (let i = 0; i < numPages; i++) {
            pageTable.push({
                pageNumber: i,
                frameNumber: frames[i],
                valid: true,
                dirty: false,
                referenced: false,
                lastAccessed: Date.now()
            });
        }

        this.pageTables.set(pid, pageTable);
        return pageTable;
    }

    translateAddress(pid, virtualAddress) {
        const pageTable = this.pageTables.get(pid);
        if (!pageTable) {
            console.error(`[MemoryManager] No page table for process ${pid}`);
            return null;
        }

        const pageNumber = Math.floor(virtualAddress / this.pageSize);
        const offset = virtualAddress % this.pageSize;

        if (pageNumber >= pageTable.length) {
            console.error(`[MemoryManager] Invalid page number ${pageNumber}`);
            return null;
        }

        const pageEntry = pageTable[pageNumber];

        if (!pageEntry.valid) {
            // Page fault!
            this.handlePageFault(pid, pageNumber);
            return null;
        }

        // Page hit
        this.pageHits++;
        pageEntry.referenced = true;
        pageEntry.lastAccessed = Date.now();
        this.pageAccessHistory.push({ pid, pageNumber, time: Date.now() });

        const physicalAddress = (pageEntry.frameNumber * this.pageSize) + offset;
        return physicalAddress;
    }

    handlePageFault(pid, pageNumber) {
        this.pageFaults++;
        console.log(`[MemoryManager] Page fault for process ${pid}, page ${pageNumber}`);

        // Find a free frame or evict a page
        let frame = null;

        if (this.freeFrames.length > 0) {
            frame = this.freeFrames.shift();
        } else {
            // Need to evict a page
            frame = this.evictPage();
        }

        // Load page into frame
        this.loadPage(pid, pageNumber, frame);
    }

    evictPage() {
        let victimFrame = null;

        switch (this.pageReplacementAlgorithm) {
            case 'FIFO':
                victimFrame = this.evictFIFO();
                break;
            case 'LRU':
                victimFrame = this.evictLRU();
                break;
            case 'OPTIMAL':
                victimFrame = this.evictOptimal();
                break;
        }

        this.swapOuts++;
        return victimFrame;
    }

    evictFIFO() {
        // Evict oldest page
        if (this.pageQueue.length === 0) {
            return this.allocatedFrames.values().next().value[0];
        }

        const victim = this.pageQueue.shift();
        return victim.frame;
    }

    evictLRU() {
        // Evict least recently used page
        if (this.pageAccessHistory.length === 0) {
            return this.allocatedFrames.values().next().value[0];
        }

        // Find page with oldest access time
        let oldestAccess = Infinity;
        let victimFrame = null;

        this.pageTables.forEach((pageTable, pid) => {
            pageTable.forEach(entry => {
                if (entry.valid && entry.lastAccessed < oldestAccess) {
                    oldestAccess = entry.lastAccessed;
                    victimFrame = entry.frameNumber;
                }
            });
        });

        return victimFrame;
    }

    evictOptimal() {
        // Evict page that won't be used for longest time (requires future knowledge)
        // For simulation, we'll use LRU as approximation
        return this.evictLRU();
    }

    loadPage(pid, pageNumber, frame) {
        const pageTable = this.pageTables.get(pid);
        if (!pageTable) return;

        pageTable[pageNumber].frameNumber = frame;
        pageTable[pageNumber].valid = true;
        pageTable[pageNumber].lastAccessed = Date.now();

        this.physicalMemory[frame] = pid;
        this.swapIns++;

        this.pageQueue.push({ pid, pageNumber, frame });
    }

    // ===================================
    // Memory Statistics
    // ===================================

    getMemoryUsage() {
        const used = this.totalPages - this.freeFrames.length;
        const usedMB = used * this.pageSize;
        const freeMB = this.freeFrames.length * this.pageSize;

        return {
            total: this.totalMemory,
            used: usedMB,
            free: freeMB,
            usagePercent: (usedMB / this.totalMemory) * 100,
            totalPages: this.totalPages,
            usedPages: used,
            freePages: this.freeFrames.length
        };
    }

    getStatistics() {
        const usage = this.getMemoryUsage();

        return {
            ...usage,
            pageFaults: this.pageFaults,
            pageHits: this.pageHits,
            hitRatio: this.pageHits / (this.pageHits + this.pageFaults) || 0,
            swapIns: this.swapIns,
            swapOuts: this.swapOuts,
            internalFragmentation: this.internalFragmentation,
            externalFragmentation: this.calculateExternalFragmentation(),
            allocationAlgorithm: this.allocationAlgorithm,
            pageReplacementAlgorithm: this.pageReplacementAlgorithm
        };
    }

    calculateExternalFragmentation() {
        // Calculate total free space in non-contiguous blocks
        let fragments = 0;
        let inBlock = false;

        for (let i = 0; i < this.totalPages; i++) {
            if (this.freeFrames.includes(i)) {
                if (!inBlock) {
                    fragments++;
                    inBlock = true;
                }
            } else {
                inBlock = false;
            }
        }

        return fragments;
    }

    getMemoryMap() {
        return this.physicalMemory.map((pid, frame) => ({
            frame,
            pid,
            address: frame * this.pageSize,
            isFree: pid === null
        }));
    }

    // ===================================
    // Configuration
    // ===================================

    setAllocationAlgorithm(algorithm) {
        const valid = ['FIRST_FIT', 'BEST_FIT', 'WORST_FIT'];
        if (valid.includes(algorithm)) {
            this.allocationAlgorithm = algorithm;
            console.log(`[MemoryManager] Allocation algorithm set to: ${algorithm}`);
            return true;
        }
        return false;
    }

    setPageReplacementAlgorithm(algorithm) {
        const valid = ['FIFO', 'LRU', 'OPTIMAL'];
        if (valid.includes(algorithm)) {
            this.pageReplacementAlgorithm = algorithm;
            console.log(`[MemoryManager] Page replacement algorithm set to: ${algorithm}`);
            return true;
        }
        return false;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MemoryManager;
}
