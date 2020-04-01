from pygame import font as _font, transform as _transform, SurfaceType as _SurfaceType, Color as _Color, \
     SRCALPHA as _SRCALPHA, draw as _draw, image as _image, error as _error
from ..constants import Layout as _Layout, Default as _Default, Fonts as _Fonts
from ..game_math import Geometry as _Geometry, Collision as _Collision


def represent(value_string, *values):
    strings = value_string.split()
    return "\n".join("{}: {}".format(strings[i], values[i]) for i in range(0, len(values)))


def load_font(name, pt, bold=False, italic=False, underline=False):
    if name.lower() in _font.get_fonts():
        try:
            font = _font.SysFont(name, pt)
        except _error:
            _font.init()
            font = _font.SysFont(name, pt)
    else:
        try:
            font = _font.Font(_Fonts[name], pt)
        except KeyError:
            print("Error: font couldn't be loaded")
            font = _font.SysFont("", pt)
    font.set_bold(bold)
    font.set_italic(italic)
    font.set_underline(underline)
    return font


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_x(self, dx):
        self.set_x(self.x + dx)

    def move_y(self, dy):
        self.set_y(self.y + dy)

    def move(self, dx, dy):
        self.set_pos(self.x + dx, self.y + dy)

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_pos(self, x, y):
        self.set_x(x)
        self.set_y(y)

    def draw(self, surface):
        pass

    def loop_behavior(self):
        pass

    def distance_to(self, point):
        return _Geometry.distance(self, point)

    def angle_to(self, point):
        return _Geometry.angle(self, point)

    def gradient(self, point):
        return _Geometry.gradient(self, point)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        else:
            raise IndexError

    def __iter__(self):
        self.__index = 0
        return self

    def __len__(self):
        return 2

    def __next__(self):
        if self.__index == 0:
            self.__index += 1
            return self.x
        if self.__index == 1:
            self.__index += 1
            return self.y
        else:
            raise StopIteration

    def __repr__(self):
        return represent("x y", self.x, self.y)


