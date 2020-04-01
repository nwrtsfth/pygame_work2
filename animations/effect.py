from ..shapes.basic import Point as _Point


class Move:
    def __init__(self, shape, destination, duration):
        self.shape = shape
        self.destination = destination
        self.duration = duration

        self.dx = (self.destination.x - self.shape.x) / self.duration
        self.dy = (self.destination.y - self.shape.y) / self.duration

    def set_speed(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def update(self):
        self.shape.move(self.dx, self.dy)
        self.duration -= 1
        return self.duration == 0

    @staticmethod
    def from_speed(shape, dx, dy, duration):
        x = shape.x + dx * duration
        y = shape.y + dy * duration
        effect = Move(shape, _Point(x, y), duration)
        effect.set_speed(dx, dy)
        return effect


class Resize:
    def __init__(self, shape, size, duration):
        self.shape = shape
        self.size = size
        self.duration = duration

        self.d_width = (self.size[0] - self.shape.width) / self.duration
        self.d_height = (self.size[1] - self.shape.height) / self.duration

    def set_speed(self, d_width, d_height):
        self.d_width = d_width
        self.d_height = d_height

    def update(self):
        self.shape.move_size(self.d_width, self.d_height)
        self.duration -= 1
        return self.duration == 0

    @staticmethod
    def from_speed(shape, d_width, d_height, duration):
        width = shape.width + d_width * duration
        height = shape.height + d_height * duration
        effect = Resize(shape, (width, height), duration)
        effect.set_speed(d_width, d_height)
        return effect


class ColorTransition:
    def __init__(self, shape, color, duration):
        self.shape = shape
        self.color = color
        self.duration = duration

        self.dr = (self.color.r - self.shape.color.r) / self.duration
        self.dg = (self.color.g - self.shape.color.g) / self.duration
        self.db = (self.color.b - self.shape.color.b) / self.duration

    def set_speed(self, dr, dg, db):
        self.dr = dr
        self.dg = dg
        self.db = db

    def update(self):
        self.shape.color.r += int(self.dr)
        self.shape.color.g += int(self.dg)
        self.shape.color.b += int(self.db)
        self.duration -= 1
        return self.duration == 0


class Rotate:
    def __init__(self, shape, angle, duration):
        self.shape = shape
        self.angle = angle
        self.duration = duration

        self.d_angle = self.angle / self.duration

    def set_speed(self, d_angle):
        self.d_angle = d_angle

    def update(self):
        self.shape.rotate(self.d_angle)
        self.duration -= 1
        return self.duration == 0


class Accelerate:
    def __init__(self, shape, x_distance, y_distance, duration):
        self.shape = shape
        self.x_distance = x_distance
        self.y_distance = y_distance
        self.duration = duration
        self.dx = 0
        self.dy = 0
        maxdx = 2 * self.x_distance / (self.duration + 0.4 * self.duration)
        maxdy = 2 * self.y_distance / (self.duration + 0.4 * self.duration)
        self.ax = maxdx / (0.3 * self.duration)
        self.ay = maxdy / (0.3 * self.duration)
        self.timer = 0

    def update(self):
        if self.timer < 0.3 * self.duration:
            self.dx += self.ax
            self.dy += self.ay
        elif self.timer >= 0.7 * self.duration:
            self.dx -= self.ax
            self.dy -= self.ay
        self.shape.move(self.dx, self.dy)
        self.timer += 1

        return self.timer == self.duration
