#ifndef SEMAFORO_H
#define SEMAFORO_H

#include "pico/stdlib.h"
#include "hardware/timer.h"
#include "hardware/pwm.h"
#include "hardware/irq.h"

#define SEG_A 0
#define SEG_B 1
#define SEG_C 2
#define SEG_D 3
#define SEG_E 4
#define SEG_F 5
#define SEG_G 6

#define DISP1_DEC 8
#define DISP1_UNI 9
#define DISP2_DEC 7
#define DISP2_UNI 28

#define V1_RED     15
#define V1_YELLOW  14
#define V1_GREEN   13

#define V2_RED     12
#define V2_YELLOW  11
#define V2_GREEN   10

#define P1_RED     16
#define P1_GREEN   17
#define P2_RED     18
#define P2_GREEN   19

#define BUTTON1    20
#define BUTTON2    21
#define BUZZER     22

#define TIME_GREEN      3
#define TIME_YELLOW     2
#define TIME_RED        5
#define TIME_PEDESTRIAN 10

typedef enum {
    STATE_VEHICULAR_AUTO,
    STATE_WAIT_V1_RED,
    STATE_P1_ACTIVE,
    STATE_WAIT_V2_RED,
    STATE_P2_ACTIVE
} system_state_t;

typedef enum {
    VEH_STATE_GREEN,
    VEH_STATE_YELLOW,
    VEH_STATE_RED
} vehicle_state_t;

extern volatile system_state_t current_state;
extern volatile int  v1_color, v2_color;
extern volatile int  v1_timer, v2_timer;
extern volatile bool pedestrian1_request, pedestrian2_request;
extern volatile int  pedestrian1_counter, pedestrian2_counter;
extern volatile bool pedestrian1_active,  pedestrian2_active;
extern volatile int  buzzer_ticks;
extern volatile bool buzzer_active;

extern const uint8_t segment_pins[7];
extern const uint8_t display_pins[4];
extern const uint8_t segment_map[10];
extern volatile int  current_display;
extern volatile int  display_values[4];
extern volatile bool displays_on[4];

void init_hardware(void);
void update_all_lights(void);
void update_traffic_lights(void);
void update_pedestrian_lights(void);
void update_displays(void);
void multiplex_display(void);
void process_state_machine(void);
void buzzer_beep(int duration_ms, int times);
void buzzer_trigger(int duracion_ms);
void buzzer_tick(void);
void button_callback(uint gpio, uint32_t events);
void check_buttons(void);

#endif