from system.zustand import Zustand

class SystemLogik:

    def __init__(self, id_rohr_hinten: int, id_rohr_vorne: int,
                 id_robot_hinten: int, id_robot_vorne: int,
                 timeout: float = 0.5):
        self.zustand = Zustand.INIT

        self.id_rohr_hinten = id_rohr_hinten
        self.id_rohr_vorne = id_rohr_vorne
        self.id_robot_hinten = id_robot_hinten
        self.id_robot_vorne = id_robot_vorne

        self.rohr_hinten_erkannt = False
        self.rohr_vorne_erkannt = False
        self.robot_hinten_erkannt = False
        self.robot_vorne_erkannt = False

        self.timeout = timeout          
        self.letzter_befehl = 0.0       

    def marker_empfangen(self, id: int, erkannt: bool, abstand: float):
        return

    def wenden_fertig(self):
        return

    def fahren_fertig(self):
        return

    def naechster_zustand(self):
        return

    def befehl_erlaubt(self, zeit: float):
        return

    def watchdog_ausgeloest(self, zeit: float):
        return
