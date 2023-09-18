# 215503408: Briseño García Edna Elizabeth
# 216464457: Muñoz Nuñez Ian Emmanuel

import network
import socket
from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)

def blink(t):
    led.on()
    sleep(t)
    led.off()
    sleep(t)

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='espNet32', authmode=3, password='ciNNam0n2412')

while True:
    blink(0.5)

