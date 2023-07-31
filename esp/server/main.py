# Beto <--> Edna <--> Ian

import socket
import sys
from colorama import init
from colorama.ansi import Fore
import numpy as np

init(autoreset=True)

L = 6.5
R = 6.5
minima = -100
maxima = 100

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
    v = input('> ')

    if v[0].lower() == 'q':
        conexion.send(b'quit')
        break

    if len(v.split(',')) > 2:
        print(Fore.YELLOW + "[!] Solo se admiten dos valores")
        continue
    else:
        # v, w = [int(i) for i in v.split(',')]
        # wr = int((2*v+w*L)/(2*R))
        # wl = int((2*v-w*L)/(2*R))
        wl, wr = [int(i) for i in v.split(',')]
        wl = np.minimum(wl, maxima)
        wl = np.maximum(wl, minima)
        wr = np.minimum(wr, maxima)
        wr = np.maximum(wr, minima)
        v = f"{wl},{wr}"
        print(v)

        conexion.send(f'{v}'.encode())
        msg = conexion.recv(chunk).decode()
        print(Fore.CYAN + f"[*] {msg}")

sock.close()
conexion.close()
print(Fore.RED + "[-] Conexion terminada")

