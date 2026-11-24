import glob

import cv2
import numpy as np

PUNKTE_X = 8
PUNKTE_Y = 6
QUADRAT = 0.02125

objektpunkte = np.zeros((PUNKTE_X * PUNKTE_Y, 3), np.float32)
objektpunkte[:, :2] = np.mgrid[0:PUNKTE_X, 0:PUNKTE_Y].T.reshape(-1, 2) * QUADRAT

alle_objektpunkte = []
alle_ecken = []

for datei in sorted(glob.glob("calib_*.png")):
    grau = cv2.imread(datei, cv2.IMREAD_GRAYSCALE)
    gefunden, ecken = cv2.findChessboardCornersSB(grau, (PUNKTE_X, PUNKTE_Y))
    if gefunden:
        alle_objektpunkte.append(objektpunkte)
        alle_ecken.append(ecken)

print(len(alle_ecken), "Bilder verwendet")

fehler, kamera_matrix, verzerrung, rvecs, tvecs = cv2.calibrateCamera(
    alle_objektpunkte, alle_ecken, grau.shape[::-1], None, None)

print("Fehler (Pixel):", fehler)
print(kamera_matrix)
np.savez("kamera_kalibrierung.npz", kamera_matrix=kamera_matrix, verzerrung=verzerrung)