from itertools import zip_longest


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
        return self.__class__([slf + oth for slf, oth
                               in zip_longest(self, other, fillvalue=0)])

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self.__class__([slf - oth for slf, oth
                               in zip_longest(self, other, fillvalue=0)])

    def __rsub__(self, other):
        tmp = self - other
        return self.__class__([0] * len(tmp)) - tmp

    def __str__(self):
        return f'{super().__str__()}, {sum(self)}'
