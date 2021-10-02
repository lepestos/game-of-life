from wtforms.validators import ValidationError

from logic import Game


class GameFieldValidator:
    def __init__(self, alive: str ='X', dead: str='.', sep: str='\n'):
        if len(alive) != 1 or len(dead) != 1:
            raise ValueError('Dead and alive cells are depicted by precisely 1 character')
        self.alive = alive
        self.dead = dead
        self.sep = sep

    def __call__(self, form, field):
        try:
            Game.from_str(field.data, self.alive, self.dead, self.sep)
        except ValueError:
            raise ValidationError("Invalid input")