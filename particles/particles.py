from ..shapes.basic import Point as _Point
from pygame import draw as _draw, Color as _Color


class Particle(_Point):
    def __init__(self, x, y, dx=0, dy=0, ax=0, ay=0, max_dx=100, max_dy=100, color=_Color(0, 0, 0), size=5):
        _Point.__init__(self, x, y)
        self.dx = dx
        self.dy = dy
        self.ax = ax
        self.ay = ay
        self.max_dx = abs(max_dx)
        self.max_dy = abs(max_dy)
        self.color = color
        self.size = size

    def accelerate_x(self, ax):
        self.dx += ax
        if self.dx > self.max_dx:
            self.dx = self.max_dx
        elif self.dx < -self.max_dx:
            self.dx = -self.max_dx

    def accelerate_y(self, ay):
        self.dy += ay
        if self.dy > self.max_dy:
            self.dy = self.max_dy
        elif self.dy < -self.max_dy:
            self.dy = -self.max_dy

    def accelerate(self, ax, ay):
        self.accelerate_x(ax)
        self.accelerate_y(ay)

    def update_move(self):
        self.accelerate(self.ax, self.ay)
        self.dx *= 0.99
        self.dy *= 0.99
        self.move(self.dx, self.dy)

    def update_in_box(self, x1, y1, x2, y2):
        if self.x <= x1:
            self.dx *= -1
            self.x = x1
        elif self.x + self.size >= x2:
            self.dx *= -1
            self.x = x2 - self.size

        if self.y <= y1:
            self.dy *= -1
            self.y = y1
        elif self.y + self.size >= y2:
            self.dy *= -1
            self.y = y2 - self.size

    def update_in_ground(self, y):
        if self.y + self.size >= y:
            self.dy *= -1
            self.y = y - self.size

    def dead(self):
        return self.size <= 0

    def draw(self, surface):
        _draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))


class Spark(Particle):
    def __init__(self, x=0, y=0, dx=0, dy=0, ax=0, ay=0, color=_Color(0, 0, 0), size=5, lifespan=5):
        Particle.__init__(self, x, y, dx, dy, ax, ay, color=color, size=size)
        self.lifespan = lifespan

    def update_lifespan(self):
        if self.lifespan - 0.05 >= 0:
            self.lifespan -= 0.05
        else:
            self.lifespan = 0

    def update_color(self):
        pass

    def update_size(self):
        if self.lifespan > 1:
            if self.size - 0.01 >= 0:
                self.size -= 0.01
            else:
                self.size = 0
        else:
            if self.size - 0.1 >= 0:
                self.size -= 0.1
            else:
                self.size = 0

    def update_appearance(self):
        self.update_color()
        self.update_size()

    def update_life(self):
        self.update_lifespan()
        self.update_appearance()

    def dead(self):
        return self.size <= 0 or self.lifespan <= 0 or self.color == (0, 0, 0)
