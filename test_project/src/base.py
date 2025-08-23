from globals import brain
import time


class Vec2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float):
        return Vec2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float):
        return Vec2D(self.x / scalar, self.y / scalar)

    def __str__(self):
        return "%s, %s" % (self.x, self.y)


class Box:
    def __init__(self, p1: Vec2D, p2: Vec2D):
        self.p1 = p1
        self.p2 = p2

    @staticmethod
    def from_topleft(x1, y1, w, h):
        return Box(Vec2D(x1, y1), Vec2D(x1 + w, y1 + h))

    def contains(self, point: Vec2D) -> bool:
        return self.p1.x <= point.x <= self.p2.x and self.p1.y <= point.y <= self.p2.y

    @property
    def x1(self):
        return self.p1.x

    @property
    def y1(self):
        return self.p1.y

    @property
    def x2(self):
        return self.p2.x

    @property
    def y2(self):
        return self.p2.y

    @property
    def width(self):
        return self.p2.x - self.p1.x

    @property
    def height(self):
        return self.p2.y - self.p1.y

    def __str__(self):
        return "from %s to %s" % (self.p1, self.p2)


class Component:
    def __init__(self):
        self.bbox = Box(Vec2D(0, 0), Vec2D(0, 0))
        self._spacing = 0

    def pressed(self, pos: Vec2D):
        # handle press logic
        ...

    def update_bbox(self, bbox: Box):
        self.bbox = Box(
            p1=bbox.p1 + Vec2D(self._spacing, self._spacing),
            p2=bbox.p2 - Vec2D(self._spacing, self._spacing),
        )

    def draw(self): ...

    def spacing(self, n: int):
        self._spacing = n
        return self

    def on_click(self, callback):
        def pressed(pos: Vec2D):
            self.pressed(pos)
            callback(pos)

        self.pressed = pressed


def run(comp: Component):
    brain.screen.render()

    def pressed_callback():
        pos = Vec2D(brain.screen.x_position(), brain.screen.y_position())
        comp.pressed(pos)

    brain.screen.pressed(pressed_callback)
    bbox = Box.from_topleft(0, 0, 480, 272 - 40)
    comp.update_bbox(bbox)
    while True:
        brain.screen.clear_screen()
        comp.draw()
        brain.screen.render()
        time.sleep(0.01)
