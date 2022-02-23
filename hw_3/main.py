from hw_3.easy import Matrix
from hw_3.medium import MixinsMatrix
from hw_3.hard import HashMixinsMatrix
import numpy as np

if __name__ == "__main__":
    np.random.seed(seed=0)
    a = np.random.randint(0, 10, (10, 10))
    b = np.random.randint(0, 10, (10, 10))

    # easy
    A = Matrix(a)
    B = Matrix(b)
    with open('./artifacts/easy/matrix+.txt', 'w') as f:
        f.write(str(A + B))
    with open('./artifacts/easy/matrix*.txt', 'w') as f:
        f.write(str(A * B))
    with open('./artifacts/easy/matrix@.txt', 'w') as f:
        f.write(str(A @ B))

    # medium
    A = MixinsMatrix(a)
    B = MixinsMatrix(b)
    (A + B).save('./artifacts/medium/matrix+.txt')
    (A * B).save('./artifacts/medium/matrix*.txt')
    (A @ B).save('./artifacts/medium/matrix@.txt')

    # hard
    A = HashMixinsMatrix([[1, 2], [3, 4]])
    B = HashMixinsMatrix([[1, 1], [1, 1]])
    C = HashMixinsMatrix([[100, 200], [300, 400]])
    D = HashMixinsMatrix([[1, 1], [1, 1]])
    AB = A @ B
    CD = C @ D

    A.save('./artifacts/hard/A.txt')
    B.save('./artifacts/hard/B.txt')
    C.save('./artifacts/hard/C.txt')
    D.save('./artifacts/hard/D.txt')
    AB.save('./artifacts/hard/AB.txt')
    CD.save('./artifacts/hard/CD.txt')

    assert (hash(A) == hash(C)) and (A != C) and (B == D) and (AB != CD)

    # collision
    A = HashMixinsMatrix([[1, 2], [3, 4]], matmul_cache=True)
    B = HashMixinsMatrix([[1, 1], [1, 1]], matmul_cache=True)
    C = HashMixinsMatrix([[100, 200], [300, 400]], matmul_cache=True)
    D = HashMixinsMatrix([[1, 1], [1, 1]], matmul_cache=True)

    print(A @ B == C @ D)  # True

    if hash(AB) == hash(CD):
        with open('./artifacts/hard/hash.txt', 'w') as f:
            f.write(str(hash(AB)))
