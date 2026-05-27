cmake_minimum_required(VERSION 3.13)

# Incluir el SDK de Pico (debe estar en la misma carpeta)
include(pico_sdk_import.cmake)

# Definir la placa (pico_w es para Pico W, pico para Pico normal)
set(PICO_BOARD pico_w)

# Nombre del proyecto (DEBE coincidir con el nombre del ejecutable)
project(Practica_9)

# Inicializar el SDK
pico_sdk_init()

# Crear el ejecutable con tu archivo .c
add_executable(Practica_9
    Practica_9.c
)

# Enlazar las librerías necesarias
target_link_libraries(Practica_9
    pico_stdlib
    hardware_gpio
)

# Habilitar salida por USB (para ver los prints)
pico_enable_stdio_usb(Practica_9 1)
pico_enable_stdio_uart(Practica_9 0)

# Generar archivos adicionales (.uf2, .elf, etc.)
pico_add_extra_outputs(Practica_9)