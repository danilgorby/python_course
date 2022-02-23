class Matrix():
    def __init__(self, value=[[]]):
        super().__init__()
        self.values = [[0] * len(value[0]) for _ in range(len(value))]
        for i in range(len(value)):
            for j in range(len(value[0])):
                self.values[i][j] = value[i][j]
        self.n = len(self.values)
        self.m = len(self.values[0])

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
        return Matrix(res)

    def __mul__(self, b):
        if self.n != b.n or self.m != b.m:
            raise Exception("Wrong matrix dimensions")
        res = [[0] * self.n for _ in range(self.m)]
        for i in range(self.n):
            for j in range(self.m):
                res[i][j] = self[i, j] * b[i, j]
        return Matrix(res)

    def __matmul__(self, b):
        if self.m != b.n:
            raise Exception("Wrong matrix dimensions")
        res = [[0] * self.n for _ in range(b.m)]
        for i in range(self.n):
            for j in range(b.m):
                val = 0
                for k in range(b.n):
                    val += self[i, k] * b[k, j]
                res[i][j] = val
        return Matrix(res)

    def __str__(self):
        res = [[0] * self.n for _ in range(self.m)]
        for i in range(self.n):
            for j in range(self.m):
                res[i][j] = str(self[i, j])

        lines = [' '.join(res[i]) for i in range(self.n)]
        return '\n'.join(lines)
