# ----------------------------------------------------------------------------- #
#                                                                               #  
#   Project:            Drive to Location (Known Starting Position)             #
#   Module:             main.py                                                 #    
#   Author:             VEX                                                     #
#   Created:            Fri Aug 05 2022                                         #
#	Description:        This example will show how to use a GPS Sensor to       #
#                       navigate a V5 Moby Hero Bot to the center of a field by #
#                       driving along the X-axis then the Y-axis                #
#   Starting Position:  Bottom Right Corner - Facing West                       #
#                                                                               #                                                                          
#   Configuration:      V5 Hero Bot (Drivetrain 2-motor, Inertial)              #
#                       Motor Group on Port 2 and 9                             #
#                       Rotation on Port 4                                      #
#                       GPS on Port 8                                           #
#                       Distance on Port 12                                     #
#                       Optical on Port 19                                      #
#                       Distance on Port 20                                     #
#                       Bumper on 3-Wire Port A                                 #
#                                                                               #                                                                          
# ----------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_drive_smart = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_drive_smart = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
drivetrain_inertial = Inertial(Ports.PORT3)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_inertial, 319.19, 320, 40, MM, 1)
ForkMotorGroup_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
ForkMotorGroup_motor_b = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
ForkMotorGroup = MotorGroup(ForkMotorGroup_motor_a, ForkMotorGroup_motor_b)
rotation_4 = Rotation(Ports.PORT4, False)
gps_8 = Gps(Ports.PORT8, 0.00, -240.00, MM, 180)
DistanceLeft = Distance(Ports.PORT12)
DistanceRight = Distance(Ports.PORT20)
optical_19 = Optical(Ports.PORT19)
bumper_a = Bumper(brain.three_wire_port.a)


def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    drivetrain_inertial.calibrate()
    while drivetrain_inertial.is_calibrating():
        sleep(25, MSEC)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)


def print_position():
    # Print GPS position values to the V5 Brain
    brain.screen.print("X: ", gps_8.x_position(MM))
    brain.screen.print("  Y: ", gps_8.y_position(MM))
    brain.screen.next_row()

# Calibrate the Drivetrain for accurate turns
calibrate_drivetrain()

# Calibrate the GPS Sensor
gps_8.calibrate()
while gps_8.is_calibrating():
    sleep(25, MSEC)

# Set the approximate starting position of the robot
# This helps the GPS sensor know its starting position
# if it is too close to the field walls to get an accurate initial reading
gps_8.set_location(56, -45, INCHES, 270, DEGREES)

# Print the starting position of the robot
print_position()

drivetrain.drive(FORWARD)

# Keep driving until the GPS's x_position passes 0 (horizontal center)
while not gps_8.x_position(MM) < 0:
    sleep(5, MSEC)
drivetrain.stop()

drivetrain.turn_to_heading(90, DEGREES, wait=True)
drivetrain.drive(FORWARD)

# Keep driving until the GPS's y_position passes 0 (vertical center)
while not gps_8.y_position(MM) > 0:
    sleep(5, MSEC)
drivetrain.stop()

# Print the ending position of the robot
print_position()
