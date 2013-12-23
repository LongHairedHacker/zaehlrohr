#include "timer.h"

volatile uint32_t timestamp;
volatile uint16_t milliseconds;

static inline void set_triggered(uint8_t id, enum TubeStatus status) {
	tubestate[id].status = status;
	tubestate[id].timeoutdelay = 1000;
	tubestate[id].milliseconds = milliseconds;
}

static inline void set_idle(uint8_t id, uint8_t set_retriggerdelay) {
	tubestate[id].status = IDLE;
	if(set_retriggerdelay) {
		tubestate[id].retriggerdelay = 100;
	}
	else {
		tubestate[id].retriggerdelay = 0;
	}
}


static inline void post_event(uint8_t id) {
	if(!fifo_full(&eventfifo)) {
		TubeEvent event;
		event.tubenumber = id;

		//We can use the current timestamp here,
		//since our event can be at maximum 500ms in the past do to our timeout.
		//This leads to an accuracy of +-1s which is accaptable.
		event.timestamp = timestamp;

		if(tubestate[id].status == TRIG1) {
			event.direction = ONE_TO_TWO;
		}
		else {
			event.direction = TWO_TO_ONE;
		}

		// Due to the timeoutdelay we can't have more then 500ms difference,
		// so the there is no need to consider the timestamp here
		if(milliseconds > tubestate[id].milliseconds) {
			//We are still in the same second
			event.time = milliseconds - tubestate[id].milliseconds;
		}	
		else {
			//We are in the next second
			event.time = milliseconds + (1000 - tubestate[id].milliseconds);
		}
		
		fifo_put(&eventfifo,event);
	}
}

ISR(TIMER0_OVF_vect) {
	TCNT0 = 6; //Preload for 250 ticks to overflow

	milliseconds++;
	if(milliseconds > 999) {
		timestamp++;
		milliseconds = 0;
	}

	uint8_t i;
	for(i = 0; i < TUBECOUNT; i++) {
		switch(tubestate[i].status) {
			case IDLE:
				//PORTC &= ~((1 << PC0) | (1 << PC1));
				if(tubestate[i].retriggerdelay == 0) {
					if((*(tube[i].pin) & tube[i].pinmask1) && !(*(tube[i].pin) & tube[i].pinmask2)) {
						set_triggered(i,TRIG1);
					}
					else if((*(tube[i].pin) & tube[i].pinmask2) && !(*(tube[i].pin) & tube[i].pinmask1)) {
						set_triggered(i,TRIG2);
					}
				}
				else {
					tubestate[i].retriggerdelay--;
				}
			break;
			
			case TRIG1:
				if((*(tube[i].pin) & tube[i].pinmask2) && !(*(tube[i].pin) & tube[i].pinmask1)) {
					post_event(i);
					set_idle(i,1);
				} else if(tubestate[i].timeoutdelay == 0) {
					set_idle(i,0);
				}
				else {
					tubestate[i].timeoutdelay--;
				}
				//PORTC |= (1 << PC0);
			break;
			
			case TRIG2:
				if((*(tube[i].pin) & tube[i].pinmask1) && !(*(tube[i].pin) & tube[i].pinmask2)) {
					post_event(i);
					set_idle(i,1);
				} else if(tubestate[i].timeoutdelay == 0) {
					set_idle(i,0);
				}
				else {
					tubestate[i].timeoutdelay--;
				}
				//PORTC |= (1 << PC1);
			break;
		}

	}
}