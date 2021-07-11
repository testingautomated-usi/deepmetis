# Getting the angles from the file
from os.path import join
SIKULIX_SCRIPT_FOLDER = "sikulix_scripts"

SIKULIX_SCRIPT_NAME_W_FMT = "unityeyes.sikuli"

SIKULIX_ANGLES_FILE_NAME = "angles.txt"

dst = join(SIKULIX_SCRIPT_FOLDER, SIKULIX_SCRIPT_NAME_W_FMT, SIKULIX_ANGLES_FILE_NAME)
with open(dst) as f:
    content = [i.strip() for i in f.readlines()]
    cam_angles = content[0]
    cam_angles = cam_angles.split(',')
    eye_angles = content[1]
    eye_angles = eye_angles.split(',')
    c_pitch = cam_angles[0]
    c_yaw = cam_angles[1]
    e_pitch = eye_angles[0]
    e_yaw = eye_angles[1]

#exit()
# Starting Unity eyes
doubleClick("1600262945133.png")
wait(3)

# Proceed
click("1589285287698.png")
wait(6)

# Input camera angles
cam_input = str(c_pitch)+","+str(c_yaw)+",0,0"
click("1600267084050.png")
type(cam_input)

# Input eye agnles
eye_input = str(e_pitch)+","+str(e_yaw)+",0,0"
click("1600267045790.png")
type(eye_input)


# Start generating images
click("1600266941410.png")
wait(5)

# Stop generating images
click("1600267101911.png")
#wait(0.5)
