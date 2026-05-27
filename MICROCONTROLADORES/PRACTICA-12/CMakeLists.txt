cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)

set(PICO_BOARD pico_w)
set(PICO_STDIO_USB 1)

project(Practica_12)

pico_sdk_init()

add_executable(rgb_pwm
    rgb_pwm.c
)

target_link_libraries(rgb_pwm
    pico_stdlib
    hardware_adc
    hardware_pwm
    hardware_gpio
)

pico_enable_stdio_usb(rgb_pwm 1)
pico_enable_stdio_uart(rgb_pwm 0)

pico_add_extra_outputs(rgb_pwm)