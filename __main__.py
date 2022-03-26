"""Entry point."""

import sys
from maze_game.game import Game
from maze_game.tui import choice
from maze_game.hero import HeroFabric
from maze_game.render import clear


def _main():
    """Entry point."""
    fabric = HeroFabric()
    clear()
    hero = choice(fabric.names(), 'Choice your hero:')
    hero = fabric.get_object(hero)
    game = Game(20, 10, hero)
    return game.start_loop()


if __name__ == '__main__':
    sys.exit(_main())
