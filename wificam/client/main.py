# Beto <--> Edna <--> Ian

import cv2 as cv 
from time import sleep
from cam import arucoDisplay, cr2xy

arucoDict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_100)
arucoParams = cv.aruco.DetectorParameters()
detector = cv.aruco.ArucoDetector(arucoDict, arucoParams)

url = "http://192.168.1.21:8080"
captura = cv.VideoCapture(url)

winName = 'esp32cam'
cv.namedWindow(winName, cv.WINDOW_AUTOSIZE)

while True:
    try:
        captura.open(url)
        leido, frame = captura.read()

        if not leido:
            break

        if cv.waitKey(1) == 27:
            break

        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
        corners, ids, rejected = cv.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
        frame, c, r, theta = arucoDisplay(corners, ids, rejected, frame)

        cv.imshow(winName, frame)
        print(f"x: {c}\ty: {r}\ttheta: {theta}")
        sleep(1/30)

    except Exception as e:
        print(e)
        break

captura.release()
cv.destroyAllWindows()
print("Fin de la conexion")

