#include "tubes.h"

const Tube tube[TUBECOUNT] = {
	{&PINB, &PORTB, &DDRB, (1 << PB4), (1 << PB5)},
	{&PINB, &PORTB, &DDRB, (1 << PB3), (1 << PB2)},
};

TubeState tubestate[TUBECOUNT];

TubeEvent tubeeventdata[8];

void tubes_init(void) {
	uint8_t i;
	for(i = 0; i < TUBECOUNT; i++) {
		*(tube[i].ddr) &= ~(tube[i].pinmask1 | tube[i].pinmask2);
		*(tube[i].port) |= (tube[i].pinmask1 | tube[i].pinmask2);
		tubestate[i].status = IDLE;
		tubestate[i].retriggerdelay = 0;
		tubestate[i].timeoutdelay = 0;
		tubestate[i].milliseconds = 0;
	}

	fifo_init(&eventfifo, 8, tubeeventdata);
}
