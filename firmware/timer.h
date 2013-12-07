#include <avr/io.h>
#include <avr/interrupt.h> 
#include <stdint.h>

uint32_t timestamp;
uint16_t milliseconds;

inline void timer_init(void) {
	TCNT0 = 6;	//Preload for 250 ticks to overflow
	TIMSK |= (1 << TOIE0);
	TCCR0 = (1 << CS00) | (1 << CS01);	// Prescaler 64
	timestamp = 0;
	milliseconds = 0;
}

inline void timer_set(uint32_t stamp) {
	TCCR0 &= ~((1 << CS00) | (1 << CS01)); // stop the timer

	TCNT0 = 6;	//Preload for 250 ticks to overflow
	timestamp = stamp;
	milliseconds = 0;

	TCCR0 = (1 << CS00) | (1 << CS01);	// Restart timer
}


ISR(TIMER0_OVF_vect) {
	TCNT0 = 6; //Preload for 250 ticks to overflow

	milliseconds++;
	if(milliseconds > 999) {
		timestamp++;
		milliseconds = 0;
	}
}