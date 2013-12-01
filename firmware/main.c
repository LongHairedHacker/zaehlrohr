#include <avr/io.h>
#include <util/delay.h>
#include <string.h>

#include "uart.h"



int main(void) {
	uint8_t i;

	uart_init();




	while(1) {


		if(PINB & (1 << PB2)) {
			uart_puts("Sensor 1\n");
		}


		if(PINB & (1 << PB3)) {
			uart_puts("Sensor 2\n");
		}
	

		for(i = 0; i < 15; i++) {
        	_delay_ms(1);
		}
	}
	
}