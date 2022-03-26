"""Maze items."""

import random

from maze_game import kruskal


def _weight():
    """Generate weight for edge."""
    return random.randint(0, 9)


class Room:
    """Maze room."""

    def __init__(self):
        """Constructor."""
        self._monsters = None
        self._weapons = None
        self._players = []
        self._visited = False

    def enter(self, player):
        """Player enters this room."""
        self._players.append(player)
        self._visited = True

    def info(self):
        """Info."""
        if self._monsters:
            monster_name = self._monsters.unit_name
            return f'Monster in the room: {monster_name}'
        if self._weapons:
            weapon_name = self._weapons.name
            return f'Weapon in the room: {weapon_name}'

        return 'There are not monster and weapon in the room'

    def is_free(self):
        """Check if room is free."""
        return self._monsters is None and self._weapons is None

    def has_monster(self):
        """Check if room has a monster."""
        return self._monsters

    def has_weapon(self):
        """Check if room has a weapon."""
        return self._weapons

    def leave(self, player):
        """Player leaves this room."""
        assert player in self._players, 'Player should be inside the room'
        self._players.remove(player)

    def monster_name(self):
        """Get monster name."""
        return self._monsters.unit_name if self._monsters else None

    def weapon_name(self):
        """Get weapon name."""
        return self._weapons.name if self._weapons else None

    def remove_monster(self):
        """Remove monster from room."""
        self._monsters = None

    def remove_weapon(self):
        """Remove weapon from room."""
        self._weapons = None

    def set_weapon(self, weapon):
        """Put weapon into the room."""
        self._weapons = weapon

    def players(self):
        """Players inside the room."""
        return self._players

    def set_monster(self, monster):
        """Set monster."""
        self._monsters = monster

    def visited(self):
        """Check if room is visited."""
        return self._visited


class Maze:
    """Maze."""

    def __init__(self, width, height):
        """Constructor."""
        self.width = width
        self.height = height
        self.rooms = []
        self.tree = []
        self._generate_rooms()

    def _filter_edges(self, edges):
        """Filter edges."""
        self.tree = kruskal.build_tree(edges)

    def _generate_edges(self):
        """Generate edges."""
        edges = []
        for i in range(self.height):
            for j in range(self.width):
                if i+1 < self.height:
                    edge = ((i, j), (i+1, j), _weight())
                    edges.append(edge)
                if j+1 < self.width:
                    edge = ((i, j), (i, j+1), _weight())
                    edges.append(edge)
        edges.sort(key=lambda x: x[2])
        # print(edges)
        return edges

    def _generate_rooms(self):
        """Generate rooms."""
        for _i in range(self.height):
            line = []
            for _j in range(self.width):
                line.append(Room())
            self.rooms.append(line)
        edges = self._generate_edges()
        self._filter_edges(edges)

    def get_random_free_room(self):
        """Random free room."""
        while True:
            col = random.randint(0, self.width-1)
            row = random.randint(0, self.height-1)
            room = self.room(row, col)
            is_start_pos = (col == 0) and (row == 0)
            is_exit_pos = (col == self.width-1) and (row == self.height-1)
            if room.is_free() and not is_start_pos and not is_exit_pos:
                return room

    def has_door(self, room_ids1, room_ids2):
        """Check if door exists."""
        return (room_ids1, room_ids2) in self.tree or \
               (room_ids2, room_ids1) in self.tree

    def room(self, row, col):
        """Get room."""
        return self.rooms[row][col]
