# Makefile for 3D OS Kernel (Windows/MinGW)

# Tools
# Using local NASM to avoid path issues
# Path confirmed: tools/nasm-2.16.01/nasm.exe
AS = tools/nasm-2.16.01/nasm.exe
CC = gcc
LD = ld

# QEMU Wrapper Script (uses Android SDK QEMU)
QEMU = qemu.bat

# Flags
# Use win32 for NASM to be compatible with MinGW GCC objects
ASFLAGS = -f win32
# Configure GCC for 32-bit freestanding (no stdlib) execution
CFLAGS = -m32 -ffreestanding -O2 -Wall -Wextra
# Link as i386pe (Windows PE format) using our linker script
LDFLAGS = -m i386pe -T linker.ld

# Objects
OBJS = boot/boot.o kernel/kernel.o

# Targets
all: kernel.bin

kernel.bin: $(OBJS)
	$(LD) $(LDFLAGS) -o $@ $^

boot/boot.o: boot/boot.asm
	$(AS) $(ASFLAGS) $< -o $@

kernel/kernel.o: kernel/kernel.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) kernel.bin

run: kernel.bin
	call $(QEMU) -kernel kernel.bin
