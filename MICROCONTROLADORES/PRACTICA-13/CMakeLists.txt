cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)

project(motor_pwm C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()

add_executable(motor_pwm
    motor_pwm.c
)

pico_enable_stdio_usb(motor_pwm 1)
pico_enable_stdio_uart(motor_pwm 0)

target_link_libraries(motor_pwm
    pico_stdlib
    hardware_pwm
    hardware_gpio
)

pico_add_extra_outputs(motor_pwm)

target_compile_options(motor_pwm PRIVATE -O2)