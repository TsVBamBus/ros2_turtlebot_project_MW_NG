import cv2

kamera = cv2.VideoCapture(0)

if not kamera.isOpened():
	print("Kamera konnte nicht geöffnet werden")
	raise SystemExit(1)
ok, bild = kamera.read()
kamera.release()

if not ok:
	print("Kein Bild bekommen")
	raise SystemExit(1)
print("Bildgröße (Höhe, Breite, Farbkanöle:", bild.shape)
cv2.imwrite("testbild.jpg", bild)
print("Bild gespeichert als testbild.jpg")
