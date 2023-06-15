# Beto <--> Edna <--> Ian

import timeit
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from colorama import init
from colorama.ansi import Fore
from kuka import Kuka, link
from wf import WaveFront
from dibujarKuka import dibujar_kuka
pi = np.pi
sq2 = np.sqrt(2)

init(autoreset=True)

l1 = link(pi/2, 0.0, 0.147, 0.0)
l2 = link(0.0, 0.155, 0.0, pi/2)
l3 = link(0.0, 0.135, 0.0, -pi/2)
l4 = link(0.0, 0.217, 0.0, -pi/2)

kuka = Kuka(19999, np.vstack((l1, l2, l3, l4)))
L = 0.471/2
l = 0.3/2
S = 16

imagen = kuka.getImage()
imagen = cv.resize(imagen, (30, 30))
wf = WaveFront(imagen)

mask = wf.mainMask((45, 150, 150), (60, 255, 255), 5)[0]

startNorm = wf.appMask((30, 150, 150), (40, 255, 255), 1)[1]
startY, startX = wf.centroide(startNorm)
start = np.array([[startY], [startX]])

goalNorm = wf.appMask((125, 150, 150), (160, 255, 255), 1)[1]
goalY, goalX = wf.centroide(goalNorm)
goal = np.array([[goalY], [goalX]])

path = wf.calcPath(mask, start, goal)
xyPath = wf.cr2xy(path, 3.7, 2.7)
wf.plotPath(path, start, goal)

N = xyPath.shape[1]
k = np.diag([0.8, 0.8, 0.8])

start = timeit.default_timer()
end = start

i = 0
while i < N:
    p_d = np.array([xyPath[0, i], xyPath[1, i], -pi/2]).reshape(-1, 1)

    x_i = kuka.getPose().ravel()
    p_i = x_i[:3]
    q_i = kuka.fkine(x_i)

    alpha = p_i[2] + (pi/4)
    m = np.array([[sq2*np.sin(alpha), -sq2*np.cos(alpha), -(L+l)],
                  [sq2*np.cos(alpha), sq2*np.sin(alpha), (L+l)],
                  [sq2*np.cos(alpha), sq2*np.sin(alpha), -(L+l)],
                  [sq2*np.sin(alpha), -sq2*np.cos(alpha), (L+l)]])
    e = p_d - p_i.reshape(-1, 1)
    if np.mean(abs(e)) <= 0.15:
        i += 1
    p_dot = np.matmul(m, np.matmul(k, e))

    kuka.setJointVelocity(p_dot)

    end = timeit.default_timer()

q_d = np.array([[2.75, 3.25],
                [-1.8, -1.8],
                [0.29, 0.4]])

i = 0
while i < 2:
    x_i = kuka.getPose().ravel()
    p_i = x_i[:3]
    q_i = kuka.fkine(x_i)

    e = q_d[:, i].reshape(-1, 1) - q_i
    if np.mean(abs(e)) < 0.01:
        i += 1
        if i == 1:
            kuka.closeGrip()
            sleep(3)
        if i == 2:
            kuka.openGrip()
            sleep(3)
            break

    J = kuka.jacob(x_i)
    q_dot = np.matmul(np.linalg.pinv(J), np.matmul(k, e))

    alpha = p_i[2] + (pi/4)
    m = np.array([[sq2*np.sin(alpha), -sq2*np.cos(alpha), -(L+l)],
                  [sq2*np.cos(alpha), sq2*np.sin(alpha), (L+l)],
                  [sq2*np.cos(alpha), sq2*np.sin(alpha), -(L+l)],
                  [sq2*np.sin(alpha), -sq2*np.cos(alpha), (L+l)]])

    v = np.matmul(m, q_dot[:3])
    q = x_i[3:].reshape(-1, 1) + q_dot[3:]*0.1

    kuka.setJointVelocity(v, q)

    end = timeit.default_timer()

kuka.stopSimulation()
print(Fore.YELLOW + "[!] Conexion terminada")

