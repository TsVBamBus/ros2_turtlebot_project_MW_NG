class QuerRegler:

    def __init__(self, kp: float, omega_max: float):
        self.kp = kp                    
        self.omega_max = omega_max      
        self.auslenkwinkel = 0.0        
        self.sollkurs = 0.0             

    def berechne_auslenkung(self, winkel: float):
        return

    def sollkurs_setzen(self, sollkurs: float):
        return

    def berechne_rot(self):
        return
