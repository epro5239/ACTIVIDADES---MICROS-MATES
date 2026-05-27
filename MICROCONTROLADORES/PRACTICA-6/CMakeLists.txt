cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)
set(PICO_BOARD pico_w)

project(Practica_6)

pico_sdk_init()

add_executable(Practica_6
    Practica_6.c
)

target_link_libraries(Practica_6
    pico_stdlib
    hardware_gpio
)

pico_enable_stdio_usb(Practica_6 1)
pico_enable_stdio_uart(Practica_6 0)

pico_add_extra_outputs(Practica_6)