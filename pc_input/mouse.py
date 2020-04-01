from pygame import mouse as _mouse, Color as _Color, draw as _draw
from ..game_math import Collision as _Collision
from .key import Button as _Button
from ..shapes.basic import Point as _Point


class _MouseObject(_Point):
    def __init__(self, x, y):
        _Point.__init__(self, x, y)
        self.left = _Button(1)
        self.middle = _Button(2)
        self.right = _Button(3)
        self.moving = True
        self.visible = True
        self.scroll = 0

        self.dx = 0
        self.dy = 0

        self.__key_binds_down = dict()
        self.__key_binds_up = dict()
        self.__key_binds_pressed = dict()

    def set_x(self, x):
        _Point.set_x(self, x)
        _mouse.set_pos(self.x, self.y)

    def set_y(self, y):
        _Point.set_y(self, y)
        _mouse.set_pos(self.x, self.y)

    def set_pos(self, x, y):
        _Point.set_pos(self, x, y)
        _mouse.set_pos(self.x, self.y)

    def set_visible(self, visible):
        self.visible = visible
        _mouse.set_visible(visible)

    def update_pos(self):
        mouse_x, mouse_y = _mouse.get_pos()
        if mouse_x != self.x or mouse_y != self.y:
            self.moving = True
            self.dx = mouse_x - self.x
            self.dy = mouse_y - self.y
            self.x = mouse_x
            self.y = mouse_y
        else:
            self.moving = False
            self.dx = 0
            self.dy = 0

    def in_rect(self, rect):
        return _Collision.rect_point(rect, self)

    def in_circle(self, circle):
        return _Collision.circle_point(circle, self)

    def in_polygon(self, polygon):
        return _Collision.polygon_point(polygon, self)

    def update_buttons(self):
        self.left.update()
        self.right.update()
        self.middle.update()
        self.scroll = 0

        if self.left.get_pressed() and self.left.get_type() in self.__key_binds_pressed:
            self.__key_binds_pressed[self.left.get_type()]()
        if self.right.get_pressed() and self.right.get_type() in self.__key_binds_pressed:
            self.__key_binds_pressed[self.right.get_type()]()
        if self.middle.get_pressed() and self.middle.get_type() in self.__key_binds_pressed:
            self.__key_binds_pressed[self.middle.get_type()]()

    def reset_buttons(self):
        self.left.reset()
        self.right.reset()
        self.middle.reset()

    def update_button_up(self, index=1):
        if index == 1:
            self.left.set_press_up()
        elif index == 2:
            self.middle.set_press_up()
        elif index == 3:
            self.right.set_press_up()

        if index in self.__key_binds_up:
            self.__key_binds_up[index]()

    def update_button_down(self, index=1):
        if index == 1:
            self.left.set_press_down()
        elif index == 2:
            self.middle.set_press_down()
        elif index == 3:
            self.right.set_press_down()
        elif index == 4:
            self.scroll = -1
        elif index == 5:
            self.scroll = 1

        if index in self.__key_binds_down:
            self.__key_binds_down[index]()

    def update(self):
        self.update_pos()
        self.update_buttons()

    def draw(self, surface):
        _draw.circle(surface, _Color(0, 0, 0), (self.x, self.y), 5, 2)

    def get_scroll(self):
        return self.scroll == 1 or self.scroll == -1

    def set_key_bind_down(self, func, index):
        self.__key_binds_down[index] = func

    def set_key_bind_up(self, func, index):
        self.__key_binds_up[index] = func

    def set_key_bind_pressed(self, func, index):
        self.__key_binds_pressed[index] = func

    def set_key_bind_scroll(self, func):
        self.set_key_bind_down(func, 4)
        self.set_key_bind_down(func, 5)

    def key_bind_down(self, index):
        def wrapper(func):
            self.set_key_bind_down(func, index)
            return func
        return wrapper

    def key_bind_up(self, index):
        def wrapper(func):
            self.set_key_bind_up(func, index)
            return func
        return wrapper

    def key_bind_pressed(self, index):
        def wrapper(func):
            self.set_key_bind_pressed(func, index)
            return func
        return wrapper

    def key_bind_scroll(self):
        def wrapper(func):
            self.set_key_bind_scroll(func)
            return func
        return wrapper


Mouse = _MouseObject(0, 0)
