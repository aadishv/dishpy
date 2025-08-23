# ---------------------------------------------------------------------------- #
#                                                                              #
#    Module:       main.py                                                       #
#    Author:       {author}                                                      #
#    Created:      {date}                                                        #
#    Description:  {description}                                                 #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import Color
from base import Component, Vec2D, run
from base_comps import HStack, VStack, Button
from globals import brain

autons = [
    {
        "name": "Auton 1",
        "color": "red",
    },
    {
        "name": "Auton 2",
        "color": "blue",
    },
    {
        "name": "Auton 3",
        "color": "red",
    },
    {
        "name": "Auton 4",
        "color": "blue",
    },
]
state = {"value": 0}

class Wrapper(Component):
    def __init__(self, i, state, autons):
        super().__init__()
        self.i = i
        self.state = state
        self.autons = autons

    def pressed(self, pos: Vec2D):
        self.state["value"] = self.i
        print("Auton ", self.autons[self.i]["name"], "pressed")

    def draw(self):
        btn = get_button(self.i, self.state, self.autons)
        btn.update_bbox(self.bbox)
        btn.draw()


def get_button(i, state, autons):
    btn = Button(
        autons[i]["name"], lambda _: None
    ).spacing(5)
    btn.rectangle.color = Color.RED if autons[i]["color"] == "red" else Color.BLUE
    btn.rectangle.border = 5 if state["value"] == i else 0
    return btn

red_indices = [i for i in range(len(autons)) if autons[i]["color"] == "red"]
blue_indices = [i for i in range(len(autons)) if autons[i]["color"] == "blue"]

run(
    VStack(
        [0.5, 0.5],
        HStack(
            [1] * len(red_indices),
            *[Wrapper(i, state, autons) for i in red_indices],
        ),
        HStack(
            [1] * len(blue_indices),
            *[Wrapper(i, state, autons) for i in blue_indices],
        )
    )
)
