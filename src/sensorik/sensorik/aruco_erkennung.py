class ArucoErkennung:

    def __init__(self, timeout: float = 0.5):
        self.kamera = None              
        self.detektor = None            
        self.anzahl_marker = 0
        self.marker_groessen = {}      
        self.objekt_punkte = None       
        self.kamera_matrix = None       
        self.verzerrung = None          
        self.zuletzt_erkannt = 0.0      
        self.timeout = timeout          

    def erkenne(self, zeit: float):
        return