class Rect(Point):
    def __init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset):
        Point.__init__(self, x, y)
        self.width = width
        self.height = height

        self.x2 = self.x + self.width
        self.y2 = self.y + self.height

        self.x_mode = x_mode
        self.y_mode = y_mode
        self.x_offset = round(x_offset)
        self.y_offset = round(y_offset)

    def _update_x2(self):
        self.x2 = self.x + self.width

    def _update_y2(self):
        self.y2 = self.y + self.height

    def _update_x_allignment(self, dx):
        if self.x_mode == _Layout.middle:
            self.move_x(-dx / 2)
        elif self.x_mode == _Layout.right:
            self.move_x(-dx)

    def _update_y_allignment(self, dy):
        if self.y_mode == _Layout.middle:
            self.move_y(-dy / 2)
        elif self.y_mode == _Layout.below:
            self.move_y(-dy)

    def move_x(self, dx):
        self.set_x(self.x + dx)

    def move_y(self, dy):
        self.set_y(self.y + dy)

    def move(self, dx, dy):
        self.set_pos(self.x + dx, self.y + dy)

    def set_x(self, x):
        Point.set_x(self, x)
        self._update_x2()

    def set_y(self, y):
        Point.set_y(self, y)
        self._update_y2()

    def set_pos(self, x, y):
        self.set_x(x)
        self.set_y(y)

    def move_width(self, d_width):
        self.set_width(self.width + d_width)

    def move_height(self, d_height):
        self.set_height(self.height + d_height)

    def move_size(self, d_width, d_height):
        self.set_size(self.width + d_width, self.height + d_height)

    def set_width(self, width):
        dx = width - self.width
        self.width = width
        self._update_x_allignment(dx)
        self._update_x2()

    def set_height(self, height):
        dy = height - self.height
        self.height = height
        self._update_y_allignment(dy)
        self._update_y2()

    def set_size(self, width, height):
        self.set_width(width)
        self.set_height(height)

    def move_x_offset(self, dx):
        self.set_x_offset(self.x_offset + dx)

    def move_y_offset(self, dy):
        self.set_y_offset(self.y_offset + dy)

    def move_offset(self, dx, dy):
        self.set_offset(self.x_offset + dx, self.y_offset + dy)

    def set_x_offset(self, x):
        x = round(x)
        dx = x - self.x_offset
        self.x_offset = round(x)
        self.move_x(dx)

    def set_y_offset(self, y):
        y = round(y)
        dy = y - self.y_offset
        self.y_offset = round(y)
        self.move_y(dy)

    def set_offset(self, x, y):
        self.set_x_offset(x)
        self.set_y_offset(y)

    def update_allignment(self, total_width, total_height, x_start=0, y_start=0):
        if self.x_mode == _Layout.left:
            self.set_x(self.x_offset + x_start)
        elif self.x_mode == _Layout.middle:
            self.set_x((total_width - self.width) / 2 + self.x_offset + x_start)
        elif self.x_mode == _Layout.right:
            self.set_x(total_width - self.width + self.x_offset + x_start)
        elif self.x_mode == _Layout.fill:
            self.set_width(total_width - self.x + self.x_offset + x_start)

        if self.y_mode == _Layout.above:
            self.set_y(self.y_offset + y_start)
        elif self.y_mode == _Layout.middle:
            self.set_y((total_height - self.height) / 2 + self.y_offset + y_start)
        elif self.y_mode == _Layout.below:
            self.set_y(total_height - self.height + self.y_offset + y_start)
        elif self.y_mode == _Layout.fill:
            self.set_height(total_height - self.y + self.y_offset + y_start)

    def update_allignment_in_rect(self, rect):
        self.update_allignment(rect.width, rect.height, rect.x, rect.y)

    def draw(self, surface):
        pass

    def collide_point(self, point):
        return _Collision.rect_point(self, point)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        else:
            raise IndexError

    def __iter__(self):
        self.__index = 0
        return self

    def __len__(self):
        return 2

    def __next__(self):
        if self.__index == 0:
            self.__index += 1
            return self.x
        if self.__index == 1:
            self.__index += 1
            return self.y
        else:
            raise StopIteration

    def __repr__(self):
        return represent("x y width height x2 y2 x_mode y_mode x_offset y_offset", self.x, self.y, self.width,
                         self.height, self.x2, self.y2, self.x_mode, self.y_mode, self.x_offset, self.y_offset)


class SurfaceRect(_SurfaceType, Rect):
    def __init__(self, x, y, x_mode, y_mode, x_offset, y_offset, width, height):
        Rect.__init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset)
        _SurfaceType.__init__(self, (self.width, self.height), _SRCALPHA)

    def _update_surfacetype(self):
        _SurfaceType.__init__(self, (self.width, self.height), _SRCALPHA)

    def _update_surface(self):
        surface = self.copy()
        self._update_surfacetype()
        self.blit(surface, (0, 0))

    def _update_draw(self):
        pass

    def set_surface(self, surface):
        self.set_size(surface.get_width(), surface.get_height())
        self.fill(_Color(0, 0, 0, 0))
        self.blit(surface, (0, 0))

    def move_width(self, d_width):
        Rect.move_width(self, d_width)
        self._update_surface()

    def move_height(self, d_height):
        Rect.move_height(self, d_height)
        self._update_surface()

    def move_size(self, d_width, d_height):
        Rect.move_size(self, d_width, d_height)
        self._update_surface()

    def set_width(self, width):
        Rect.set_width(self, width)
        self._update_surface()

    def set_height(self, height):
        Rect.set_height(self, height)
        self._update_surface()

    def set_size(self, width, height):
        Rect.set_width(self, width)
        Rect.set_height(self, height)
        self._update_surface()

    def chop(self, x, y, width, height):
        pass

    def flip(self, xbool, ybool):
        self.set_surface(_transform.flip(self, xbool, ybool))

    def rotate(self):
        pass

    def rotozoom(self):
        pass

    def scale(self, width, height):
        self.set_surface(_transform.scale(self, (width, height)))

    def scale2x(self):
        pass

    def smoothscale(self):
        pass

    def save(self, filename):
        _image.save(self, filename)

    def tostring(self, str_format, flipped=False):
        return _image.tostring(self, str_format, flipped)

    def draw(self, surface):
        surface.blit(self, (self.x, self.y))

    @staticmethod
    def from_surface(x, y, x_mode, y_mode, x_offset, y_offset, surface):
        new_surface = SurfaceRect(x, y, x_mode, y_mode, x_offset, y_offset, surface.get_width(),
                                  surface.get_height())
        new_surface.blit(surface, (0, 0))
        return new_surface

    @staticmethod
    def from_image(x, y, x_mode, y_mode, x_offset, y_offset, image_path):
        return SurfaceRect.from_surface(x, y, x_mode, y_mode, x_offset, y_offset, _image.load(image_path))


