def spaces_num(max_len, val):
    return max_len - len(str(val)) + 1


class StrMixin:
    def __str__(self,):
        max_num_len = [max([len(str(self.values[j][i])) for j in range(self.n)]) for i in range(self.m)]
        res = [[0] * self.m for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                res[i][j] = ' ' * spaces_num(max_num_len[j], self.values[i][j]) + str(self.values[i][j])

        lines = [' '.join(res[i]) for i in range(self.n)]
        return '\n'.join(lines)


class SaveMixin:
    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))

class HashMixin:
    def __eq__(self, b):
        return self.values == b.values

    def __hash__(self):
        """
        1. Считаем сумму значениц в каждой строке матрицы
        2. Полученные значения умножаются на номера строк
        3. Всё суммируется в переменную `code`
        4. Складываем остаток от деления `code` на 100
           и целую часть от деления `code` на 100
        """
        code = sum((i + 1) * sum(line) for i, line in enumerate(self.values))
        hash_code = code % 100 + code // 100
        return int(hash_code)


class HashMixinsMatrix(StrMixin, SaveMixin, HashMixin):
    cash_dict = dict()

    def __init__(self, value=[[]], matmul_cache=False):
        super().__init__()
        self.values = [[0] * len(value[0]) for _ in range(len(value))]
        for i in range(len(value)):
            for j in range(len(value[0])):
                self.values[i][j] = value[i][j]
        self.n = len(self.values)
        self.m = len(self.values[0])
        # self.__hash__ == HashMixin.__hash__
        self.matmul_cache = matmul_cache

    def __getitem__(self, ij):
        i, j = ij
        return self.values[i][j]

    def __add__(self, b):
        if self.n != b.n or self.m != b.m:
            raise Exception("Wrong matrix dimensions")
        res = [[0] * self.n for _ in range(self.m)]
        for i in range(self.n):
            for j in range(self.m):
                res[i][j] = self[i, j] + b[i, j]
        return HashMixinsMatrix(res)

    def __mul__(self, b):
        if self.n != b.n or self.m != b.m:
            raise Exception("Wrong matrix dimensions")
        res = [[0] * self.n for _ in range(self.m)]
        for i in range(self.n):
            for j in range(self.m):
                res[i][j] = self[i, j] * b[i, j]
        return HashMixinsMatrix(res)

    def __matmul__(self, b):
        if self.matmul_cache:
            key = (hash(self), hash(b))
            if key not in self.cash_dict:
                res = matmul_function(self, b)
                self.cash_dict[key] = res
            else:
                res = self.cash_dict[key]
        else:
            res = matmul_function(self, b)

        return res


def matmul_function(a, b):
    if a.m != b.n:
        raise Exception("Wrong matrix dimensions")
    res = [[0] * a.n for _ in range(b.m)]
    for i in range(a.n):
        for j in range(b.m):
            val = 0
            for k in range(b.n):
                val += a[i, k] * b[k, j]
            res[i][j] = val
    return HashMixinsMatrix(res)
