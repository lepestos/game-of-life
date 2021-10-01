import unittest

from logic import Game


class GameTestCase(unittest.TestCase):
    field1 = [[True, True, False],
              [False, True, False],
              [True, False, True],
              [False, False, False]]

    def test_living_neighbours(self):
        field = [[True, True, False],
                 [False, True, False],
                 [True, False, True],
                 [False, False, False]]
        game = Game(field)
        expected = [[2, 2, 3],
                    [5, 4, 5],
                    [2, 3, 2],
                    [4, 4, 4]]
        for i in range(game.n):
            for j in range(game.m):
                self.assertEqual(expected[i][j],
                                 game.living_neighbours(i, j))

    def test_repr(self):
        field = [[True, True, False],
                 [False, True, False],
                 [True, False, True],
                 [False, False, False]]
        game = Game(field)
        exp = 'XX.\n' \
              '.X.\n' \
              'X.X\n' \
              '...'
        self.assertEqual(exp, str(game))

    def test_next_state(self):
        field = [[True, True, False],
                 [False, True, False],
                 [True, False, True],
                 [False, False, False]]
        exp = [[True, True, True],
               [False, False, False],
               [True, True, True],
               [False, False, False]]
        game = Game(field)
        game.next_state()
        self.assertEqual(exp, game.state)

    def test_str_init(self):
        game = Game.from_str('XX.\n'
                             'XX.\n'
                             'X.X')
        exp = [[True, True, False],
               [True, True, False],
               [True, False, True]]
        self.assertEqual(exp, game.state)

        invalid_strs = ['XXX\nXX\nXXX', 'XXX\nx..\nX.X', 'x\nax']
        for st in invalid_strs:
            with self.assertRaises(ValueError):
                Game.from_str(st)

    def test_step_increment(self):
        game = Game(self.field1)
        self.assertEqual(0, game.step)
        for i in range(1, 5):
            game.next_state()
            self.assertEqual(i, game.step)

    def test_binary_state(self):
        game = Game([[True]])
        self.assertEqual(1, game.binary_state())
        game = Game([[False], [True]])
        self.assertEqual(1, game.binary_state())
        game = Game([[True], [False]])
        self.assertEqual(2, game.binary_state())
        game = Game(self.field1)
        self.assertEqual(3240, game.binary_state())

    def test_cache(self):
        game = Game(self.field1)
        self.assertEqual([3240], game.cache)
        for i in range(2, 7):
            game.next_state()
            self.assertEqual(game.binary_state(), game.cache[-1])
            self.assertEqual(i, len(game.cache))