class Time:
    def __init__(self, ticks=0, factor=1):
        self._counter = ticks
        self._factor = factor

    def set_counter(self, counter):
        self._counter = counter

    def set_factor(self, factor):
        self._factor = factor

    def get_counter(self):
        return self._counter

    def get_factor(self):
        return self._factor

    def seconds(self):
        return self._counter // self._factor

    def minutes(self):
        return self.seconds() // 60

    def hours(self):
        return self.minutes() // 60

    def time(self):
        time = (self.hours(), self.minutes() % 60, self.seconds() % 60)
        return time

    def time_string(self):
        hours, minutes, seconds = self.time()
        if seconds < 10:
            seconds = "0{}".format(seconds)
        if minutes < 10:
            minutes = "0{}".format(minutes)
        if hours == 0:
            return "{}:{}".format(minutes, seconds)
        elif hours < 10:
            hours = "0{}".format(hours)
        return "{}:{}:{}".format(hours, minutes, seconds)

    def __add__(self, other):
        self._counter += other * self._factor
        return self

    def __sub__(self, other):
        self._counter -= other * self._factor
        return self

    def __mul__(self, other):
        self._counter *= other
        return self

    def __truediv__(self, other):
        self._counter /= other
        return self

    def __floordiv__(self, other):
        self._counter //= other
        return self

    def __mod__(self, other):
        self._counter %= other
        return self

    def __and__(self, other):
        self._counter &= other
        return self

    def __xor__(self, other):
        self._counter ^= other
        return self

    def __invert__(self):
        self._counter = ~self._counter
        return self

    def __or__(self, other):
        self._counter |= other
        return self

    def __pow__(self, power):
        self._counter = pow(self._counter, power)
        return self

    def __radd__(self, other):
        self._counter = other * self._factor + self._counter
        return self

    def __rsub__(self, other):
        self._counter = other * self._factor - self._counter
        return self

    def __rmul__(self, other):
        self._counter = other * self._counter
        return self

    def __rtruediv__(self, other):
        self._counter = other / self._counter
        return self

    def __rfloordiv__(self, other):
        self._counter = other // self._counter
        return self

    def __rmod__(self, other):
        self._counter = other % self._counter
        return self

    def __rand__(self, other):
        self._counter = other & self._counter
        return self

    def __rxor__(self, other):
        self._counter = other ^ self._counter
        return self

    def __ror__(self, other):
        self._counter = other | self._counter
        return self

    def __rpow__(self, other):
        self._counter = pow(other, self._counter)
        return self

    def __iadd__(self, other):
        self._counter += other * self._factor
        return self

    def __isub__(self, other):
        self._counter -= other * self._factor
        return self

    def __imul__(self, other):
        self._counter *= other
        return self

    def __itruediv__(self, other):
        self._counter /= other
        return self

    def __ifloordiv__(self, other):
        self._counter //= other
        return self

    def __imod__(self, other):
        self._counter %= other
        return self

    def __ipow__(self, other):
        self._counter **= other
        return self

    def __lt__(self, other):
        return self.seconds() < other

    def __le__(self, other):
        return self.seconds() <= other

    def __eq__(self, other):
        return self.seconds() == other

    def __ne__(self, other):
        return self.seconds() != other

    def __gt__(self, other):
        return self.seconds() > other

    def __ge__(self, other):
        return self.seconds() >= other

    def __neg__(self):
        self._counter = -self._counter
        return self

    def __pos__(self):
        self._counter = +self._counter
        return self

    def __abs__(self):
        self._counter = abs(self._counter)
        return self

    def __round__(self, n=None):
        self._counter = round(self._counter, n)
        return self

    def __str__(self):
        return self.time_string()

    def __repr__(self):
        return self.time_string()

    def __complex__(self):
        return complex(self.seconds())

    def __int__(self):
        return int(self.seconds())

    def __float__(self):
        return float(self.seconds())

    def __bool__(self):
        return self._counter != 0


class Timer(Time):
    def __init__(self, ticks=0, factor=1):
        Time.__init__(self, ticks, factor)
        self._active = False

    def set_active(self, active):
        self._active = active

    def get_active(self):
        return self._active

    def tick(self):
        if self._active:
            self._counter += 1

    def start(self):
        self._active = True

    def stop(self):
        self._active = False

    def toggle_active(self):
        self._active = not self._active

    def reset(self):
        self._counter = 0
        self._active = False


class CountDown(Timer):
    def __init__(self, ticks=0, factor=1, func=None, params=()):
        Timer.__init__(self, ticks, factor)
        self._base = ticks
        self._function = func
        if type(params) in (list, set, tuple):
            self._parameters = params
        else:
            self._parameters = (params,)

    def set_base(self, ticks):
        self._base = ticks
        self._counter = self._base

    def get_base(self):
        return self._base

    def tick(self):
        if self._active:
            self._counter -= 1
            if self._counter <= 0:
                self._counter = 0
                self._active = False
                if self._function is not None:
                    self._function(*self._parameters)

    def start(self):
        self._counter = self._base
        self._active = True

    def reset(self):
        self._counter = self._base
        self._active = False