class Line(Rect):
    def __init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset, thickness, color):
        Rect.__init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset)
        self.thickness = thickness
        self.color = color

    def get_length(self):
        return _Geometry.distance(self, (self.x2, self.y2))

    def get_angle(self):
        return _Geometry.angle(self, (self.x2, self.y2))

    def set_angle(self, angle):
        width, height = _Geometry.get_dimensions(angle, self.get_length())
        self.set_size(width, height)

    def set_length(self, length):
        width, height = _Geometry.get_dimensions(-self.get_angle(), length)
        self.set_size(width, height)

    def draw(self, surface):
        _draw.line(surface, self.color, (self.x, self.y), (self.x2, self.y2), self.thickness)

    def __repr__(self):
        return represent("x y width height x2 y2 x_mode y_mode x_offset y_offset thickness color", self.x, self.y,
                         self.width, self.height, self.x2, self.y2, self.x_mode, self.y_mode, self.x_offset,
                         self.y_offset, self.thickness, self.color)

    @staticmethod
    def from_angle(x, y, length, angle, x_mode, y_mode, x_offset, y_offset, thickness, color):
        width, height = _Geometry.get_dimensions(angle, length)
        return Line(x, y, width, height, x_mode, y_mode, x_offset, y_offset, thickness, color)

    @staticmethod
    def from_points(x, y, x2, y2, x_mode, y_mode, x_offset, y_offset, thickness, color):
        return Line(x, y, x2 - x, y2 - y, x_mode, y_mode, x_offset, y_offset, thickness, color)


class Rectangle(Rect):
    def __init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset, color):
        Rect.__init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset)
        self.color = color

    def draw(self, surface):
        _draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def __repr__(self):
        return represent("x y width height x2 y2 x_mode y_mode x_offset y_offset color", self.x, self.y, self.width,
                         self.height, self.x2, self.y2, self.x_mode, self.y_mode, self.x_offset, self.y_offset,
                         self.color)


class Circle(Rect):
    def __init__(self, x, y, radius, x_mode, y_mode, x_offset, y_offset, color):
        Rect.__init__(self, x, y, radius * 2, radius * 2, x_mode, y_mode, x_offset, y_offset)
        self.color = color
        self.radius = radius
        self.xm = int(self.x + self.radius)
        self.ym = int(self.y + self.radius)

    def _update_xm(self):
        self.xm = int(self.x + self.radius)

    def _update_ym(self):
        self.ym = int(self.y + self.radius)

    def move_x(self, dx):
        Rect.move_x(self, dx)
        self._update_xm()

    def move_y(self, dy):
        Rect.move_y(self, dy)
        self._update_ym()

    def move(self, dx, dy):
        self.move_x(dx)
        self.move_y(dy)

    def set_x(self, x):
        Rect.set_x(self, x)
        self._update_xm()

    def set_y(self, y):
        Rect.set_y(self, y)
        self._update_ym()

    def set_pos(self, x, y):
        self.set_x(x)
        self.set_y(y)

    def set_middle_pos(self, x, y):
        self.set_x(x - self.radius)
        self.set_y(y - self.radius)

    def move_width(self, d_width):
        self.move_radius(d_width / 2)

    def move_height(self, d_height):
        self.move_radius(d_height / 2)

    def move_size(self, d_width, d_height):
        if d_width < d_height:
            size = d_width
        else:
            size = d_height
        self.move_radius(size / 2)

    def set_width(self, width):
        self.set_radius(width / 2)

    def set_height(self, height):
        self.set_radius(height / 2)

    def set_size(self, width, height):
        if width < height:
            size = width
        else:
            size = height
        self.set_radius(size / 2)

    def move_radius(self, d_radius):
        self.radius += d_radius
        Rect.move_width(self, d_radius * 2)
        Rect.move_height(self, d_radius * 2)

    def set_radius(self, radius):
        self.radius = radius
        Rect.set_width(self, self.radius * 2)
        Rect.set_height(self, self.radius * 2)

    def get_middle_pos(self):
        return self.xm, self.ym

    def draw(self, surface):
        _draw.circle(surface, self.color, (self.xm, self.ym), int(self.radius))

    def collide_point(self, point):
        return _Collision.circle_point(self, point)

    def __repr__(self):
        return represent("x y width height x2 y2 x_mode y_mode x_offset y_offset radius xm ym color", self.x, self.y,
                         self.width, self.height, self.x2, self.y2, self.x_mode, self.y_mode, self.x_offset,
                         self.y_offset, self.radius, self.xm, self.ym, self.color)


