"""Demo for battle hero vs creature."""

import sys

from ..hero import HeroFabric
from ..unit import UnitFabric
from ..tui import choice, separating_string, yes_no

ATTACK_TYPE = ['Physical attack', 'Magic attack']


def _main():
    """Entry point."""
    fabric = HeroFabric()
    heroes = fabric.names()
    separating_string()
    hero = choice(heroes, 'Please choice your character!')
    hero = fabric.get_object(hero)
    fabric = UnitFabric()
    units = fabric.names()
    run = True
    while run:
        print('Your character is:')
        separating_string()
        print(hero)
        separating_string()
        enemy = choice(units, 'Please choice your enemy!')
        enemy = fabric.get_object(enemy)
        print('Your enemy is:')
        separating_string()
        print(enemy)
        separating_string()
        rounds = 1
        potential_exp = enemy.health
        while hero.is_alive() and enemy.is_alive():
            print(f'Battle round: {rounds}')
            separating_string()
            option = choice(ATTACK_TYPE, 'Choice attack type')
            if option == 'Physical attack':
                hero.physycal_attack(enemy)
            else:
                hero.magic_attack(enemy)
            enemy.physycal_attack(hero)
            rounds += 1
            separating_string()
            print(hero)
            separating_string()
            print(enemy)
            separating_string()
        if not hero.is_alive():
            print('Unfortunately you are died!')
            separating_string()
            run = False
        else:
            print('You are winner!')
            hero.level_increase(potential_exp)
            run = not yes_no('Do you want to quit?')


if __name__ == '__main__':
    sys.exit(_main())
