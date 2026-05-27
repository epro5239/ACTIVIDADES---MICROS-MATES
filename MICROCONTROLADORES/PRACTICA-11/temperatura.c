/*
 * Práctica 11: Medición de temperatura con LM35 y control de ventilador
 * Sensor: LM35 (10mV/°C)
 * Ventilador: Control por PWM con transistor 2N2222
 * LED verde (GP12) = Temperatura normal
 * LED rojo (GP14) = Alarma
 * Zumbador activo (GP13) = Alarma sonora
 */

#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/gpio.h"
#include "hardware/pwm.h"

// Definición de pines
#define LM35_PIN 26          // GP26 = ADC0
#define FAN_PIN 15           // GP15 para control del ventilador (PWM)
#define LED_PIN 25           // LED interno para indicar estado
#define LED_VERDE_PIN 12     // GP12 para LED verde (temperatura normal)  ← NUEVO
#define ZUMBADOR_PIN 13      // GP13 para ZUMBADOR ACTIVO                  ← NUEVO
#define LED_ROJO_PIN 14      // GP14 para LED rojo (alarma)               ← NUEVO

// Constantes del ADC
#define ADC_MAX_VALUE 4095   // 12 bits
#define ADC_VREF 3.3f        // Voltaje de referencia

// Umbral de temperatura para activar ventilador (°C)
#define TEMP_UMBRAL 45.0f    // Cambiar a 70.0f para el valor real de la práctica

// Variables para almacenamiento de datos
#define MAX_MUESTRAS 100
float temperaturas[MAX_MUESTRAS];
uint32_t tiempos[MAX_MUESTRAS];
int indice_muestra = 0;

// Prototipos
void init_adc(void);
void init_pwm(void);
void init_indicadores(void);        // ← NUEVO
float leer_temperatura(void);
void controlar_ventilador(float temp);
void actualizar_indicadores(float temp);  // ← NUEVO
void enviar_datos_serial(void);

int main() {
    stdio_init_all();
    
    // Inicializar LED interno
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    gpio_put(LED_PIN, 0);
    
    // Inicializar indicadores (LEDs y zumbador)  ← NUEVO
    init_indicadores();
    
    // Inicializar ADC
    init_adc();
    
    // Inicializar PWM para ventilador
    init_pwm();
    
    printf("====================================\n");
    printf("Práctica 11: Medición de Temperatura\n");
    printf("Sensor: LM35\n");
    printf("Umbral ventilador: %.1f°C\n", TEMP_UMBRAL);
    printf("LED verde: Temperatura normal\n");
    printf("LED rojo + Zumbador: Alarma\n");
    printf("====================================\n\n");
    
    uint32_t tiempo_inicio = to_ms_since_boot(get_absolute_time());
    
    while (true) {
        // Leer temperatura
        float temperatura = leer_temperatura();
        
        // Calcular tiempo transcurrido
        uint32_t tiempo_actual = to_ms_since_boot(get_absolute_time());
        uint32_t tiempo_transcurrido = (tiempo_actual - tiempo_inicio) / 1000; // segundos
        
        // Guardar datos para la gráfica
        if (indice_muestra < MAX_MUESTRAS) {
            temperaturas[indice_muestra] = temperatura;
            tiempos[indice_muestra] = tiempo_transcurrido;
            indice_muestra++;
        }
        
        // Controlar ventilador
        controlar_ventilador(temperatura);
        
        // Actualizar LEDs y zumbador según temperatura  ← NUEVO
        actualizar_indicadores(temperatura);
        
        // Enviar datos por serial (formato para Python)
        printf("T:%.2f,", temperatura);
        fflush(stdout);
        
        // Parpadear LED según temperatura
        if (temperatura > TEMP_UMBRAL) {
            gpio_put(LED_PIN, 1);
            sleep_ms(100);
            gpio_put(LED_PIN, 0);
        }
        
        sleep_ms(500); // Leer cada 500ms
    }
    
    return 0;
}

void init_adc(void) {
    adc_init();
    adc_gpio_init(LM35_PIN);
    adc_select_input(0); // ADC0 = GP26
}

void init_pwm(void) {
    // Configurar pin para PWM
    gpio_set_function(FAN_PIN, GPIO_FUNC_PWM);
    
    // Obtener número de slice de PWM
    uint slice_num = pwm_gpio_to_slice_num(FAN_PIN);
    
    // Configurar PWM
    pwm_set_wrap(slice_num, 255); // 8-bit resolution
    pwm_set_enabled(slice_num, true);
    pwm_set_gpio_level(FAN_PIN, 0); // Inicialmente apagado
}

// ← NUEVA FUNCIÓN: Inicializar LEDs y zumbador
void init_indicadores(void) {
    // LED verde (temperatura normal)
    gpio_init(LED_VERDE_PIN);
    gpio_set_dir(LED_VERDE_PIN, GPIO_OUT);
    gpio_put(LED_VERDE_PIN, 1);  // Inicia encendido (temperatura normal)
    
    // LED rojo (alarma)
    gpio_init(LED_ROJO_PIN);
    gpio_set_dir(LED_ROJO_PIN, GPIO_OUT);
    gpio_put(LED_ROJO_PIN, 0);   // Inicia apagado
    
    // Zumbador activo
    gpio_init(ZUMBADOR_PIN);
    gpio_set_dir(ZUMBADOR_PIN, GPIO_OUT);
    gpio_put(ZUMBADOR_PIN, 0);   // Inicia apagado
}

float leer_temperatura(void) {
    // Leer ADC
    uint16_t raw = adc_read();
    
    // Convertir a voltaje
    float voltaje = (raw * ADC_VREF) / ADC_MAX_VALUE;
    
    // LM35: 10mV por °C
    float temperatura = voltaje * 100.0f;
    
    return temperatura;
}

void controlar_ventilador(float temp) {
    uint slice_num = pwm_gpio_to_slice_num(FAN_PIN);
    
    if (temp >= TEMP_UMBRAL) {
        // Ventilador ON - PWM al 100%
        pwm_set_gpio_level(FAN_PIN, 255);
        printf("VENTILADOR ON - Temp: %.2f°C\n", temp);
    } else {
        // Ventilador OFF
        pwm_set_gpio_level(FAN_PIN, 0);
    }
}

// ← NUEVA FUNCIÓN: Actualizar LEDs y zumbador según temperatura
void actualizar_indicadores(float temp) {
    if (temp >= TEMP_UMBRAL) {
        // MODO ALARMA
        gpio_put(LED_VERDE_PIN, 0);  // LED verde APAGADO
        gpio_put(LED_ROJO_PIN, 1);   // LED rojo ENCENDIDO
        gpio_put(ZUMBADOR_PIN, 1);   // Zumbador SUENA
    } else {
        // MODO NORMAL
        gpio_put(LED_VERDE_PIN, 1);  // LED verde ENCENDIDO
        gpio_put(LED_ROJO_PIN, 0);   // LED rojo APAGADO
        gpio_put(ZUMBADOR_PIN, 0);   // Zumbador APAGADO
    }
}

void enviar_datos_serial(void) {
    // Esta función ya no es necesaria porque enviamos en el loop principal
    // pero la dejamos como referencia
}