class Ellipse(Rect):
    def __init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset, color):
        Rect.__init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset)
        self.color = color

    def draw(self, surface):
        _draw.ellipse(surface, self.color, (self.x, self.y, self.width, self.height))

    def __repr__(self):
        return represent("x y width height x2 y2 x_mode y_mode x_offset y_offset color", self.x, self.y, self.width,
                         self.height, self.x2, self.y2, self.x_mode, self.y_mode, self.x_offset, self.y_offset,
                         self.color)


class PointsRect(Rect):
    def __init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset, points):
        Rect.__init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset)
        self.points = tuple(Point(p[0], p[1]) for p in points)
        self._update_pos()
        self._update_size()
        self.ratios = tuple((point.x / self.width, point.y / self.height) for point in self.points)
        # self._update_points_pos(self.x, self.y)

    def _update_size(self):
        for p1 in self.points:
            for p2 in self.points:
                if p1 != p2:
                    width = abs(p1.x - p2.x)
                    height = abs(p1.y - p2.y)
                    if width > self.width:
                        Rect.set_width(self, width)
                    if height > self.height:
                        Rect.set_height(self, height)

    def _update_pos(self):
        dx = self.points[0].x - self.x
        dy = self.points[0].y - self.y
        for point in self.points[1:]:
            x_difference = point.x - self.x
            y_difference = point.y - self.y
            if x_difference < dx:
                dx = x_difference
            if y_difference < dy:
                dy = y_difference
        self._update_points_pos(-dx, -dy)

    def _update_points_width(self, new_width):
        for i in range(0, len(self.points)):
            ratio_width = self.ratios[i][0]
            self.points[i].set_x(self.x + ratio_width * new_width)

    def _update_points_height(self, new_height):
        for i in range(0, len(self.points)):
            ratio_height = self.ratios[i][1]
            self.points[i].set_y(self.y + ratio_height * new_height)

    def _update_points_x(self, dx):
        for point in self.points:
            point.move_x(dx)

    def _update_points_y(self, dy):
        for point in self.points:
            point.move_y(dy)

    def _update_points_pos(self, dx, dy):
        for point in self.points:
            point.move(dx, dy)

    def set_x(self, x):
        self._update_points_x(x - self.x)
        Rect.set_x(self, x)

    def set_y(self, y):
        self._update_points_y(y - self.y)
        Rect.set_y(self, y)

    def set_width(self, width):
        self._update_points_width(width)
        Rect.set_width(self, width)

    def set_height(self, height):
        self._update_points_height(height)
        Rect.set_height(self, height)

    def set_x_offset(self, x):
        self._update_points_x(x - self.x_offset)
        Rect.set_x_offset(self, x)

    def set_y_offset(self, y):
        self._update_points_y(y - self.y_offset)
        Rect.set_y_offset(self, y)

    def draw(self, surface):
        _draw.polygon(surface, _Color(0, 0, 0), self.points, 2)

    def rotate(self, radians):
        mx = self.x + self.width / 2
        my = self.y + self.height / 2

        for point in self.points:
            angle = _Geometry.angle((mx, my), point) + radians
            length = _Geometry.distance((mx, my), point)
            width, height = _Geometry.get_dimensions(angle, length)
            point.set_pos(mx + width, my + height)
        self._update_size()

    def collide_point(self, point):
        return _Collision.polygon_point(self, point)

    def __getitem__(self, item):
        return self.points[item]

    def __iter__(self):
        self.__index = 0
        return self

    def __len__(self):
        return len(self.points)

    def __next__(self):
        if self.__index < len(self.points):
            point = self.points[self.__index]
            self.__index += 1
            return point
        else:
            raise StopIteration

    def __repr__(self):
        return represent("x y width height x2 y2 x_mode y_mode x_offset y_offset points", self.x, self.y, self.width,
                         self.height, self.x2, self.y2, self.x_mode, self.y_mode, self.x_offset, self.y_offset,
                         self.points)


