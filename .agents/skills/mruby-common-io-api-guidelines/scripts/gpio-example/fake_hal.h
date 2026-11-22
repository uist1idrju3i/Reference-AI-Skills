#ifndef GPIO_EXAMPLE_FAKE_HAL_H
#define GPIO_EXAMPLE_FAKE_HAL_H

enum { FAKE_PIN_COUNT = 8 };
void fake_reset(void);
void fake_setmode(int pin, int flags);
int fake_mode(int pin);
void fake_write(int pin, int value);
int fake_read(int pin);
int fake_write_count(void);

#endif
