from itertools import product
from typing import List


class Game:
    def __init__(self, state, n, m):
        self.state = state
        self.n = n
        self.m = m
        self.step = 0
        self.cache = []
        self.cache_state()

    def __repr__(self):
        bm = self.boolean_matrix
        return '\n'.join(''.join('X' if s is True else '.' for s in row) for row in bm)

    @classmethod
    def from_str(cls, str_state: str, alive: str='X',
                 dead: str='.', sep: str = '\n'):
        cls.validate_str_state(str_state, alive, dead, sep)
        state = [[s == alive for s in row]
                 for row in str_state.split(sep)]
        return cls.from_boolean_matrix(state)

    @classmethod
    def from_boolean_matrix(cls, matrix: List[List[bool]]):
        b = 0
        n = len(matrix)
        m = len(matrix[0])
        for i, row in enumerate(matrix):
            for j, x in enumerate(row):
                b += (x << (i * m + j))
        return cls(b, n, m)

    @property
    def boolean_matrix(self):
        return [[self.state & (1 << (i*self.m + j)) > 0
                 for j in range(self.m)] for i in range(self.n)]

    @staticmethod
    def validate_str_state(state: str, alive: str, dead: str, sep: str):
        rows = state.split(sep)
        l = len(rows[0])
        if alive == dead:
            raise ValueError("Characters for dead and alive cells must be different")
        for row in rows:
            if len(row) != l:
                raise ValueError("The field is not rectangular")
            for char in row:
                if char not in [alive, dead]:
                    raise ValueError(f"Cannot read {char}: only '{alive}' and '{dead}' are allowed")

    def next_state(self):
        res = 0
        for i in range(self.n):
            for j in range(self.m):
                if self.state & (1 << (i * self.m + j)):
                    res += ((1 << (i * self.m + j))
                            * (self.living_neighbours(i, j) in {2, 3}))
                else:
                    res += ((1 << (i * self.m + j))
                            * (self.living_neighbours(i, j) == 3))
        self.state = res
        self.step += 1
        self.cache_state()

    def living_neighbours(self, i: int, j: int) -> int:
        mask = sum(1 << (((i + x) % self.n) * self.m + ((j + y) % self.m))
                   for x, y in product(range(-1, 2), range(-1, 2))
                   if (x, y) != (0, 0))
        neighbours = self.state & mask
        return sum(neighbours & (1 << k) > 0 for k in range(self.n * self.m))


    def cache_state(self):
        self.cache.append(self.state)
