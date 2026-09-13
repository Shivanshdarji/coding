// ===================================
// File System - Virtual File System with Inodes
// ===================================

class FileSystem {
    constructor() {
        // Disk Configuration
        this.diskSize = 512 * 1024; // 512 GB in MB
        this.blockSize = 4; // 4 MB per block
        this.totalBlocks = this.diskSize / this.blockSize;

        // Inode Configuration
        this.maxInodes = 10000;
        this.inodes = new Map(); // inode number -> inode
        this.nextInodeNumber = 1;

        // Block Management
        this.blocks = new Array(this.totalBlocks).fill(null);
        this.freeBlocks = Array.from({ length: this.totalBlocks }, (_, i) => i);
        this.usedBlocks = new Map(); // inode -> [block indices]

        // Directory Structure
        this.root = this.createDirectory('/', null);
        this.currentDirectory = this.root;

        // File Allocation Method
        this.allocationMethod = 'INDEXED'; // CONTIGUOUS, LINKED, INDEXED

        // I/O Scheduling
        this.ioScheduler = new IOScheduler();

        // Statistics
        this.filesCreated = 0;
        this.filesDeleted = 0;
        this.bytesWritten = 0;
        this.bytesRead = 0;
    }

    // ===================================
    // Inode Management
    // ===================================

    createInode(name, type, parent) {
        const inode = {
            number: this.nextInodeNumber++,
            name: name,
            type: type, // 'file' or 'directory'
            parent: parent,
            size: 0,
            blocks: [],
            created: Date.now(),
            modified: Date.now(),
            accessed: Date.now(),
            permissions: {
                owner: { read: true, write: true, execute: type === 'directory' },
                group: { read: true, write: false, execute: type === 'directory' },
                others: { read: true, write: false, execute: false }
            },
            owner: 'root',
            group: 'root',
            children: type === 'directory' ? new Map() : null,
            content: type === 'file' ? '' : null,
            links: 1
        };

        this.inodes.set(inode.number, inode);

        return inode;
    }

    // ===================================
    // File Operations
    // ===================================

    createFile(name, content = '', parent = null) {
        parent = parent || this.currentDirectory;

        // Check if file already exists
        if (parent.children && parent.children.has(name)) {
            console.error(`[FileSystem] File ${name} already exists`);
            return null;
        }

        const inode = this.createInode(name, 'file', parent.number);

        if (content) {
            this.writeFile(inode.number, content);
        }

        if (parent.children) {
            parent.children.set(name, inode.number);
        }

        this.filesCreated++;
        console.log(`[FileSystem] Created file: ${this.getPath(inode)}`);

        return inode;
    }

    createDirectory(name, parent = null) {
        parent = parent || this.currentDirectory;

        // Check if directory already exists
        if (parent && parent.children && parent.children.has(name)) {
            console.error(`[FileSystem] Directory ${name} already exists`);
            return null;
        }

        const inode = this.createInode(name, 'directory', parent ? parent.number : null);

        if (parent && parent.children) {
            parent.children.set(name, inode.number);
        }

        console.log(`[FileSystem] Created directory: ${this.getPath(inode)}`);

        return inode;
    }

    deleteFile(inodeNumber) {
        const inode = this.inodes.get(inodeNumber);
        if (!inode) return false;

        if (inode.type === 'directory' && inode.children.size > 0) {
            console.error(`[FileSystem] Directory not empty`);
            return false;
        }

        // Free blocks
        this.freeBlocks.push(...inode.blocks);
        inode.blocks.forEach(block => {
            this.blocks[block] = null;
        });

        // Remove from parent
        if (inode.parent) {
            const parent = this.inodes.get(inode.parent);
            if (parent && parent.children) {
                parent.children.delete(inode.name);
            }
        }

        this.inodes.delete(inodeNumber);
        this.filesDeleted++;

        console.log(`[FileSystem] Deleted: ${inode.name}`);

        return true;
    }

    readFile(inodeNumber) {
        const inode = this.inodes.get(inodeNumber);
        if (!inode || inode.type !== 'file') return null;

        inode.accessed = Date.now();
        this.bytesRead += inode.size;

        // Schedule I/O operation
        this.ioScheduler.addRequest({
            type: 'READ',
            inode: inodeNumber,
            block: inode.blocks[0] || 0,
            time: Date.now()
        });

        return inode.content;
    }

