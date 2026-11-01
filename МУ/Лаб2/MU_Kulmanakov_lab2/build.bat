
bin\arm-none-eabi-as.exe main.s -o main.o
bin\arm-none-eabi-ld.exe -T stm32f42x_map.ld -o main.elf main.o
bin\arm-none-eabi-objcopy.exe -O ihex main.elf main.hex

pause
