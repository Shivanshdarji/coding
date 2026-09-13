; ==============================================================================
; Bootloader for 3D OS Kernel
; ==============================================================================

; Multiboot header constants
MBOOT_PAGE_ALIGN    equ 1 << 0
MBOOT_MEM_INFO      equ 1 << 1
MBOOT_HEADER_MAGIC  equ 0x1BADB002
MBOOT_HEADER_FLAGS  equ MBOOT_PAGE_ALIGN | MBOOT_MEM_INFO
MBOOT_CHECKSUM      equ -(MBOOT_HEADER_MAGIC + MBOOT_HEADER_FLAGS)

; Bit 31 in standard register means paging is enabled
CR0_PAGING_BIT      equ 0x80000000

; Define the Multiboot header
section .multiboot
align 4
    dd MBOOT_HEADER_MAGIC
    dd MBOOT_HEADER_FLAGS
    dd MBOOT_CHECKSUM

; Stack configuration
section .bss
align 16
stack_bottom:
    resb 16384 ; 16 KB stack
stack_top:

; Entry point
section .text
global _start
; MinGW GCC adds an underscore to C functions, so we look for _kernel_main
extern _kernel_main

_start:
    ; Set up the stack
    mov esp, stack_top

    ; Push Multiboot data structure pointer (in EBX)
    push ebx
    
    ; Push magic number (in EAX)
    push eax

    ; Call the high-level kernel (note the underscore)
    call _kernel_main

    ; If kernel returns, disable interrupts and hang
    cli
.hang:
    hlt
    jmp .hang
