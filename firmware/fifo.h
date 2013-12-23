#ifndef FIFO_H_ 
#define FIFO_H_ FIFO_H_

#include <stdint.h>

typedef struct {
	uint8_t tubenumber;
	enum { ONE_TO_TWO, TWO_TO_ONE} direction;
	uint32_t timestamp;
	uint16_t time;
} TubeEvent;


#define FIFO_TYPE TubeEvent

struct fifo {
	FIFO_TYPE *data;

	uint8_t size;
	uint8_t len;

	uint8_t read;
	uint8_t write;
};

extern struct fifo eventfifo;

static inline void fifo_init(struct fifo *f, uint8_t size, FIFO_TYPE *data) {
	f->data = data;
	f->read = 0;
	f->write = 0;
	f->len = 0;
	f->size = size;
}


static inline uint8_t fifo_empty(struct fifo *f) {
	return f->len == 0;
}

static inline uint8_t fifo_full(struct fifo *f) {
	return f->len == f->size;
}

static inline void fifo_put(struct fifo *f, FIFO_TYPE value) {
	if(!fifo_full(f)) {
		f->data[f->write] = value;
		f->len++;
		f->write = (f->write + 1) % f->size;
	}
}

static inline FIFO_TYPE fifo_get(struct fifo *f) {
	FIFO_TYPE tmp;
	if(!fifo_empty(f)) {
		tmp = f->data[f->read];
		f->read = (f->read + 1) % f->size;
		f->len--;
	}
	return tmp;
}

static inline void fifo_clear(struct fifo *f) {
	f->read = 0;
	f->write = 0;
	f->len = 0;
}

#endif
