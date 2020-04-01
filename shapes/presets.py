from .basic import Polygon as _Polygon


def rhombus(x, y, width, height, x_mode, y_mode, x_offset, y_offset, color):
    points = ((width / 2, 0), (width, height / 2), (width / 2, height), (0, height / 2))
    return _Polygon(x, y, points, x_mode, y_mode, x_offset, y_offset, color)


def plus(x, y, x_length, y_length, x_width, y_width, x_mode, y_mode, x_offset, y_offset, color):
    x1 = x_length / 2 - x_width / 2
    x2 = x_length / 2 + x_width / 2
    y1 = y_length / 2 - y_width / 2
    y2 = y_length / 2 + y_width / 2

    points = ((x1, 0), (x2, 0), (x2, y1), (x_length, y1), (x_length, y2), (x2, y2), (x2, y_length), (x1, y_length),
              (x1, y2), (0, y2), (0, y1), (x1, y1))

    return _Polygon(x, y, points, x_mode, y_mode, x_offset, y_offset, color)


def regular_polygon(x, y, diameter, vertices, x_mode, y_mode, x_offset, y_offset, color):
    pass
