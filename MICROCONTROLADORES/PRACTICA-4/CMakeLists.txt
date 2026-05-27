cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)
set(PICO_BOARD pico_w)

project(Práctica_4)

pico_sdk_init()

add_executable(Parpadeo
    Parpadeo.c
)

target_link_libraries(Parpadeo
    pico_stdlib
    pico_cyw43_arch_none
)

pico_add_extra_outputs(Parpadeo)