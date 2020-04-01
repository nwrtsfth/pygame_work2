from .basic import Rectangle as _Rectangle, Text as _Text, Line as _Line, LineRect as _LineRect
from .collection import Group as _Group
from .button import AbstractButton as _AbstractButton, CircleButton as _CircleButton, RectButton as _RectButton
from ..constants import Layout as _Layout
from ..pc_input.mouse import Mouse as _Mouse
from ..game_math import Collision as _Collision
from pygame import Color as _Color, draw as _draw


class AbstractSlider(_AbstractButton):
    def __init__(self, val_range, default_value, rounding):
        _AbstractButton.__init__(self, None, None)
        self.min_value = val_range[0]
        self.max_value = val_range[1]
        self.default_value = default_value
        self.rounding = rounding
        self.value = default_value
        self.value_change = True

    def set_value(self, value):
        if value != self.value:
            if value < self.min_value:
                value = self.min_value
            elif value > self.max_value:
                value = self.max_value

            if self.rounding > 0:
                self.value = round(value, self.rounding)
            else:
                self.value = int(value)
            self.value_change = True

    def reset_value(self):
        self.set_value(self.default_value)


class Slider(_Group, AbstractSlider):
    def __init__(self, x, y, x_mode, y_mode, x_offset, y_offset, total_width, total_height, slider_width, slider_height,
                 header_color, header_font, header_pt, header_text, slider_color, slider_button_color,
                 slider_line_color, value_color, value_font, value_pt, value_text, val_range, default_value, rounding):

        h_height = total_height - slider_height
        v_width = total_width - slider_width
        line_y = h_height + slider_height / 2

        self.header = _Rectangle(0, 0, total_width, h_height, 0, 0, 0, 0, header_color)
        self.slider = _Rectangle(0, h_height, slider_width, slider_height, 0, 0, 0, 0, slider_color)
        self.value_rect = _Rectangle(slider_width, h_height, v_width, slider_height, 0, 0, 0, 0, value_color)
        self.header_text = _Text(10, 0, 0, _Layout.middle, 0, 0, header_pt, header_font, header_text)
        self.value_text = _Text(0, 0, _Layout.middle, _Layout.middle, 0, 0, value_pt, value_font, value_text)
        self.line = _Line(0.1 * slider_width, line_y, 0.8 * slider_width, 0, 0, 0, 0, 0, 5, slider_line_color)
        self.circle = _CircleButton(0, line_y - 10, 10, 0, 0, 0, 0, slider_button_color, None, None)

        AbstractSlider.__init__(self, val_range, default_value, rounding)
        _Group.__init__(self, x, y, x_mode, y_mode, x_offset, y_offset, [self.header, self.slider, self.value_rect,
                        self.line, self.circle, self.value_text, self.header_text], 0, 0)

        self.set_value(self.default_value / 1)
        self.update_slider()
        self._update_display_number()
        self.header_text.update_allignment_in_rect(self.header)

    def _update_state(self):
        if self.state_change == 0:
            self.circle.color = self.circle.default_color
        elif self.state_change == 1:
            self.circle.color = self.circle.hover_color
        elif self.state_change == 2:
            self.circle.color = self.circle.click_color

    def _update_shape_allignment(self):
        pass

    def _update_display_number(self):
        self.value_text.set_content(str(self.value), 0)
        self.value_text.update_allignment_in_rect(self.value_rect)
        self._update_draw()

    def move_slider(self):
        if _Mouse.x < self.line.x:
            self.circle.set_x(self.line.x - self.circle.radius)
            self.set_value(self.min_value)
        elif _Mouse.x > self.line.x2:
            self.circle.set_x(self.line.x2 - self.circle.radius)
            self.set_value(self.max_value)
        else:
            self.circle.set_x(_Mouse.x - self.circle.radius)
            self.update_value()

    def set_value(self, value):
        AbstractSlider.set_value(self, value)
        self.update_slider()

    def update_value(self):
        percentage = (self.circle.xm - self.line.x) / self.line.width
        self.set_value(self.min_value + percentage * (self.max_value - self.min_value))
        self._update_display_number()

    def update_slider(self):
        percentage = (self.value - self.min_value) / (self.max_value - self.min_value)
        self.circle.set_x(self.line.x + self.line.width * percentage - 10)
        self._update_display_number()

    def point_collide(self, point=_Mouse):
        return _Collision.rect_point(self, point)

    def loop_behavior(self):
        self.value_change = False
        update = self.mouse_states()
        if self.mouse_hover and self.mouse_click:
            self.move_slider()
            update = True
        if update:
            self._update_draw()

    @staticmethod
    def preset(x, y, x_mode, y_mode, x_offset, y_offset, total_width, total_height, average_color, header_str, pt, font,
               text_color, val_range, default_value, rounding):

        slider_width = total_width * 0.8
        slider_height = total_height * 0.5
        header_color = average_color + _Color(20, 20, 20, 0)
        slider_color = average_color - _Color(20, 20, 20, 0)
        value_color = average_color - _Color(50, 50, 50, 0)

        slider_button_color = _Color(150, 150, 150)
        slider_line_color = _Color(10, 10, 10)

        return Slider(x, y, x_mode, y_mode, x_offset, y_offset, total_width, total_height, slider_width, slider_height,
                      header_color, font, pt, [(header_str, text_color)], slider_color, slider_button_color,
                      slider_line_color, value_color, font, pt, [("", text_color)], val_range, default_value, rounding)


