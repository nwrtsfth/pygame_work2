# def _cmyk_to_rgb(c, m, y, k):
#     r = 255 * (1 - c / 100) * (1 - k / 100)
#     g = 255 * (1 - m / 100) * (1 - k / 100)
#     b = 255 * (1 - y / 100) * (1 - k / 100)
#     return r, g, b
#
#
# def _rgb_to_cmyk(r, g, b):
#     r /= 255
#     g /= 255
#     b /= 255
#     k = 1 - max(r, g, b)
#     c = (1 - r - k) / (1 - k)
#     m = (1 - g - k) / (1 - k)
#     y = (1 - b - k) / (1 - k)
#     return c, m, y, k
#
#
# def _in_range(number, low_range, high_range):
#     if number <= low_range:
#         return low_range
#     elif number >= high_range:
#         return high_range
#     return number
#
#
# def _in_cmyk(number):
#     return _in_range(number, 0, 100)
#
#
# class RGB:
#     __defaults = {"red": (255, 0, 0, 255),
#                   "green": (0, 255, 0, 255),
#                   "blue": (0, 0, 255, 255),
#                   "yellow": (255, 255, 0, 255),
#                   "magenta": (255, 0, 255, 255),
#                   "cyan": (0, 255, 255, 255),
#                   "black": (0, 0, 0, 255),
#                   "white": (255, 255, 255, 255)}
#
#     @staticmethod
#     def _in_rgb(number):
#         return _in_range(number, 0, 255)
#
#     def __init__(self, r=int, g=int, b=int, a=255):
#         self.__r = RGB._in_rgb(r)
#         self.__g = RGB._in_rgb(g)
#         self.__b = RGB._in_rgb(b)
#         self.__a = RGB._in_rgb(a)
#         self.__color = self.__r, self.__g, self.__b, self.__a
#
#     def _update_color(self):
#         self.__color = self.__r, self.__g, self.__b, self.__a
#
#     def set_r(self, new):
#         self.__r = RGB._in_rgb(new)
#         self._update_color()
#
#     def set_g(self, new):
#         self.__g = RGB._in_rgb(new)
#         self._update_color()
#
#     def set_b(self, new):
#         self.__b = RGB._in_rgb(new)
#         self._update_color()
#
#     def set_a(self, new):
#         self.__a = RGB._in_rgb(new)
#         self._update_color()
#
#     def get_r(self):
#         return self.__r
#
#     def get_g(self):
#         return self.__g
#
#     def get_b(self):
#         return self.__b
#
#     def get_a(self):
#         return self.__a
#
#     def change(self, offset):
#         self.__r = RGB._in_rgb(self.__r + offset)
#         self.__g = RGB._in_rgb(self.__g + offset)
#         self.__b = RGB._in_rgb(self.__b + offset)
#         self._update_color()
#
#     def light(self, offset=30):
#         self.change(offset)
#
#     def dark(self, offset=10):
#         self.change(-offset)
#
#     def new_change(self, offset):
#         color = RGB(*self)
#         color.change(offset)
#         return color
#
#     def new_light(self, offset=30):
#         return self.new_change(offset)
#
#     def new_dark(self, offset=10):
#         return self.new_change(-offset)
#
#     def to_cmyk(self):
#          return CMYK(*_rgb_to_cmyk(self.__r, self.__g, self.__b))
#
#     def __contains__(self, item):
#         return item in self.__color
#
#     def __getitem__(self, item):
#         return self.__color[item]
#
#     def __setitem__(self, key, color):
#         if key == 0:
#             self.set_r(color)
#         elif key == 1:
#             self.set_g(color)
#         elif key == 2:
#             self.set_b(color)
#         elif key == 3:
#             self.set_a(color)
#         else:
#             raise IndexError
#
#     def __len__(self):
#         return 4
#
#     def __str__(self):
#         return "({}, {}, {}, {})".format(self.__r, self.__g, self.__b, self.__a)
#
#     def __repr__(self):
#         return self.__str__()
#
#     def __iter__(self):
#         self.__index = 0
#         return self
#
#     def __next__(self):
#         if self.__index < 4:
#             color = self.__color[self.__index]
#             self.__index += 1
#             return color
#         else:
#             raise StopIteration
#
#     def __eq__(self, other):
#         return self.__color == other
#
#     def __ne__(self, other):
#         return self.__color != other
#
#     @classmethod
#     def from_cmyk(cls, *cmyk):
#         if type(cmyk[0]) is CMYK:
#             return cmyk[0].to_rgb()
#         return cls(*_cmyk_to_rgb(*cmyk))
#
#     @classmethod
#     def default(cls, color):
#         return cls(*RGB.__defaults[color])
#
#
# class CMYK:
#     def __init__(self, c, m, y, k):
#         self.__c = _in_cmyk(c)
#         self.__m = _in_cmyk(m)
#         self.__y = _in_cmyk(y)
#         self.__k = _in_cmyk(k)
#
#         self.__color = self.__c, self.__m, self.__y, self.__k
#
#     def _update_color(self):
#         self.__color = self.__c, self.__m, self.__y, self.__k
#
#     def light(self, offset=10):
#         self.__k = _in_cmyk(self.__k + offset)
#         self._update_color()
#
#     def dark(self, offset=10):
#         self.__k = _in_cmyk(self.__k - offset)
#         self._update_color()
#
#     def to_rgb(self):
#         return RGB(*_cmyk_to_rgb(self.__c, self.__m, self.__y, self.__k))
#
#     @classmethod
#     def from_rgb(cls, *rgb):
#         if type(rgb[0]) is RGB:
#             return rgb[0].to_cmyk()
#         return cls(*_rgb_to_cmyk(*rgb))
