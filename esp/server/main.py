#!/bin/python3

# 215503408: Briseño García Edna Elizabeth
# 216464457: Muñoz Nuñez Ian Emmanuel

import socket
import sys
import re
from colorama import init
from colorama.ansi import Fore
import numpy as np
pi = np.pi

init(autoreset=True)

L = 6.5
R = 6.5
minima = -100
maxima = 100
minArray = np.array([-1023, -1023, -1023])
maxArray = np.array([1023, 1023, 1023])

x_i = np.array([0.0, 0.0, 0.0])
m = np.array([[-np.sin(x_i[2]), np.cos(x_i[2]), L],
              [-np.sin(x_i[2]+2*pi/3), np.cos(x_i[2]+2*pi/3), L],
              [-np.sin(x_i[2]+4*pi/3), np.cos(x_i[2]+4*pi/3), L]])

host, port = '0.0.0.0', 9999
chunk = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((host, port))
sock.listen(1)
print(Fore.CYAN + f"[*] Esperando conexion en el puerto {port}")

conexion, addr = sock.accept()
print(Fore.GREEN + f"[+] Conectado a \'{addr}\'")

while True:
    cmd = input('> ')

    if re.match(r"\d+,\d+,\d+", cmd):
        x_dot = np.array([float(i) for i in cmd.split(',')]).reshape(-1, 1)
        v = [int(i) for i in np.matmul(m, x_dot).flatten()]
        v = np.min(np.vstack((v, maxArray)), axis=0)
        v = np.max(np.vstack((v, minArray)), axis=0)
        v = f"{v[0]},{v[1]},{v[2]}"
        print(v)
        conexion.send(v.encode())
        msg = conexion.recv(8).decode()
        print(Fore.CYAN + f"[*] {msg}")


    elif cmd[0].lower() == 'q':
        conexion.send(b'q')
        msg = conexion.recv(1024).decode()
        print(Fore.YELLOW + f"{msg}")
        break

    else:
        print(Fore.RED + f"[-] Error en la entrada \"{cmd}\"")

sock.close()
conexion.close()
print(Fore.RED + "[-] Conexion terminada")

