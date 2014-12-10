#include <avr/io.h>
#include <util/delay.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "tubes.h"
#include "uart.h"
#include "timer.h"
#include "fifo.h"

#define OUTPUTBUFFER_SIZE 64
#define INPUTBUFFER_SIZE 32

enum {RESET, RUNNING, WAITACK} state;
char outputbuffer[OUTPUTBUFFER_SIZE];
char inputbuffer[INPUTBUFFER_SIZE];

void syncTime(const char* stamp) {
	uint32_t startime = strtoul(stamp,NULL,10);
	timer_set(startime);
	uart_puts("Sync ack\n");
}

uint8_t checkCommand(const char* cmd) {
	return (strncmp(inputbuffer,cmd, strlen(cmd)) == 0);
}

void generateEventMessage(const TubeEvent event) {
	char dir[9];

	if(event.direction == ONE_TO_TWO) {
		strcpy(dir,"OneToTwo");
	}
	else {
		strcpy(dir,"TwoToOne");
	}

	snprintf(outputbuffer, OUTPUTBUFFER_SIZE, "Capsule %u %lu %s %u\n", 
				event.tubenumber, event.timestamp, dir, event.time);
}

/*
 *  Initial state
 */
static inline void state_reset(void) {
	if(uart_get_line(inputbuffer,INPUTBUFFER_SIZE)) {
		if(checkCommand("Reset")) {
			uart_puts("Reset ack\n");
		}
		else if(checkCommand("Set")) {
			syncTime(inputbuffer + 4);
			fifo_clear(&eventfifo);
			state = RUNNING; 
		}
	}
}


/*
 * State in which we wate for new samples to come in
 */ 
static inline void state_running(void) {
	if(uart_get_line(inputbuffer,INPUTBUFFER_SIZE)) {
		if(checkCommand("Reset")) {
			uart_puts("Reset ack\n");
			state = RESET;
		}
		else if(checkCommand("Set")) {
			syncTime(inputbuffer + 4);
		}
	} else if(!fifo_empty(&eventfifo)) {
		TubeEvent event = fifo_get(&eventfifo);
		generateEventMessage(event);
		uart_puts(outputbuffer);
		state = WAITACK;
	}
	
}

/*
 * State in which we wait for a acknowledgement of the last sample send
 */
static inline void  state_waitack(void) {
	if(uart_get_line(inputbuffer,INPUTBUFFER_SIZE)) {
		if(checkCommand("Reset")) {
			uart_puts("Reset ack\n");
			state = RESET;
		}
		else if(checkCommand("Ack")) {
			state = RUNNING;
		}
	} else {
		//send message again
		uart_puts(outputbuffer);
	}
}


int main(void) {
	DDRC |= (1 << PC0) | (1 << PC1) | (1 << PC2);

	state = RESET;

	tubes_init();
	timer_init();
	uart_init();

	sei();

	while(1) {

		switch(state) {
			case RESET:
				state_reset();
				break;
			case RUNNING:
				state_running();
				break;
			case WAITACK:
				state_waitack();
				break;
		}

	}
	
}
