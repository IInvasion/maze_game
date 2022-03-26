"""Battle tools."""


from maze_game import render, tui

ATTACK_TYPE = ['Physical attack', 'Magic attack']


class Battle:
    """Battle."""

    def __init__(self, hero, enemy):
        """Constructor."""
        self.rounds = 1
        self.potential_exp = enemy.max_health
        self.hero = hero
        self.enemy = enemy
        render.clear()

    def battle_loop(self):
        """Battle loop."""
        while True:
            while self.hero.is_alive() and self.enemy.is_alive():
                render.battle_info(self)
                self.battle_round()

        return self.hero.is_alive()

    def battle_round(self):
        """Battle round."""
        option = tui.choice(ATTACK_TYPE, 'Choice attack type')
        if option == 'Physical attack':
            self.hero.physycal_attack(self.enemy)
        else:
            self.hero.magic_attack(self.enemy)
        self.enemy.physycal_attack(self.hero)
        self.rounds += 1
