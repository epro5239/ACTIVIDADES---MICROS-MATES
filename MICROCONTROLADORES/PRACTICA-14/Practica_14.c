#include "semaforo.h"
#include <stdio.h>

bool timer_callback(struct repeating_timer *t) {
    process_state_machine();
    return true;
}

bool fast_timer_callback(struct repeating_timer *t) {
    multiplex_display();
    return true;
}

int main() {
    stdio_init_all();
    sleep_ms(2000);
    
    printf("\n=== CRUCE PEATONAL ===\n");
    
    init_hardware();
    
    struct repeating_timer timer;
    add_repeating_timer_ms(1000, timer_callback, NULL, &timer);
    
    struct repeating_timer fast_timer;
    add_repeating_timer_ms(5, fast_timer_callback, NULL, &fast_timer);
    
    printf("SISTEMA INICIADO\n");
    
    while (1) {
        tight_loop_contents();
    }
    return 0;
}