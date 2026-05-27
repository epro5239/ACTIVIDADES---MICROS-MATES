/*
 * Práctica 8: Contador ascendente 0-F con reinicio
 * Display de 7 segmentos - Versión con reinicio inmediato
 */

#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"

// Definimos los pines
#define FIRST_GPIO 2      // Primer pin del display (A)
#define BUTTON_GPIO 9      // Botón de inicio/reinicio

// Tabla de bits para los números 0-F en hexadecimal
int hexDigits[16] = {
    0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07,
    0x7F, 0x6F, 0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71
};

int main() {
    stdio_init_all();
    
    printf("Práctica 8: Contador 0-F con reinicio inmediato\n");

    // Inicializamos los pines del display como salida
    for (int i = FIRST_GPIO; i < FIRST_GPIO + 7; i++) {
        gpio_init(i);
        gpio_set_dir(i, GPIO_OUT);
        gpio_put(i, 0);
    }

    // Configuramos el botón como entrada con pull-up
    gpio_init(BUTTON_GPIO);
    gpio_set_dir(BUTTON_GPIO, GPIO_IN);
    gpio_pull_up(BUTTON_GPIO);

    int count = 0;
    bool boton_anterior = true;
    uint32_t mask_actual = 0;  // Para mantener la máscara actual
    
    while (true) {
        // Leer botón (activo en bajo por pull-up)
        bool boton_actual = gpio_get(BUTTON_GPIO);
        
        // Detectar flanco de bajada (botón presionado)
        if (boton_anterior == 1 && boton_actual == 0) {
            count = 0;  // Reiniciar contador
            printf("Contador reiniciado\n");
            
            // ACTUALIZACIÓN INMEDIATA: Cambiar el display sin apagarlo
            uint32_t mask_nueva = hexDigits[count] << FIRST_GPIO;
            
            // Apagar solo los segmentos que ya no deben encenderse
            uint32_t apagar = mask_actual & ~mask_nueva;
            gpio_clr_mask(apagar);
            
            // Encender los nuevos segmentos necesarios
            uint32_t encender = mask_nueva & ~mask_actual;
            gpio_set_mask(encender);
            
            mask_actual = mask_nueva;  // Actualizar máscara actual
            
            // Pequeño delay para debounce (no afecta al display)
            sleep_ms(50);
        }
        boton_anterior = boton_actual;

        // Si no se presionó el botón, proceder con el contador normal
        if (boton_actual == 1) {
            // Preparar la nueva máscara para el siguiente número
            uint32_t mask_nueva = hexDigits[count] << FIRST_GPIO;
            
            // Cambiar SOLO los segmentos necesarios
            uint32_t apagar = mask_actual & ~mask_nueva;
            uint32_t encender = mask_nueva & ~mask_actual;
            
            if (apagar) gpio_clr_mask(apagar);
            if (encender) gpio_set_mask(encender);
            
            mask_actual = mask_nueva;
            
            // Mostrar valor en monitor serial
            if (count < 10) printf("Número: %d\n", count);
            else printf("Número: %c\n", 'A' + (count - 10));
            
            sleep_ms(1000);
            
            // Incrementar contador
            count = (count + 1) % 16;
        }
    }
    
    return 0;
}