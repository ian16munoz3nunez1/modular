# Beto <--> Edna <--> Ian

from machine import Pin
import camera as cv
import network
import binascii
import socket
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

addr = ('192.168.1.28', 9000)
chunk = 4194304

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.sendto(b'ok', addr)

sleep(1)
while True:
    cv.framesize(cv.FRAME_CIF)
    cv.quality(10)
    cv.brightness(0)
    cv.contrast(0)
    cv.saturation(0)
    frame = cv.capture()
    frame = binascii.b2a_base64(frame)
    sock.sendto(frame, addr)

    msg = sock.recvfrom(8)[0]
    if msg == b'end':
        break
    sleep(1/30)

sock.close()
cv.deinit()
print("Conexion terminada")

