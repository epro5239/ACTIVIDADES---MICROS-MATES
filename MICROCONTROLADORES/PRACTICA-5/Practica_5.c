/*
 * Práctica 5: Parpadeo de LED con GPIO
 * Basado en código del Ing. Jesús Padrón
 */

#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"

#define LED_PIN 15  // GPIO15 para el LED (puedes cambiarlo)

int main() {
    stdio_init_all();
    
    printf("Práctica 5: Parpadeo de LED\n");
    
    // Inicializar pin del LED como salida
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    
    while (true) {
        // Encender LED
        gpio_put(LED_PIN, 1);
        printf("LED ENCENDIDO\n");
        sleep_ms(1000);  // 1 segundo
        
        // Apagar LED
        gpio_put(LED_PIN, 0);
        printf("LED APAGADO\n");
        sleep_ms(1000);  // 1 segundo
    }
    
    return 0;
}