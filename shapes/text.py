# from .basic import Rect as _Rect, Text as _Text
# from ..functions import custom_default as _csdf
# from ..constants import Def as _Def, Align as _Al
# from ..colors import RGB as _RGB
# from ..pc_input.keyboard import Keyboard as _Keyboard
# from ..pc_input.mouse import Mouse as _Mouse
# from ..output.display import Screen as _Screen
# from ..output.pages import App as _App
# from pygame import font as _font
#
#
# class TextDisplay(_Rect):
#     def __init__(self, x=0, y=0, characters="", font=None, pt=None, color=None, x_mode=_Al.df(), y_mode=_Al.df(),
#                  x_offset=0, y_offset=0, width=None, height=None, string=None):
#         _Rect.__init__(self, x, y, x_mode, y_mode, x_offset, y_offset, width, height)
#         self.fontname = _csdf(font, _Def.font())
#         self.pt = _csdf(pt, _Def.pt())
#         self.font = _font.SysFont(self.fontname, self.pt)
#         self.color = _csdf(color, _Def.text_color())
#         self.last_string = str()
#         self.char_renders = list()
#         self.characters = dict()
#         for char in characters:
#             char = str(char)
#             self.characters[char] = self.font.render(char, True, self.color)
#         if string is not None:
#             self.set_text(string)
#
#     def update_font(self):
#         self.font = _font.SysFont(self.fontname, self.pt)
#         for char in self.characters:
#             self.characters[char] = self.font.render(char, True, self.color)
#
#     def update_text(self):
#         width, height = 0, self.font.get_height()
#         self.char_renders = list()
#         for char in self.last_string:
#             if char not in self.characters:
#                 char = str(char)
#                 self.characters[char] = self.font.render(char, True, self.color)
#             render = self.characters[char]
#             self.char_renders.append((render, width, char))
#             width += render.get_width()
#
#         if width != self.width or height != self.height:
#             if self.x_mode == _Al.middle():
#                 self.x += (self.width - width) / 2
#             elif self.x_mode == _Al.right():
#                 self.x += (self.width - width)
#             if self.y_mode == _Al.middle():
#                 self.y += (self.height - height) / 2
#             elif self.y_mode == _Al.below():
#                 self.y += (self.height - height)
#             self.set_size(width, height)
#
#     def set_text(self, string):
#         string = str(string)
#         if string != self.last_string:
#             self.last_string = string
#             TextDisplay.update_text(self)
#
#     def set_font(self, font):
#         self.fontname = font
#         self.update_font()
#         self.update_text()
#
#     def set_pt(self, pt):
#         self.pt = pt
#         self.update_font()
#         self.update_text()
#
#     def set_color(self, color):
#         self.color = color
#         self.update_font()
#         for i in range(0, len(self.char_renders)):
#             render = self.char_renders[i]
#             char = render[2]
#             self.char_renders[i] = (self.characters[char], render[1], char)
#
#     def display(self):
#         for char in self.char_renders:
#             _Screen.blit(self.x + char[1], self.y, char[0])
#
#
# class TextBox(_Rect):
#     def __init__(self, content, x=0, y=0, font=None, pt=None, color=None, width=None, x_mode=_Al.df(), y_mode=_Al.df(),
#                  x_offset=0, y_offset=0, distribute=_Al.text_left()):
#         _Rect.__init__(self, x, y, x_mode, y_mode, x_offset, y_offset, width, 0)
#         self.content = content.split()
#         self.color = _csdf(color, _Def.text_color())
#         self.fontname = _csdf(font, _Def.font())
#         self.pt = _csdf(pt, _Def.pt())
#         self.font = _font.SysFont(self.fontname, self.pt)
#         self.distribute = distribute
#         self.renders = list(_Text(word, font=self.fontname, pt=self.pt, color=self.color) for word in self.content)
#         self.lines = list()
#         self.space_width = self.font.render(" ", False, (0, 0, 0)).get_width()
#         self.last_width = 0
#
#         self.update_pos()
#
#     def divide_text(self):
#         self.lines = list()
#         line = list()
#         width = 0
#         for word in self.renders:
#             if width + word.width < self.width:
#                 line.append(word)
#                 width += word.width + self.space_width
#             elif width + word.width == self.width or len(line) == 0 and word.width > self.width:
#                 line.append(word)
#                 self.lines.append(line)
#                 line = list()
#                 width = 0
#             else:
#                 self.lines.append(line)
#                 line = [word]
#                 width = word.width + self.space_width
#
#         if self.lines[-1:] != line:
#             self.lines.append(line)
#
#     def outline_text(self):
#         height = 0
#         line_height = self.font.get_height()
#         for line in self.lines:
#             for word in line:
#                 word.set_y(self.y + height)
#             height += line_height
#         self.set_height(height)
#
#         if self.distribute == _Al.text_left():
#             for line in self.lines:
#                 width = 0
#                 for word in line:
#                     word.set_x(self.x + width)
#                     width += word.width + self.space_width
#         elif self.distribute == _Al.text_right():
#             for line in self.lines:
#                 width = 0
#                 for word in reversed(line):
#                     width -= word.width + self.space_width
#                     word.set_x(self.x2 + width)
#         elif self.distribute == _Al.text_fill():
#             for line in self.lines:
#                 width = 0
#                 if line == self.lines[-1] or len(line) == 1:
#                     for word in line:
#                         word.set_x(self.x + width)
#                         width += word.width + self.space_width
#                 else:
#                     space_width = (self.width - sum(word.width for word in line)) / (len(line) - 1)
#                     for word in line:
#                         word.set_x(self.x + width)
#                         width += word.width + space_width
#
#     def update_font(self):
#         self.font = _font.SysFont(self.fontname, self.pt)
#         self.space_width = self.font.render(" ", False, (0, 0, 0)).get_width()
#         for line in self.lines:
#             for word in line:
#                 word.fontname = self.fontname
#                 word.pt = self.pt
#                 word.update_font()
#
#     def set_font(self, font, x_start=0, y_start=0, total_width=None, total_height=None):
#         self.fontname = font
#         self.update_font()
#         self.divide_text()
#         self.outline_text()
#         self.update_pos(x_start, y_start, total_width, total_height)
#
#     def set_pt(self, pt, x_start=0, y_start=0, total_width=None, total_height=None):
#         self.pt = pt
#         self.update_font()
#         self.divide_text()
#         self.outline_text()
#         self.update_pos(x_start, y_start, total_width, total_height)
#
#     def set_color(self, color):
#         self.color = color
#         for line in self.lines:
#             for word in line:
#                 word.set_color(color)
#
#     def update_pos(self, x_start=0, y_start=0, total_width=None, total_height=None):
#         _Rect.update_pos(self, x_start, y_start, total_width, total_height)
#         if self.last_width != self.width:
#             self.last_width = self.width
#             self.divide_text()
#             self.outline_text()
#             _Rect.update_pos(self, x_start, y_start, total_width, total_height)
#
#     def display(self):
#         for line in self.lines:
#             for word in line:
#                 word.display()
#
#
# class TextInput(_Text):
#     def __init__(self, content="", x=0, y=0, x_mode=_Al.df(), y_mode=_Al.df(), x_offset=0, y_offset=0, font=None,
#                  pt=None, color=None, selected_color=_RGB(255, 255, 0, 100), selected=False):
#         self.selected = selected
#         self.selected_color = selected_color
#         _Text.__init__(self, content, x, y, x_mode, y_mode, x_offset, y_offset, font, pt, color)
#
#     def keyboard_input(self):
#         last_pressed = _Keyboard.get_last()
#         if last_pressed is not None:
#             press_time = last_pressed.get_pressed_time()
#             if last_pressed.is_char():
#                 if last_pressed.get_press_down():
#                     self.set_text(self.content + last_pressed.get_char())
#                 elif press_time > _App.get_tick() / 2 and press_time % round(_App.get_tick() / 20) == 0:
#                     self.set_text(self.content + last_pressed.get_char())
#             elif last_pressed.get_type() == 8:
#                 if last_pressed.get_press_down():
#                     self.set_text(self.content[:-1])
#                 elif press_time > _App.get_tick() / 2 and press_time % round(_App.get_tick() / 20) == 0:
#                     self.set_text(self.content[:-1])
#
#     def mouse_interact(self):
#         if _Mouse.get_pressed():
#             if _Mouse.in_box(self.x, self.x2, self.y, self.y2):
#                 self.selected = True
#             else:
#                 self.selected = False
#
#     def display(self):
#         if self.selected:
#             _Screen.rect(self.x, self.y, self.width, self.height, self.selected_color)
#         _Text.display(self)
#
#     def functions(self):
#         _Text.functions(self)
#         self.mouse_interact()
#         if self.selected:
#             self.keyboard_input()
