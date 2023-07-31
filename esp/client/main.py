# Beto <--> Edna <--> Ian

import network
import socket
from machine import Pin, PWM
from time import sleep

led = Pin(2, Pin.OUT)
rf = PWM(Pin(4, Pin.OUT), freq=60)
rb = PWM(Pin(5, Pin.OUT), freq=60)
lf = PWM(Pin(18, Pin.OUT), freq=60)
lb = PWM(Pin(19, Pin.OUT), freq=60)
chunk = 1024

rf.duty(0)
rb.duty(0)
lf.duty(0)
lb.duty(0)

def rightForward(v):
    rb.duty(0)
    rf.duty(v)

def rightBackward(v):
    rf.duty(0)
    rb.duty(v)

def leftForward(v):
    lb.duty(0)
    lf.duty(v)

def leftBackward(v):
    lf.duty(0)
    lb.duty(v)

def blink(v, t):
    for i in range(v):
        led.on()
        sleep(t)
        led.off()
        sleep(t)

def conectar(ssid, password):
    blink(2, 0.5)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    blink(2, 0.5)

conectar('IZZI-BC36', 'vm5sstg3')

while True:
    try:
        led.on()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.connect(('192.168.1.28', 9999))
        break
    except:
        led.off()
        sleep(2)

blink(5, 0.2)
while True:
    try:
        v = sock.recv(chunk).decode()
        print(v)

        if v[0].lower() == 'q':
            break

        w = [int(i) for i in v.split(',')]
        wl = int(abs(w[0])*1023/100)
        wr = int(abs(w[1])*1023/100)

        sock.send(b'ok')
        if w[0] >= 0:
            leftForward(wl)
        else:
            leftBackward(wl)
        if w[1] >= 0:
            rightForward(wr)
        else:
            rightBackward(wr)

    except Exception as e:
        print(e)
        break

sock.close()
blink(5, 0.2)

