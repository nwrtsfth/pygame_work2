from pygame import Color as _Color
from .basic import Rect as _Rect, SurfaceRect as _SurfaceRect, represent
from ..constants import Layout as _Layout


class DynamicGroup(_Rect):
    def __init__(self, x, y, x_mode, y_mode, x_offset, y_offset, shapes, width, height):
        _Rect.__init__(self, x, y, width, height, x_mode, y_mode, x_offset, y_offset)
        self.shapes = shapes
        self._update_shapes_pos(self.x, self.y)
        self._update_size()
        self._update_shape_allignment()

    def _update_pos(self):
        x_min = 0
        y_min = 0
        for shape in self.shapes:
            if shape.x_mode == _Layout.default:
                x_min = shape.x
                break
        for shape in self.shapes:
            if shape.y_mode == _Layout.default:
                y_min = shape.y
                break

        for shape in self.shapes[1:]:
            if shape.x_mode == _Layout.default:
                if shape.x < x_min:
                    x_min = shape.x
            if shape.y_mode == _Layout.default:
                if shape.y < y_min:
                    y_min = shape.y
        dx = self.x - x_min
        dy = self.y - y_min
        _Rect.set_x(self, x_min)
        _Rect.set_y(self, y_min)
        if self.x_mode == _Layout.middle:
            self.move_x(dx)
        if self.y_mode == _Layout.middle:
            self.move_y(dy)

    def _update_size(self):
        if len(self.shapes) > 0:
            width_max = self.shapes[0].width
            height_max = self.shapes[0].height
        else:
            width_max = 0
            height_max = 0

        for shape in self.shapes:
            if shape.width > width_max:
                width_max = shape.width
            if shape.height > height_max:
                height_max = shape.height

        for shape in self.shapes:
            if shape.x_mode == _Layout.default:
                if shape.x2 - self.x > width_max:
                    width_max = shape.x2 - self.x
            if shape.y_mode == _Layout.default:
                if shape.y2 - self.y > height_max:
                    height_max = shape.y2 - self.y

        if self.x_mode != _Layout.fill:
            _Rect.set_width(self, width_max)
        if self.y_mode != _Layout.fill:
            _Rect.set_height(self, height_max)

    def _update_shapes_x(self, dx):
        for shape in self.shapes:
            shape.move_x(dx)

    def _update_shapes_y(self, dy):
        for shape in self.shapes:
            shape.move_y(dy)

    def _update_shapes_pos(self, dx, dy):
        for shape in self.shapes:
            shape.move(dx, dy)

    def _update_shape_allignment(self):
        for shape in self.shapes:
            shape.update_allignment_in_rect(self)

    def set_x(self, x):
        self._update_shapes_x(x - self.x)
        _Rect.set_x(self, x)

    def set_y(self, y):
        self._update_shapes_y(y - self.y)
        _Rect.set_y(self, y)

    def set_width(self, width):
        _Rect.set_width(self, width)
        self._update_shape_allignment()

    def set_height(self, height):
        _Rect.set_height(self, height)
        self._update_shape_allignment()

    def set_size(self, width, height):
        _Rect.set_size(self, width, height)
        self._update_shape_allignment()

    def set_x_offset(self, x):
        self._update_shapes_x(x - self.x_offset)
        _Rect.set_x_offset(self, x)

    def set_y_offset(self, y):
        self._update_shapes_y(y - self.y_offset)
        _Rect.set_y_offset(self, y)

    def update_allignment(self, total_width, total_height, x_start=0, y_start=0):
        _Rect.update_allignment(self, total_width, total_height, x_start, y_start)
        self._update_shape_allignment()

    def append(self, shape):
        self.shapes.append(shape)
        shape.update_allignment_in_rect(self)
        self._update_pos()
        self._update_size()
        self._update_shape_allignment()

    def clear(self):
        self.shapes.clear()
        self.set_size(0, 0)

    def count(self, shape):
        return self.shapes.count(shape)

    def extend(self, shapes):
        self.shapes.extend(shapes)
        self._update_pos()
        self._update_size()
        self._update_shape_allignment()

    def index(self, shape, start=0, stop=0):
        return self.shapes.index(shape, start, stop)

    def insert(self, index, shape):
        self.shapes.insert(index, shape)
        self._update_pos()
        self._update_size()
        self._update_shape_allignment()

    def pop(self, index):
        self.shapes.pop(index)
        self._update_pos()
        self._update_size()
        self._update_shape_allignment()

    def remove(self, shape):
        self.shapes.remove(shape)
        self._update_pos()
        self._update_size()
        self._update_shape_allignment()

    def reverse(self):
        self.shapes.reverse()

    def loop_behavior(self):
        for shape in self.shapes:
            shape.loop_behavior()

    def draw(self, surface):
        for shape in self.shapes:
            shape.draw(surface)

    def __getitem__(self, item):
        return self.shapes[item]

    def __iter__(self):
        self.__index = 0
        return self

    def __len__(self):
        return len(self.shapes)

    def __next__(self):
        if self.__index < len(self.shapes):
            shape = self.shapes[self.__index]
            self.__index += 1
            return shape
        else:
            raise StopIteration

    def __repr__(self):
        return represent("x y width height x2 y2 x_mode y_mode x_offset y_offset shapes", self.x, self.y,
                         self.width, self.height, self.x2, self.y2, self.x_mode, self.y_mode, self.x_offset,
                         self.y_offset, self.shapes)


