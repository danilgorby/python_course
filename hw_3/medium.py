import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin
from numbers import Number


def spaces_num(max_len, val):
    return max_len - len(str(val)) + 1


class StrMixin:
    def __str__(self,):
        max_num_len = [max([len(str(self.value[j][i])) for j in range(self.n)]) for i in range(self.m)]
        res = [[0] * self.m for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                res[i][j] = ' ' * spaces_num(max_num_len[j], self.value[i][j]) + str(self.value[i][j])

        lines = [' '.join(res[i]) for i in range(self.n)]
        return '\n'.join(lines)


class SaveMixin:
    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))

class ValueMixin:
    def __init__(self, values=[[]]):
        if len(values) == 1 and values[0] == []:
            self._n = 0
        else:
            self._n = len(values)
        self._m = len(values[0])
        self._value = np.asarray(values)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, val):
        self._n = val

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, val):
        self._m = val


class MixinsMatrix(ValueMixin, NDArrayOperatorsMixin, SaveMixin, StrMixin):

    _HANDLED_TYPES = (np.ndarray, Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (MixinsMatrix,)):
                return NotImplemented

        inputs = tuple(x.value if isinstance(x, MixinsMatrix) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.value if isinstance(x, MixinsMatrix) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)
