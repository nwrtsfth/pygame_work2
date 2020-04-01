from pygame import event as _event


class Events:
    __all = list()
    __functions = dict()
    __current = None

    @staticmethod
    def get_current():
        return Events.__current

    @staticmethod
    def update():
        Events.__all = _event.get()
        for event in Events.__all:
            if event.type in Events.__functions:
                Events.__current = event
                Events.__functions[event.type]()
        Events.__current = None

    @staticmethod
    def set_new(func, event):
        Events.__functions[event] = func

    @staticmethod
    def new(event):
        def wrapper(func):
            Events.__functions[event] = func
            return func
        return wrapper
