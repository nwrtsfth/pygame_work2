from math import sqrt as _sqrt, atan2 as _atan2, cos as _cos, sin as _sin, pi as _pi


class Geometry:
    @staticmethod
    def _point(point):
        if hasattr(point, "x") and hasattr(point, "y"):
            return point.x, point.y
        return point[0], point[1]

    @staticmethod
    def _rect(rect):
        if hasattr(rect, "x") and hasattr(rect, "y") and hasattr(rect, "x2") and hasattr(rect, "y2"):
            return rect.x, rect.y, rect.x2, rect.y2
        return rect[0], rect[1], rect[2], rect[3]

    @staticmethod
    def distance(point_1, point_2):
        x1, y1 = Geometry._point(point_1)
        x2, y2 = Geometry._point(point_2)
        return _sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    @staticmethod
    def angle(point_1, point_2):
        x1, y1 = Geometry._point(point_1)
        x2, y2 = Geometry._point(point_2)
        return _atan2(-(y2 - y1), (x2 - x1))

    @staticmethod
    def get_dimensions(angle, length):
        if angle > 2 * _pi:
            angle = angle - 2 * _pi
        angle = -angle
        width = _cos(angle) * length
        height = _sin(angle) * length
        return width, height

    @staticmethod
    def get_dimensions2(point_1, point_2, length=1, dist=None):
        if dist is None:
            dist = Geometry.distance(point_1, point_2)
        x1, y1 = Geometry._point(point_1)
        x2, y2 = Geometry._point(point_2)
        width = length * (x2 - x1) / dist
        height = length * (y2 - y1) / dist
        return width, height

    @staticmethod
    def gradient(point_1, point_2):
        x1, y1 = Geometry._point(point_1)
        x2, y2 = Geometry._point(point_2)
        return (y2 - y1) / (x2 - x1)

    @staticmethod
    def rect_points(point_1, point_2):
        x1, y1 = Geometry._point(point_1)
        x2, y2 = Geometry._point(point_2)

        point_list = list()
        width = int(abs(x2 - x1))
        height = int(abs(y2 - y1))
        for x in range(width):
            for y in range(height):
                point_list.append((x + x1, y + y1))
        return point_list

    @staticmethod
    def line_points(x1, y1, x2, y2):
        point_list = list()
        width = x2 - x1
        height = y2 - y1
        length = _sqrt(width ** 2 + height ** 2)
        dx = width / length
        dy = height / length

        x = x1
        y = y1

        for i in range(int(length)):
            point_list.append((int(x), int(y)))
            x += dx
            y += dy
        return point_list


class Collision:
    @staticmethod
    def rect_point(rect, point):
        x, y = Geometry._point(point)
        rx, ry, rx2, ry2 = Geometry._rect(rect)
        return rx < x < rx2 and ry < y < ry2

    @staticmethod
    def circle_point(circle, point):
        if not Collision.rect_point(circle, point):
            return False
        return Geometry.distance(point, (circle.xm, circle.ym)) < circle.radius
        pass

    @staticmethod
    def between_angles(side_1, side_2, angle):
        if side_1 > side_2:
            angle_a, angle_b = side_1, side_2
        else:
            angle_a, angle_b = side_2, side_1

        if (side_1 >= 0 and side_2 >= 0) or (side_1 <= 0 and side_2 <= 0) or angle_a - angle_b < _pi:
            return angle_b < angle < angle_a
        return angle_b > angle or angle_a < angle

    @staticmethod
    def polygon_point(polygon, point):
        if not Collision.rect_point(polygon, point):
            return False

        point_x, point_y = Geometry._point(point)
        x_right = 0
        p1 = polygon[-1]
        for i in range(0, len(polygon)):
            p2 = polygon[i]

            if p1.y < p2.y:
                min_y = p1.y
                max_y = p2.y
            else:
                min_y = p2.y
                max_y = p1.y

            if min_y <= point_y < max_y:
                if p1.x != p2.x:
                    gradient = Geometry.gradient(p1, p2)
                    x = (point_y - p1.y) / gradient + p1.x
                else:
                    x = p1.x
                if x > point_x:
                    x_right += 1
            p1 = p2

        return x_right % 2 == 1


class Area:
    @staticmethod
    def rect(rect):
        return rect.width * rect.height

    @staticmethod
    def circle(circle):
        return circle.radius**2 * _pi

    @staticmethod
    def polygon(polygon, self_intersect=False):
        if self_intersect:
            print("Warning: current algoritm doesn't work for self-intersecting polygons")
            return 0

        area = 0

        p1 = polygon[-1]
        for i in range(0, len(polygon)):
            p2 = polygon[i]
            area += p1.x * p2.y - p1.y * p2.x
            p1 = p2

        return abs(area) / 2


class Perimiter:
    @staticmethod
    def rect(rect):
        return 2 * rect.width + 2 * rect.height

    @staticmethod
    def circle(circle):
        return circle.radius * 2 * _pi

    @staticmethod
    def polygon(polygon):
        length = 0
        p1 = polygon[-1]
        for i in range(0, len(polygon)):
            p2 = polygon[i]
            length += Geometry.distance(p1, p2)
            p1 = p2
        return length


class Volume:
    @staticmethod
    def sphere(circle):
        return (circle.radius**3 * 4 * _pi) / 3
