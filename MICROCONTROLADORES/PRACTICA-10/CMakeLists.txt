cmake_minimum_required(VERSION 3.13)

# Incluir el SDK de Pico (debe estar en la misma carpeta)
include(pico_sdk_import.cmake)

# Definir la placa (pico_w para Pico W)
set(PICO_BOARD pico_w)

# Nombre del proyecto
project(Practica_10)

# Inicializar el SDK
pico_sdk_init()

# Crear el ejecutable con tu archivo .c
add_executable(Practica_10
    Practica_10.c
)

# Enlazar las librerías necesarias
target_link_libraries(Practica_10
    pico_stdlib
    hardware_adc
)

# Habilitar salida por USB (para ver los prints)
pico_enable_stdio_usb(Practica_10 1)
pico_enable_stdio_uart(Practica_10 0)

# Generar archivos adicionales (.uf2, .elf, .hex, .bin)
pico_add_extra_outputs(Practica_10)