/*
 * Práctica 12: Control de LED RGB - VERSIÓN DIAGNÓSTICO
 */

#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/pwm.h"
#include "hardware/gpio.h"

// ============================================
// PINES - VERIFICA QUE COINCIDAN CON TUS CONEXIONES
// ============================================
#define POT_R_PIN 26  // ADC0 - GP26 (PIN FÍSICO 31)
#define POT_G_PIN 27  // ADC1 - GP27 (PIN FÍSICO 32)
#define POT_B_PIN 28  // ADC2 - GP28 (PIN FÍSICO 34)

#define LED_R_PIN 15  // PWM - GP15 (PIN FÍSICO 20)
#define LED_G_PIN 14  // PWM - GP14 (PIN FÍSICO 19)
#define LED_B_PIN 13  // PWM - GP13 (PIN FÍSICO 17)

// ============================================
// CONFIGURACIÓN
// ============================================
#define CATHODE_COMMON false  // false = ÁNODO COMÚN (3.3V en pata larga)
#define PWM_WRAP 255
#define ADC_MAX 4095

// ============================================
// ESTRUCTURA
// ============================================
typedef struct {
    uint8_t pin_adc;
    uint8_t pin_pwm;
    uint16_t raw_value;
    uint8_t porcentaje;
    uint8_t pwm_actual;
} CanalRGB;

CanalRGB rojo = {.pin_adc = POT_R_PIN, .pin_pwm = LED_R_PIN};
CanalRGB verde = {.pin_adc = POT_G_PIN, .pin_pwm = LED_G_PIN};
CanalRGB azul = {.pin_adc = POT_B_PIN, .pin_pwm = LED_B_PIN};

// ============================================
// PROTOTIPOS
// ============================================
void init_adc(void);
void init_pwm(void);
void prueba_leds(void);
uint16_t leer_adc(uint8_t pin);
uint8_t adc_a_pwm(uint16_t adc_val);
void actualizar_led(CanalRGB *canal);
void imprimir_estado(void);
// ============================================
// MAIN
// ============================================
int main() {
    stdio_init_all();
    sleep_ms(3000);
    
    // Solo mostramos el encabezado requerido
    printf("Canales de color:\n");
    
    init_adc();
    init_pwm();
    
    uint32_t ultima_impresion = 0;
    
    while (true) {
        // Leer potenciómetros
        rojo.raw_value = leer_adc(rojo.pin_adc);
        rojo.porcentaje = (rojo.raw_value * 100) / ADC_MAX;
        
        verde.raw_value = leer_adc(verde.pin_adc);
        verde.porcentaje = (verde.raw_value * 100) / ADC_MAX;
        
        azul.raw_value = leer_adc(azul.pin_adc);
        azul.porcentaje = (azul.raw_value * 100) / ADC_MAX;
        
        // Actualizar LEDs
        actualizar_led(&rojo);
        actualizar_led(&verde);
        actualizar_led(&azul);
        
        // Mostrar cada 200ms
        uint32_t ahora = to_ms_since_boot(get_absolute_time());
        if (ahora - ultima_impresion >= 1000) {
            imprimir_estado();
            ultima_impresion = ahora;
        }
        
        sleep_ms(10);
    }
}
// ============================================
// INICIALIZACIONES
// ============================================
void init_adc(void) {
    adc_init();
    adc_gpio_init(rojo.pin_adc);
    adc_gpio_init(verde.pin_adc);
    adc_gpio_init(azul.pin_adc);
    printf("✅ ADC inicializado\n");
}

