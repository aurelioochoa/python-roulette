from datetime import datetime
import os

# ANSI color codes
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GRAY = '\033[90m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


class Logger:
    """Logger for Russian Roulette game events."""
    
    def __init__(self):
        self.history = []
    
    def _get_timestamp(self):
        """Generate formatted timestamp."""
        return f"{Colors.GRAY}[{datetime.now().strftime('%H:%M:%S')}]{Colors.RESET} "
    
    def _log(self, level, color, message):
        """Internal logging method."""
        formatted = f"{self._get_timestamp()}{color}{level}{Colors.RESET} {message}"
        self.history.append((datetime.now(), level, message))
        print(formatted)
    
    def info(self, message):
        """Log informational message."""
        self._log("INFO", Colors.CYAN, message)
    
    def action(self, message):
        """Log player/game action."""
        self._log("ACTION", Colors.GREEN, message)
    
    def warning(self, message):
        """Log warning message."""
        self._log("WARNING", Colors.YELLOW, message)
    
    def danger(self, message):
        """Log dangerous/critical event (like firing)."""
        self._log("DANGER", Colors.RED, message)
    
    def result(self, message):
        """Log game result."""
        self._log("RESULT", Colors.MAGENTA + Colors.BOLD, message)
    
    def player(self, player_name, message):
        """Log player-specific event."""
        self._log(f"[{player_name}]", Colors.CYAN + Colors.BOLD, message)
    
    def round(self, round_number):
        """Log round start."""
        self._log("ROUND", Colors.BOLD, f"========== Round {round_number} ==========")
    
    def game_over(self, winner=None):
        """Log game over."""
        if winner:
            self._log("GAME OVER", Colors.GREEN + Colors.BOLD, f"Winner: {winner}")
        else:
            self._log("GAME OVER", Colors.RED + Colors.BOLD, "No survivors!")
    
    def get_history(self):
        """Return log history."""
        return self.history.copy()
    
    def clear_history(self):
        """Clear log history."""
        self.history = []

    def save_to_file(self, directory="records"):
        """Save game history to a timestamped file.
        
        Args:
            directory: Directory to save records (default: 'records')
        
        Returns:
            str: Path to the saved file
        """
        # Create records directory relative to source
        records_dir = os.path.join(os.path.dirname(__file__), '..', directory)
        os.makedirs(records_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        filename = f"game_record_{timestamp}.txt"
        filepath = os.path.join(records_dir, filename)
        
        # Write history to file
        with open(filepath, 'w') as f:
            f.write("=" * 50 + "\n")
            f.write("  PYTHON ROULETTE - GAME RECORD\n")
            f.write(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            
            for entry in self.history:
                time, level, message = entry
                f.write(f"[{time.strftime('%H:%M:%S')}] {level}: {message}\n")
            
            f.write("\n" + "=" * 50 + "\n")
        
        return filepath

    class Tests:
        """Test logging helpers."""
        
        @staticmethod
        def format_drum(drum, activeChamberPosition=None):
            """Format drum state with colors: O=live (red), @=fired (gray), ○=empty (green)
            If activeChamberPosition is provided, show parentheses around that chamber."""
            result = "[ "
            for i, chamber in enumerate(drum):
                if chamber is None:
                    symbol = f"{Colors.GREEN}○{Colors.RESET}"
                elif chamber is True:
                    symbol = f"{Colors.RED}●{Colors.RESET}"
                else:
                    symbol = f"{Colors.GRAY}@{Colors.RESET}"
                
                if activeChamberPosition is not None and i == activeChamberPosition:
                    result += f"({symbol}) "
                else:
                    result += f"{symbol} "
            return result + "]" + f" -> Active chamber: {activeChamberPosition}" if activeChamberPosition is not None else ""

        @staticmethod
        def log_test(msg):
            print(f"\n{Colors.BOLD}{Colors.CYAN}▶ {msg}{Colors.RESET}")

        @staticmethod
        def log_info(label, value):
            print(f"  {Colors.YELLOW}{label}:{Colors.RESET} {value}")

        @staticmethod
        def log_drum(label, drum, activeChamberPosition=None):
            print(f"  {Colors.YELLOW}{label}:{Colors.RESET} {Logger.Tests.format_drum(drum, activeChamberPosition)}")

        @staticmethod
        def log_result(label, value):
            color = Colors.RED if value else Colors.GREEN
            symbol = "BANG!" if value else "*click*"
            print(f"  {Colors.YELLOW}{label}:{Colors.RESET} {color}{symbol}{Colors.RESET}")

        @staticmethod
        def log_pass_fail(label, expected, actual):
            color = Colors.GREEN if expected == actual else Colors.RED
            status = "PASS" if expected == actual else "FAIL"
            print(f"  {Colors.YELLOW}{label}:{Colors.RESET} {color}{status}{Colors.RESET} (expected: {expected}, got: {actual})")

        @staticmethod
        def count_bullets(drum):
            """Count live bullets (True) in drum."""
            return sum(1 for c in drum if c is True)

if __name__ == '__main__':
    # Test the logger
    logger = Logger()
    
    logger.info("...Logger test...")
    logger.info("Game starting...")
    logger.round(1)
    logger.player("Alice", "picks up the revolver")
    logger.action("Spinning drum...")
    logger.danger("Pulling trigger!")
    logger.result("*click* - survived!")
    logger.player("Bob", "takes the revolver")
    logger.danger("Pulling trigger!")
    logger.result("BANG! - eliminated")
    logger.game_over("Alice")
 