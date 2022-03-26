"""Character tools."""

import random

from configparser import ConfigParser
from maze_game.fabric import config_path
from maze_game.unit import Unit
from maze_game.fabric import Fabric
from maze_game import tui

VALID_KEYS = {'attack',
              'defense',
              'health',
              'damage',
              'mana',
              'power'}


class HeroFabric(Fabric):
    """Hero fabric."""

    def __init__(self):
        """Constructor."""
        Fabric.__init__(self, 'heroes.ini')

    def _process_section(self, data, section):
        """Process section."""
        hero = Hero(section)
        for key, value in data.items():
            assert key in VALID_KEYS, f'Invalid {key} in {section}'
            hero.__dict__[key] = int(value)
        hero.max_health = hero.health
        hero.max_mana = hero.mana

        self.storage[section] = hero


class Hero(Unit):
    """Player hero."""

    def __init__(self, name):
        """Constructor."""
        Unit.__init__(self, name)
        self.mana = 0
        self.max_mana = 0
        self.power = 0
        self.level = 1
        self.exp = 0
        self._pos = None
        parser = ConfigParser()
        parser.read(config_path('increase_prob.ini'))
        self.increase_prob = parser[name]

    def position(self):
        """Player's position."""
        return self._pos

    def set_position(self, pos):
        """Set position."""
        self._pos = pos

    def total_power(self):
        """Evaluate additional attack from artifacts."""
        bonus_power = 0
        for weapon in self.weapons:
            if weapon:
                bonus_power += weapon.power
        return self.power + bonus_power

    def magic_attack(self, target):
        """Attack enemy using magic damage."""
        if (self.mana == 0 or self.power == 0):
            tui.separating_string('ATTACK FAILED! Not enough mana or magic power!')
        else:
            if target.unit_name == 'Dwarf':
                magic_damage = 1
            else:
                magic_damage = self.total_power() * 10
            target.health -= magic_damage
            self.mana -= 1
            if target.health < 0:
                target.health = 0

    def level_increase(self, exp):
        """Increase hero level."""
        levels = exp // 10
        self.exp += exp % 10
        while levels > 0:
            tui.separating_string('Congratulations! Your level increased!')
            for key, value in self.increase_prob.items():
                assert key in VALID_KEYS, f'Invalid {key} in {self.unit_name}'
                rand = random.uniform(0, 1.0)
                if rand < float(value):
                    if key != 'mana':
                        self.__dict__[key] += 1
                        tui.separating_string(f'{key} increased'.capitalize())
                    else:
                        self.max_mana += 1
                        tui.separating_string('Mana increased')
            self.level += 1
            self.max_health += 10
            self.health = self.max_health
            self.mana = self.max_mana
            levels -= 1

    def pick_weapon(self, weapon, slot_number):
        """Pick weapon."""
        assert slot_number in [0, 1], f'Wrong slot number in {self.unit_name}'
        current_weapon = self.weapons[slot_number]
        if current_weapon:
            self.max_mana -= current_weapon.mana
        self.weapons[slot_number] = weapon
        self.max_mana += weapon.mana

    def can_use(self, weapon):
        """Check if hero can use weapon."""
        return self.level >= weapon.level

    def __str__(self):
        """Cast to string."""
        return super().__str__() + \
            f'  Level:   {self.level:4}\n' + \
            f'  Exp:    {self.exp:4}' + \
            f'  Power:   {self.power:4}\n' + \
            f'  Mana:   {self.mana:4}' + \
            f'  Max MP:  {self.max_mana:4}'


if __name__ == '__main__':
    from maze_game.weapon import WeaponFabric

    def _test():
        fabric = HeroFabric()
        warrior = fabric.get_object('Knight')
        print(warrior)
        weapon_fabric = WeaponFabric()
        weapon = weapon_fabric.get_object('Titan\'s shield')
        warrior.pick_weapon(weapon, 0)
        print(warrior)
        print(warrior.total_power())
        weapon = weapon_fabric.get_object('Archangel flame-bladed sword')
        warrior.pick_weapon(weapon, 0)
        print(warrior)
        print(warrior.total_power())
        weapon = weapon_fabric.get_object('Short sword')
        warrior.pick_weapon(weapon, 0)
        print(warrior)
        print(warrior.total_attack(), warrior.total_defense())
    _test()