void init_pwm(void) {
    gpio_set_function(rojo.pin_pwm, GPIO_FUNC_PWM);
    gpio_set_function(verde.pin_pwm, GPIO_FUNC_PWM);
    gpio_set_function(azul.pin_pwm, GPIO_FUNC_PWM);
    
    uint slice_r = pwm_gpio_to_slice_num(rojo.pin_pwm);
    uint slice_g = pwm_gpio_to_slice_num(verde.pin_pwm);
    uint slice_b = pwm_gpio_to_slice_num(azul.pin_pwm);
    
    pwm_set_wrap(slice_r, PWM_WRAP);
    pwm_set_wrap(slice_g, PWM_WRAP);
    pwm_set_wrap(slice_b, PWM_WRAP);
    
    pwm_set_enabled(slice_r, true);
    pwm_set_enabled(slice_g, true);
    pwm_set_enabled(slice_b, true);
    
    // Iniciar apagados (255 = apagado en ánodo común)
    pwm_set_gpio_level(rojo.pin_pwm, 255);
    pwm_set_gpio_level(verde.pin_pwm, 255);
    pwm_set_gpio_level(azul.pin_pwm, 255);
    
    printf("✅ PWM inicializado\n");
}

// ============================================
// PRUEBA DE LEDS
// ============================================
void prueba_leds(void) {
    printf("\n🔴 PRUEBA DE LEDS INDIVIDUALES\n");
    
    // ROJO
    printf("  ROJO: ");
    pwm_set_gpio_level(LED_R_PIN, 0);  // Encender
    sleep_ms(1500);
    pwm_set_gpio_level(LED_R_PIN, 255);  // Apagar
    printf("✅\n");
    sleep_ms(500);
    
    // VERDE
    printf("  VERDE: ");
    pwm_set_gpio_level(LED_G_PIN, 0);
    sleep_ms(1500);
    pwm_set_gpio_level(LED_G_PIN, 255);
    printf("✅\n");
    sleep_ms(500);
    
    // AZUL
    printf("  AZUL: ");
    pwm_set_gpio_level(LED_B_PIN, 0);
    sleep_ms(1500);
    pwm_set_gpio_level(LED_B_PIN, 255);
    printf("✅\n");
    sleep_ms(500);
    
    // TODOS
    printf("  TODOS: ");
    pwm_set_gpio_level(LED_R_PIN, 0);
    pwm_set_gpio_level(LED_G_PIN, 0);
    pwm_set_gpio_level(LED_B_PIN, 0);
    sleep_ms(1500);
    pwm_set_gpio_level(LED_R_PIN, 255);
    pwm_set_gpio_level(LED_G_PIN, 255);
    pwm_set_gpio_level(LED_B_PIN, 255);
    printf("✅\n");
    sleep_ms(500);
    
    printf("✅ Prueba completada\n\n");
}

// ============================================
// LEER ADC
// ============================================
uint16_t leer_adc(uint8_t pin) {
    if (pin == 26) adc_select_input(0);
    else if (pin == 27) adc_select_input(1);
    else if (pin == 28) adc_select_input(2);
    else return 0;
    
    sleep_us(10);
    return adc_read();
}

// ============================================
// CONVERTIR ADC A PWM
// ============================================
uint8_t adc_a_pwm(uint16_t adc_val) {
    uint8_t pwm = (adc_val * PWM_WRAP) / ADC_MAX;
    
    if (!CATHODE_COMMON) {  // Ánodo común
        pwm = PWM_WRAP - pwm;  // Invertir
    }
    
    return pwm;
}

// ============================================
// ACTUALIZAR LED
// ============================================
void actualizar_led(CanalRGB *canal) {
    uint8_t nuevo_pwm = adc_a_pwm(canal->raw_value);
    
    if (canal->pwm_actual != nuevo_pwm) {
        canal->pwm_actual = nuevo_pwm;
        pwm_set_gpio_level(canal->pin_pwm, canal->pwm_actual);
    }
}

// ============================================
// IMPRIMIR ESTADO - FORMATO VERTICAL (LISTA)
// ============================================
void imprimir_estado(void) {
    // Usamos \n para crear nueva línea cada vez (formato vertical)
    printf("R:%3d%% | G:%3d%% | B:%3d%%\n", 
           rojo.porcentaje, verde.porcentaje, azul.porcentaje);
    fflush(stdout);
}