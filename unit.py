"""Unit tools."""

from maze_game.fabric import Fabric

VALID_KEYS = {'attack', 'defense', 'health', 'damage'}


class UnitFabric(Fabric):
    """Unit fabric."""

    def __init__(self):
        """Constructor."""
        Fabric.__init__(self, 'units.ini')

    def _process_section(self, data, section):
        """Process parser section."""
        unit = Unit(section)
        for key, value in data.items():
            assert key in VALID_KEYS, f'Invalid {key} in {section}'
            unit.__dict__[key] = int(value) if value != 'inf' \
                else float(value)
        unit.max_health = unit.health

        self.storage[section] = unit


class Unit:
    """Unit."""

    def __init__(self, name):
        """Constructor."""
        self.attack = 0
        self.defense = 0
        self.health = 0
        self.damage = 0
        self.max_health = 0
        self.unit_name = name
        self.weapons = [None, None]

    def __str__(self):
        """Cast to string."""
        return f'{self.unit_name}\n' + \
               f'  Attack: {self.attack:4}' + \
               f'  Defense: {self.defense:4}\n' + \
               f'  Health: {self.health:4}' + \
               f'  Max HP:  {self.max_health:4}\n' + \
               f'  Damage: {self.damage:4}'

    def total_attack(self):
        """Evaluate additional attack from artifacts."""
        bonus_attack = 0
        for weapon in self.weapons:
            if weapon is not None:
                bonus_attack += weapon.attack
        return self.attack + bonus_attack

    def total_defense(self):
        """Evaluate additional defense from artifacts."""
        bonus_defense = 0
        for weapon in self.weapons:
            if weapon is not None:
                bonus_defense += weapon.defense
        return self.defense + bonus_defense

    def physycal_attack(self, target):
        """Attack enemy using physical damage."""
        modifier = 0.05
        attack = self.total_attack()
        defense = self.total_defense()
        if attack > defense:
            modifier *= (attack - defense)
            modifier += 1.0
        else:
            modifier *= (defense - attack)
            modifier += 1.0
            modifier = 1.0 / modifier
        physycal_damage = int(self.damage * modifier)
        if physycal_damage < 1:
            physycal_damage = 1
        target.health -= physycal_damage
        if target.health < 0:
            target.health = 0

    def is_alive(self):
        """Check unit state alive."""
        return self.health > 0

    def pick_weapon(self, weapon, slot_number):
        """Pick weapon."""
        assert slot_number in [0, 1], f'Wrong slot number in {self.unit_name}'
        self.weapons[slot_number] = weapon

    def show_weapons(self):
        """Print weapons information for user."""
        if self.weapons[0] is None and self.weapons[1] is None:
            print(f'{self.unit_name} has no weapons')
        else:
            for i in range(2):
                if self.weapons[i] is not None:
                    print(f'Weapon in {i + 1} hand is {self.weapons[i].name}')


if __name__ == '__main__':
    from maze_game.weapon import WeaponFabric

    def _test():
        fabric = UnitFabric()
        unit = fabric.get_object('Skeleton')
        print(unit)
        weapon_fabric = WeaponFabric()
        weapon = weapon_fabric.get_object('Sword')
        unit.pick_weapon(weapon, 0)
        unit.show_weapons()
        print(unit.total_attack())
        print(unit.total_defense())
    _test()
