AVRMCU = atmega8
F_CPU = 16000000
ISPPORT = /dev/ttyUSB0

VERSION = 0.1

HEADERS = uart.h timer.h tubes.h fifo.h
SRC = main.c uart.c timer.c tubes.c fifo.c
TARGET = zahlrohr-$(AVRMCU)
OBJDIR = bin

CC = avr-gcc
OBJCOPY = avr-objcopy
OBJDUMP = avr-objdump
SIZE = avr-size


OBJ = $(SRC:%.c=$(OBJDIR)/%.o)

CFLAGS = -Os -Wall -Wstrict-prototypes 
CFLAGS += -fshort-enums -fpack-struct -funsigned-char -funsigned-bitfields
CFLAGS += -mmcu=$(AVRMCU) -DF_CPU=$(F_CPU)UL -DVERSION=$(VERSION)


all: start $(OBJDIR)/$(TARGET).hex size
	@echo ":: Done !"
	
start:
	@echo "Zaehlrohr firmare version $(VERSION)"
	@echo "===================================="
	@echo ":: Building for $(AVRMCU)"
	@echo ":: MCU operating frequency is $(F_CPU)Hz"
	
$(OBJDIR)/%.o : %.c $(HEADERS)
	@mkdir -p $$(dirname $@)
	$(CC) $(CFLAGS) -c $< -o $@

	
$(OBJDIR)/$(TARGET).elf : $(OBJ)
	$(CC) $(CFLAGS) $+ -o $@
	
$(OBJDIR)/$(TARGET).hex : $(OBJDIR)/$(TARGET).elf
	$(OBJCOPY) -O ihex $< $@

size : $(OBJDIR)/$(TARGET).elf
	@echo
	@$(SIZE) $(OBJDIR)/$(TARGET).hex
	@echo
	
clean :
	@rm -rf $(OBJDIR)
	
flash : all
	avrdude -c arduino \
		-p $(AVRMCU) -P $(ISPPORT) \
        -U flash:w:$(OBJDIR)/$(TARGET).hex 
