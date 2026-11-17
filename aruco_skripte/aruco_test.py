import cv2

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
parameter = cv2.aruco.DetectorParameters()
detektor = cv2.aruco.ArucoDetector(dictionary, parameter)

kamera = cv2.VideoCapture(0)
for i in range(10):
	ok, bild = kamera.read()
kamera.release()

if not ok:
	print("kein bild bekommen")
	raise SystemExit(1)

grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)

ecken, ids, abgelehnt = detektor.detectMarkers(grau)

if ids is None:
	print("Marker NICHT erkannt")
else:
	print("Marker erkannt, ID:", ids.flatten())
	cv2.aruco.drawDetectedMarkers(bild, ecken, ids)

cv2.imwrite("ergebnis.jpg", bild)
print("Bild gespeichert als ergebnis.jpg")
