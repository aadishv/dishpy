from base import Component, Vec2D, Box
from vex import Color
from globals import brain


class Text(Component):
    def __init__(self, text: str, color: Color = Color.WHITE, centered=False):
        super().__init__()
        self.text = text
        self.color = color
        self.centered = centered

    def pressed(self, pos: Vec2D):
        self.text = "Pressed at %s, %s" % (pos.x, pos.y)

    def draw(self):
        if self.centered:
            x = self.bbox.x1 + self.bbox.width / 2 - brain.screen.get_string_width(self.text) / 2
            y = self.bbox.y1 + self.bbox.height / 2
        else:
            x = self.bbox.x1
            y = self.bbox.y1
        brain.screen.set_pen_color(self.color)
        brain.screen.print_at(self.text, x=x, y=y, opaque=False)


class HStack(Component):
    def __init__(self, splits: list[float] | None = None, *components: Component, adjust: bool = True):
        super().__init__()
        self.components = components
        if splits is None:
            splits = [1] * len(components)
        sum_splits = sum(splits)
        if not adjust:
            sum_splits = 1
        self.splits = [i / sum_splits for i in splits]

    def _component_at_x(self, x_pos: float):
        x = self.bbox.x1
        i = 0
        while i < len(self.components):
            width = self.bbox.width * self.splits[i]
            if x <= x_pos < x + width:
                return i, self.components[i], x, width
            x += width
            i += 1
        return None, None, None, None

    def pressed(self, pos: Vec2D):
        idx, comp, x, width = self._component_at_x(pos.x)
        if comp is not None:
            comp.pressed(pos - Vec2D(x, self.bbox.y1))

    def update_bbox(self, bbox: Box):
        super().update_bbox(bbox)
        x = bbox.x1
        i = 0
        while i < len(self.components):
            comp = self.components[i]
            width = bbox.width * self.splits[i]
            comp.update_bbox(Box.from_topleft(x, bbox.y1, width, bbox.height))
            x += width
            i += 1

    def draw(self):
        for comp in self.components:
            comp.draw()


class VStack(Component):
    def __init__(self, splits: list[float] | None = None, *components: Component, adjust: bool = True):
        super().__init__()
        self.components = components
        if splits is None:
            splits = [1] * len(components)
        sum_splits = sum(splits)
        if not adjust:
            sum_splits = 1
        self.splits = [i / sum_splits for i in splits]

    def _component_at_y(self, y_pos: float):
        y = self.bbox.y1
        i = 0
        while i < len(self.components):
            height = self.bbox.height * self.splits[i]
            if y <= y_pos < y + height:
                return i, self.components[i], y, height
            y += height
            i += 1
        return None, None, None, None

    def pressed(self, pos: Vec2D):
        idx, comp, y, height = self._component_at_y(pos.y)
        if comp is not None:
            comp.pressed(pos)

    def update_bbox(self, bbox: Box):
        super().update_bbox(bbox)
        y = bbox.y1
        i = 0
        while i < len(self.components):
            comp = self.components[i]
            height = bbox.height * self.splits[i]
            b = Box.from_topleft(bbox.x1, y, bbox.width, height)
            comp.update_bbox(b)
            y += height
            i += 1

    def draw(self):
        for comp in self.components:
            comp.draw()


class Rectangle(Component):
    def __init__(self, color: Color, radius: int = 20, border: int = 5):
        super().__init__()
        self.color = color
        self.radius = radius
        self.border_color = Color.WHITE
        self.border = border

    def update_bbox(self, bbox: Box):
        super().update_bbox(bbox)
        # self.bbox.p1.y -= 18
        # self.bbox.p2.y -= 18 * 3

    def draw(self):
        # MARK: - fill
        brain.screen.set_pen_color(self.color)
        brain.screen.draw_rectangle(
            self.bbox.x1 + self.radius, self.bbox.y1, self.bbox.width - self.radius * 2, self.bbox.height - 2, self.color
        )
        brain.screen.draw_rectangle(
            self.bbox.x1, self.bbox.y1 + self.radius, self.bbox.width - 1, self.bbox.height - self.radius * 2, self.color
        )
        xs = [self.bbox.x1 + self.radius, self.bbox.x2 - self.radius]
        ys = [self.bbox.y1 + self.radius, self.bbox.y2 - self.radius]
        for x in xs:
            for y in ys:
                brain.screen.draw_circle(x, y, self.radius, self.color)

        # MARK: - border
        if self.border <= 0:
            return
        brain.screen.set_pen_color(self.border_color)
        brain.screen.set_pen_width(self.border)
        for x in xs:
            for y in ys:
                if x == xs[0]:
                    x_clip = self.bbox.x1
                else:
                    x_clip = self.bbox.x2 - self.radius
                if y == ys[0]:
                    y_clip = self.bbox.y1
                else:
                    y_clip = self.bbox.y2 - self.radius
                brain.screen.set_clip_region(x_clip - 2, y_clip - 2, self.radius + 4, self.radius + 4)
                brain.screen.draw_circle(x, y, self.radius, Color.TRANSPARENT)
        brain.screen.set_clip_region(0, 0, 480, 272)
        brain.screen.set_pen_width(self.border + 2)
        brain.screen.draw_line(self.bbox.x1 + self.radius, self.bbox.y1, self.bbox.x2 - self.radius, self.bbox.y1)
        brain.screen.draw_line(self.bbox.x1 + self.radius, self.bbox.y2, self.bbox.x2 - self.radius, self.bbox.y2)
        brain.screen.draw_line(self.bbox.x1, self.bbox.y1 + self.radius, self.bbox.x1, self.bbox.y2 - self.radius)
        brain.screen.draw_line(self.bbox.x2, self.bbox.y1 + self.radius, self.bbox.x2, self.bbox.y2 - self.radius)


class Button(Component):
    def __init__(self, text: str, callback):
        super().__init__()
        self.text = Text(text, centered=True)
        self.rectangle = Rectangle(Color.BLUE).spacing(5)
        self.callback = callback

    def pressed(self, pos: Vec2D):
        print("pressed slay")
        self.callback(pos)

    def update_bbox(self, bbox: Box):
        super().update_bbox(bbox)
        self.text.update_bbox(self.bbox)
        self.rectangle.update_bbox(self.bbox)

    def draw(self):
        self.rectangle.draw()
        self.text.draw()
