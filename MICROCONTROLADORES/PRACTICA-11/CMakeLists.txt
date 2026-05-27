cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)
set(PICO_BOARD pico_w)

project(Practica_11)

pico_sdk_init()

add_executable(temperatura
    temperatura.c
)

target_link_libraries(temperatura
    pico_stdlib
    hardware_adc
    hardware_gpio
    hardware_pwm
)

pico_enable_stdio_usb(temperatura 1)
pico_enable_stdio_uart(temperatura 0)

pico_add_extra_outputs(temperatura)