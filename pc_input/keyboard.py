from .key import Key as _Key
from pygame import K_LSHIFT as _K_LSHIFT, K_RSHIFT as _K_RSHIFT


class K_default:
    up = 273
    down = 274
    left = 276
    right = 275
    shiftLeft = 304
    shiftRight = 303
    altLeft = 308
    altRight = 307
    ctrlLeft = 306
    ctrlRight = 305
    capslock = 301
    tab = 9
    backspace = 8
    enter = 13
    windows = 211


class _KeyboardObject:
    def __init__(self):
        self.last_key = None
        self.active_keys = list()
        self.writing_mode = True

        self.__key_binds_down = list()
        self.__key_binds_up = list()
        self.__key_binds_pressed = list()

    @staticmethod
    def _add_binds(key_list, func, keys):
        keys = set(sorted(list(keys)))
        for key_bind in key_list:
            if key_bind[0] == keys:
                key_list.remove(key_bind)
                break
        key_list.append((keys, func))

    def key_press_down(self, keypress):
        self.last_key = _Key(keypress.key, keypress.mod, keypress.unicode)
        self.last_key.set_press_down()
        self.active_keys.append(self.last_key)

        active_keys = set(key.get_type() for key in self.active_keys)
        for combination in self.__key_binds_down:
            keys, func = combination
            if keys.issubset(active_keys):
                func()

    def key_press_up(self, keypress):
        for key in self.active_keys:
            if key.get_type() == keypress.key:
                key.set_press_up()
                if self.writing_mode and key.get_type() in (_K_LSHIFT, _K_RSHIFT):
                    self.reset_shift()

        active_keys = set(key.get_type() for key in self.active_keys)
        for combination in self.__key_binds_up:
            keys, func = combination
            if keys.issubset(active_keys):
                func()

    def update_keys(self):
        for key in self.active_keys:
            key.update()

        active_keys = set(key.get_type() for key in self.active_keys)
        for combination in self.__key_binds_pressed:
            keys, func = combination
            if keys.issubset(active_keys):
                func()

    def reset_shift(self):
        for key in self.active_keys:
            if key.get_mod() == 1 or key.get_mod() == 2:
                key.set_press_up()

    def reset_last_keys(self):
        for key in self.active_keys:
            if not key.get_pressed():
                self.active_keys.remove(key)
                if key == self.last_key:
                    self.last_key = None

    def update(self):
        self.reset_last_keys()
        self.update_keys()

    def set_key_bind_down(self, func, *keys):
        Keyboard._add_binds(self.__key_binds_down, func, keys)

    def set_key_bind_up(self, func, *keys):
        Keyboard._add_binds(self.__key_binds_up, func, keys)

    def set_key_bind_pressed(self, func, *keys):
        Keyboard._add_binds(self.__key_binds_pressed, func, keys)

    def key_bind_down(self, *keys):
        def wrapper(func):
            self.set_key_bind_down(func, *keys)
            return func
        return wrapper

    def key_bind_up(self, *keys):
        def wrapper(func):
            self.set_key_bind_up(func, *keys)
            return func
        return wrapper

    def key_bind_pressed(self, *keys):
        def wrapper(func):
            self.set_key_bind_pressed(func, *keys)
            return func
        return wrapper


Keyboard = _KeyboardObject()
