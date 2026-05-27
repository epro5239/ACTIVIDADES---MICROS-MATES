# Práctica 17 - Sistema de Riego
# Versión para arrastrar a la Pico

import network
import socket
import time
from machine import Pin, ADC

# Configuración WiFi (CÁMBIAME)
SSID = "Piso 2"
PASSWORD = "Z2WhVh9FDw"

# Pines
sensor = ADC(Pin(26))
rele = Pin(15, Pin.OUT)
rele.value(1)

# Conectar WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Conectando...", end="")
for i in range(20):
    if wlan.isconnected():
        break
    time.sleep(1)
    print(".", end="")

ip = wlan.ifconfig()[0]
print(f"\n✅ IP: {ip}")

# Servidor web
server = socket.socket()
server.bind(('0.0.0.0', 80))
server.listen(1)

while True:
    cliente, addr = server.accept()
    req = cliente.recv(1024)
    
    valor = sensor.read_u16()
    humedad = 100 - (valor * 100 // 65535)
    
    if b"/regar" in req:
        rele.value(0)
        time.sleep(5)
        rele.value(1)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Riego</title>
    <meta name="viewport" content="width=device-width">
    <meta http-equiv="refresh" content="5">
    <style>
        body{{font-family:Arial;text-align:center;padding:20px;background:#e8f5e9;}}
        h1{{color:#2e7d32;}}
        .h{{font-size:60px;color:#2e7d32;}}
        button{{background:#2e7d32;color:white;padding:15px 30px;font-size:18px;border:none;border-radius:10px;}}
    </style>
</head>
<body>
    <h1>🌱 Sistema de Riego</h1>
    <div class="h">💧 {humedad}%</div>
    <progress value="{humedad}" max="100"></progress>
    <br><br>
    <form action="/regar"><button>💦 Regar (5s)</button></form>
    <hr>
    <small>Práctica 17 - Microcontroladores</small>
</body>
</html>"""
    cliente.send(html)
    cliente.close()