class Polygon(PointsRect):
    def __init__(self, x, y, points, x_mode, y_mode, x_offset, y_offset, color):
        PointsRect.__init__(self, x, y, 0, 0, x_mode, y_mode, x_offset, y_offset, points)
        self.color = color

    def draw(self, surface):
        _draw.polygon(surface, self.color, self.points)

    def __repr__(self):
        return represent("x y width height x2 y2 x_mode y_mode x_offset y_offset color points", self.x, self.y,
                         self.width, self.height, self.x2, self.y2, self.x_mode, self.y_mode, self.x_offset,
                         self.y_offset, self.color, self.points)


class LineRect(Rectangle):
    def __init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset, color, thickness):
        Rectangle.__init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset, color)
        self.thickness = thickness

    def draw(self, surface):
        _draw.rect(surface, self.color, (self.x, self.y, self.width, self.thickness))
        _draw.rect(surface, self.color, (self.x, self.y2 - self.thickness, self.width, self.thickness))
        _draw.rect(surface, self.color, (self.x, self.y, self.thickness, self.height))
        _draw.rect(surface, self.color, (self.x2 - self.thickness, self.y, self.thickness, self.height))


class LineCircle(Circle):
    def __init__(self, x, y, radius, x_mode, y_mode, x_offset, y_offset, color, thickness):
        Circle.__init__(self, x, y, radius, x_mode, y_mode, x_offset, y_offset, color)
        self.thickness = thickness

    def draw(self, surface):
        _draw.circle(surface, self.color, (self.xm, self.ym), self.radius, self.thickness)


class EllipseCircle(Ellipse):
    def __init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset, color, thickness):
        Ellipse.__init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset, color)
        self.thickness = thickness

    def draw(self, surface):
        _draw.ellipse(surface, self.color, (self.x, self.y, self.width, self.height), self.thickness)


class LinePolygon(Polygon):
    def __init__(self, x, y, points, x_mode, y_mode, x_offset, y_offset, color, thickness):
        Polygon.__init__(self, x, y, points, x_mode, y_mode, x_offset, y_offset, color)
        self.thickness = thickness

    def draw(self, surface):
        _draw.polygon(surface, self.color, self.points, self.thickness)


