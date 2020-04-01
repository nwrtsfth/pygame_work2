from .basic import SurfaceRect as _SurfaceRect, Rectangle as _Rectangle, Circle as _Circle, Polygon as _Polygon
from .collection import Group as _Group
from ..pc_input.mouse import Mouse as _Mouse
from pygame import Color as _Color


class AbstractButton:
    none = -1
    default = 0
    hover = 1
    click = 2

    def __init__(self, func, parameters):
        self.function = func
        self.parameters = parameters
        self.mouse_hover = False
        self.mouse_click = False
        self.state_change = AbstractButton.default

    def _update_state(self):
        pass

    def point_collide(self, point=_Mouse):
        pass

    def execute(self):
        if self.function is not None:
            if self.parameters is not None:
                return self.function(*self.parameters)
            return self.function()

    def execute_pressed(self):
        pass

    def mouse_states(self, point=_Mouse):
        self.state_change = AbstractButton.none
        if self.point_collide(point):
            if not self.mouse_hover:
                self.mouse_hover = True
                self.state_change = AbstractButton.hover
            if _Mouse.left.get_press_down():
                self.mouse_click = True
                self.state_change = AbstractButton.click
            elif self.mouse_click:
                if _Mouse.left.get_press_up():
                    self.mouse_click = False
                    self.execute()
                    self.state_change = AbstractButton.hover
                else:
                    self.execute_pressed()
        elif self.mouse_hover:
            self.mouse_hover = False
            self.mouse_click = False
            self.state_change = AbstractButton.default
        self._update_state()
        return self.state_change != AbstractButton.none

    def loop_behavior(self):
        return self.mouse_states()


class SurfaceButton(AbstractButton, _SurfaceRect):
    def __init__(self, x, y, x_mode, y_mode, x_offset, y_offset, width, height, state_surfaces, func, parameters,
                 collide_function):
        _SurfaceRect.__init__(self, x, y, x_mode, y_mode, x_offset, y_offset, width, height)
        AbstractButton.__init__(self, func, parameters)
        self.state_surfaces = state_surfaces
        self.collide_function = collide_function
        self._update_state()

    def _update_state(self):
        if self.state_change != -1:
            try:
                _SurfaceRect.set_surface(self, self.state_surfaces[self.state_change])
            except IndexError:
                pass

    def mouse_collide(self):
        return self.collide_function(self)


class RectButton(AbstractButton, _Rectangle):
    def __init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset, color, func, parameters):
        _Rectangle.__init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset, color)
        AbstractButton.__init__(self, func, parameters)
        self.default_color = self.color
        self.hover_color = self.default_color + _Color(40, 40, 40, 0)
        self.click_color = self.default_color - _Color(30, 30, 30, 0)
        self._update_state()

    def _update_state(self):
        if self.state_change == 0:
            self.color = self.default_color
        elif self.state_change == 1:
            self.color = self.hover_color
        elif self.state_change == 2:
            self.color = self.click_color

    def point_collide(self, point=_Mouse):
        return self.collide_point(_Mouse)

    def set_color(self, color, update_hover_click=True):
        self.default_color = color
        if update_hover_click:
            self.hover_color = self.default_color + _Color(40, 40, 40, 0)
            self.click_color = self.default_color - _Color(30, 30, 30, 0)
        if self.mouse_click:
            self.color = self.click_color
        elif self.mouse_hover:
            self.color = self.hover_color
        else:
            self.color = self.default_color


class CircleButton(RectButton, _Circle):
    def __init__(self, x, y, radius, x_mode, y_mode, x_offset, y_offset, color, func, parameters):
        _Circle.__init__(self, x, y, radius, x_mode, y_mode, x_offset, y_offset, color)
        RectButton.__init__(self, x, y, radius * 2, radius * 2, x_mode, y_mode, x_offset, y_offset, color, func,
                            parameters)

    def draw(self, surface):
        _Circle.draw(self, surface)

    def point_collide(self, point=_Mouse):
        return self.collide_point(_Mouse)


class PolygonButton(RectButton, _Polygon):
    def __init__(self, x, y, points, x_mode, y_mode, x_offset, y_offset, color, func, parameters):
        _Polygon.__init__(self, x, y, points, x_mode, y_mode, x_offset, y_offset, color)
        RectButton.__init__(self, x, y, self.width, self.height, x_mode, y_mode, x_offset, y_offset, color, func,
                            parameters)

    def draw(self, surface):
        _Polygon.draw(self, surface)

    def point_collide(self, point=_Mouse):
        return self.collide_point(_Mouse)


class GroupButton(AbstractButton, _Group):
    def __init__(self, x, y, x_mode, y_mode, x_offset, y_offset, shapes, width, height, func, parameters):
        _Group.__init__(self, x, y, x_mode, y_mode, x_offset, y_offset, shapes, width, height)
        AbstractButton.__init__(self, func, parameters)
        self.base_shape = self.shapes[0]

    def point_collide(self, point=_Mouse):
        return self.base_shape.collide_point(_Mouse)


# def rect_text_button(x, y, width, height, x_mode, y_mode, x_offset, y_offset, text_list, pt, font, color, func,
#                      parameters):
#     light_color = color + _Color(30, 30, 30, 0)
#     dark_color = color - _Color(30, 30, 30, 0)
#     df_rect = Rectangle(0, 0, width, height, 0, 0, 0, 0, color)
#     hv_rect = Rectangle(0, 0, width, height, 0, 0, 0, 0, light_color)
#     c1_rect = Rectangle(0, 0, width, height, 0, 0, 0, 0, dark_color)
#
#     t1 = Text(0, 0, Layout.middle, Layout.middle, 0, 0, pt, font, text_list)
#
#     df_group = Group(0, 0, 0, 0, 0, 0, [df_rect, t1], 0, 0)
#     hv_group = Group(0, 0, 0, 0, 0, 0, [hv_rect, t1], 0, 0)
#     cl_group = Group(0, 0, 0, 0, 0, 0, [c1_rect, t1], 0, 0)
#
#     return SurfaceButton(x, y, x_mode, y_mode, x_offset, y_offset, width, height, [df_group, hv_group, cl_group],
#                          func, parameters, _Mouse.in_rect)
