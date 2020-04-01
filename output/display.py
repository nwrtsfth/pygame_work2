from pygame import display as _display, RESIZABLE as _RESIZABLE, FULLSCREEN as _FULLSCREEN,  NOFRAME as _NOFRAME, \
     error as _error, SurfaceType as _SurfaceType
from pygame.image import load as _load
from ctypes import windll as _windll


class Display:
    surface = None
    width = 500
    height = 500

    min_width = 0
    min_height = 0

    max_width = -1
    max_height = -1

    flags = set()

    __smallscreen_width = width
    __smallscreen_height = height

    __fullscreen_width = _windll.user32.GetSystemMetrics(0)
    __fullscreen_height = _windll.user32.GetSystemMetrics(1)

    @staticmethod
    def _update_size():
        return _display.set_mode((Display.width, Display.height), sum(Display.flags))

    @staticmethod
    def _update_fullscreen():
        Display.__smallscreen_width = Display.width
        Display.__smallscreen_height = Display.height
        return _display.set_mode((Display.__fullscreen_width, Display.__fullscreen_height), _FULLSCREEN)

    @staticmethod
    def _update_smallscreen():
        Display.width = Display.__smallscreen_width
        Display.height = Display.__smallscreen_height
        return Display._update_size()

    @staticmethod
    def set_mode(width, height, resizable=False, fullscreen=False, noframe=False):
        Display.width = width
        Display.height = height

        if resizable:
            Display.flags.add(_RESIZABLE)
        if fullscreen:
            Display.flags.add(_FULLSCREEN)
        if noframe:
            Display.flags.add(_NOFRAME)
        Display.surface = Display._update_size()

    @staticmethod
    def set_width(width):
        if width < Display.min_width:
            Display.width = Display.min_width
        elif Display.max_width != -1 and width > Display.max_width:
            Display.width = Display.max_width
        else:
            Display.width = width
        Display.surface = Display._update_size()

    @staticmethod
    def set_height(height):
        if height < Display.min_height:
            Display.height = Display.min_height
        elif Display.max_height != -1 and height > Display.max_height:
            Display.height = Display.max_height
        else:
            Display.height = height
        Display.surface = Display._update_size()

    @staticmethod
    def set_size(width, height):
        if width < Display.min_width:
            Display.width = Display.min_width
        elif Display.max_width != -1 and width > Display.max_width:
            Display.width = Display.max_width
        else:
            Display.width = width
        if height < Display.min_height:
            Display.height = Display.min_height
        elif Display.max_height != -1 and height > Display.max_height:
            Display.height = Display.max_height
        else:
            Display.height = height
        Display.surface = Display._update_size()

    @staticmethod
    def set_min_width(min_width):
        Display.min_width = min_width
        Display.set_width(Display.width)

    @staticmethod
    def set_min_height(min_height):
        Display.min_height = min_height
        Display.set_height(Display.height)

    @staticmethod
    def set_min_size(min_width, min_height):
        Display.min_width = min_width
        Display.min_height = min_height
        Display.set_size(Display.width, Display.height)

    @staticmethod
    def set_max_width(max_width):
        Display.max_width = max_width
        Display.set_width(Display.width)

    @staticmethod
    def set_max_height(max_height):
        Display.max_height = max_height
        Display.set_height(Display.height)

    @staticmethod
    def set_max_size(max_width, max_height):
        Display.max_width = max_width
        Display.max_height = max_height
        Display.set_size(Display.width, Display.height)

    @staticmethod
    def disable_max_width():
        Display.max_width = -1

    @staticmethod
    def disable_max_height():
        Display.max_height = -1

    @staticmethod
    def disable_max_size():
        Display.disable_max_width()
        Display.disable_max_height()

    @staticmethod
    def set_resizable(resizable):
        if resizable:
            Display.flags.add(_RESIZABLE)
            Display.surface = Display._update_size()
        else:
            try:
                Display.flags.remove(_RESIZABLE)
                Display.surface = Display._update_size()
            except KeyError:
                pass

    @staticmethod
    def set_fullscreen(fullscreen):
        if fullscreen:
            Display.flags.add(_FULLSCREEN)
            Display._update_fullscreen()
        else:
            try:
                Display.flags.remove(_FULLSCREEN)
                Display._update_smallscreen()
            except KeyError:
                pass

    @staticmethod
    def set_noframe(noframe):
        if noframe:
            Display.flags.add(_NOFRAME)
            Display.surface = Display._update_size()
        else:
            try:
                Display.flags.remove(_NOFRAME)
                Display.surface = Display._update_size()
            except KeyError:
                pass

    @staticmethod
    def load_icon(filename):
        try:
            _display.set_icon(_load(filename))
        except _error:
            print("Error: icon couldn't be loaded")

    @staticmethod
    def clear_icon():
        surface = _SurfaceType((1, 1))
        surface.set_alpha(0)
        _display.set_icon(surface)

    @staticmethod
    def toggle_fullscreen():
        Display.set_fullscreen(not Display.get_fullscreen())

    @staticmethod
    def get_resizable():
        return _RESIZABLE in Display.flags

    @staticmethod
    def get_fullscreen():
        return _FULLSCREEN in Display.flags

    @staticmethod
    def get_noframe():
        return _NOFRAME in Display.flags

    @staticmethod
    def fill(color):
        Display.surface.fill(color)

    @staticmethod
    def flip():
        if _display.get_active():
            _display.flip()

    @staticmethod
    def update(rects):
        if _display.get_active():
            _display.update(rects)

    @staticmethod
    def update_shapes_mode(shapes):
        for shape in shapes:
            if hasattr(shape, "update_allignment"):
                shape.update_allignment(Display.width, Display.height)
            else:
                print("AttributeError: couldn't update shape of {}".format(shape))
