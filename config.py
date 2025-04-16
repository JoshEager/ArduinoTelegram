
"""

Configurations for the telegraph app. 

"""

# The amount of time between serial prints and buzzes in ms for the arduino firmware
# More or less the refresh rate of the arduino. 1000 / ARDUINO_REFRESH_DELAY gives the 
# Number of refreshes per second. 
ARDUINO_REFRESH_DELAY = 20 # ms

# Corresponds to how long of a message you can send. 
# 2^TRANSMISSION_BYTES / (1000 / ARDUINO_REFRESH_DELAY) yeilds the amount of seconds of 
# buzzing that can be sent continuosly.  
TRANSMISSION_BYTES = 16 

# The port that the arduino is connected on. 
SERIAL_PORT = "COM3"

BAUDRATE = 115200

# Address of the relay
REMOTE_HOST = "telegram.moddedminecraft.uk"
REMOTE_PORT = 25555
