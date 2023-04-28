import cProfile, pstats
from cProfile import Profile
from typing import Callable


class Wrapper:
    def __init__(self, profiler: Profile, func: Callable):
        self.profiler = profiler
        self.func = func
        self.__name__ = func.__name__

    def __call__(self, *args, **kwargs):
        self.profiler.enable()
        res = self.func(*args, **kwargs)
        self.profiler.disable()
        return res

    def print_stat(self):
        stats = pstats.Stats(self.profiler).sort_stats('tottime')
        stats.print_stats()


def profile_deco(func):
    return Wrapper(Profile(), func)


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


add(1, 2)
add(4, 5)
sub(4, 5)


add.print_stat()  # выводится результат профилирования суммарно по всем вызовам функции add (всего два вызова)
sub.print_stat()  # выводится результат профилирования суммарно по всем вызовам функции sub (всего один вызов)
