"""Test module for battles between creatures."""

import sys

from ..unit import UnitFabric
from ..tui import choice, separating_string


def _main():
    """Entry point."""
    fabric = UnitFabric()
    units = fabric.names()
    unit_1 = choice(units)
    unit_1 = fabric.get_object(unit_1)
    separating_string()
    print(unit_1)
    separating_string()
    unit_2 = choice(units)
    unit_2 = fabric.get_object(unit_2)
    separating_string()
    print(unit_2)
    separating_string()
    rounds = 0
    while (unit_1.is_alive() and unit_2.is_alive()):
        unit_1.physycal_attack(unit_2)
        unit_2.physycal_attack(unit_1)
        rounds += 1
        print('Round', rounds)
        print(unit_1)
        print(unit_2)
        separating_string()
    if unit_1.is_alive():
        print('First unit won:', unit_1.unit_name)
    elif unit_2.is_alive():
        print('Second unit won:', unit_2.unit_name)
    else:
        print('Both units are dead')
    print('Number of battle rounds:', rounds)


if __name__ == '__main__':
    sys.exit(_main())
