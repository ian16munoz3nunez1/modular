#!/bin/python3

# 215503408: Briseño García Edna Elizabeth
# 216464457: Muñoz Nuñez Ian Emmanuel

import socket
import sys
from colorama import init
from colorama.ansi import Fore
import numpy as np
pi = np.pi

init(autoreset=True)

L = 6.5
R = 6.5
minima = -100
maxima = 100

x_i = np.array([0.0, 0.0, 0.0])
m = np.array([[-np.sin(x_i[2]), np.cos(x_i[2]), L],
              [-np.sin(x_i[2]+2*pi/3), np.cos(x_i[2]+2*pi/3), L],
              [-np.sin(x_i[2]+4*pi/3), np.cos(x_i[2]+4*pi/3), L]])

host, port = sys.argv[1], int(sys.argv[2])
chunk = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((host, port))
sock.listen(1)
print(Fore.CYAN + f"[*] Esperando conexion en el puerto {port}")

conexion, addr = sock.accept()
print(Fore.GREEN + f"[+] Conectado a \'{addr}\'")

while True:
    x_dot = input('> ')

    if x_dot[0].lower() == 'q':
        conexion.send(b'q')
        msg = conexion.recv(1024).decode()
        print(Fore.YELLOW + f"{msg}")
        break
    else:
        x_dot = np.array([float(i) for i in x_dot.split(',')]).reshape(-1, 1)
        v = [int(i) for i in np.matmul(m, x_dot).flatten()]
        v = f"{v[0]},{v[1]},{v[2]}"
        print(v)
        conexion.send(v.encode())
        msg = conexion.recv(8).decode()
        print(Fore.CYAN + f"[*] {msg}")

sock.close()
conexion.close()
print(Fore.RED + "[-] Conexion terminada")

