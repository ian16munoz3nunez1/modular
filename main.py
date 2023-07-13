import cv2 as cv
import numpy as np

def arucoDisplay(corners, ids, rejected, image):
    x = None
    y = None
    theta = None

    if len(corners) > 0:
        ids = ids.flatten()

        (topLeft, topRight, bottomRight, bottomLeft) = corners[0][0][:4]

        topLeft = (int(topLeft[0]), int(topLeft[1]))
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))

        cv.line(image, topLeft, topRight, (0, 255, 255), 2)
        cv.line(image, topRight, bottomRight, (0, 255, 255), 2)
        cv.line(image, bottomRight, bottomLeft, (0, 255, 255), 2)
        cv.line(image, bottomLeft, topLeft, (0, 255, 255), 2)

        x = int((topLeft[0]+bottomRight[0])/2.0)
        y = int((topLeft[1]+bottomRight[1])/2.0)
        try:
            # theta = -np.arctan( (topRight[1]-topLeft[1])/(topRight[0]-topLeft[0]) ) * (180/np.pi)
            theta = -np.arctan2( (topRight[1]-topLeft[1]), (topRight[0]-topLeft[0]) ) * (180/np.pi)
        except:
            pass
        cv.circle(image, (x, y), 4, (0, 255, 0), -1)

        cv.putText(image, str(ids[0]), (topLeft[0],topLeft[1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image, x, y, theta

def cr2xy(imagen, c, r, m_x, m_y):
    x = None
    y = None
    if c is not None and r is not None:
        R, C = imagen.shape[:2]

        x = -m_x * ((C-2*c)/C)
        y = m_y * ((R-2*r)/R)

    return x, y

arucoDict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_100)
arucoParams = cv.aruco.DetectorParameters()
detector = cv.aruco.ArucoDetector(arucoDict, arucoParams)

# x: 64cm
# y: 46cm
m_x = 32
m_y = 23

captura = cv.VideoCapture(2)

while True:
    leido, video = captura.read()

    if not leido:
        break

    if cv.waitKey(1) == 27:
        break

    corners, ids, rejected = cv.aruco.detectMarkers(video, arucoDict, parameters=arucoParams)
    video, c, r, theta = arucoDisplay(corners, ids, rejected, video)

    x, y = cr2xy(video, c, r, m_x, m_y)
    print(f"x: {x}\ty: {y}\ttheta: {theta}")

    cv.imshow('Video', video)

captura.release()
cv.destroyAllWindows()

