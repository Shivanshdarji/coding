# 3D OS Kernel - Build Instructions

## Prerequisites

1.  **GCC (MinGW)** - Application to compile C code. (Installed ✅)
2.  **Make** - Application to automate the build. (Installed via `make.bat` ✅)
3.  **NASM** - Assembler. (Installed via `winget` ✅)
4.  **QEMU** - Emulator. (Installed via `winget` ✅)

**⚠️ CRITICAL STEP:**
You **MUST** restart your terminal (close VS Code and reopen it, or close the PowerShell window) for `nasm` and `qemu` to be recognized!

## Building & Running

1.  **Restart your terminal** strictly.
2.  Open the `OS-Kernel` directory.
3.  Run the following command:

```powershell
.\make run
```
(Note the `.\` which runs the `make.bat` file we created)

This will:
1.  Compile `boot.asm` and `kernel.c`
2.  Link them into `kernel.bin`
3.  Launch QEMU with the kernel

## Troubleshooting

- **"make is not recognized"**: Ensure you use `.\make` or just `make` if you are in the directory.
- **"nasm is not recognized"**: You didn't restart your terminal!
- **"qemu-system-i386 is not recognized"**: You didn't restart your terminal!
