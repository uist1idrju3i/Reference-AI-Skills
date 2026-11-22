#include "fake_hal.h"

static int modes[FAKE_PIN_COUNT];
static int levels[FAKE_PIN_COUNT];
static int writes;

void fake_reset(void)
{
  for (int pin = 0; pin < FAKE_PIN_COUNT; pin++) {
    modes[pin] = 4;
    levels[pin] = 0;
  }
  writes = 0;
}

void fake_setmode(int pin, int flags) { modes[pin] = flags; }
int fake_mode(int pin) { return modes[pin]; }
void fake_write(int pin, int value) { levels[pin] = value; writes++; }
int fake_read(int pin) { return levels[pin]; }
int fake_write_count(void) { return writes; }
