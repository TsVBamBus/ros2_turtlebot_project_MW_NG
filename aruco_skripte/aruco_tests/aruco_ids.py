import cv2

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
detektor = cv2.aruco.ArucoDetector(dictionary, cv2.aruco.DetectorParameters())

kamera = cv2.VideoCapture(0)
kamera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
kamera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
for i in range(10):
    kamera.read()

print("Marker vor die Kamera halten, Enter = suchen, q und Enter = beenden")

while True:
    eingabe = input()
    if eingabe == "q":
        break

    for i in range(10):
        ok, bild = kamera.read()
    if not ok:
        print("Kein Bild bekommen")
        continue

    grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
    ecken, ids, abgelehnt = detektor.detectMarkers(grau)
    if ids is None:
        print("Kein Marker erkannt")
    else:
        print("IDs:", ids.flatten())

kamera.release()