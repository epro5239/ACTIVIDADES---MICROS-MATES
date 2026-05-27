/*
 * Practica_9: Contador 0-99 con multiplexeo para 2 displays
 * PARA DISPLAY 5161BS (CÁTODO COMÚN)
 * Cuenta: 00,01,02,03,...,99,00,...
 */

#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"

// ============================================
// CONFIGURACIÓN DE VELOCIDADES
// ============================================
#define VELOCIDAD_CONTADOR_MS 500      // Tiempo entre cada número (ms)
                                        // 500 = 0.5 segundos (2 números por segundo)
                                        // 1000 = 1 segundo
                                        // 200 = rápido

#define TIEMPO_MULTIPLEX_US 2000        // Tiempo por display (microsegundos)
#define CICLOS_MULTIPLEX 50             // Ciclos antes de cambiar número

// ============================================
// DEFINICIÓN DE PINES
// ============================================
#define SEG_A 2
#define SEG_B 3
#define SEG_C 4
#define SEG_D 5
#define SEG_E 6
#define SEG_F 7
#define SEG_G 8

#define DISPLAY_DECENAS 9
#define DISPLAY_UNIDADES 10
#define BUTTON_GPIO 11

// ============================================
// MAPA DE SEGMENTOS PARA CÁTODO COMÚN
// ============================================
const uint8_t digitos[10] = {
    0x3F, // 0
    0x06, // 1
    0x5B, // 2
    0x4F, // 3
    0x66, // 4
    0x6D, // 5
    0x7D, // 6
    0x07, // 7
    0x7F, // 8
    0x6F  // 9
};

// ============================================
// VARIABLES GLOBALES
// ============================================
int contador = 0;
int direccion = 1;
bool boton_anterior = true;
uint32_t ultimo_tiempo_boton = 0;

// ============================================
// PROTOTIPOS
// ============================================
void init_gpios(void);
void mostrar_numero(int num);
void set_segmentos(int digito);
void seleccionar_display(int display);
bool leer_boton(void);

// ============================================
// MAIN
// ============================================
int main() {
    stdio_init_all();
    init_gpios();
    
    printf("Práctica 9: Contador 0-99 con multiplexeo\n");
    printf("Velocidad: %d ms por número\n", VELOCIDAD_CONTADOR_MS);
    
    while (true) {
        // Leer botón para invertir dirección
        if (leer_boton()) {
            direccion *= -1;
            printf("Dirección: %s\n", direccion == 1 ? "ASC ↑" : "DESC ↓");
        }
        
        // Mostrar el número actual (con multiplexeo durante TODO el tiempo)
        mostrar_numero(contador);
        
        // Actualizar contador
        contador += direccion;
        if (contador > 99) contador = 0;
        if (contador < 0) contador = 99;
        
        // Mostrar en serial cuando cambia
        printf("Número: %02d\n", contador);
    }
    
    return 0;
}

// ============================================
// INICIALIZACIÓN
// ============================================
void init_gpios(void) {
    gpio_init(SEG_A); gpio_set_dir(SEG_A, GPIO_OUT); gpio_put(SEG_A, 0);
    gpio_init(SEG_B); gpio_set_dir(SEG_B, GPIO_OUT); gpio_put(SEG_B, 0);
    gpio_init(SEG_C); gpio_set_dir(SEG_C, GPIO_OUT); gpio_put(SEG_C, 0);
    gpio_init(SEG_D); gpio_set_dir(SEG_D, GPIO_OUT); gpio_put(SEG_D, 0);
    gpio_init(SEG_E); gpio_set_dir(SEG_E, GPIO_OUT); gpio_put(SEG_E, 0);
    gpio_init(SEG_F); gpio_set_dir(SEG_F, GPIO_OUT); gpio_put(SEG_F, 0);
    gpio_init(SEG_G); gpio_set_dir(SEG_G, GPIO_OUT); gpio_put(SEG_G, 0);
    
    gpio_init(DISPLAY_DECENAS); gpio_set_dir(DISPLAY_DECENAS, GPIO_OUT); gpio_put(DISPLAY_DECENAS, 0);
    gpio_init(DISPLAY_UNIDADES); gpio_set_dir(DISPLAY_UNIDADES, GPIO_OUT); gpio_put(DISPLAY_UNIDADES, 0);
    
    gpio_init(BUTTON_GPIO); gpio_set_dir(BUTTON_GPIO, GPIO_IN); gpio_pull_up(BUTTON_GPIO);
}

// ============================================
// CONFIGURAR SEGMENTOS
// ============================================
void set_segmentos(int digito) {
    uint8_t pattern = digitos[digito];
    gpio_put(SEG_A, (pattern >> 0) & 1);
    gpio_put(SEG_B, (pattern >> 1) & 1);
    gpio_put(SEG_C, (pattern >> 2) & 1);
    gpio_put(SEG_D, (pattern >> 3) & 1);
    gpio_put(SEG_E, (pattern >> 4) & 1);
    gpio_put(SEG_F, (pattern >> 5) & 1);
    gpio_put(SEG_G, (pattern >> 6) & 1);
}

// ============================================
// SELECCIONAR DISPLAY
// ============================================
void seleccionar_display(int display) {
    gpio_put(DISPLAY_DECENAS, display == 1 ? 1 : 0);
    gpio_put(DISPLAY_UNIDADES, display == 2 ? 1 : 0);
}

// ============================================
// MOSTRAR NÚMERO CON MULTIPLEXEO
// ============================================
void mostrar_numero(int num) {
    int decenas = num / 10;
    int unidades = num % 10;
    
    // Calcular cuántos ciclos necesitamos para el tiempo total
    int ciclos_totales = (VELOCIDAD_CONTADOR_MS * 350) / (TIEMPO_MULTIPLEX_US * 2);
    
    for (int i = 0; i < ciclos_totales; i++) {
        // Mostrar decenas
        set_segmentos(decenas);
        seleccionar_display(1);
        sleep_us(TIEMPO_MULTIPLEX_US);
        
        // Apagar decenas
        gpio_put(DISPLAY_DECENAS, 0);
        
        // Mostrar unidades
        set_segmentos(unidades);
        seleccionar_display(2);
        sleep_us(TIEMPO_MULTIPLEX_US);
        
        // Apagar unidades
        gpio_put(DISPLAY_UNIDADES, 0);
    }
}

// ============================================
// LEER BOTÓN
// ============================================
bool leer_boton(void) {
    uint32_t ahora = time_us_32();
    bool estado = gpio_get(BUTTON_GPIO);
    
    if (boton_anterior == 1 && estado == 0) {
        if (ahora - ultimo_tiempo_boton > 200000) {
            ultimo_tiempo_boton = ahora;
            boton_anterior = estado;
            return true;
        }
    }
    boton_anterior = estado;
    return false;
}