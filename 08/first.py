import weakref
from time import time
from copy import deepcopy
from pprint import pprint
import cProfile
from memory_profiler import profile


class Klass:
    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e


class KlassSlots:
    __slots__ = ('a', 'b', 'c', 'd', 'e')

    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e


class KlassWref:
    def __init__(self, a, b, c, d, e):
        self.a = weakref.ref(a)
        self.b = weakref.ref(b)
        self.c = weakref.ref(c)
        self.d = weakref.ref(d)
        self.e = weakref.ref(e)


class Obj:
    pass


# @profile
def run_kclass(N, results):
    a, b, c, d, e = Obj(), Obj(), Obj(), Obj(), Obj()
    t0 = time()
    objs = [Klass(a, b, c, d, e) for i in range(N)]
    results['create'][Klass.__name__] = (time() - t0) / N

    t0 = time()
    for obj in objs:
        obj.a
        obj.b
        obj.c
        obj.d
        obj.e
    results['read'][Klass.__name__] = (time() - t0) / N


# @profile
def run_kclass_slots(N, results):
    a, b, c, d, e = Obj(), Obj(), Obj(), Obj(), Obj()
    t0 = time()
    objs = [KlassSlots(a, b, c, d, e) for i in range(N)]
    results['create'][KlassSlots.__name__] = (time() - t0) / N

    t0 = time()
    for obj in objs:
        obj.a
        obj.b
        obj.c
        obj.d
        obj.e
    results['read'][KlassSlots.__name__] = (time() - t0) / N


# @profile
def run_kclass_wref(N, results):
    a, b, c, d, e = Obj(), Obj(), Obj(), Obj(), Obj()
    t0 = time()
    objs = [KlassWref(a, b, c, d, e) for i in range(N)]
    results['create'][KlassWref.__name__] = (time() - t0) / N

    t0 = time()
    for obj in objs:
        obj.a()
        obj.b()
        obj.c()
        obj.d()
        obj.e()
    results['read'][KlassWref.__name__] = (time() - t0) / N


def main():
    N = 10**6
    results = {'create': {}, 'read': {}}
    run_kclass(N, results)
    run_kclass_slots(N, results)
    run_kclass_wref(N, results)

    print(f'{N=}')
    pprint(results)


if __name__ == '__main__':
    cProfile.run('main()')
    # main()

