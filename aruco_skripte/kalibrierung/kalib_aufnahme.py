import cv2

PUNKTE_X = 8
PUNKTE_Y = 6

kamera = cv2.VideoCapture(0)
kamera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
kamera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

for i in range(10):
    kamera.read()

nummer = 17
print("Enter = Foto aufnehmen, q und Enter = beenden")

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
    gefunden, ecken = cv2.findChessboardCornersSB(grau, (PUNKTE_X, PUNKTE_Y))
    if not gefunden:
        print("Schachbrett NICHT gefunden, nicht gespeichert")
        continue

    dateiname = f"calib_{nummer:02d}.png"
    cv2.imwrite(dateiname, bild)
    print("Gespeichert:", dateiname, "Größe:", bild.shape)
    nummer += 1

kamera.release()