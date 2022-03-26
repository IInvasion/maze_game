#!/usr/env/bin python3
# -*- coding: utf-8 -*-

"""Maze filler."""

from maze_game.fabric import Fabric

VALID_KEYS = {'count'}


class MonsterGenerator(Fabric):
    """Maze filler for monsters."""
    def __init__(self):
        """Constructor."""
        Fabric.__init__(self, 'units_meta.ini')

    def _process_section(self, data, section):
        """Process parser section."""
        unit_data = dict()
        for key, value in data.items():
            assert key in VALID_KEYS, f'Invalid {key} in {section}'
            unit_data[key] = value

        self.storage[section] = unit_data

    def fill(self, maze, unit_fabric):
        """Fill maze by monsters."""
        for name in self.names():
            data = self.get_object(name)
            for _i in range(int(data['count'])):
                room = maze.get_random_free_room()
                unit = unit_fabric.get_object(name)
                room.set_monster(unit)


class WeaponGenerator(Fabric):
    """Maze filler for weapons."""
    def __init__(self):
        """Constructor."""
        Fabric.__init__(self, 'weapons_meta.ini')

    def _process_section(self, data, section):
        """Process parser section."""
        weapon_data = dict()
        for key, value in data.items():
            assert key in VALID_KEYS, f'Invalid {key} in {section}'
            weapon_data[key] = value

        self.storage[section] = weapon_data

    def fill(self, maze, weapon_fabric):
        """Fill maze by weapons."""
        for name in self.names():
            data = self.get_object(name)
            for _i in range(int(data['count'])):
                room = maze.get_random_free_room()
                weapon = weapon_fabric.get_object(name)
                room.set_weapon(weapon)
