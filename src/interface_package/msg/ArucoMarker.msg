# Zustand aller bekannten ArUco-Marker in einem Kamerabild
# gegebenfalls mehr als ein Marker im Bild 
# 5 ist die vorläufige länge des Arrays ==> 5 Marker im Projekt --> muss angepasst werden


std_msgs/Header header
bool[5] sichtbare_id
float32[5] abstand
float32[5] winkel