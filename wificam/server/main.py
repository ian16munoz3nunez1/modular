# 215503408: Briseño García Edna Elizabeth
# 216464457: Muñoz Nuñez Ian Emmanuel

import camera as cv
import socket
import network
from machine import Pin
from time import sleep

led = Pin(4, Pin.OUT)

def blink(n, t):
    for i in range(n):
        led.on()
        sleep(t)
        led.off()
        sleep(t)

def conectar(ssid, password):
    blink(2, 0.2)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    blink(2, 0.2)

conectar('IZZI-BC36', 'vm5sstg3')
cv.init(0, format=cv.JPEG)

host, port = '0.0.0.0', 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((host, port))
sock.listen(1)
print('Esperando conexion...')

while True:
    conexion, addr = sock.accept()
    request = conexion.recv(1024)

    frame = cv.capture()
    header = 'HTTP/1.1 200 OK\r\n\r\n'.encode()
    finalResponse = header + frame
    conexion.send(finalResponse)

    conexion.close()

cv.deinit()
sock.close()
print("Conexion terminada")

