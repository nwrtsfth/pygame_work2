from ..timer import Timer as _Timer


class Button:
    def __init__(self, index):
        self._type = index
        self._pressed = False
        self._press_down = False
        self._press_up = False
        self._timer = _Timer()
        self._last_pressed_time = 0

    def get_type(self):
        return self._type

    def get_pressed(self):
        return self._pressed

    def get_press_down(self):
        return self._press_down

    def get_press_up(self):
        return self._press_up

    def get_pressed_time(self):
        return self._timer.get_counter()

    def get_last_time(self):
        return self._last_pressed_time

    def set_press_down(self):
        self._press_down = True
        self._pressed = True
        self._timer.start()

    def set_press_up(self):
        self._press_up = True
        self._pressed = False
        self._last_pressed_time = self._timer.get_counter()
        self._timer.reset()

    def reset(self):
        self._press_down = False
        self._press_up = False

    def update(self):
        self.reset()
        self._timer.tick()


class Key(Button):
    def __init__(self, index, mod=0, unicode=""):
        Button.__init__(self, index)
        self._mod = mod
        self._unicode = unicode

    def get_mod(self):
        return self._mod

    def get_unicode(self):
        return self._unicode

    def get_char(self):
        if self._unicode not in ("", "\t", "\r", "\x08", "\x1b"):
            return self._unicode
        return None

    def is_char(self):
        if self._unicode not in ("", "\t", "\r", "\x08", "\x1b"):
            return True
        return False
