from revolver import Revolver

class Crupier:
    def __init__(self, revolver=None):
        self.name = "Crupier"
        self.revolverInHand = revolver if revolver else Revolver()

    def give_revolver_to_player(self, player):
        """Hand the revolver to a player."""
        player.revolverInHand = self.revolverInHand
        self.revolverInHand = None

    def dump_and_load_single_bullet(self):
        """Clear drum and load a single bullet in chamber 0."""
        self.revolverInHand.unload_drum()
        self.revolverInHand.load_bullet(0)

    def dump_and_load_bullets_randomly(self, count=1):
        """Clear drum and load specified number of bullets randomly."""
        self.revolverInHand.unload_drum()
        self.revolverInHand.load_bullets_randomly(count)

    def setup_round_with_random_bullet_positions(self, bullets=3):
        """Setup a round with multiple randomly positioned bullets."""
        self.revolverInHand.unload_drum()
        self.revolverInHand.load_bullets_randomly(bullets)
        self.revolverInHand.free_spin_drum()

        """Check if crupier is holding the revolver."""
        return self.revolverInHand is not None