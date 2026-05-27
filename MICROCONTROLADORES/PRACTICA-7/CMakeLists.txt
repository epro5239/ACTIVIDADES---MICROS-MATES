cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)
set(PICO_BOARD pico_w)    # Le decimos al compilador que nuestra placa es la versión w

project(Practica_7)        # Nombre de la carpeta de proyecto

pico_sdk_init()            # Inicializa el SDK del proyecto

add_executable(Practica_7  # Nombre del ejecutable
    Practica_7.c           # Archivo de código fuente
)

target_link_libraries(Practica_7
    pico_stdlib            # Librerías estándar
    hardware_gpio          # Para control de GPIO
)

pico_enable_stdio_usb(Practica_7 1)
pico_enable_stdio_uart(Practica_7 0)

pico_add_extra_outputs(Practica_7)  # Genera .uf2, .elf, etc.