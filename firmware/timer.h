#ifndef TIMER_H_
#define TIMER_H_ TIMER_H_


#include <avr/io.h>
#include <avr/interrupt.h> 
#include <stdint.h>

#include "fifo.h"
#include "tubes.h"

extern volatile uint32_t timestamp;
extern volatile uint16_t milliseconds;

/*
 * Timer setting:
 * MCU running at 16MHz:
 * Prescaler is 64 which results in 250000 ticks per second
 * Preloading the counter with 6 leads to 1000 overflow interrupts per second
 * or one overflow every millisecond.
 *
 * MCU running at 7.372800Mhz
 * Prescaler is 256 which results in 28800 ticks per second.
 * Preloading the counter with 112 leads to 200 overflow interrupts per second
 * or one overflow every 5 milliseconds.
 */

static inline void timer_init(void) {
	TCNT0 = 6;	//Preload for 250 ticks to overflow
	TIMSK |= (1 << TOIE0);
	TCCR0 = (1 << CS00) | (1 << CS01);	// Prescaler 64 
	timestamp = 0;
	milliseconds = 0;
}

static inline void timer_set(uint32_t stamp) {
	TCCR0 &= ~((1 << CS00) | (1 << CS01)); // stop the timer

	TCNT0 = 6;	//Preload for 250 ticks to overflow
	timestamp = stamp;
	milliseconds = 0;

	TCCR0 = (1 << CS00) | (1 << CS01);	// Restart timer
}


#endif 