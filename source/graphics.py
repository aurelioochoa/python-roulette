import time
import os

def print_revolver_pointed_at_player():
    """Print the revolver pointed at the player in ASCII art."""
    print("          ^")
    print("         | |")
    print("       @#####@")
    print("     (###   ###)-.")
    print("   .(###     ###) \\")
    print("  /  (###   ###)   )")
    print(" (=-  .@#####@|_--\"")
    print(" /\\    \\_|l|_/ (\\")
    print("(=-\\     |l|    /")
    print(" \\  \\.___|l|___/")
    print(" /\\      |_|   /")
    print("(=-\\._________/\\")
    print(" \\             /")
    print("   \\._________/")
    print("     #  ----  #")
    print("     #   __   #")
    print("     \\########/")
    

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_chamber_symbol(state):
    """Convert chamber state to display symbol.
    
    Args:
        state: None (empty), True (live bullet), False (fired cartridge)
    
    Returns:
        str: ' ' for empty, 'O' for live, '@' for fired
    """
    if state is None:
        return ' '
    elif state is True:
        return 'O'
    else:
        return '@'


def display_drum(drum):
    """Display the revolver drum state in ASCII art.
    
    Args:
        drum: List of 6 chamber states (None, True, or False)
    
    Drum layout:
           [5]
        [4]   [0]
        [3]   [1]
           [2]
    """
    currentDrum = drum.copy()
    chamberSymbols = [get_chamber_symbol(chamber) for chamber in currentDrum]
    
    print(f"   _________")
    print(f"  /         \\")
    print(f" /    [{chamberSymbols[5]}]    \\")
    print(f" | [{chamberSymbols[4]}]   [{chamberSymbols[0]}] |")
    print(f" | [{chamberSymbols[3]}]   [{chamberSymbols[1]}] |")
    print(f" \\    [{chamberSymbols[2]}]    /")
    print(f"  \\_________/")
    print()


def reload_in_given_order_animation(drum, bulletsToLoad, chambersToLoad, delay=0.5):
    """Animate loading bullets into the drum one by one.
    
    Args:
        drum: List of 6 chamber states to modify
        bulletsToLoad: Number of bullets to load
        chambersToLoad: List of chambers to load bullets into
        delay: Time between each frame in seconds
    """
    # Find empty positions
    currentDrum = drum.copy()
    
    if bulletsToLoad > len(chambersToLoad):
        bulletsToLoad = len(chambersToLoad)
    
    clear_screen()
    display_drum(currentDrum)
    time.sleep(delay)
    
    for bullet in range(bulletsToLoad):
        if bullet < len(chambersToLoad):
            clear_screen()
            
            # Load bullet into position
            chamber = chambersToLoad[bullet]
            currentDrum[chamber] = True
            
            display_drum(currentDrum)
            time.sleep(delay)
    
    clear_screen()
    display_drum(currentDrum)


def unload_empty_cartridges_animation(drum, delay=0.5):
    """Animate unloading fired cartridges from the drum.
    
    Args:
        drum: List of 6 chamber states (None, True, or False)
        delay: Time between each frame in seconds
    
    Returns:
        The drum state after unloading empty cartridges
    """
    current_drum = drum.copy()
    
    clear_screen()
    display_drum(current_drum)
    time.sleep(delay)
    
    for chamber in range(6):
        if current_drum[chamber] is False:
            clear_screen()
            
            # Unload the fired cartridge
            current_drum[chamber] = None
            
            display_drum(current_drum)
            time.sleep(delay)
    
    clear_screen()
    display_drum(current_drum)
    
    return current_drum


def spin_drum_animation(drum, stepsToSpin, delay=0.08):
    """Animate the actual drum spinning with all bullet states visible.
    
    Args:
        drum: List of 6 chamber states (None, True, or False)
        stepsToSpin: Number of rotation steps
        delay: Time between each frame
    
    Returns:
        The rotated drum state after spinning
    """
    
    # Copy the drum to avoid modifying original during animation
    current_drum = drum.copy()
    
    time.sleep(0.3)
    
    for step in range(stepsToSpin):
        clear_screen()
        
        chamberSymbols = [get_chamber_symbol(chamber) for chamber in current_drum]
        
        print(f"   _________")
        print(f"  /         \\")
        print(f" /    [{chamberSymbols[5]}]    \\")
        print(f" | [{chamberSymbols[4]}]   [{chamberSymbols[0]}] |")
        print(f" | [{chamberSymbols[3]}]   [{chamberSymbols[1]}] |")
        print(f" \\    [{chamberSymbols[2]}]    /")
        print(f"  \\_________/")
        
        # Rotate the drum visually counter-clockwise (shift positions)
        current_drum = current_drum[1:] + [current_drum[0]]
        
        # Slow down near the end for dramatic effect
        if step > stepsToSpin - 10:
            time.sleep(delay * 2)
        elif step > stepsToSpin - 20:
            time.sleep(delay * 1.5)
        else:
            time.sleep(delay)
    
    clear_screen()
    display_drum(current_drum)
    
    return current_drum


def fire_revolver_animation(drum, delay=0.1):
    """Animate firing the revolver - drum rotates and fires if chamber is loaded.
    
    Args:
        drum: List of 6 chamber states (None, True, or False)
        delay: Time between animation frames
    
    Returns:
        Tuple of (fired: bool/None, updated drum state)
    """
    current_drum = drum.copy()
    
    clear_screen()
    print("Pulling trigger...")
    display_drum(current_drum)
    time.sleep(delay * 3)
    
    # Rotate drum counter-clockwise (active chamber is position 5)
    clear_screen()
    print("*click*")
    current_drum = current_drum[1:] + [current_drum[0]]
    display_drum(current_drum)
    time.sleep(delay * 2)
    
    # Check if chamber 5 (active) has a live bullet
    chamber_state = current_drum[5]
    
    # Show pointed_at_you graphic before result
    clear_screen()
    print_revolver_pointed_at_player()
    time.sleep(delay * 5)
    
    clear_screen()
    if chamber_state is True:
        print("BANG!")
        current_drum[5] = False  # Mark as fired
    elif chamber_state is False:
        print("*click* (already fired)")
    else:
        print("*click* (empty)")

    display_drum(current_drum)
    time.sleep(delay * 3)
    
    return chamber_state, current_drum


if __name__ == '__main__':
    # Test code - only runs when executed directly
    emptyDrum = [None, None, None, None, None, None]
    loadedDrum = [None, True, None, None, None, False]
    fullyLoadedDrum = [True, True, True, True, True, False]
    chambersToLoad = [0, 4, 3, 5, 1, 2]  # List of chamber indices, not drum state
    # # test reload
    # reload_in_given_order_animation(emptyDrum, 4, chambersToLoad, delay=1)
    # # test spin
    # spin_drum_animation(loadedDrum, 12, delay=0.05)
    # # test unload
    # unload_empty_cartridges_animation(loadedDrum, delay=0.5)

    # test firing
    fire_revolver_animation(emptyDrum, delay=0.3)