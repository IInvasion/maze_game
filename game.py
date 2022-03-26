"""Game loop."""

from maze_game import render, tui
from maze_game.maze import Maze
from maze_game.maze_filler import MonsterGenerator, WeaponGenerator
from maze_game.position import Position
from maze_game.unit import UnitFabric
from maze_game.weapon import WeaponFabric
from maze_game.battle import Battle

HANDS = ['right', 'left']


def exit_is_found(game):
    """Exit found condition."""
    pos = game.player.position().pair()
    width = game.maze.width
    height = game.maze.height
    return pos == (height-1, width-1)


class Move:
    """Move processor."""

    def __init__(self):
        """Constructor."""
        self.cmd_list = ['down', 'left', 'right', 'up']
        self.cmd_map = {
            'down': lambda pos: pos.down(),
            'left': lambda pos: pos.left(),
            'right': lambda pos: pos.right(),
            'up': lambda pos: pos.up(),
        }

    def command(self, cmd):
        """Get command."""
        for item in self.cmd_list:
            if item.startswith(cmd):
                return item
        return None

    def process(self, maze, pos, cmd_part):
        """Process command."""
        cmd = self.command(cmd_part)
        if cmd is None:
            print('Wrong move command!')
            return None
        func = self.cmd_map[cmd]
        new_pos = func(pos)
        if new_pos is None:
            print(f'Cannot move {cmd} (border)')
            return None
        if not maze.has_door(pos.pair(), new_pos.pair()):
            print(f'Cannot move {cmd} (no door)')
            return None
        return new_pos


class Game:
    """Game."""

    def __init__(self, width, height, hero):
        """Constructor."""
        # maze
        self.maze = Maze(width, height)
        self.monster_filler = MonsterGenerator()
        self.monster_filler.fill(self.maze, UnitFabric())
        self.weapon_filler = WeaponGenerator()
        self.weapon_filler.fill(self.maze, WeaponFabric())

        # player
        pos = Position(height, width)
        self.player = hero
        self.player.set_position(pos)
        self.move = Move()
        self.maze.room(*pos.pair()).enter(self.player)
        self.render = render.Render(self.maze, self.monster_filler,
                                    self.weapon_filler)
        self.last_command = None

    def room_info(self):
        """Room info."""
        pos = self.player.position()
        info = self.maze.room(*pos.pair()).info()
        print(info)

    def start_loop(self):
        """Start game loop."""
        render.clear()
        while self.step():
            pass
        self.render.draw_maze()
        return 0

    def set_hero_weapon(self, weapon):
        """Set hero weapon."""
        hand = tui.choice(HANDS, 'Please choice hand for this weapon')
        hand = HANDS.index(hand)
        current_weapon = self.player.weapons[hand]
        self.player.pick_weapon(weapon, hand)
        return current_weapon

    def pick_weapon(self, room):
        """Pick weapon."""
        weapon = room.weapon_name()
        weapon = WeaponFabric().get_object(weapon)
        render.weapon_info(weapon)
        if self.player.can_use(weapon):
            decision = tui.yes_no('Do you want to pick up the weapon?')
            if decision:
                last_weapon = self.set_hero_weapon(weapon)
                room.remove_weapon()
                if last_weapon is not None:
                    room.set_weapon(last_weapon)
            render.clear()
        else:
            render.clear()
            tui.separating_string()
            print('You are not able to pick the weapon! ' +
                  'Hero level is too small!')

    def meet_monster(self, room):
        """Meet monster in the room."""
        monster = room.monster_name()
        monster = UnitFabric().get_object(monster)
        render.monster_info(monster)
        battle = Battle(self.player, monster)
        battle_result = battle.battle_loop()
        render.clear()
        if battle_result:
            tui.separating_string('You are winner!')
            self.player.level_increase(battle.potential_exp)
            room.remove_monster()
        else:
            tui.separating_string('GAME OVER!')
            tui.separating_string('Unfortunately you are died!')
            return False
        return battle_result

    def step(self):
        """Game loop step."""
        self.room_info()
        self.render.draw_maze()
        render.player_weapons_info(self.player)
        command = input('>> ')
        render.clear()
        command = command.strip()
        if command and 'exit'.startswith(command):
            return False
        if not command and self.last_command:
            command = self.last_command

        pos = self.player.position()
        new_pos = self.move.process(self.maze, pos, command)
        if new_pos:
            self.last_command = command
            self.maze.room(*pos.pair()).leave(self.player)
            self.maze.room(*new_pos.pair()).enter(self.player)
            self.player.set_position(new_pos)
            self.render.invalidate(pos.pair(), new_pos.pair())
            pos = self.player.position()
            room = self.maze.room(*pos.pair())
            render.clear()
            if room.has_weapon():
                self.pick_weapon(room)
            elif room.has_monster():
                if not self.meet_monster(room):
                    return False

            if exit_is_found(self):
                print('Exit is found! You win!')
                return False

        return True
