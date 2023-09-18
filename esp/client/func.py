# 215503408: Briseño García Edna Elizabeth
# 216464457: Muñoz Nuñez Ian Emmanuel

from machine import Pin, PWM
from time import sleep

led = Pin(2, Pin.OUT)
w1f = PWM(Pin(32, Pin.OUT), freq=60)
w1b = PWM(Pin(33, Pin.OUT), freq=60)
w2f = PWM(Pin(25, Pin.OUT), freq=60)
w2b = PWM(Pin(26, Pin.OUT), freq=60)
w3f = PWM(Pin(27, Pin.OUT), freq=60)
w3b = PWM(Pin(14, Pin.OUT), freq=60)

w1f.duty(0)
w1b.duty(0)
w2f.duty(0)
w2b.duty(0)
w3f.duty(0)
w3b.duty(0)

def forward(w, v):
    if w == '1':
        w1f.duty(v)
        w1b.duty(0)
    elif w == '2':
        w2f.duty(v)
        w2b.duty(0)
    elif w == '3':
        w3f.duty(v)
        w3b.duty(0)
    else:
        w1f.duty(0)
        w1b.duty(0)
        w2f.duty(0)
        w2b.duty(0)
        w3f.duty(0)
        w3b.duty(0)

def backward(w, v):
    if w == '1':
        w1b.duty(v)
        w1f.duty(0)
    elif w == '2':
        w2b.duty(v)
        w2f.duty(0)
    elif w == '3':
        w3b.duty(v)
        w3f.duty(0)
    else:
        w1f.duty(0)
        w1b.duty(0)
        w2f.duty(0)
        w2b.duty(0)
        w3f.duty(0)
        w3b.duty(0)

def blink(v, t):
    for i in range(v):
        led.on()
        sleep(t)
        led.off()
        sleep(t)

