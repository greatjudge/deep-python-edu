class CustomList(list):
    def __eq__(self, other):
        return sum(self) == sum(other)

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __qt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __add__(self, other):
        self_size, other_size = len(self), len(other)
        return self.__class__([(self[i] if i < self_size else 0) +
                               (other[i] if i < other_size else 0)
                               for i in range(max(self_size,
                                                  other_size))
                               ])

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        self_size, other_size = len(self), len(other)
        return self.__class__([(self[i] if i < self_size else 0) -
                               (other[i] if i < other_size else 0)
                               for i in range(max(self_size,
                                                  other_size))
                               ])

    def __rsub__(self, other):
        tmp = self - other
        return self.__class__([0] * len(tmp)) - tmp

    def __str__(self):
        return f'{super().__str__()}, {sum(self)}'
