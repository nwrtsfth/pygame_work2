from .basic import SurfaceRect, Rect as _Rect
from pygame import draw as _draw, SurfaceType as _SurfaceType, SRCALPHA as _SRCALPHA


class TransitionRect(SurfaceRect):
    def __init__(self, x, y, x_mode, y_mode, x_offset, y_offset, width, height, color1, color2, horizontal):
        SurfaceRect.__init__(self, x, y, x_mode, y_mode, x_offset, y_offset, width, height)
        self.color1 = color1
        self.color2 = color2
        self.horizontal = horizontal

        self._update_transition()

    def _update_transition(self):
        r, g, b = self.color1[0], self.color1[1], self.color1[2]
        if self.horizontal:
            length = self.width
        else:
            length = self.height
        dr = (self.color2[0] - r) / length
        dg = (self.color2[1] - g) / length
        db = (self.color2[2] - b) / length

        for i in range(0, length):
            if self.horizontal:
                _draw.rect(self, (r, g, b), (self.x + i, self.y, 1, self.height))
            else:
                _draw.rect(self, (r, g, b), (self.x, self.y + i, self.width, 1))
            r += dr
            g += dg
            b += db

    def _update_surface(self):
        _SurfaceType.__init__(self, (self.width, self.height), _SRCALPHA)
        self._update_transition()

    def move_width(self, d_width):
        _Rect.move_width(self, d_width)
        self._update_transition()

    def move_height(self, d_height):
        _Rect.move_height(self, d_height)
        self._update_transition()

    def move_size(self, d_width, d_height):
        _Rect.move_size(self, d_width, d_height)
        self._update_transition()

    def set_width(self, width):
        _Rect.set_width(self, width)
        self._update_surface()

    def set_height(self, height):
        _Rect.set_height(self, height)
        self._update_surface()

    def set_size(self, width, height):
        _Rect.set_width(self, width)
        _Rect.set_height(self, height)
        self._update_surface()

    def set_color1(self, color):
        if color != self.color1:
            self.color1 = color
            self._update_transition()

    def set_color2(self, color):
        if color != self.color2:
            self.color2 = color
            self._update_transition()
