#ifndef TM1637_H
#define TM1637_H

#include "pico/stdlib.h"

typedef struct {
    uint8_t clk_pin;
    uint8_t dio_pin;
    uint8_t brightness;
} tm1637_t;

// Comandos TM1637
#define TM1637_ADDR_AUTO  0x40
#define TM1637_ADDR_FIXED 0x44
#define TM1637_CMD_DISPLAY 0x80
#define TM1637_CMD_BRIGHTNESS 0x88

// Segmentos para números 0-9
extern const uint8_t SEGMENT_MAP[];

void tm1637_init(tm1637_t *disp, uint8_t clk, uint8_t dio);
void tm1637_start(tm1637_t *disp);
void tm1637_stop(tm1637_t *disp);
void tm1637_write_byte(tm1637_t *disp, uint8_t data);
void tm1637_display_number(tm1637_t *disp, int16_t number);
void tm1637_display_segments(tm1637_t *disp, const uint8_t *segments);
void tm1637_set_brightness(tm1637_t *disp, uint8_t brightness);
void tm1637_display_on(tm1637_t *disp);
void tm1637_display_off(tm1637_t *disp);

#endif