    writeFile(inodeNumber, content) {
        const inode = this.inodes.get(inodeNumber);
        if (!inode || inode.type !== 'file') return false;

        const sizeNeeded = Math.ceil(content.length / 1024); // KB to MB
        const blocksNeeded = Math.ceil(sizeNeeded / this.blockSize);

        // Free old blocks
        if (inode.blocks.length > 0) {
            this.freeBlocks.push(...inode.blocks);
            inode.blocks.forEach(block => {
                this.blocks[block] = null;
            });
            inode.blocks = [];
        }

        // Allocate new blocks
        const allocatedBlocks = this.allocateBlocks(blocksNeeded, inode.number);
        if (allocatedBlocks.length < blocksNeeded) {
            console.error(`[FileSystem] Not enough disk space`);
            return false;
        }

        inode.blocks = allocatedBlocks;
        inode.content = content;
        inode.size = content.length;
        inode.modified = Date.now();

        this.bytesWritten += content.length;

        // Schedule I/O operation
        this.ioScheduler.addRequest({
            type: 'WRITE',
            inode: inodeNumber,
            block: allocatedBlocks[0],
            time: Date.now()
        });

        return true;
    }

    // ===================================
    // Block Allocation
    // ===================================

    allocateBlocks(count, inodeNumber) {
        if (count > this.freeBlocks.length) {
            return [];
        }

        let allocated = [];

        switch (this.allocationMethod) {
            case 'CONTIGUOUS':
                allocated = this.allocateContiguous(count);
                break;
            case 'LINKED':
                allocated = this.allocateLinked(count);
                break;
            case 'INDEXED':
                allocated = this.allocateIndexed(count);
                break;
        }

        allocated.forEach(block => {
            this.blocks[block] = inodeNumber;
            this.freeBlocks = this.freeBlocks.filter(b => b !== block);
        });

        return allocated;
    }

    allocateContiguous(count) {
        // Find contiguous block sequence
        for (let i = 0; i <= this.totalBlocks - count; i++) {
            let contiguous = true;
            for (let j = 0; j < count; j++) {
                if (!this.freeBlocks.includes(i + j)) {
                    contiguous = false;
                    break;
                }
            }
            if (contiguous) {
                return Array.from({ length: count }, (_, k) => i + k);
            }
        }
        return [];
    }

    allocateLinked(count) {
        // Allocate any available blocks (linked list)
        return this.freeBlocks.slice(0, count);
    }

    allocateIndexed(count) {
        // Allocate blocks and use index block
        return this.freeBlocks.slice(0, count);
    }

    // ===================================
    // Directory Operations
    // ===================================

    changeDirectory(path) {
        const inode = this.resolvePath(path);
        if (!inode || inode.type !== 'directory') {
            console.error(`[FileSystem] Invalid directory: ${path}`);
            return false;
        }

        this.currentDirectory = inode;
        return true;
    }

    listDirectory(inodeNumber = null) {
        const dir = inodeNumber ? this.inodes.get(inodeNumber) : this.currentDirectory;
        if (!dir || dir.type !== 'directory') return [];

        const entries = [];
        dir.children.forEach((childInodeNum, name) => {
            const child = this.inodes.get(childInodeNum);
            entries.push({
                name: name,
                type: child.type,
                size: child.size,
                modified: child.modified,
                permissions: child.permissions,
                inode: child.number
            });
        });

        return entries;
    }

    resolvePath(path) {
        if (path === '/') return this.root;

        const parts = path.split('/').filter(p => p);
        let current = path.startsWith('/') ? this.root : this.currentDirectory;

        for (const part of parts) {
            if (part === '..') {
                if (current.parent) {
                    current = this.inodes.get(current.parent);
                }
            } else if (part !== '.') {
                if (!current.children || !current.children.has(part)) {
                    return null;
                }
                current = this.inodes.get(current.children.get(part));
            }
        }

        return current;
    }

    getPath(inode) {
        if (!inode || inode === this.root) return '/';

        const parts = [];
        let current = inode;

        while (current && current !== this.root) {
            parts.unshift(current.name);
            current = current.parent ? this.inodes.get(current.parent) : null;
        }

        return '/' + parts.join('/');
    }

    // ===================================
    // Statistics
    // ===================================

