cmake_minimum_required(VERSION 3.12)

# Pull in SDK (must be before project)
include(pico_sdk_import.cmake)

if (PICO_SDK_VERSION_STRING VERSION_LESS "1.5.0")
    message(FATAL_ERROR "Raspberry Pi Pico SDK version 1.5.0 (or later) required. Your version is ${PICO_SDK_VERSION_STRING}")
endif()

project(Practica_15 C CXX ASM)
set(PICO_BOARD pico_w)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialize the SDK
pico_sdk_init()

# ---------------------------------------------------------------
# Ejecutable 1: SERVIDOR BLE (RPi Pico 1)
# Lee el sensor de temperatura interno y lo anuncia via BLE
# ---------------------------------------------------------------
add_executable(picow_ble_temp_sensor
    server.c server_common.c
)
target_link_libraries(picow_ble_temp_sensor
    pico_stdlib
    pico_btstack_ble
    pico_btstack_cyw43
    pico_cyw43_arch_none
    hardware_adc
)

# FIX: Habilitar UART para ver printf del servidor (USB no funciona sin conexion a PC)
pico_enable_stdio_usb(picow_ble_temp_sensor 1)
pico_enable_stdio_uart(picow_ble_temp_sensor 0)

target_include_directories(picow_ble_temp_sensor PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}
)

pico_btstack_make_gatt_header(picow_ble_temp_sensor
    PRIVATE ${CMAKE_CURRENT_LIST_DIR}/temp_sensor.gatt
)

pico_add_extra_outputs(picow_ble_temp_sensor)

# ---------------------------------------------------------------
# Ejecutable 2: CLIENTE BLE (RPi Pico 2)
# Se conecta al servidor y muestra la temperatura en el monitor serial
# ---------------------------------------------------------------
add_executable(picow_ble_temp_reader
    client.c
)
target_link_libraries(picow_ble_temp_reader
    pico_stdlib
    pico_btstack_ble
    pico_btstack_cyw43
    pico_cyw43_arch_none
    hardware_adc
)

# El cliente DEBE tener stdio USB habilitado para ver el monitor serial
pico_enable_stdio_usb(picow_ble_temp_reader 1)
pico_enable_stdio_uart(picow_ble_temp_reader 0)

target_include_directories(picow_ble_temp_reader PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}
)
target_compile_definitions(picow_ble_temp_reader PRIVATE
    RUNNING_AS_CLIENT=1
)

pico_add_extra_outputs(picow_ble_temp_reader)