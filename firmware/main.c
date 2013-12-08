#include <avr/io.h>
#include <util/delay.h>
#include <string.h>
#include <stdlib.h>

#include "uart.h"
#include "timer.h"


int main(void) {
	uint8_t i;

	timer_init();
	uart_init();

	/* Quick and dirty initial time synchronization
	 *TODO: replace with something robust 
	 *  ----- snipp -----
	 */ 
	char tmp[12];

	uint8_t c = 0;
	while(c < 11) {
		char t = uart_getc_timeout();
		if(uart_timed_out && (c == 10 && t != '\n')) {
			c = 0;
			//uart_putc('\n');
		}
		else {
			//uart_putc(t);
 			tmp[c] = t;
 			c++;
		}
	}
	tmp[11] = 0;
	uint32_t startime = strtoul(tmp,NULL,10);
	timer_set(startime);

	//   ----- snapp -----

	sei();

	while(1) {

		/*
		if(PINB & (1 << PB2)) {
			uart_puts("Sensor 1\n");
		}

		if(PINB & (1 << PB3)) {
			uart_puts("Sensor 2\n");
		}
		*/

		// This is only testcode for debugging the timer

		uart_puts("timestamp: ");

		ultoa(timestamp,tmp,10);
		tmp[11] = 0;
		uart_puts(tmp);

		uart_putc(':');

		utoa(milliseconds,tmp,10);
		tmp[11] = 0;
		uart_puts(tmp);

		uart_puts("\n");

		for(i = 0; i < 250; i++) {
        	_delay_ms(1);
		}
	}
	
}