class _TextObject(_SurfaceType):
    def __init__(self, content, color, font, pt, bold=False, italic=False, underline=False):
        self.content = content
        self.color = color
        self.pt = pt
        self.fontname = font
        self.font = load_font(self.fontname, self.pt, bold, italic, underline)

        surface = self.font.render(self.content, True, self.color)
        _SurfaceType.__init__(self, (surface.get_width(), surface.get_height()), _SRCALPHA)
        _SurfaceType.blit(self, surface, (0, 0))

    def _update_font(self, bold, italic, underline):
        self.font = load_font(self.fontname, self.pt, bold, italic, underline)

    def _update_content(self):
        self.set_surface(self.font.render(self.content, True, self.color))

    def set_surface(self, surface):
        _SurfaceType.__init__(self, (surface.get_width(), surface.get_height()), _SRCALPHA)
        self.blit(surface, (0, 0))

    def set_color(self, color):
        self.color = color
        self._update_content()

    def set_content(self, content):
        self.content = content
        self._update_content()

    def set_pt(self, pt):
        self.pt = pt
        self._update_font(self.font.get_bold(), self.font.get_italic(), self.font.get_underline())
        self._update_content()

    def set_font(self, font):
        self.fontname = font
        self._update_font(self.font.get_bold(), self.font.get_italic(), self.font.get_underline())
        self._update_content()

    def set_bold(self, bold):
        self._update_font(bold, self.font.get_italic(), self.font.get_underline())
        self._update_content()

    def set_italic(self, italic):
        self._update_font(self.font.get_bold(), italic, self.font.get_underline())
        self._update_content()

    def set_underline(self, underline):
        self._update_font(self.font.get_bold(), self.font.get_italic(), underline)
        self._update_content()

    def __repr__(self):
        return represent("content color pt fontname bold italic underline", self.content, self.color, self.pt,
                         self.fontname, self.font.get_bold(), self.font.get_italic(), self.font.get_underline())

    @staticmethod
    def from_tuple(font, pt, attributes):
        content = ""
        color = _Default.text_color
        bold = _Default.bold
        italic = _Default.italic
        underline = _Default.underline

        for attribute in attributes:
            if type(attribute) is str:
                content = attribute
            elif type(attribute) is _Color:
                color = attribute
            elif attribute == _Layout.bold:
                bold = True
            elif attribute == _Layout.italic:
                italic = True
            elif attribute == _Layout.underline:
                underline = True

        return _TextObject(content, color, font, pt, bold, italic, underline)


class Text(SurfaceRect):
    def __init__(self, x, y, x_mode, y_mode, x_offset, y_offset, pt, font, text_list):
        SurfaceRect.__init__(self, x, y, x_mode, y_mode, x_offset, y_offset, 0, 0)
        self.text_list = text_list
        self.text_objects = list()
        self.pt = pt
        self.fontname = font
        self.font = load_font(self.fontname, self.pt)

        for text in self.text_list:
            self.text_objects.append(_TextObject.from_tuple(self.fontname, self.pt, text))
        self._update_surface()

    def _update_surface(self):
        width = sum(text.get_width() for text in self.text_objects)
        height = self.font.get_height()

        if width != self.width or height != self.height:
            _SurfaceType.__init__(self, (width, height), _SRCALPHA)
            Rect.set_width(self, width)
            Rect.set_height(self, height)

        SurfaceRect.fill(self, _Color(0, 0, 0, 0))
        x = 0
        for text in self.text_objects:
            SurfaceRect.blit(self, text, (x, 0))
            x += text.get_width()

    def _update_font(self):
        self.font = load_font(self.fontname, self.pt)
        for text in self.text_objects:
            text.set_font(self.fontname)
            text.set_pt(self.pt)

    def set_color(self, color, *index):
        if len(index) == 0:
            for text in self.text_objects:
                text.set_color(color)
        else:
            for i in index:
                self.text_objects[i].set_color(color)
        self._update_surface()

    def set_content(self, content, *index):
        if len(index) == 0:
            for text in self.text_objects:
                text.set_content(content)
        else:
            for i in index:
                self.text_objects[i].set_content(content)
        self._update_surface()

    def set_bold(self, bold, *index):
        if len(index) == 0:
            for text in self.text_objects:
                text.set_bold(bold)
        else:
            for i in index:
                self.text_objects[i].set_bold(bold)
        self._update_surface()

    def set_italic(self, italic, *index):
        if len(index) == 0:
            for text in self.text_objects:
                text.set_italic(italic)
        else:
            for i in index:
                self.text_objects[i].set_italic(italic)
        self._update_surface()

    def set_underline(self, underline, *index):
        if len(index) == 0:
            for text in self.text_objects:
                text.set_underline(underline)
        else:
            for i in index:
                self.text_objects[i].set_underline(underline)
        self._update_surface()

    def set_pt(self, pt):
        self.pt = pt
        self._update_font()
        self._update_surface()

    def set_font(self, font):
        self.fontname = font
        self._update_font()
        self._update_surface()

    def __repr__(self):
        return represent("x y width height x2 y2 x_mode y_mode x_offset y_offset pt font text_objects", self.x, self.y,
                         self.width, self.height, self.x2, self.y2, self.x_mode, self.y_mode, self.x_offset,
                         self.y_offset, self.pt, self.fontname, self.text_objects)

