# Ergebnis der Roboter-Erkennung
uint8 SEITE_HINTEN=0
uint8 SEITE_VORNE=1

std_msgs/Header header
bool erkannt
int32 marker_id
uint8 seite             # SEITE_HINTEN =  Heck, SEITE_VORNE = seine Front
float32 abstand         # [m]
bool steht
float32 geschwindigkeit # geschaetzte Geschwindigkeit des anderen [m/s]