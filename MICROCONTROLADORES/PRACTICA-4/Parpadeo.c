#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"

int main() {
    // Inicializar el chip inalámbrico
    if (cyw43_arch_init()) {
        return -1;  // Sin printf para evitar complicaciones
    }
    
    while (true) {
        // Encender LED - NOTA: Usar CYW43_WL_GPIO_LED_PIN en mayúsculas
        cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
        sleep_ms(250);
        
        // Apagar LED
        cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 0);
        sleep_ms(250);
    }
}