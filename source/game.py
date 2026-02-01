import random
from player import Player
from crupier import Crupier
from logger import Logger
import graphics
import soundEffects


class RussianRoulette:
    """Main game class for Russian Roulette."""
    
    def __init__(self, player1_name="Player 1", player2_name="Player 2", 
                 lives=3, bullets_per_round=1, animations=True, sound=True):
        """Initialize the game.
        
        Args:
            player1_name: Name of first player
            player2_name: Name of second player
            lives: Starting lives for each player (default: 3)
            bullets_per_round: Number of bullets loaded each round (default: 1)
            animations: Enable graphics animations (default: True)
            sound: Enable sound effects (default: True)
        """
        self.crupier = Crupier()
        self.logger = Logger()
        self.animations = animations
        self.sound = sound
        self.bullets_per_round = bullets_per_round
        self.round_number = 0
        self.game_over = False
        
        # Create players without revolvers (crupier manages the gun)
        self.player1 = Player(player1_name, lives=lives, revolver=None)
        self.player1.revolverInHand = None
        self.player2 = Player(player2_name, lives=lives, revolver=None)
        self.player2.revolverInHand = None
        
        self.current_player = self.player1
        self.other_player = self.player2

    def get_alive_players(self):
        """Return list of players still alive."""
        alive = []
        if self.player1.is_alive():
            alive.append(self.player1)
        if self.player2.is_alive():
            alive.append(self.player2)
        return alive

    def switch_player(self):
        """Switch current player to the other player."""
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.other_player = self.player1
        else:
            self.current_player = self.player1
            self.other_player = self.player2

    def setup_round(self):
        """Setup a new round - crupier loads bullets and spins drum."""
        self.round_number += 1
        self.logger.round(self.round_number)
        
        # Crupier prepares the revolver
        self.crupier.dump_and_load_bullets_randomly(self.bullets_per_round)
        
        if self.sound:
            soundEffects.play_shells_drop(block=False)
        
        self.logger.action(f"Crupier loads {self.bullets_per_round} bullet(s)")
        
        # Spin the drum
        if self.animations:
            steps = self.crupier.revolverInHand.free_spin_drum()
            graphics.spin_drum_animation(self.crupier.revolverInHand.drum, steps)
        else:
            self.crupier.revolverInHand.free_spin_drum()
        
        if self.sound:
            soundEffects.play_spin()
        
        self.logger.action("Crupier spins the drum")

    def display_status(self):
        """Display current game status."""
        print("\n" + "=" * 40)
        print(f"  {self.player1.name}: {'❤️ ' * self.player1.lives}{'🖤 ' * (3 - self.player1.lives)}")
        print(f"  {self.player2.name}: {'❤️ ' * self.player2.lives}{'🖤 ' * (3 - self.player2.lives)}")
        print("=" * 40 + "\n")

    def get_player_choice(self, auto=False):
        """Prompt current player to choose target.
        
        Args:
            auto: If True, randomly choose target
        """
        if auto:
            return random.choice(["self", "other"])
        
        print(f"\n{self.current_player.name}'s turn!")
        print(f"  1. Shoot yourself")
        print(f"  2. Shoot {self.other_player.name}")
        
        while True:
            choice = input("\nChoose (1 or 2): ").strip()
            if choice == "1":
                return "self"
            elif choice == "2":
                return "other"
            else:
                print("Invalid choice. Enter 1 or 2.")

    def play_turn(self, auto=False):
        """Execute one player's turn.
        
        Args:
            auto: If True, run in automatic mode (no input/animations)
        """
        # Give revolver to current player
        self.crupier.give_revolver_to_player(self.current_player)
        self.logger.player(self.current_player.name, "takes the revolver")
        
        if self.sound and not auto:
            soundEffects.play_cock()
        
        # Get player choice
        choice = self.get_player_choice(auto=auto)
        
        if choice == "self":
            target = self.current_player
            self.logger.danger(f"{self.current_player.name} points at themselves...")
        else:
            target = self.other_player
            self.logger.danger(f"{self.current_player.name} points at {self.other_player.name}...")
        
        if not auto:
            input("\nPress ENTER to pull the trigger...")
        
        # Fire animation
        if self.animations and not auto:
            fired, new_drum = graphics.fire_revolver_animation(
                self.current_player.revolverInHand.drum
            )
            self.current_player.revolverInHand.drum = new_drum
        else:
            fired = self.current_player.revolverInHand.pull_trigger()
        
        # Handle result
        if fired:
            if self.sound:
                soundEffects.play_gunshot()
            target.take_damage()
            self.logger.result(f"BANG! {target.name} loses a life!")
            
            if not target.is_alive():
                self.logger.result(f"{target.name} is eliminated!")
        else:
            if self.sound:
                soundEffects.play_dryfire()
            self.logger.result(f"*click* - {target.name} survives!")
        
        # Return revolver to crupier
        self.current_player.give_revolver_to_crupier(self.crupier)
        
        return fired

    def check_game_over(self):
        """Check if the game is over."""
        alive = self.get_alive_players()
        if len(alive) == 1:
            self.game_over = True
            return alive[0]
        elif len(alive) == 0:
            self.game_over = True
            return None
        return None

    def check_drum_empty(self):
        """Check if drum has any live bullets left."""
        drum = self.crupier.revolverInHand.drum
        return not any(bullet is True for bullet in drum)

    def play(self):
        """Main game loop."""
        if self.animations:
            graphics.clear_screen()
        
        print("\n" + "=" * 50)
        print("       🔫 PYTHON ROULETTE 🔫")
        print("=" * 50)
        print(f"\n{self.player1.name} vs {self.player2.name}")
        print(f"Lives: {self.player1.lives} | Bullets per round: {self.bullets_per_round}")
        print("\n" + "=" * 50)
        
        input("\nPress ENTER to start...")
        
        while not self.game_over:
            # Setup new round
            self.setup_round()
            
            # Play until drum is empty or game over
            while not self.check_drum_empty() and not self.game_over:
                self.display_status()
                
                # Skip dead players
                if not self.current_player.is_alive():
                    self.switch_player()
                    continue
                
                # Play turn
                self.play_turn()
                
                # Check for winner
                winner = self.check_game_over()
                if winner:
                    break
                
                # Switch to other player for next turn
                self.switch_player()
            
            if not self.game_over:
                print("\n🔄 Drum is empty! Starting new round...\n")
                input("Press ENTER to continue...")
        
        # Game over
        self.display_status()
        winner = self.get_alive_players()
        if winner:
            self.logger.game_over(winner[0].name)
            print(f"\n🎉 {winner[0].name} WINS! 🎉\n")
        else:
            self.logger.game_over()
            print("\n💀 No survivors! 💀\n")
        
        # Save game record
        filepath = self.logger.save_to_file()
        print(f"📝 Game record saved to: {filepath}\n")

    def play_auto(self):
        """Automatic game mode - no graphics, no sound, just logs."""
        self.logger.info("=== AUTOMATIC MODE ===")
        self.logger.info(f"{self.player1.name} vs {self.player2.name}")
        self.logger.info(f"Lives: {self.player1.lives} | Bullets: {self.bullets_per_round}")
        
        while not self.game_over:
            # Setup new round (no animations)
            self.round_number += 1
            self.logger.round(self.round_number)
            self.crupier.dump_and_load_bullets_randomly(self.bullets_per_round)
            self.logger.action(f"Crupier loads {self.bullets_per_round} bullet(s)")
            self.crupier.revolverInHand.free_spin_drum()
            self.logger.action("Crupier spins the drum")
            
            # Play until drum is empty or game over
            while not self.check_drum_empty() and not self.game_over:
                # Skip dead players
                if not self.current_player.is_alive():
                    self.switch_player()
                    continue
                
                # Log status
                self.logger.info(f"{self.player1.name}: {self.player1.lives} lives | {self.player2.name}: {self.player2.lives} lives")
                
                # Play turn in auto mode
                self.play_turn(auto=True)
                
                # Check for winner
                if self.check_game_over():
                    break
                
                # Switch to other player
                self.switch_player()
            
            if not self.game_over:
                self.logger.info("Drum empty - new round")
        
        # Game over
        winner = self.get_alive_players()
        if winner:
            self.logger.game_over(winner[0].name)
        else:
            self.logger.game_over()
        
        # Save game record
        filepath = self.logger.save_to_file()
        self.logger.info(f"Game record saved to: {filepath}")
        
        return winner[0] if winner else None


if __name__ == '__main__':
    print("\n🔫 PYTHON ROULETTE 🔫\n")
    
    # Mode selection
    print("Select mode:")
    print("  1. Interactive (with graphics and sound)")
    print("  2. Automatic (logs only)")
    
    mode = input("\nChoose (1 or 2, default 1): ").strip()
    auto_mode = mode == "2"
    
    # Get player names
    p1_name = input("Enter Player 1 name (or press ENTER for 'Player 1'): ").strip()
    if not p1_name:
        p1_name = "Player 1"
    
    p2_name = input("Enter Player 2 name (or press ENTER for 'Player 2'): ").strip()
    if not p2_name:
        p2_name = "Player 2"
    
    bullets = input("Bullets per round (1-6, default 1): ").strip()
    try:
        bullets = int(bullets)
        bullets = max(1, min(6, bullets))
    except ValueError:
        bullets = 1
    
    # Create and start game
    game = RussianRoulette(
        player1_name=p1_name,
        player2_name=p2_name,
        bullets_per_round=bullets,
        animations=not auto_mode,
        sound=not auto_mode
    )
    
    if auto_mode:
        game.play_auto()
    else:
        game.play()