class AbstractCheckBox:
    def __init__(self, value1, value2, default_value, value_function, value_function_params):
        self.value1 = value1
        self.value2 = value2
        self.default_value = default_value
        self.value = default_value
        self.value_change = True
        self.value_function = value_function
        self.value_function_params = value_function_params

    def toggle_value(self):
        if self.value == self.value1:
            self.value = self.value2
        else:
            self.value = self.value1
        self.value_change = True
        if self.value_function is not None:
            if self.value_function_params is not None:
                self.value_function(self.value_function_params)
            else:
                self.value_function()


class CheckBox(_Group, AbstractCheckBox):
    def __init__(self, x, y, x_mode, y_mode, x_offset, y_offset, width, height, val1_color, val2_color, line_color,
                 line_width, font, pt, default_text, value_text, value1, value2, default_value, func, params):
        self.val1_color = val1_color
        self.val2_color = val2_color

        self.check_button = _RectButton(0, 0, width, height, 0, 0, 0, 0, val1_color, self.toggle_value,
                                        None)
        self.line_box = _LineRect(0, 0, width, height, 0, 0, 0, 0, line_color, line_width)
        self.text = _Text(width + 10, 0, 0, _Layout.middle, 0, 0, pt, font, [default_text, value_text])

        AbstractCheckBox.__init__(self, value1, value2, default_value, func, params)
        _Group.__init__(self, x, y, x_mode, y_mode, x_offset, y_offset, [self.check_button, self.line_box, self.text],
                        0, 0)
        self._update_text_box()
        self._update_draw()

    def _update_shape_allignment(self):
        pass

    def _update_text_box(self):
        self.text.set_content(str(self.value), 1)
        self.text.update_allignment_in_rect(self)
        self._update_size()

    def toggle_value(self):
        AbstractCheckBox.toggle_value(self)
        if self.check_button.default_color == self.val1_color:
            self.check_button.set_color(self.val2_color)
        else:
            self.check_button.set_color(self.val1_color)
        self._update_text_box()
        self._update_draw()

    def draw(self, surface):
        _Group.draw(self, surface)

    @staticmethod
    def preset(x, y, x_mode, y_mode, x_offset, y_offset, width, height, val1_color, val2_color, font, pt, def_str,
               text_color, value1, value2, func=None, params=None):
        return CheckBox(x, y, x_mode, y_mode, x_offset, y_offset, width, height, val1_color, val2_color,
                        _Color(0, 0, 0), 5,  font, pt, (def_str, text_color), ("", text_color), value1, value2, value1,
                        func, params)
