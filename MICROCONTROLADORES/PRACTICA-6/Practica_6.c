/*
 * Práctica 6: Encendido de LED con botón
 * Basado en código del Ing. Jesús Padrón
 */

#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"

#define LED_PIN 3      // GPIO3 (pin 4) para el LED
#define BUTTON_PIN 4    // GPIO4 (pin 5) para el botón

int main() {
    stdio_init_all();  // ← CORREGIDO: estaba "stdo_init_all()"
    
    printf("Práctica 6: LED con botón\n");
    
    // Inicializar pin del LED como salida
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    gpio_put(LED_PIN, 0);  // LED apagado inicialmente
    
    // Inicializar pin del botón como entrada con pull-down
    gpio_init(BUTTON_PIN);
    gpio_set_dir(BUTTON_PIN, GPIO_IN);
    gpio_pull_down(BUTTON_PIN);  // Configuración pull-down
    
    while (true) {
        // Leer estado del botón
        if (gpio_get(BUTTON_PIN)) {
            // Botón presionado (1 lógico)
            gpio_put(LED_PIN, 1);  // Encender LED
            printf("Botón presionado - LED ENCENDIDO\n");
        } else {
            // Botón no presionado (0 lógico)
            gpio_put(LED_PIN, 0);  // Apagar LED
            printf("Botón liberado - LED APAGADO\n");
        }
        
        sleep_ms(100);  // Pequeña pausa para evitar rebotes
    }
    
    return 0;
}