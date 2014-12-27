#ifndef TUBES_H
#define TUBES_H TUBES_H

#include <stdlib.h>
#include <avr/io.h>

#include "fifo.h"

#define TUBECOUNT 6 

typedef struct {
	volatile uint8_t *pin;
	volatile uint8_t *port;
	volatile uint8_t *ddr;
	uint8_t pinmask1, pinmask2;
} Tube;

extern const Tube tube[TUBECOUNT];

enum TubeStatus {
	IDLE, 
	TRIG1, 
	TRIG2
};

typedef struct {
	enum TubeStatus status;
	uint16_t milliseconds;
	uint16_t timeoutdelay;
	uint8_t retriggerdelay;
} TubeState;

extern TubeState tubestate[TUBECOUNT];

void tubes_init(void);


#endif
