import math

import cv2
import numpy as np

MARKER_GROESSEN = {
    0: 0.172,
    1: 0.067,
    2: 0.195,
    3: 0.032,
    4: 0.114,
    69: 0.075,
}


class ArucoErkennung:
    def __init__(self, kalibrierdatei="kamera_kalibrierung.npz"):
        daten = np.load(kalibrierdatei)
        self.kameramatrix = daten["kamera_matrix"]
        self.verzerrung = daten["verzerrung"]

        if hasattr(cv2.aruco, "ArucoDetector"):
            self.neue_version = True
            dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)
            parameter = cv2.aruco.DetectorParameters()
            parameter.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
            self.detektor = cv2.aruco.ArucoDetector(dictionary, parameter)
        else:
            self.neue_version = False
            self.dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_100)
            self.parameter = cv2.aruco.DetectorParameters_create()
            self.parameter.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX

        self.kamera = cv2.VideoCapture(0)
        self.kamera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.kamera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def suche_marker(self, grau):
        if self.neue_version:
            ecken, ids, abgelehnt = self.detektor.detectMarkers(grau)
        else:
            ecken, ids, abgelehnt = cv2.aruco.detectMarkers(
                grau, self.dictionary, parameters=self.parameter)
        return ecken, ids

    def objektpunkte(self, groesse):
        h = groesse / 2
        return np.array([[-h,  h, 0],
                         [ h,  h, 0],
                         [ h, -h, 0],
                         [-h, -h, 0]], dtype=np.float32)

    def erkenne(self):
        ok, bild = self.kamera.read()
        if not ok:
            return None

        ergebnisse = []
        grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
        ecken, ids = self.suche_marker(grau)
        if ids is None:
            return ergebnisse

        for i in range(len(ids)):
            marker_id = int(ids[i][0])
            if marker_id not in MARKER_GROESSEN:
                continue

            ok, rvec, tvec = cv2.solvePnP(
                self.objektpunkte(MARKER_GROESSEN[marker_id]),
                ecken[i][0], self.kameramatrix, self.verzerrung,
                flags=cv2.SOLVEPNP_IPPE_SQUARE)
            if not ok:
                continue

            x, y, z = tvec.flatten()
            ergebnisse.append({
                "id": marker_id,
                "tiefe": float(z),
                "abstand": float(math.sqrt(x * x + y * y + z * z)),
                "winkel": math.degrees(math.atan2(x, z)),
            })
        return ergebnisse

    def schliessen(self):
        self.kamera.release()


if __name__ == "__main__":
    erkennung = ArucoErkennung()
    print("Auflösung:",
          erkennung.kamera.get(cv2.CAP_PROP_FRAME_WIDTH),
          erkennung.kamera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    for i in range(10):
        ergebnisse = erkennung.erkenne()
    erkennung.schliessen()

    if ergebnisse is None:
        print("Kein Bild bekommen")
    elif len(ergebnisse) == 0:
        print("Marker NICHT erkannt")
    else:
        for m in ergebnisse:
            print(f"ID {m['id']}: Abstand {m['abstand'] * 100:.1f} cm, "
                  f"Tiefe {m['tiefe'] * 100:.1f} cm, Winkel {m['winkel']:.1f} Grad")