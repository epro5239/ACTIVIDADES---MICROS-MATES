/*
 * Práctica 7: Contador binario ascendente de 4 bits mediante pulsador
 * Basado en código del Ing. Jesús Padrón
 */

#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"

// Definición de pines para los 4 LEDs (bits del contador)
#define BIT0 2  // GPIO2 - Bit menos significativo (LSB)
#define BIT1 3  // GPIO3
#define BIT2 4  // GPIO4
#define BIT3 5  // GPIO5 - Bit más significativo (MSB)

#define BUTTON 6  // GPIO6 para el botón

// Variable global para el contador (0-15)
uint8_t contador = 0;

// Función para actualizar las salidas GPIO con el valor del contador
void actualizar_gpio(uint8_t valor) {
    gpio_put(BIT0, valor & 0x01);          // Bit 0 (LSB)
    gpio_put(BIT1, (valor >> 1) & 0x01);   // Bit 1
    gpio_put(BIT2, (valor >> 2) & 0x01);   // Bit 2
    gpio_put(BIT3, (valor >> 3) & 0x01);   // Bit 3 (MSB)
}

int main() {
    stdio_init_all();
    
    printf("Práctica 7: Contador binario ascendente de 4 bits\n");
    printf("Presiona el botón para incrementar\n");
    
    // Configurar los pines de los LEDs como salida
    gpio_init(BIT0);
    gpio_init(BIT1);
    gpio_init(BIT2);
    gpio_init(BIT3);
    
    gpio_set_dir(BIT0, GPIO_OUT);
    gpio_set_dir(BIT1, GPIO_OUT);
    gpio_set_dir(BIT2, GPIO_OUT);
    gpio_set_dir(BIT3, GPIO_OUT);
    
    // Configurar el botón como entrada con pull-down interno
    gpio_init(BUTTON);
    gpio_set_dir(BUTTON, GPIO_IN);
    gpio_set_pulls(BUTTON, false, true);   // Pull-down activado (false = pull-up desactivado, true = pull-down activado)
    
    // Mostrar el estado inicial del contador (0)
    actualizar_gpio(contador);
    printf("Contador: %d (binario: %d%d%d%d)\n", 
           contador, 
           (contador >> 3) & 1,
           (contador >> 2) & 1,
           (contador >> 1) & 1,
           contador & 1);
    
    while (1) {
        // Esperar a que el botón sea presionado (flanco de subida)
        if (gpio_get(BUTTON) == 1) {
            sleep_ms(50);                    // Anti-rebote (esperar a que se estabilice)
            
            while (gpio_get(BUTTON) == 1) {
                // Esperar a que se suelte el botón
            }
            
            sleep_ms(50);                    // Anti-rebote (esperar a que se estabilice al soltar)
            
            // Incrementar el contador en 1 (0 a 15)
            contador = (contador + 1) & 0x0F; // 0x0F = 15 (1111 binario) asegura que se quede en 4 bits
            
            // Actualizar LEDs con el nuevo valor
            actualizar_gpio(contador);
            
            // Mostrar en monitor serial
            printf("Contador: %d (binario: %d%d%d%d)\n", 
                   contador, 
                   (contador >> 3) & 1,
                   (contador >> 2) & 1,
                   (contador >> 1) & 1,
                   contador & 1);
        }
        
        // Pequeña pausa para no saturar la CPU
        sleep_ms(10);
    }
    
    return 0;
}