from copy import deepcopy
from itertools import product
from typing import List


class Game:
    def __init__(self, initial_state: List[List[bool]]):
        self.state = deepcopy(initial_state)
        self.step = 0
        self.n = len(self.state)
        self.m = len(self.state[0])
        self.cache = []
        self.cache_state()

    def __repr__(self):
        return '\n'.join(''.join('X' if s is True else '.' for s in row) for row in self.state)

    @classmethod
    def from_str(cls, str_state: str, alive: str='X',
                 dead: str='.', sep: str = '\n'):
        cls.validate_str_state(str_state, alive, dead, sep)
        state = [[s == alive for s in row]
                 for row in str_state.split(sep)]
        return cls(state)

    @classmethod
    def from_number(cls, number: int, n: int, m: int):
        state = [[number & (1 << (i*m + j)) > 0 for j in range(m)] for i in range(n)]
        return cls(state)

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
        res = [[False for _ in range(self.m)] for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                if self.state[i][j]:
                    res[i][j] = self.living_neighbours(i, j) in {2, 3}
                else:
                    res[i][j] = self.living_neighbours(i, j) == 3
        self.state = res
        self.step += 1
        self.cache_state()

    def living_neighbours(self, i: int, j: int) -> int:
        return sum(self.state[(i + x) % self.n][(j + y) % self.m]
                   for x, y in product(range(-1, 2), range(-1, 2))
                   if (x, y) != (0, 0))

    def binary_state(self) -> int:
        b = 0
        for i, row in enumerate(self.state):
            for j, x in enumerate(row):
                b += (x << (i * self.m + j))
        return b

    def cache_state(self):
        self.cache.append(self.binary_state())