    getStatistics() {
        const usedBlocks = this.totalBlocks - this.freeBlocks.length;
        const usedSpace = usedBlocks * this.blockSize;
        const freeSpace = this.freeBlocks.length * this.blockSize;

        return {
            totalSpace: this.diskSize,
            usedSpace: usedSpace,
            freeSpace: freeSpace,
            usagePercent: (usedSpace / this.diskSize) * 100,
            totalInodes: this.inodes.size,
            maxInodes: this.maxInodes,
            filesCreated: this.filesCreated,
            filesDeleted: this.filesDeleted,
            bytesWritten: this.bytesWritten,
            bytesRead: this.bytesRead,
            allocationMethod: this.allocationMethod,
            ioStats: this.ioScheduler.getStatistics()
        };
    }

    // ===================================
    // Demo Files
    // ===================================

    createDemoFiles() {
        // Create directory structure
        const home = this.createDirectory('home', this.root);
        const user = this.createDirectory('user', home);
        const docs = this.createDirectory('Documents', user);
        const pics = this.createDirectory('Pictures', user);
        const downloads = this.createDirectory('Downloads', user);

        // Create some files
        this.createFile('readme.txt', 'Welcome to 3D OS!', user);
        this.createFile('notes.txt', 'This is a note file.', docs);
        this.createFile('todo.txt', '1. Build OS\n2. Test OS\n3. Deploy OS', docs);
        this.createFile('image1.jpg', '[Binary image data]', pics);
        this.createFile('download.zip', '[Binary archive data]', downloads);

        // System directories
        const etc = this.createDirectory('etc', this.root);
        const var_dir = this.createDirectory('var', this.root);
        const usr = this.createDirectory('usr', this.root);

        this.createFile('config.conf', 'system_config=true', etc);
        this.createFile('log.txt', 'System started successfully', var_dir);
    }
}

// ===================================
// I/O Scheduler
// ===================================

class IOScheduler {
    constructor() {
        this.algorithm = 'SCAN'; // FCFS, SSTF, SCAN, C-SCAN
        this.requestQueue = [];
        this.currentPosition = 0;
        this.direction = 'up'; // up or down
        this.totalSeekTime = 0;
        this.requestsProcessed = 0;
    }

    addRequest(request) {
        this.requestQueue.push(request);
    }

    schedule() {
        if (this.requestQueue.length === 0) return null;

        let request = null;

        switch (this.algorithm) {
            case 'FCFS':
                request = this.scheduleFCFS();
                break;
            case 'SSTF':
                request = this.scheduleSSTF();
                break;
            case 'SCAN':
                request = this.scheduleSCAN();
                break;
            case 'C-SCAN':
                request = this.scheduleCSCAN();
                break;
        }

        if (request) {
            this.totalSeekTime += Math.abs(request.block - this.currentPosition);
            this.currentPosition = request.block;
            this.requestsProcessed++;
        }

        return request;
    }

    scheduleFCFS() {
        return this.requestQueue.shift();
    }

    scheduleSSTF() {
        // Shortest Seek Time First
        let closest = 0;
        let minDistance = Infinity;

        this.requestQueue.forEach((req, index) => {
            const distance = Math.abs(req.block - this.currentPosition);
            if (distance < minDistance) {
                minDistance = distance;
                closest = index;
            }
        });

        return this.requestQueue.splice(closest, 1)[0];
    }

    scheduleSCAN() {
        // Elevator algorithm
        const filtered = this.direction === 'up'
            ? this.requestQueue.filter(r => r.block >= this.currentPosition)
            : this.requestQueue.filter(r => r.block <= this.currentPosition);

        if (filtered.length === 0) {
            this.direction = this.direction === 'up' ? 'down' : 'up';
            return this.schedule();
        }

        filtered.sort((a, b) => this.direction === 'up' ? a.block - b.block : b.block - a.block);
        const request = filtered[0];
        this.requestQueue = this.requestQueue.filter(r => r !== request);

        return request;
    }

    scheduleCSCAN() {
        // Circular SCAN
        const filtered = this.requestQueue.filter(r => r.block >= this.currentPosition);

        if (filtered.length === 0) {
            this.currentPosition = 0;
            return this.schedule();
        }

        filtered.sort((a, b) => a.block - b.block);
        const request = filtered[0];
        this.requestQueue = this.requestQueue.filter(r => r !== request);

        return request;
    }

    getStatistics() {
        return {
            algorithm: this.algorithm,
            queueLength: this.requestQueue.length,
            totalSeekTime: this.totalSeekTime,
            requestsProcessed: this.requestsProcessed,
            avgSeekTime: this.requestsProcessed > 0 ? this.totalSeekTime / this.requestsProcessed : 0
        };
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { FileSystem, IOScheduler };
}
