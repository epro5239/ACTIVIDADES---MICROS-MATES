/*
 * Práctica 10: Lectura de valores analógicos con potenciómetro
 * Basado en código del Ing. Jesús Padrón
 */

#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/adc.h"

#define POT_PIN 26          // GP26 = ADC0
#define ADC_MAX_VALUE 4095  // Valor máximo para ADC de 12 bits
#define ADC_VREF 3.3f       // Voltaje de referencia de la Raspberry Pi Pico

int main() {
    stdio_init_all();           // Inicializa la comunicación serial
    adc_init();                 // Inicializa el ADC
    adc_gpio_init(POT_PIN);     // Habilita el pin GP26 como entrada ADC
    adc_select_input(0);        // Selecciona el canal ADC0 (GP26)
    
    printf("Práctica 10: Lectura de potenciómetro\n");
    printf("Valor ADC | Voltaje (V)\n");
    printf("------------------------\n");
    
    while (1) {
        uint16_t raw_value = adc_read();                    // Lee el valor del ADC (0 - 4095)
        float voltage = (raw_value * ADC_VREF) / ADC_MAX_VALUE; // Convierte a voltaje
        
        printf("%4d      | %.2f\n", raw_value, voltage);   // Imprime en el monitor serial
        
        sleep_ms(500);  // Espera 500 ms antes de la siguiente lectura
    }
    
    return 0;
}