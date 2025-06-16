# ----------------------------------------------------------------------------- #
#                                                                               #
# 	Project:        Limit / Bumper Sensing                                      #
#   Module:         main.py                                                     #
#   Author:         VEX                                                         #
#   Created:        Fri Aug 05 2022                                             #
#	Description:    This example will show all of the available commands        #
#                   for using the Limit and Bumper Sensors                      #
#                                                                               #
#   Configuration:  V5 Speedbot (Drivetrain 2-motor, No Gyro)                   #
#                   + Limit Sensor                                              #
#                   + Bumper Sensor                                             #
#                   Limit Switch in 3-Wire Port A                               #
#                   Bumper in 3-Wire Port B                                     #
#                                                                               #
# ----------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_drive_smart = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_drive_smart = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
limit_switch_a = Limit(brain.three_wire_port.a)
bumper_b = Bumper(brain.three_wire_port.b)

# Begin project code

# Print all Inertial sensing values to the screen in an infinite loop
while True:
    # Clear the screen and set the cursor to top left corner on each loop
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)

    brain.screen.print("Limit Switch:", "True" if limit_switch_a.pressing() == 1 else "False")
    brain.screen.next_row()

    brain.screen.print("Bumper:", "True" if bumper_b.pressing() == 1 else "False")
    brain.screen.next_row()

    # A brief delay to allow text to be printed without distortion or tearing
    wait(50,MSEC)
