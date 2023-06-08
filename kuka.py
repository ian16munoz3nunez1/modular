# Ian Mu;oz Nu;ez

import cv2 as cv
import numpy as np
from time import sleep
from colorama import init
from colorama.ansi import Fore
import sim

init(autoreset=True)

class Kuka:
    def __init__(self, port):
        self.__clientID = []

        self.__kuka = []
        self.__motor1 = []
        self.__motor2 = []
        self.__motor3 = []
        self.__motor4 = []
        self.__camera = []

        self.__wl = -2.5*np.ones((4, 1))
        self.__wu = 2.5*np.ones((4, 1))

        sim.simxFinish(-1)
        self.__clientID = sim.simxStart("127.0.0.1", port, True, True, 5000, 5)

        if self.__clientID == 0:
            _, self.__kuka = sim.simxGetObjectHandle(self.__clientID, '/youBot/youBot_ref', sim.simx_opmode_oneshot_wait)
            _, self.__motor1 = sim.simxGetObjectHandle(self.__clientID, '/youBot/rollingJoint_fl', sim.simx_opmode_oneshot_wait)
            _, self.__motor2 = sim.simxGetObjectHandle(self.__clientID, '/youBot/rollingJoint_fr', sim.simx_opmode_oneshot_wait)
            _, self.__motor3 = sim.simxGetObjectHandle(self.__clientID, '/youBot/rollingJoint_rl', sim.simx_opmode_oneshot_wait)
            _, self.__motor4 = sim.simxGetObjectHandle(self.__clientID, '/youBot/rollingJoint_rr', sim.simx_opmode_oneshot_wait)
            _, self.__camera = sim.simxGetObjectHandle(self.__clientID, '/kinect/rgb', sim.simx_opmode_oneshot_wait)

            sim.simxGetStringSignal(self.__clientID, 'measuredDataAtThisTime', sim.simx_opmode_streaming)
            sleep(1)

            print(Fore.GREEN + "[+] ok")

        else:
            print(Fore.RED + "[-] error")

    def getPose(self):
        aux = np.ones((2, 1))

        while np.sum(aux) != 0:
            if sim.simxGetConnectionId(self.__clientID) == 1:
                aux[0], position = sim.simxGetObjectPosition(self.__clientID, self.__kuka, -1, sim.simx_opmode_streaming)
                aux[1], orientation = sim.simxGetObjectOrientation(self.__clientID, self.__kuka, -1, sim.simx_opmode_streaming)
                x_i = np.array([[position[0]], [position[1]], [orientation[2]]], dtype=np.float64)

            else:
                print(Fore.RED + "[-] Conexion perdida (getPose)")
                raise RuntimeError("error")

        return x_i

    def setJointVelocity(self, w):
        R = 0.1
        w = w/R

        if sim.simxGetConnectionId(self.__clientID) == 1:
            w = np.maximum(w, self.__wl)
            w = np.minimum(w, self.__wu)

            sim.simxSetJointTargetVelocity(self.__clientID, self.__motor1, -w[0], sim.simx_opmode_streaming)
            sim.simxSetJointTargetVelocity(self.__clientID, self.__motor2, -w[1], sim.simx_opmode_streaming)
            sim.simxSetJointTargetVelocity(self.__clientID, self.__motor3, -w[2], sim.simx_opmode_streaming)
            sim.simxSetJointTargetVelocity(self.__clientID, self.__motor4, -w[3], sim.simx_opmode_streaming)

        else:
            print(Fore.RED + "[-] Conexion perdida (setJointVelocity)")
            raise RuntimeError("error")

    def getImage(self):
        if sim.simxGetConnectionId(self.__clientID) == 1:
            ret, resolution, img = sim.simxGetVisionSensorImage(self.__clientID, self.__camera, 0, sim.simx_opmode_oneshot_wait)
            img = np.array(img, dtype=np.uint8)
            img.resize([resolution[1], resolution[0], 3])

        else:
            print(Fore.RED + "[-] Conexion perdida (getImage)")
            raise RuntimeError("error")

        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        img = cv.flip(img, 0)
        return img

    def stopSimulation(self):
        sim.simxStopSimulation(self.__clientID, sim.simx_opmode_oneshot_wait)

