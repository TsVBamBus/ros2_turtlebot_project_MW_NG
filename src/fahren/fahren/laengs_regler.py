class LaengsRegler:
    
    def __init__(self, kp: float, ki: float, v_max: float = 0.2, sollabstand: float = 0.0):
        self.ki = ki                    # [1/s²]
        self.kp = kp                    # [1/s]
        self.v_max = v_max              # [m/s]
        self.sollabstand = sollabstand  # [m]

    def berechne_v(self, abstand: float, sollabstand: float, v_max: float, dt: float):
        return
