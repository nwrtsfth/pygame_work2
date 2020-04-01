from pygame import Color as _Color, image as _image


class Layout:
    default = 0
    left = 1
    right = 2
    middle = 3
    above = 4
    below = 5
    fill = 6

    text_left = 7
    text_right = 8
    text_fill = 9

    bold = 0
    italic = 1
    underline = 2


class Default:
    pt = 30
    font = "Arial"
    text_color = _Color(0, 0, 0)
    bold = False
    italic = False
    underline = False

    rect_width = 120
    rect_height = 50
    circle_radius = 50

    shape_color1 = _Color(50, 170, 230)
    shape_color2 = _Color(160, 50, 100)
    shape_color3 = _Color(160, 160, 160)

    background_color = _Color(250, 250, 250)

    ticks = 60


class _FileLoader:
    def __init__(self):
        self.__loaded = dict()

    def load(self, name, path):
        self.__loaded[name] = path

    def get(self, name):
        return open(self.__loaded[name], 'rb')

    def __setitem__(self, key, value):
        self.load(key, value)

    def __getitem__(self, item):
        return self.get(item)


class _ImageLoader(_FileLoader):
    def get(self, name):
        _image.load(self.__loaded[name]).convert()


Fonts = _FileLoader()
Images = _FileLoader()
Sounds = _FileLoader()
Colors = {"red": _Color(255, 0, 0),
          "green": _Color(0, 255, 0),
          "blue": _Color(0, 0, 255),
          "yellow": _Color(255, 255, 0),
          "magenta": _Color(255, 0, 255),
          "cyan": _Color(0, 255, 255),
          "white": _Color(255, 255, 255),
          "black": _Color(0, 0, 0)
          }
