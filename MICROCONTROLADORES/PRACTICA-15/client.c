/**
 * Copyright (c) 2023 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include <stdio.h>
#include "btstack.h"
#include "pico/cyw43_arch.h"
#include "pico/stdlib.h"

// Cambia a #if 1 para ver mensajes de debug detallados
#if 0
#define DEBUG_LOG(...) printf(__VA_ARGS__)
#else
#define DEBUG_LOG(...)
#endif

#define LED_QUICK_FLASH_DELAY_MS 100
#define LED_SLOW_FLASH_DELAY_MS  1000

typedef enum {
    TC_OFF,
    TC_IDLE,
    TC_W4_SCAN_RESULT,
    TC_W4_CONNECT,
    TC_W4_SERVICE_RESULT,
    TC_W4_CHARACTERISTIC_RESULT,
    TC_W4_ENABLE_NOTIFICATIONS_COMPLETE,
    TC_W4_READY
} gc_state_t;

static btstack_packet_callback_registration_t hci_event_callback_registration;
static gc_state_t state = TC_OFF;
static bd_addr_t server_addr;
static bd_addr_type_t server_addr_type;
static hci_con_handle_t connection_handle;
static gatt_client_service_t server_service;
static gatt_client_characteristic_t server_characteristic;
static bool listener_registered;
static gatt_client_notification_t notification_listener;
static btstack_timer_source_t heartbeat;

static void client_start(void){
    printf("[Cliente] Iniciando escaneo BLE...\n");
    state = TC_W4_SCAN_RESULT;
    gap_set_scan_parameters(0, 0x0030, 0x0030);
    gap_start_scan();
}

// FIX: Corregido el switch-case con break apropiado para evitar fall-through
static bool advertisement_report_contains_service(uint16_t service, uint8_t *advertisement_report){
    const uint8_t * adv_data = gap_event_advertising_report_get_data(advertisement_report);
    uint8_t adv_len = gap_event_advertising_report_get_data_length(advertisement_report);

    ad_context_t context;
    for (ad_iterator_init(&context, adv_len, adv_data);
         ad_iterator_has_more(&context);
         ad_iterator_next(&context))
    {
        uint8_t data_type = ad_iterator_get_data_type(&context);
        uint8_t data_size = ad_iterator_get_data_len(&context);
        const uint8_t * data = ad_iterator_get_data(&context);

        if (data_type == BLUETOOTH_DATA_TYPE_COMPLETE_LIST_OF_16_BIT_SERVICE_CLASS_UUIDS ||
            data_type == BLUETOOTH_DATA_TYPE_INCOMPLETE_LIST_OF_16_BIT_SERVICE_CLASS_UUIDS)
        {
            for (int i = 0; i < data_size; i += 2) {
                uint16_t type = little_endian_read_16(data, i);
                DEBUG_LOG("[Cliente] Servicio encontrado en advertisement: 0x%04X\n", type);
                if (type == service) return true;
            }
        }
    }
    return false;
}

static void handle_gatt_client_event(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size) {
    UNUSED(packet_type);
    UNUSED(channel);
    UNUSED(size);

    uint8_t att_status;
    switch(state){
        case TC_W4_SERVICE_RESULT:
            switch(hci_event_packet_get_type(packet)) {
                case GATT_EVENT_SERVICE_QUERY_RESULT:
                    DEBUG_LOG("[Cliente] Servicio GATT encontrado, almacenando...\n");
                    gatt_event_service_query_result_get_service(packet, &server_service);
                    break;
                case GATT_EVENT_QUERY_COMPLETE:
                    att_status = gatt_event_query_complete_get_att_status(packet);
                    if (att_status != ATT_ERROR_SUCCESS) {
                        printf("[Cliente] Error en SERVICE_QUERY: ATT 0x%02x\n", att_status);
                        gap_disconnect(connection_handle);
                        break;
                    }
                    // FIX: Usar discover_by_uuid16 para buscar especificamente la caracteristica de temperatura
                    state = TC_W4_CHARACTERISTIC_RESULT;
                    printf("[Cliente] Servicio encontrado. Buscando caracteristica de temperatura...\n");
                    gatt_client_discover_characteristics_for_service_by_uuid16(
                        handle_gatt_client_event,
                        connection_handle,
                        &server_service,
                        ORG_BLUETOOTH_CHARACTERISTIC_TEMPERATURE
                    );
                    break;
                default:
                    break;
            }
            break;

        case TC_W4_CHARACTERISTIC_RESULT:
            switch(hci_event_packet_get_type(packet)) {
                case GATT_EVENT_CHARACTERISTIC_QUERY_RESULT:
                    DEBUG_LOG("[Cliente] Caracteristica encontrada, almacenando...\n");
                    gatt_event_characteristic_query_result_get_characteristic(packet, &server_characteristic);
                    break;
                case GATT_EVENT_QUERY_COMPLETE:
                    att_status = gatt_event_query_complete_get_att_status(packet);
                    if (att_status != ATT_ERROR_SUCCESS) {
                        printf("[Cliente] Error en CHARACTERISTIC_QUERY: ATT 0x%02x\n", att_status);
                        gap_disconnect(connection_handle);
                        break;
                    }
                    // Registrar listener para notificaciones
                    listener_registered = true;
                    gatt_client_listen_for_characteristic_value_updates(
                        &notification_listener,
                        handle_gatt_client_event,
                        connection_handle,
                        &server_characteristic
                    );
                    // Habilitar notificaciones en el servidor
                    printf("[Cliente] Caracteristica encontrada. Habilitando notificaciones...\n");
                    state = TC_W4_ENABLE_NOTIFICATIONS_COMPLETE;
                    gatt_client_write_client_characteristic_configuration(
                        handle_gatt_client_event,
                        connection_handle,
                        &server_characteristic,
                        GATT_CLIENT_CHARACTERISTICS_CONFIGURATION_NOTIFICATION
                    );
                    break;
                default:
                    break;
            }
            break;

        case TC_W4_ENABLE_NOTIFICATIONS_COMPLETE:
            switch(hci_event_packet_get_type(packet)){
                case GATT_EVENT_QUERY_COMPLETE:
                    att_status = gatt_event_query_complete_get_att_status(packet);
                    if (att_status != ATT_ERROR_SUCCESS) {
                        printf("[Cliente] Error habilitando notificaciones: ATT 0x%02x\n", att_status);
                        gap_disconnect(connection_handle);
                        break;
                    }
                    printf("[Cliente] Notificaciones habilitadas. Esperando datos de temperatura...\n");
                    state = TC_W4_READY;
                    break;
                default:
                    break;
            }
            break;

        case TC_W4_READY:
            switch(hci_event_packet_get_type(packet)){
                case GATT_EVENT_NOTIFICATION: {
                    uint16_t value_length = gatt_event_notification_get_value_length(packet);
                    const uint8_t *value = gatt_event_notification_get_value(packet);
                    if (value_length == 2) {
                        uint16_t raw = little_endian_read_16(value, 0);
                        float temp = (float)raw / 100.0f;
                        printf("[Cliente] Temperatura recibida: %.2f degC\n", temp);
                    } else {
                        printf("[Cliente] Longitud inesperada: %d bytes\n", value_length);
                    }
                    break;
                }
                default:
                    DEBUG_LOG("[Cliente] Paquete desconocido: 0x%02x\n", hci_event_packet_get_type(packet));
                    break;
            }
            break;

        default:
            printf("[Cliente] Error: estado inesperado %d\n", state);
            break;
    }
}

static void hci_event_handler(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size) {
    UNUSED(size);
    UNUSED(channel);
    bd_addr_t local_addr;
    if (packet_type != HCI_EVENT_PACKET) return;

    uint8_t event_type = hci_event_packet_get_type(packet);
    switch(event_type){
        case BTSTACK_EVENT_STATE:
            if (btstack_event_state_get_state(packet) == HCI_STATE_WORKING) {
                gap_local_bd_addr(local_addr);
                printf("[Cliente] BTstack activo en: %s\n", bd_addr_to_str(local_addr));
                client_start();
            } else {
                state = TC_OFF;
            }
            break;

        case GAP_EVENT_ADVERTISING_REPORT:
            if (state != TC_W4_SCAN_RESULT) return;
            // Filtrar por el servicio Environmental Sensing
            if (!advertisement_report_contains_service(ORG_BLUETOOTH_SERVICE_ENVIRONMENTAL_SENSING, packet)) return;
            // Guardar dirección del servidor
            gap_event_advertising_report_get_address(packet, server_addr);
            server_addr_type = gap_event_advertising_report_get_address_type(packet);
            // Detener escaneo y conectar
            state = TC_W4_CONNECT;
            gap_stop_scan();
            printf("[Cliente] Servidor encontrado en: %s. Conectando...\n", bd_addr_to_str(server_addr));
            gap_connect(server_addr, server_addr_type);
            break;

        case HCI_EVENT_LE_META:
            switch (hci_event_le_meta_get_subevent_code(packet)) {
                case HCI_SUBEVENT_LE_CONNECTION_COMPLETE:
                    if (state != TC_W4_CONNECT) return;
                    connection_handle = hci_subevent_le_connection_complete_get_connection_handle(packet);
                    printf("[Cliente] Conexion establecida! Buscando servicio de temperatura...\n");
                    state = TC_W4_SERVICE_RESULT;
                    gatt_client_discover_primary_services_by_uuid16(
                        handle_gatt_client_event,
                        connection_handle,
                        ORG_BLUETOOTH_SERVICE_ENVIRONMENTAL_SENSING
                    );
                    break;
                default:
                    break;
            }
            break;

        case HCI_EVENT_DISCONNECTION_COMPLETE:
            connection_handle = HCI_CON_HANDLE_INVALID;
            if (listener_registered){
                listener_registered = false;
                gatt_client_stop_listening_for_characteristic_value_updates(&notification_listener);
            }
            printf("[Cliente] Desconectado de %s. Reiniciando escaneo...\n", bd_addr_to_str(server_addr));
            if (state == TC_OFF) break;
            client_start();
            break;

        default:
            break;
    }
}

static void heartbeat_handler(struct btstack_timer_source *ts) {
    static bool quick_flash;
    static bool led_on = true;

    led_on = !led_on;
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, led_on);
    if (listener_registered && led_on) {
        quick_flash = !quick_flash;
    } else if (!listener_registered) {
        quick_flash = false;
    }

    btstack_run_loop_set_timer(ts, (led_on || quick_flash) ? LED_QUICK_FLASH_DELAY_MS : LED_SLOW_FLASH_DELAY_MS);
    btstack_run_loop_add_timer(ts);
}

int main() {
    stdio_init_all();

    if (cyw43_arch_init()) {
        printf("Error: no se pudo inicializar cyw43_arch\n");
        return -1;
    }

    l2cap_init();
    sm_init();
    sm_set_io_capabilities(IO_CAPABILITY_NO_INPUT_NO_OUTPUT);

    // ATT server vacio (necesario para que iOS/Android puedan hacer ATT queries)
    att_server_init(NULL, NULL, NULL);

    gatt_client_init();

    hci_event_callback_registration.callback = &hci_event_handler;
    hci_add_event_handler(&hci_event_callback_registration);

    // Timer para el LED
    heartbeat.process = &heartbeat_handler;
    btstack_run_loop_set_timer(&heartbeat, LED_SLOW_FLASH_DELAY_MS);
    btstack_run_loop_add_timer(&heartbeat);

    hci_power_control(HCI_POWER_ON);

    // FIX: El cliente DEBE llamar btstack_run_loop_execute() para procesar eventos BLE
    // En modo threadsafe background esto es seguro y necesario
    btstack_run_loop_execute();

    return 0;
}