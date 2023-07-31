# Beto <--> Edna <--> Ian

import socket
import cv2 as cv
import base64
import numpy as np
from cam import arucoDisplay, cr2xy

arucoDict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_100)
arucoParams = cv.aruco.DetectorParameters()
detector = cv.aruco.ArucoDetector(arucoDict, arucoParams)

addr = ('0.0.0.0', 9000)
chunk = 4194304

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(addr)

msg, addr = sock.recvfrom(chunk)
print(msg, addr)

while True:
    frame = sock.recvfrom(chunk)[0]
    frame = base64.b64decode(frame)
    frame = np.frombuffer(frame, dtype=np.uint8)
    frame = cv.imdecode(frame, -1)

    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
    corners, ids, rejected = cv.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
    frame, c, r, theta = arucoDisplay(corners, ids, rejected, frame)
    cv.imshow('esp32cam', frame)
    print(f"x: {c}\ty: {r}\ttheta:{theta}")

    if cv.waitKey(1) == 27:
        sock.sendto(b'end', addr)
        break
    else:
        sock.sendto(b'ok', addr)

sock.close()
cv.destroyAllWindows()

