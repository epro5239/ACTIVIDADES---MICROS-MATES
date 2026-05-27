/**
 * motor_pwm_final.c - VERSION DEFINITIVA
 * Practica 13 - Control de motor DC con puente H
 * 
 * Mejoras:
 * - Arranque suave con impulso inicial
 * - Curva de velocidad lineal real
 * - Frenado antes de invertir direccion
 * - Respuesta inmediata a comandos
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "pico/stdlib.h"
#include "hardware/pwm.h"
#include "hardware/gpio.h"

// ==================== PINES ====================
#define PIN_PWM_FWD    2   
#define PIN_PWM_REV    3   
#define PIN_EN_FWD     4   
#define PIN_EN_REV     5   
#define LED_PIN        25  

// ==================== CONSTANTES ====================
#define PWM_MAX        255
#define PWM_MIN        0
#define SPEED_MIN      15      // Velocidad minima para arrancar el motor (%)
#define BRAKE_TIME_MS  50      // Tiempo de frenado antes de invertir (ms)

// ==================== VARIABLES ====================
static int velocidad_actual = 0;
static bool direccion_adelante = true;
static bool motor_encendido = false;

// ==================== CONFIGURACION ====================
void setup_pines(void) {
    // Configurar pines de enable
    gpio_init(PIN_EN_FWD);
    gpio_init(PIN_EN_REV);
    gpio_set_dir(PIN_EN_FWD, GPIO_OUT);
    gpio_set_dir(PIN_EN_REV, GPIO_OUT);
    gpio_put(PIN_EN_FWD, 0);
    gpio_put(PIN_EN_REV, 0);
    
    // Configurar pines PWM
    gpio_set_function(PIN_PWM_FWD, GPIO_FUNC_PWM);
    gpio_set_function(PIN_PWM_REV, GPIO_FUNC_PWM);
    
    uint slice_fwd = pwm_gpio_to_slice_num(PIN_PWM_FWD);
    uint slice_rev = pwm_gpio_to_slice_num(PIN_PWM_REV);
    
    pwm_set_wrap(slice_fwd, PWM_MAX);
    pwm_set_wrap(slice_rev, PWM_MAX);
    pwm_set_clkdiv(slice_fwd, 4.0f);
    pwm_set_clkdiv(slice_rev, 4.0f);
    pwm_set_enabled(slice_fwd, true);
    pwm_set_enabled(slice_rev, true);
    
    pwm_set_gpio_level(PIN_PWM_FWD, 0);
    pwm_set_gpio_level(PIN_PWM_REV, 0);
    
    // LED interno
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    gpio_put(LED_PIN, 0);
}

// ==================== FUNCIONES DE CONTROL ====================

// Convierte porcentaje (0-100) a nivel PWM con curva lineal
uint16_t porcentaje_a_nivel(int velocidad) {
    if (velocidad <= 0) return 0;
    if (velocidad >= 100) return PWM_MAX;
    
    // Curva lineal simple
    return (velocidad * PWM_MAX) / 100;
}

// Aplica velocidad actual al motor
void aplicar_velocidad(void) {
    uint16_t nivel = porcentaje_a_nivel(velocidad_actual);
    
    if (direccion_adelante) {
        pwm_set_gpio_level(PIN_PWM_FWD, nivel);
        pwm_set_gpio_level(PIN_PWM_REV, 0);
        gpio_put(PIN_EN_FWD, nivel > 0 ? 1 : 0);
        gpio_put(PIN_EN_REV, 0);
    } else {
        pwm_set_gpio_level(PIN_PWM_FWD, 0);
        pwm_set_gpio_level(PIN_PWM_REV, nivel);
        gpio_put(PIN_EN_FWD, 0);
        gpio_put(PIN_EN_REV, nivel > 0 ? 1 : 0);
    }
    
    motor_encendido = (nivel > 0);
}

// Frena el motor completamente (corto circuito)
void frenar_motor(void) {
    // Activar ambos enable para frenado regenerativo
    gpio_put(PIN_EN_FWD, 1);
    gpio_put(PIN_EN_REV, 1);
    pwm_set_gpio_level(PIN_PWM_FWD, 0);
    pwm_set_gpio_level(PIN_PWM_REV, 0);
    sleep_ms(BRAKE_TIME_MS);
    gpio_put(PIN_EN_FWD, 0);
    gpio_put(PIN_EN_REV, 0);
}

// ==================== COMANDOS DEL MOTOR ====================
void motor_adelante(int velocidad) {
    // Validar velocidad
    if (velocidad < 0) velocidad = 0;
    if (velocidad > 100) velocidad = 100;
    
    // Si el motor estaba en reversa, frenar primero
    if (!direccion_adelante && motor_encendido && velocidad > 0) {
        frenar_motor();
    }
    
    velocidad_actual = velocidad;
    direccion_adelante = true;
    
    // Aplicar velocidad (con arranque suave si es necesario)
    if (velocidad_actual > 0 && velocidad_actual < SPEED_MIN) {
        // Empuje inicial para arrancar
        uint16_t empuje = porcentaje_a_nivel(SPEED_MIN);
        if (direccion_adelante) {
            pwm_set_gpio_level(PIN_PWM_FWD, empuje);
            gpio_put(PIN_EN_FWD, 1);
        } else {
            pwm_set_gpio_level(PIN_PWM_REV, empuje);
            gpio_put(PIN_EN_REV, 1);
        }
        sleep_ms(80);  // Empuje breve
    }
    
    aplicar_velocidad();
    
    // Indicador visual
    gpio_put(LED_PIN, 1);
    sleep_ms(30);
    gpio_put(LED_PIN, 0);
    
    printf("ACK:FWD:%d\n", velocidad_actual);
}

void motor_atras(int velocidad) {
    if (velocidad < 0) velocidad = 0;
    if (velocidad > 100) velocidad = 100;
    
    // Si el motor estaba en adelante, frenar primero
    if (direccion_adelante && motor_encendido && velocidad > 0) {
        frenar_motor();
    }
    
    velocidad_actual = velocidad;
    direccion_adelante = false;
    
    // Empuje inicial para arrancar
    if (velocidad_actual > 0 && velocidad_actual < SPEED_MIN) {
        uint16_t empuje = porcentaje_a_nivel(SPEED_MIN);
        if (direccion_adelante) {
            pwm_set_gpio_level(PIN_PWM_FWD, empuje);
            gpio_put(PIN_EN_FWD, 1);
        } else {
            pwm_set_gpio_level(PIN_PWM_REV, empuje);
            gpio_put(PIN_EN_REV, 1);
        }
        sleep_ms(80);
    }
    
    aplicar_velocidad();
    
    gpio_put(LED_PIN, 1);
    sleep_ms(30);
    gpio_put(LED_PIN, 0);
    
    printf("ACK:BWD:%d\n", velocidad_actual);
}

void motor_stop(void) {
    frenar_motor();
    velocidad_actual = 0;
    motor_encendido = false;
    
    // Parpadeo doble
    gpio_put(LED_PIN, 1);
    sleep_ms(80);
    gpio_put(LED_PIN, 0);
    sleep_ms(80);
    gpio_put(LED_PIN, 1);
    sleep_ms(80);
    gpio_put(LED_PIN, 0);
    
    printf("ACK:STOP\n");
}

void motor_invertir(void) {
    if (velocidad_actual > 0) {
        // Frenar antes de invertir
        frenar_motor();
        sleep_ms(50);
        
        if (direccion_adelante) {
            direccion_adelante = false;
        } else {
            direccion_adelante = true;
        }
        
        aplicar_velocidad();
        printf("ACK:INV:%s:%d\n", direccion_adelante ? "FWD" : "BWD", velocidad_actual);
    }
}

// ==================== PROCESAR COMANDOS ====================
void procesar_comando(char *cmd) {
    char comando = cmd[0];
    
    switch(comando) {
        case 'F': case 'f': {
            int vel = atoi(&cmd[1]);
            motor_adelante(vel);
            break;
        }
        case 'B': case 'b': {
            int vel = atoi(&cmd[1]);
            motor_atras(vel);
            break;
        }
        case 'S': case 's':
            motor_stop();
            break;
        case 'I': case 'i':
            motor_invertir();
            break;
        default:
            printf("ERR:CMD_UNKNOWN:%s\n", cmd);
            break;
    }
}

// ==================== MAIN ====================
int main() {
    stdio_init_all();
    sleep_ms(3000);  // Esperar USB
    
    setup_pines();
    motor_stop();
    
    printf("\n");
    printf("========================================\n");
    printf("   PRACTICA 13 - CONTROL DE MOTOR DC\n");
    printf("   Version Final con Frenado\n");
    printf("========================================\n");
    printf("Comandos:\n");
    printf("  F<0-100>  -> Adelante\n");
    printf("  B<0-100>  -> Atras\n");
    printf("  S         -> Stop\n");
    printf("  I         -> Invertir\n");
    printf("========================================\n");
    printf("LISTO!\n\n");
    
    char buffer[32];
    int indice = 0;
    
    while (1) {
        int c = getchar_timeout_us(10000);
        
        if (c != PICO_ERROR_TIMEOUT) {
            if (c == '\n' || c == '\r') {
                if (indice > 0) {
                    buffer[indice] = '\0';
                    procesar_comando(buffer);
                    indice = 0;
                }
            } else if (indice < sizeof(buffer) - 1) {
                buffer[indice++] = (char)c;
            }
        }
        
        sleep_ms(5);
    }
    
    return 0;
}