import pytest

from logic import Game


class TestGame:
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

    @pytest.mark.parametrize("field, exp", [
        (field1, [[2, 2, 3],
                  [5, 4, 5],
                  [2, 3, 2],
                  [4, 4, 4]]),
        (field2, [[6, 6, 6, 5, 4],
                  [6, 6, 5, 5, 4],
                  [7, 6, 5, 4, 5]])
    ])
    def test_living_neighbours(self, field, exp):
        game = Game.from_boolean_matrix(field)
        for i in range(game.n):
            for j in range(game.m):
                assert exp[i][j] == game.living_neighbours(i, j)

    def test_repr(self):
        game = Game.from_boolean_matrix(self.field1)
        exp = 'XX.\n' \
              '.X.\n' \
              'X.X\n' \
              '...'
        assert exp == str(game)

    @pytest.mark.parametrize("field, exp", [
        (field1, [[True, True, True],
                  [False, False, False],
                  [True, True, True],
                  [False, False, False]]),
        (field3, [[False, False, False, False, False, False],
                  [False, True, True, False, False, False],
                  [False, True, False, False, False, False],
                  [False, False, False, False, True, False],
                  [False, False, False, True, True, False],
                  [False, False, False, False, False, False]])
    ])
    def test_next_state(self, field, exp):
        game = Game.from_boolean_matrix(field)
        game.next_state()
        assert exp == game.boolean_matrix

    def test_str_init(self):
        game = Game.from_str('XX.\n'
                             'XX.\n'
                             'X.X')
        exp = [[True, True, False],
               [True, True, False],
               [True, False, True]]
        assert exp == game.boolean_matrix

    def test_str_init_invalid_inputs(self):
        invalid_strs = ['XXX\nXX\nXXX', 'XXX\nx..\nX.X', 'x\nax']
        for st in invalid_strs:
            with pytest.raises(ValueError):
                Game.from_str(st)

    def test_step_increment(self):
        game = Game.from_boolean_matrix(self.field1)
        assert 0 == game.step
        for i in range(1, 5):
            game.next_state()
            assert i == game.step

    @pytest.mark.parametrize("field, exp", [
        ([[True]], 1),
        ([[False], [True]], 2),
        ([[True], [False]], 1),
        (field1, 339),
    ])
    def test_binary_state(self, field, exp):
        game = Game.from_boolean_matrix(field)
        assert exp == game.state

    def test_cache(self):
        game = Game.from_boolean_matrix(self.field1)
        assert [339] == game.cache
        for i in range(2, 7):
            game.next_state()
            assert game.state == game.cache[-1]
            assert i == len(game.cache)

    def test_custom_characters(self):
        field_str = 'aaad aadd ddaa'
        game = Game.from_str(field_str, alive='a', dead='d', sep=' ')
        exp = [[True, True, True, False],
               [True, True, False, False],
               [False, False, True, True]]
        assert exp == game.boolean_matrix

    @pytest.mark.parametrize("string, alive, dead", [
        ('XXX', 'a', '.'),
        ('..dd', 'X', 'd'),
        ('aaa', 'a', 'a'),
    ])
    def test_custom_characters_invalid(self, string, alive, dead):
        with pytest.raises(ValueError):
            Game.from_str(string, alive=alive, dead=dead)

    @pytest.mark.parametrize("num, n, m, exp", [
        (1023, 3, 3, [[True, True, True],
                      [True, True, True],
                      [True, True, True]]),
        (1, 3, 3, [[True, False, False],
                   [False, False, False],
                   [False, False, False]])
    ])
    def test_from_number(self, num, n, m, exp):
        game = Game(num, n, m)
        assert exp == game.boolean_matrix

    def test_from_number_trivial(self):
        game = Game(12345, 5, 6)
        assert game.state == 12345
        assert (5, 6) == (game.n, game.m)

    @pytest.mark.parametrize("field", [
        field1,
        field2,
        field3,
    ])
    def test_to_json(self, field):
        game = Game.from_boolean_matrix(field)
        game_json = game.to_json()
        assert Game.from_json(game_json) == game
