MEMORY
{
	FLASH (RX) : ORIGIN = 0x08000000, LENGTH = 2M
	SRAM (RW) : ORIGIN = 0x20000000, LENGTH = 0x30000
}

SECTIONS
{
	.text :
	{
		*(.vectors);
		*(.text)
	} > FLASH
	.data :
	{
		*(.data)
	}>SRAM AT>FLASH
	.bss :
	{
		. = ALIGN(1);
		*(.bss);
	} > SRAM
}




