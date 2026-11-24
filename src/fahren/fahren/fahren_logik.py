from fahren.laengs_regler import LaengsRegler
from fahren.quer_regler import QuerRegler
from fahren.wenden_logik import WendenLogik


class FahrenLogik:
    
    def __init__(self):
        self.v_soll = 0.0             
        self.d_soll = 0.5             
        self.marker_id = -1            
        self.abstand_ist = 0.0          

        # TODO: Startwerte, am Roboter einstellen
        self.quer = QuerRegler(kp=1.5, omega_max=1.0)
        self.wenden = WendenLogik(k=1.5, omega_max=1.5, toleranz=0.03)
        self.laengs_fahren = LaengsRegler(kp=0.5, ki=0.0)     # P
        self.laengs_folgen = LaengsRegler(kp=0.6, ki=0.09)    # PI

    def setze_geschwindigkeit(self, v: float):
        return

    def setze_abstand(self, d: float):
        return
    
    def setze_orientierung(self, x: float, y: float, z: float, w: float):
        return
    
    def marker_empfangen(self, id: int, erkannt: bool, abstand: float, winkel: float):
        return

    def starte_fahren(self, marker_id: int, abstand_ziel: float):
        return

    def fahrbefehl(self):
        return

    def fahren_fertig(self):
        return

    def starte_folgen(self, marker_id: int):
        return

    def folgebefehl(self):
        return
    
    def starte_wenden(self, winkel: float):
        return

    def wendebefehl(self):
        return

    def restwinkel(self):
        return

    def wenden_fertig(self):
        return
