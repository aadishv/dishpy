# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       {file}                                                       #
# 	Author:       {author}                                                     #
# 	Created:      {date}                                                       #
# 	Description:  {description}                                                #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

brain = Brain()

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place driver control in this while loop
    while True:
        wait(20, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()