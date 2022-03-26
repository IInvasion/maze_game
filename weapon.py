"""Weapon tools."""

from maze_game.fabric import Fabric

TYPES = ['knight', 'wizard', 'shield', 'elite']

INT_KEYS = {'attack', 'defense', 'power', 'mana', 'level'}
VALID_KEYS = INT_KEYS | {'type', }


class WeaponFabric(Fabric):
    """Weapon fabric."""

    def __init__(self):
        """Constructor."""
        Fabric.__init__(self, 'weapons.ini')

    def _process_section(self, data, section):
        """Initialize."""
        weapon = Weapon(section)
        for key, value in data.items():
            assert key in VALID_KEYS, f'Invalid key {key} in {section}'
            weapon.__dict__[key] = \
                int(value) if key in INT_KEYS else value

        self.storage[section] = weapon


class Weapon:
    """Weapon."""

    def __init__(self, name):
        """Constructor."""
        self.attack = 0
        self.defense = 0
        self.power = 0
        self.mana = 0
        self.type = None
        self.level = 0
        self.name = name

    def __str__(self):
        """Cast to string."""
        return f'{self.name}\n    A: {self.attack}. D: {self.defense}. ' + \
               f'P: {self.power}. M: {self.mana}\n    ' + \
               f'L: {self.level}. T: {self.type}'

    def validate(self):
        """Validate weapon."""
        assert self.type in TYPES and self.level > 0, f'{self.name}'


if __name__ == '__main__':
    def _test():
        """Test."""
        fabric = WeaponFabric()
        for weapon in fabric.storage.values():
            print(weapon)
            weapon.validate()
    _test()
