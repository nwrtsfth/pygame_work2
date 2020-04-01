from pygame import draw as _draw, Color as _Color


def transition(surface, x, y, width, height, color1, color2, horizontal=True):
    r = color1[0]
    g = color1[1]
    b = color1[2]

    if horizontal:
        dr = (color2[0] - color1[0]) / width
        dg = (color2[1] - color1[1]) / width
        db = (color2[2] - color1[2]) / width
        for i in range(0, width):
            _draw.rect(surface, (r, g, b), (x + i, y, 1, height))
            r += dr
            g += dg
            b += db
    else:
        dr = (color2[0] - color1[0]) / height
        db = (color2[2] - color1[2]) / height
        dg = (color2[1] - color1[1]) / height
        for i in range(0, height):
            _draw.rect(surface, (r, g, b), (x, y + i, width, 1))
            r += dr
            g += dg
            b += db


def rainbow_transition(surface, x, y, width, height, rgb=255, horizontal=True):
    rgb = int(rgb)

    if horizontal:
        avg_width = int(width / 6)
        transition(surface, x, y, avg_width, height, _Color(rgb, 0, 0), _Color(rgb, rgb, 0))
        transition(surface, int(x + avg_width), y, avg_width, height, _Color(rgb, rgb, 0), _Color(0, rgb, 0))
        transition(surface, int(x + avg_width * 2), y, avg_width, height, _Color(0, rgb, 0), _Color(0, rgb, rgb))
        transition(surface, int(x + avg_width * 3), y, avg_width, height, _Color(0, rgb, rgb), _Color(0, 0, rgb))
        transition(surface, int(x + avg_width * 4), y, avg_width, height, _Color(0, 0, rgb), _Color(rgb, 0, rgb))
        transition(surface, int(x + avg_width * 5), y, avg_width + width % 6, height, _Color(rgb, 0, rgb),
                   _Color(rgb, 0, 0))
    else:
        avg_height = int(height / 6)
        transition(surface, x, y, width, avg_height, _Color(rgb, 0, 0), _Color(rgb, rgb, 0), False)
        transition(surface, x, int(y + avg_height), width, avg_height, _Color(rgb, rgb, 0), _Color(0, rgb, 0), False)
        transition(surface, x, int(y + avg_height * 2), width, avg_height, _Color(0, rgb, 0), _Color(0, rgb, rgb),
                   False)
        transition(surface, x, int(y + avg_height * 3), width, avg_height, _Color(0, rgb, rgb),
                   _Color(0, 0, rgb), False)
        transition(surface, x, int(y + avg_height * 4), width, avg_height, _Color(0, 0, rgb), _Color(rgb, 0, rgb),
                   False)
        transition(surface, x, int(y + avg_height * 5), width, avg_height + height % 6, _Color(rgb, 0, rgb),
                   _Color(rgb, 0, 0), False)
