.thumb
.cpu cortex-m4
.section .vectors

@ STM32F429I-DISC1
@ SRAM1 and SRAM2 mapped at address 0x2000 0000
@ – Main internal SRAM1 (112 KB)
@ – Auxiliary internal SRAM2 (16 KB)
@ – Auxiliary internal SRAM3 (64 KB)


.word 0x20000000 + 0x30000
.word Start + 1

.text
Start:












