import math
import numpy as np
import cv2

MARKER_GROESSE = 0.075
BRENNWEITE = 615.0

kameramatrix = np.array([[BRENNWEITE, 0, 320],
                         [0, BRENNWEITE, 240],
                         [0, 0, 1]], dtype=np.float32)
verzerrung = np.zeros((5, 1), dtype=np.float32)

h = MARKER_GROESSE / 2
objektpunkte = np.array([[-h,  h, 0],
                         [ h,  h, 0],
                         [ h, -h, 0],
                         [-h, -h, 0]], dtype=np.float32)

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
parameter = cv2.aruco.DetectorParameters()
parameter.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
detektor = cv2.aruco.ArucoDetector(dictionary, parameter)

kamera = cv2.VideoCapture(0)
for i in range(10):
    ok, bild = kamera.read()
kamera.release()

if not ok:
    print("Kein Bild bekommen")
    raise SystemExit(1)

grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
ecken, ids, abgelehnt = detektor.detectMarkers(grau)

if ids is None:
    print("Marker NICHT erkannt")
else:
    for i in range(len(ids)):
        ok, rvec, tvec = cv2.solvePnP(
            objektpunkte, ecken[i][0], kameramatrix, verzerrung,
            flags=cv2.SOLVEPNP_IPPE_SQUARE)
        x, y, z = tvec.flatten()
        abstand = math.sqrt(x * x + y * y + z * z)
        winkel = math.degrees(math.atan2(x, z))
        print(f"ID {ids[i][0]}: Abstand {abstand * 100:.1f} cm, Winkel {winkel:.1f} Grad")