from psychopy import visual, core, event
import DoorPlay
import helpers
from psychopy.iohub import launchHubServer
import runConfigDialog
#import pyautogui
from instructionsScreen import show_instructions
import LoggerSetup
import VAS

io = launchHubServer()

log = LoggerSetup.set_up_logger()
configDialogBank = runConfigDialog.user_input_play()

params = {
    'subjectID': configDialogBank[0],
    'practiceTrials': configDialogBank[1],  # Number if Practice Trials, taken from Config Dialog
    'numOfScreensTask1': configDialogBank[2],  # Number of Screens in the 1st task, either 49 (7*7) or 36 (6*6)
    'numOfScreensTask2': configDialogBank[3],  # Number of Screens in the 2nd task, either 49 (7*7) or 36 (6*6)
    'startingDistance': configDialogBank[4],  # Decide whether the starting distance is random, or fixed on 50
    'fullScreen': configDialogBank[5],
    'keyboardMode': configDialogBank[6],
    'joystickSensitivity': configDialogBank[7],
    'screenSize': (1024, 768),  # Get Screen Resolution to match Full Screen
    'recordPhysio': configDialogBank[8],
    # 'portAddress': int("0xE050", 16)
}

# Initialize Screen
window = visual.Window(params['screenSize'], monitor="testMonitor", color="black", winType='pyglet',
                       fullscr=True if params['fullScreen'] else False, units="pix")
image = visual.ImageStim(win=window, image="./img/ITI_fixation.jpg", units="norm", opacity=1,
                         size=(2,2) if not params['fullScreen'] else None)
image.draw()
window.update()
helpers.wait_for_space(window)

# Initialize DataFrame

# Initialize Sensors

# Run VAS
VAS.beginning_vas(window, params)

# Show Instructions
show_instructions(window, params, image)

# Practice run

# Task 1
DoorPlay.run_task(window, params, 1, 0, io)

# Mid-VAS
VAS.middle_vas(window, params, 0)

# Task 2
DoorPlay.run_task(window, params, 2, 0, io)

# Final VAS
VAS.final_vas(window, params)

# Recap

core.quit()