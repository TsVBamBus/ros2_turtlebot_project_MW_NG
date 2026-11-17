# Zustand aller bekannten ArUco-Marker in einem Kamerabild
# gegebenfalls mehr als ein Marker im Bild 
# 5 ist die vorläufige länge des Arrays ==> 5 Marker im Projekt --> muss angepasst werden

# Bedeutung der IDs
uint8 ROHRENDE_A=0
uint8 ROHRENDE_B=1

std_msgs/Header header
bool[5] sichtbar
float32[5] abstand              # [m], inf wenn nicht sichtbar
geometry_msgs/Pose[5] pose      # Pose im Kamera-Frame, nur gueltig wenn sichtbar