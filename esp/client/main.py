# 215503408: Briseño García Edna Elizabeth
# 216464457: Muñoz Nuñez Ian Emmanuel

import network
import socket
from time import sleep
from func import forward, backward, blink, led

ip, port = '192.168.1.28', 9999
chunk = 1024

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

        sock.connect((ip, port))
        break
    except:
        led.off()
        sleep(2)

blink(5, 0.2)
while True:
    try:
        msg = sock.recv(chunk).decode()
        print(msg)

        if msg[0].lower() == 'q':
            sock.send(b"Fin de la conexion")
            break

        v = [int(i) for i in msg.split(',')]

        sock.send(b'ok')
        if v[0] >= 0:
            forward('1', v[0])
        else:
            backward('1', abs(v[0]))
        if v[1] >= 0:
            forward('2', v[1])
        else:
            backward('2', abs(v[1]))
        if v[2] >= 0:
            forward('3', v[2])
        else:
            backward('3', abs(v[2]))

    except Exception as e:
        print(e)
        break

sock.close()
blink(5, 0.2)

