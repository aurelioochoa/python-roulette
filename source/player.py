from revolver import Revolver

class Player:
    def __init__(self, name, lives=3, revolver=None):
        self.name = name
        self.lives = lives
        self.revolverInHand = revolver if revolver else Revolver()

    def is_alive(self):
        return self.lives > 0

    def take_damage(self):
        self.lives -= 1

    def die(self):
        self.lives = 0

    def shoot_himself(self):
        if self.revolverInHand.pull_trigger():
            self.take_damage()

    def shoot_player(self, player):
        if self.revolverInHand.pull_trigger():
            player.take_damage()

    def give_revolver_to_crupier(self, crupier):
        crupier.revolverInHand = self.revolverInHand
        self.revolverInHand = None
