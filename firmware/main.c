#include <avr/io.h>
#include <util/delay.h>
#include <string.h>
#include <stdlib.h>

#include "tubes.h"
#include "uart.h"
#include "timer.h"



enum state_t {RESET, RUNNING, WAITACK};


void syncTime(const char* buffer) {
	uint32_t startime = strtoul(buffer,NULL,10);
	timer_set(startime);
	uart_puts("Sync ack\n");
}

uint8_t checkCommand(const char* buffer, const char* cmd) {
	return (strncmp(buffer,cmd, strlen(cmd)) == 0);
}


/*
 *  Initial state
 */
enum state_t state_reset(void) {
	char buffer[32];
	if(uart_get_line(buffer,32)) {
		if(checkCommand(buffer,"Reset")) {
			uart_puts("Reset ack\n");
			return RESET;
		}
		else if(checkCommand(buffer,"Set")) {
			syncTime(buffer + 4);
			return RUNNING; 
		}
	}

	return RESET;
}


/*
 * State in which we wate for new samples to come in
 */ 
enum state_t state_running(void) {
	char buffer[32];

	if(uart_get_line(buffer,32)) {
		if(checkCommand(buffer,"Reset")) {
			uart_puts("Reset ack\n");
			return RESET;
		}
		else if(checkCommand(buffer,"Set")) {
			syncTime(buffer + 4);
			return RUNNING;
		}
	}

	/*
	if(new sample avaiable) {
		send sample
		return WAITACK;
	}
	*/
	return RUNNING;
}


/*
 * State in which we wait for a acknowledgement of the last sample send
 */
enum state_t state_waitack(void) {
	char buffer[32];

	if(uart_get_line(buffer,32)) {
		if(checkCommand(buffer,"Reset")) {
			uart_puts("Reset ack\n");
			return RESET;
		}
		else if(checkCommand(buffer,"Ack")) {
			return RUNNING;
		}
	}

	/*
	 *	send sample again
	 */
	return WAITACK;
}


int main(void) {
	DDRC |= (1 << PC0) | (1 << PC1) | (1 << PC2);

	enum state_t state = RESET;

	tubes_init();
	timer_init();
	uart_init();

	sei();

	while(1) {

		switch(state) {
			case RESET:
				state = state_reset();
				break;
			case RUNNING:
				state = state_running();
			break;
			case WAITACK:
				state = state_waitack();
			break;
		}

	}
	
}