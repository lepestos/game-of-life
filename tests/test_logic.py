import unittest

from logic import Game


class GameTestCase(unittest.TestCase):
    field1 = [[True, True, False],
              [False, True, False],
              [True, False, True],
              [False, False, False]]
    field2 = [[True, True, False, False, True],
              [True, True, True, False, True],
              [False, True, True, True, False]]
    field3 = [[False, False, False, False, False, False],
              [False, True, True, False, False, False],
              [False, True, True, False, False, False],
              [False, False, False, True, True, False],
              [False, False, False, True, True, False],
              [False, False, False, False, False, False]]

    def test_living_neighbours(self):
        game = Game.from_boolean_matrix(self.field1)
        exp = [[2, 2, 3],
               [5, 4, 5],
               [2, 3, 2],
               [4, 4, 4]]
        for i in range(game.n):
            for j in range(game.m):
                self.assertEqual(exp[i][j],
                                 game.living_neighbours(i, j))
        game = Game.from_boolean_matrix(self.field2)
        exp = [[6, 6, 6, 5, 4],
               [6, 6, 5, 5, 4],
               [7, 6, 5, 4, 5]]
        for i in range(game.n):
            for j in range(game.m):
                self.assertEqual(exp[i][j],
                                 game.living_neighbours(i, j))

    def test_repr(self):
        field = [[True, True, False],
                 [False, True, False],
                 [True, False, True],
                 [False, False, False]]
        game = Game.from_boolean_matrix(field)
        exp = 'XX.\n' \
              '.X.\n' \
              'X.X\n' \
              '...'
        self.assertEqual(exp, str(game))

    def test_next_state(self):
        game = Game.from_boolean_matrix(self.field1)
        game.next_state()
        exp = [[True, True, True],
               [False, False, False],
               [True, True, True],
               [False, False, False]]
        self.assertEqual(exp, game.boolean_matrix)
        game = Game.from_boolean_matrix(self.field3)
        game.next_state()
        exp = [[False, False, False, False, False, False],
               [False, True, True, False, False, False],
               [False, True, False, False, False, False],
               [False, False, False, False, True, False],
               [False, False, False, True, True, False],
               [False, False, False, False, False, False]]
        self.assertEqual(exp, game.boolean_matrix)
        game.next_state()
        self.assertEqual(self.field3, game.boolean_matrix)


    def test_str_init(self):
        game = Game.from_str('XX.\n'
                             'XX.\n'
                             'X.X')
        exp = [[True, True, False],
               [True, True, False],
               [True, False, True]]
        self.assertEqual(exp, game.boolean_matrix)

        invalid_strs = ['XXX\nXX\nXXX', 'XXX\nx..\nX.X', 'x\nax']
        for st in invalid_strs:
            with self.assertRaises(ValueError):
                Game.from_str(st)

    def test_step_increment(self):
        game = Game.from_boolean_matrix(self.field1)
        self.assertEqual(0, game.step)
        for i in range(1, 5):
            game.next_state()
            self.assertEqual(i, game.step)

    def test_binary_state(self):
        game = Game.from_boolean_matrix([[True]])
        self.assertEqual(1, game.state)
        game = Game.from_boolean_matrix([[False], [True]])
        self.assertEqual(2, game.state)
        game = Game.from_boolean_matrix([[True], [False]])
        self.assertEqual(1, game.state)
        game = Game.from_boolean_matrix(self.field1)
        self.assertEqual(339, game.state)

    def test_cache(self):
        game = Game.from_boolean_matrix(self.field1)
        self.assertEqual([339], game.cache)
        for i in range(2, 7):
            game.next_state()
            self.assertEqual(game.state, game.cache[-1])
            self.assertEqual(i, len(game.cache))

    def test_custom_characters(self):
        field_str = 'aaad aadd ddaa'
        game = Game.from_str(field_str, alive='a', dead='d', sep=' ')
        exp = [[True, True, True, False],
               [True, True, False, False],
               [False, False, True, True]]
        self.assertEqual(exp, game.boolean_matrix)

        with self.assertRaises(ValueError):
            Game.from_str('XXX', alive='a')
        with self.assertRaises(ValueError):
            Game.from_str('..dd', dead='d')
        with self.assertRaises(ValueError):
            Game.from_str('aaa', alive='a', dead='a')

    def test_from_number(self):
        game = Game(1023, 3, 3)
        exp = [[True, True, True],
               [True, True, True],
               [True, True, True]]
        self.assertEqual(exp, game.boolean_matrix)
        game = Game(1, 3, 3)
        exp = [[True, False, False],
               [False, False, False],
               [False, False, False]]
        self.assertEqual(exp, game.boolean_matrix)
        game = Game(12345, 5, 6)
        self.assertEqual(game.state, 12345)
        self.assertEqual((5, 6), (game.n, game.m))

    def test_to_json(self):
        for field in [self.field1, self.field2, self.field3]:
            game = Game.from_boolean_matrix(field)
            game_json = game.to_json()
            self.assertEqual(Game.from_json(game_json), game)
