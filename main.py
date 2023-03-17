# Type help("robodk.robolink") or help("robodk.robomath") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/robodk.html
# Note: It is not required to keep a copy of this file, your Python script is saved with your RDK project
import time
import visiontest
from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

# Link to RoboDK
# RDK = Robolink()


# Program example:
time.sleep(2)
print('height',visiontest.height)# visiontest.heigt ya esta convertido a cm

time.sleep(2)
if visiontest.height <= 26.0:
    RDK.RunCode('final_ch',True)
    print("Rutina zapato: ",visiontest.height)
elif 26<visiontest.height<=28:
    RDK.RunCode('final',True)
else:
    RDK.RunCode('final_gr',True)






