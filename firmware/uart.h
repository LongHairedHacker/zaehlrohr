#ifndef UART_H_
#define UART_H_ UART_H_

#include  <avr/io.h>
#include  <stdlib.h>
#include  <util/delay.h>


//#define BAUD 76800UL		// baudrate
#define BAUD 9600UL
#define UART_TIMEOUT 100	// Timeout in ms

// Some calculations ...
#define UBRR_VAL ((F_CPU+BAUD*8)/(BAUD*16)-1)   // Rounding magic
#define BAUD_REAL (F_CPU/(16*(UBRR_VAL+1)))     // Real baudrate
#define BAUD_ERROR ((BAUD_REAL*1000)/BAUD)		// Error in 0,1%

#if ((BAUD_ERROR<950) || (BAUD_ERROR>1050))		// Make sure your UBRR_VAL will work
  #error Baudrate error is bigger then 1% !
#endif

static uint8_t uart_timed_out = 0;

static inline void uart_init(void) {
	UBRRH = UBRR_VAL >> 8;		//Setting baudrate
	UBRRL = UBRR_VAL & 0xFF;

	UCSRB |= (1<<TXEN) | (1<<RXEN);  // UART TX
	UCSRC = (1<<URSEL)|(1<<UCSZ1)|(1<<UCSZ0);  // Asynchronous 8N1

	    // flush receive buffer
    do
    {
        UDR;
    }
    while (UCSRA & (1 << RXC));

	//reset tx and rx completeflags
	UCSRA = (1 << RXC) | (1 << TXC) | (1 <<  UDRE); 
}

static inline void uart_putc(uint8_t data) {
	UDR = data;						// write byte to data register
	while (!(UCSRA & (1<<  UDRE))); 	// waiting for the uart to finish transmission
	UCSRA |= (1 <<  UDRE); 
}

static inline void uart_puts(char *data) {
  uint8_t i;
  for(i = 0; i < strlen(data); i++) {
    uart_putc(data[i]);
  }
}



static inline uint8_t uart_getc(void) {
	while (!(UCSRA & (1<<RXC)));
	return UDR;
}

static inline uint8_t uart_getc_timeout(void) {
	uint8_t retries = UART_TIMEOUT;
	uint8_t delays = 0;

	while (!(UCSRA & (1<<RXC)) && (retries > 0)) {
		if(delays == 0) {
			retries--;
		}
		delays = (delays + 1) % 250;
		_delay_us(4);
	}

	if(retries > 0) {
		uart_timed_out = 0;
		return UDR;
	}

	uart_timed_out = 1;
	return 0;
}




#endif