cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.2.0)
set(toolchainVersion 14_2_Rel1)
set(picotoolVersion 2.2.0-a4)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()

set(PICO_BOARD pico_w CACHE STRING "Board type")
include(pico_sdk_import.cmake)

project(Practica_14 C CXX ASM)
pico_sdk_init()

add_executable(Practica_14 
    Practica_14.c
    semaforo.c
)

pico_set_program_name(Practica_14 "Practica_14")
pico_set_program_version(Practica_14 "0.1")

pico_enable_stdio_uart(Practica_14 0)
pico_enable_stdio_usb(Practica_14 1)

target_link_libraries(Practica_14
    pico_stdlib
    hardware_timer
    hardware_pwm
    hardware_irq
)

target_include_directories(Practica_14 PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}
)

pico_add_extra_outputs(Practica_14)