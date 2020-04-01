from .display import Display as _Display
from ..pc_input.mouse import Mouse as _Mouse
from ..pc_input.event import Events as _Events
from ..pc_input.keyboard import Keyboard as _Keyboard
from ..constants import Default as _Default
from pygame import VIDEORESIZE as _VIDEORESIZE, QUIT as _QUIT, MOUSEBUTTONUP as _MOUSEBUTTONUP, MOUSEBUTTONDOWN as \
     _MOUSEBUTTONDOWN, KEYDOWN as _KEYDOWN, KEYUP as _KEYUP, init as _pygame_init, quit as _pygame_quit, K_F4 as _K_F4,\
     K_LALT as _K_LALT, K_RALT as _K_RALT
from pygame.time import Clock as _Clock


class Page:
    def __init__(self, name, shapes, **variables):
        self.name = name
        self.shapes = shapes
        self.variables = variables
        self.running = False

        self._loop_behavior_shapes = list()
        self._get_loop_behavior_shapes()

    def _get_loop_behavior_shapes(self):
        self._loop_behavior_shapes = list(shape for shape in self.shapes if hasattr(shape, "loop_behavior"))

    def init(self):
        self.update_shapes_pos()

    def loop(self):
        while self.running:
            _Display.fill(_Default.background_color)
            for shape in self._loop_behavior_shapes:
                shape.loop_behavior()
            for shape in self.shapes:
                shape.draw(_Display.surface)
            self.loop_function()
            Application.update()

    def quit(self):
        pass

    def loop_function(self):
        pass

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def update_shapes_pos(self):
        _Display.update_shapes_mode(self.shapes)

    def __getitem__(self, item):
        return self.variables[item]


class Application:
    pages = dict()
    selected_name = None
    selected_page = None
    running = True
    clock = _Clock()
    ticks = _Default.ticks

    @staticmethod
    def init(page_name, ticks=_Default.ticks):
        _pygame_init()
        Application.ticks = ticks
        Application.set_page(page_name)

    @staticmethod
    def quit():
        _pygame_quit()

    @staticmethod
    def set_page(page_name):
        Application.selected_name = page_name
        Application.update_page()

    @staticmethod
    def update_page():
        Application.selected_page = Application.pages[Application.selected_name]
        if hasattr(Application.selected_page, "start"):
            Application.selected_page.start()

    @staticmethod
    def get_page(page_name):
        return Application.pages[page_name]

    @staticmethod
    def get_current_page():
        return Application.selected_page

    @staticmethod
    def add_page(page, name=None):
        if name is None:
            name = page.name
        Application.pages[name] = page

    @staticmethod
    def update():
        _Mouse.update()
        _Keyboard.update()
        _Display.flip()
        _Events.update()
        Application.clock.tick(Application.ticks)

    @staticmethod
    def loop():
        while Application.running:
            Application.update_page()
            Application.selected_page.init()
            Application.selected_page.loop()
            Application.selected_page.quit()

    @staticmethod
    @_Events.new(_VIDEORESIZE)
    def update_screen():
        event = _Events.get_current()
        _Display.set_size(event.w, event.h)
        if hasattr(Application.selected_page, "update_shapes_pos"):
            Application.selected_page.update_shapes_pos()

    @staticmethod
    @_Events.new(_QUIT)
    @_Keyboard.key_bind_down(_K_LALT, _K_F4)
    @_Keyboard.key_bind_down(_K_RALT, _K_F4)
    def stop():
        if hasattr(Application.selected_page, "stop"):
            Application.selected_page.stop()
        Application.running = False

    @staticmethod
    @_Events.new(_MOUSEBUTTONDOWN)
    def update_mouse_button_down():
        button = _Events.get_current().button
        _Mouse.update_button_down(button)

    @staticmethod
    @_Events.new(_MOUSEBUTTONUP)
    def update_mouse_button_up():
        button = _Events.get_current().button
        _Mouse.update_button_up(button)

    @staticmethod
    @_Events.new(_KEYDOWN)
    def update_keyboard_down():
        _Keyboard.key_press_down(_Events.get_current())

    @staticmethod
    @_Events.new(_KEYUP)
    def update_keyboard_up():
        _Keyboard.key_press_up(_Events.get_current())
