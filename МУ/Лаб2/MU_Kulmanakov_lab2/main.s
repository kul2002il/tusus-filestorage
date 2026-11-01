.thumb
.cpu cortex-m4
.section .vectors

.word 0x20000000 + 0x30000
.word Start + 1


.section .text

@ STM32F429I-DISC1
@ green: PG13; red: PG14

.equ RCC, 0x40023800                   @ 2.3
.equ AHB1ENR_OFFSET, 0x30              @ 7.3.25
.equ RCC_AHB1ENR, RCC + AHB1ENR_OFFSET @
.equ RCC_AHB1ENR_GPIOGEN_BIT, 1<<6     @ 7.3.10

.equ GPIOG,  0x40021800       @ 2.3
.equ MODER_OFFSET, 0x00       @ 8.4.1
.equ MODER_BITS_FOR_OUTPUT, 1 @ 8.4.1
.equ BSSR_OFFSET,  0x18       @ 8.4.7 0..15 - set, 16..31 - reset.

.equ GPIO_LED, GPIOG
.equ GPIO_LED_MODER, GPIO_LED + MODER_OFFSET
.equ GPIO_LED_BSSR, GPIO_LED + BSSR_OFFSET

.equ LED_RED_NUMBER, 14
.equ LED_GREEN_NUMBER, 13

Start:
@ Enable GPIOG
LDR R0, =RCC_AHB1ENR
LDR R1, =RCC_AHB1ENR_GPIOGEN_BIT
LDR R2, [R0]
ORR R2, R1
STR R2, [R0]

@ Set led pin in output mode
LDR R0, =GPIO_LED_MODER
LDR R1, =(MODER_BITS_FOR_OUTPUT << (LED_RED_NUMBER * 2)) | (MODER_BITS_FOR_OUTPUT << (LED_GREEN_NUMBER * 2))
LDR R2, [R0]
ORR R2, R1
STR R2, [R0]

@ Led on
LDR R0, =GPIO_LED_BSSR
LDR R1, =(1<<LED_RED_NUMBER) | (1<<LED_GREEN_NUMBER)
LDR R2, [R0]
ORR R2, R1
STR R2, [R0]




