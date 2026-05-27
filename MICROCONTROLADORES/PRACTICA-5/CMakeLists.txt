cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)
set(PICO_BOARD pico_w)    # Le decimos al compilador que nuestra placa es la versión w

project(Practica_5)        # Nombre de la carpeta de proyecto

pico_sdk_init()            # Inicializa el SDK del proyecto

add_executable(Practica_5  # Nombre del ejecutable
    Practica_5.c           # Archivo de código fuente
)

target_link_libraries(Practica_5
    pico_stdlib            # Librerías estándar
    hardware_gpio          # Para control de GPIO
)

pico_enable_stdio_usb(Practica_5 1)
pico_enable_stdio_uart(Practica_5 0)

pico_add_extra_outputs(Practica_5)  # Genera .uf2, .elf, etc.