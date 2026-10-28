"""Bahnberechnung fuer einen mobilen Roboter (ohne ROS2-Abhaengigkeiten).

 

Die Klasse berechnet aus der aktuellen Pose (x, y, theta) und einer
Zielposition (x, y) die Geschwindigkeitsbefehle (linear, angular), die ein
Differentialantrieb braucht, um das Ziel anzufahren.

 

Der ROS2-Teil (odom abonnieren, cmd_vel publizieren, Action-Server) wird
spaeter nur noch "drumherum" gebaut:
    - odom-Callback        -> setAktuellePos(x, y, theta)
    - Action-Goal          -> setZiel(x, y)
    - Timer / Schleife     -> bahn() aufrufen und Ergebnis per pubWeg() senden
    - cmd_vel-Publisher    -> als `publisher`-Funktion uebergeben
"""

 

import math
import numpy


 

def normalisiere_winkel(winkel):
    """Bringt einen Winkel in den Bereich (-pi, pi]."""
    while winkel > math.pi:
        winkel -= 2 * math.pi
    while winkel <= -math.pi:
        winkel += 2 * math.pi
    return winkel


 

class Bahnberechnung:
    """Berechnet Fahrbefehle zu einer Zielposition.

 

    Parameter
    ---------
    toleranz : float
        Abstand (m) zum Ziel, ab dem das Ziel als erreicht gilt.
    max_lin : float
        Maximale Vorwaertsgeschwindigkeit (m/s).
    max_rot : float
        Maximale Drehgeschwindigkeit (rad/s).
    k_lin, k_rot : float
        Proportionalfaktoren der Regelung.
    publisher : callable | None
        Funktion, die einen Fahrbefehl (vel, rot) entgegennimmt.
        In ROS2 wird hier spaeter das Befehlspublizieren (cmd_vel) angebunden.
    """

 

    def __init__(self, toleranz=0.05, max_lin=0.5, max_rot=1.0,
                 k_lin=0.5, k_rot=1.5, publisher=None):
        self.aktuelle_position = (0, 0)
        self.aktuelle_orientierung = 0.0  # theta in rad
        self.ziel_position = (0, 0)

 

        self.toleranz = toleranz
        self.max_lin = max_lin
        self.max_rot = max_rot
        self.k_lin = k_lin
        self.k_rot = k_rot
        self.ziel_orientierung = 0.0
        self.hat_ziel_orientierung = False
        self.winkel_toleranz = 0.05

 

        self.publisher = publisher
        self.letzter_weg = (0.0, 0.0)  # zuletzt "veroeffentlichter" Befehl

 

    # ------------------------------------------------------------------
    # Zugriff auf Zustand
    # ------------------------------------------------------------------
    def aktuellePos(self):
        """Gibt die aktuelle Position (x, y) zurueck."""
        return self.aktuelle_position

 

    def setAktuellePos(self, x, y, theta):
        """Setzt die aktuelle Pose (wird spaeter vom odom-Callback aufgerufen)."""
        self.aktuelle_position = (x, y)
        self.aktuelle_orientierung = theta

 

    def getZiel(self):
        """Gibt die Zielposition (x, y) zurueck."""
        return self.ziel_position

 

    def setZiel(self, x, y, theta=None):
        """Setzt die Zielposition."""
        self.ziel_position = (x, y)
        if theta is not None:
            self.ziel_orientierung = theta
            self.hat_ziel_orientierung = True
        else:
            self.hat_ziel_orientierung = False


    # ------------------------------------------------------------------
    # Geometrie
    # ------------------------------------------------------------------
    def abstand(self):
        """Euklidischer Abstand zwischen aktueller Position und Ziel."""
        dx = self.ziel_position[0] - self.aktuelle_position[0]
        dy = self.ziel_position[1] - self.aktuelle_position[1]
        return math.hypot(dx, dy)

    def position_erreicht(self):
        return self.abstand() <= self.toleranz

    def orientierung_erreicht(self):
        if not self.hat_ziel_orientierung:
            return True
        fehler = normalisiere_winkel(self.ziel_orientierung - self.aktuelle_orientierung)
        return abs(fehler) <= self.winkel_toleranz

    def ziel_erreicht(self):
        return self.position_erreicht() and self.orientierung_erreicht()   # mit Klammern!

    def winkel_zum_ziel(self):
        """Winkelfehler (rad) zwischen Blickrichtung und Ziel, in (-pi, pi].

 

        Positiv = Ziel liegt links, Roboter muss sich gegen den Uhrzeigersinn drehen.
        """
        dx = self.ziel_position[0] - self.aktuelle_position[0]
        dy = self.ziel_position[1] - self.aktuelle_position[1]
        winkel_ziel = math.atan2(dy, dx)
        return normalisiere_winkel(winkel_ziel - self.aktuelle_orientierung)


 

    # ------------------------------------------------------------------
    # Bahn
    # ------------------------------------------------------------------
    def bahn(self):
    # Phase 1: zur Position fahren
        if not self.position_erreicht():
            fehler = self.winkel_zum_ziel()
            rot = max(-self.max_rot, min(self.max_rot, self.k_rot * fehler))
            vel = min(self.max_lin, self.k_lin * self.abstand())
            vel *= max(0.0, math.cos(fehler))
            return (vel, rot)

    # Phase 2: auf Zielwinkel drehen
        if not self.orientierung_erreicht():
            fehler = normalisiere_winkel(self.ziel_orientierung - self.aktuelle_orientierung)
            rot = max(-self.max_rot, min(self.max_rot, self.k_rot * fehler))
            return (0.0, rot)

        return (0.0, 0.0)

 

    def pubWeg(self, weg):
        """Veroeffentlicht einen Fahrbefehl (vel, rot).

 

        Ohne ROS2 wird der Befehl gespeichert und - falls gesetzt - an die
        `publisher`-Funktion weitergereicht.
        """
        self.letzter_weg = weg
        if self.publisher is not None:
            self.publisher(weg)

 

    def stopp(self):
        """Haelt den Roboter an (fuer cancel / abort der Action)."""
        self.pubWeg((0.0, 0.0))
