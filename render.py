"""Render utilities."""

import os
from maze_game.tui import separating_string

VERTICAL = '\u2551'  # ||
VERTICAL_HOLE = ' '
HORIZONTAL = '\u2550' * 3  # =
HORIZONTAL_HOLE = '\u2550 \u2550'
HORIZONTAL_HIDDEN = '\u2550'

LEFT_NODE = '\u2560'   # ||=
RIGHT_NODE = '\u2563'  # =||

TOP_LEFT = '\u2554'   # r
TOP_NODE = '\u2566'   # T
TOP_RIGHT = '\u2557'  #

BOTTOM_LEFT = '\u255A'   # L
BOTTOM_NODE = '\u2569'   # _L
BOTTOM_RIGHT = '\u255D'  # _|

CROSS = '\u256C'  # +
EMPTY = ' ' * 3
PLAYER = ' P '

FOG_1 = '-'
FOG_2 = FOG_1 * 3
HAS_CONTENT = ' # '


def _draw_room(room):
    """Draw room."""
    if room.players():
        return PLAYER
    if room.visited():
        if room.is_free():
            return EMPTY
        if room.has_monster():
            symbol = 'M'
            return f' {symbol} '
        if room.has_weapon():
            symbol = 'A'
            return f' {symbol} '
    return FOG_2


def clear():
    """Clear screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def player_weapons_info(player):
    """Print player weapons."""
    print(player)
    separating_string()
    hands = ['right', 'left']
    for idx, hand in enumerate(hands):
        if player.weapons[idx] is not None:
            print(f'Weapon in {hand} hand is {player.weapons[idx]}')
        print(f'No weapon in {hand} hand')
    separating_string()


def monster_info(monster):
    """Print room monster."""
    print('Monster in the room!')
    print(monster)


def weapon_info(weapon):
    """Print room weapon."""
    print('Weapon in the room!')
    print(weapon)
    separating_string()


def battle_info(battle):
    """Print battle."""
    clear()
    if battle.rounds == 1:
        separating_string('HERO vs MONSTER! FIGHT!!!')
    separating_string(f'BATTLE ROUND: {battle.rounds}')
    separating_string('Your character is:')
    separating_string(battle.hero)
    separating_string('Your enemy is:')
    separating_string(battle.enemy)


class Render:
    """Render."""

    def __init__(self, maze, monster_filler, weapon_filler):
        """Constructor."""
        self.maze = maze
        self.monster_filler = monster_filler
        self.weapon_filler = weapon_filler
        self.top_wall = None
        self.room_layers = []
        self.internal_walls = []
        self.bottom_wall = None
        self._initialize()

    def _check_visited(self, *positions):
        """Check if any room is visited."""
        for position in positions:
            if self.maze.room(*position).visited():
                return True
        return False

    def _create_room_layer(self, layer):
        """Create room layer."""
        width = self.maze.width
        tiles = [VERTICAL]
        for i in range(width-1):
            room = self.maze.room(layer, i)
            tiles.append(_draw_room(room))
            # check spaces between rooms
            next_room = self.maze.room(layer, i+1)
            drawn = room.visited() or next_room.visited()
            if drawn:
                drawn = not self.maze.has_door((layer, i), (layer, i+1))
                tile = VERTICAL if drawn else VERTICAL_HOLE
            else:
                tile = FOG_1
            tiles.append(tile)
        room = self.maze.room(layer, width-1)
        tiles.append(_draw_room(room))
        tiles.append(VERTICAL)
        return ''.join(tiles)

    def _create_internal_wall(self, layer):
        """Create internal wall."""
        width = self.maze.width
        drawn = self._check_visited((layer, 0), (layer+1, 0))
        tiles = [LEFT_NODE if drawn else VERTICAL]
        for i in range(width):
            drawn = self._check_visited((layer, i), (layer+1, i))
            if drawn:
                door = self.maze.has_door((layer, i), (layer+1, i))
                tile = HORIZONTAL_HOLE if door else HORIZONTAL
            else:
                tile = FOG_2
            tiles.append(tile)
            if i != width - 1:
                if drawn:
                    tiles.append(CROSS)
                else:
                    drawn = self._check_visited((layer, i+1), (layer+1, i+1))
                    tiles.append(CROSS if drawn else FOG_1)
            else:
                tiles.append(RIGHT_NODE if drawn else VERTICAL)
        return ''.join(tiles)

    def _initialize(self):
        """Initialize layers."""
        self._init_top_wall()
        height = self.maze.height
        for layer in range(height-1):
            self._init_room_layer(layer)
            self._init_internal_wall(layer)
        self._init_room_layer(height-1)
        self._init_bottom_wall()

    def _init_top_wall(self):
        """Initialize top wall of maze."""
        width = self.maze.width
        tiles = [TOP_LEFT]
        for i in range(width-1):
            drawn = self._check_visited((0, i), (0, i+1))
            tile = TOP_NODE if drawn else HORIZONTAL_HIDDEN
            tiles.append(tile)
        tiles.append(TOP_RIGHT)
        self.top_wall = HORIZONTAL.join(tiles)

    def _init_room_layer(self, layer):
        """Initialize room layer."""
        result = self._create_room_layer(layer)
        self.room_layers.append(result)

    def _init_internal_wall(self, layer):
        """Initialize internal wall."""
        result = self._create_internal_wall(layer)
        self.internal_walls.append(result)

    def _init_bottom_wall(self):
        """Initialize bottom wall."""
        width = self.maze.width
        tiles = [BOTTOM_LEFT]
        for i in range(width-1):
            last = self.maze.height-1
            drawn = self._check_visited((last, i), (last, i+1))
            tiles.append(BOTTOM_NODE if drawn else HORIZONTAL_HIDDEN)
        tiles.append(BOTTOM_RIGHT)
        self.bottom_wall = HORIZONTAL.join(tiles)

    def debug_string(self):
        """Render debug output."""
        output = [self.top_wall]
        for i in range(self.maze.height-1):
            output.append(self.room_layers[i])
            output.append(self.internal_walls[i])
        output.append(self.room_layers[self.maze.height-1])
        output.append(self.bottom_wall)
        return '\n'.join(output)

    def draw_maze(self):
        """Draw maze."""
        print(self.top_wall)
        for i in range(self.maze.height-1):
            print(self.room_layers[i])
            print(self.internal_walls[i])
        print(self.room_layers[self.maze.height-1])
        print(self.bottom_wall)

    def invalidate(self, *positions):
        """Invalidate maze for changed positions."""
        room_layers = set()
        wall_layers = set()
        update_top_wall = False
        update_bottom_wall = False
        for position in positions:
            layer = position[0]
            room_layers.add(layer)
            if layer-1 >= 0:
                wall_layers.add(layer-1)
            else:
                update_top_wall = True
            if layer < self.maze.height-1:
                wall_layers.add(layer)
                if layer+1 < self.maze.height-1:
                    wall_layers.add(layer+1)
            else:
                update_bottom_wall = True

        for layer in room_layers:
            result = self._create_room_layer(layer)
            self.room_layers[layer] = result

        for layer in wall_layers:
            result = self._create_internal_wall(layer)
            self.internal_walls[layer] = result

        if update_top_wall:
            self._init_top_wall()

        if update_bottom_wall:
            self._init_bottom_wall()