class Group(_SurfaceRect, DynamicGroup):
    def __init__(self, x, y, x_mode, y_mode, x_offset, y_offset, shapes, width, height):
        _SurfaceRect.__init__(self, x, y, x_mode, y_mode, x_offset, y_offset, width, height)
        DynamicGroup.__init__(self, x, y, x_mode, y_mode, x_offset, y_offset, shapes, width, height)
        self._update_draw()

    def _update_size(self):
        DynamicGroup._update_size(self)
        self._update_surface()

    def _update_draw(self):
        self.fill(_Color(0, 0, 0, 0))
        for shape in self.shapes:
            shape.move(-self.x, -self.y)
            shape.draw(self)
            shape.move(self.x, self.y)

    def set_x(self, x):
        self._update_shapes_x(x - self.x)
        _SurfaceRect.set_x(self, x)

    def set_y(self, y):
        self._update_shapes_y(y - self.y)
        _SurfaceRect.set_y(self, y)

    def set_width(self, width):
        _SurfaceRect.set_width(self, width)
        self._update_size()
        self._update_shape_allignment()

    def set_height(self, height):
        _SurfaceRect.set_height(self, height)
        self._update_size()
        self._update_shape_allignment()

    def set_size(self, width, height):
        _SurfaceRect.set_size(self, width, height)
        self._update_size()
        self._update_shape_allignment()

    def set_x_offset(self, x):
        self._update_shapes_x(x - self.x_offset)
        _SurfaceRect.set_x_offset(self, x)

    def set_y_offset(self, y):
        self._update_shapes_y(y - self.y_offset)
        _SurfaceRect.set_y_offset(self, y)

    def update_allignment(self, total_width, total_height, x_start=0, y_start=0):
        _SurfaceRect.update_allignment(self, total_width, total_height, x_start, y_start)
        self._update_shape_allignment()
        self._update_draw()

    def append(self, shapes):
        DynamicGroup.append(self, shapes)
        self._update_draw()

    def extend(self, shapes):
        DynamicGroup.extend(self, shapes)
        self._update_draw()

    def insert(self, index, shape):
        DynamicGroup.insert(self, index, shape)
        self._update_draw()

    def pop(self, index):
        DynamicGroup.pop(self, index)
        self._update_draw()

    def remove(self, shape):
        DynamicGroup.remove(self, shape)
        self._update_draw()

    def reverse(self):
        DynamicGroup.reverse(self)
        self._update_draw()

    def loop_behavior(self):
        update = False
        for shape in self.shapes:
            if shape.loop_behavior() and not update:
                update = True
        if update:
            self._update_draw()


class StackGroup(DynamicGroup):
    def __init__(self, x, y, x_mode, y_mode, x_offset, y_offset, shapes, width, height, shape_offset, horizontal):
        DynamicGroup.__init__(self, x, y, x_mode, y_mode, x_offset, y_offset, shapes, width, height)
        self.shape_offset = shape_offset
        self.horizontal = horizontal

    def update_allignment(self, total_width, total_height, x_start=0, y_start=0):
        DynamicGroup.update_allignment(self, total_width, total_height, x_start, y_start)
        length = 0
        for shape in self.shapes:
            if self.horizontal:
                shape.set_x(self.x + length)
                length += shape.width
            else:
                shape.set_y(self.y + length)
                length += shape.height
            shape.update_allignment()


