import os
import time

try:
    import pygame
    pygame.mixer.init()
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False
    print("Warning: pygame not installed. Sound effects disabled.")
except Exception as e:
    SOUND_ENABLED = False
    print(f"Warning: pygame audio init failed. Sound effects disabled. ({e})")

# Path to sound effects directory
SFX_DIR = os.path.join(os.path.dirname(__file__), '..', 'sfx')


def _get_sfx_path(filename):
    """Get full path to a sound effect file."""
    return os.path.join(SFX_DIR, filename)


def _play(filename, block=True):
    """Play a sound effect file.
    
    Args:
        filename: Name of the sound file in sfx directory
        block: If True, wait for sound to finish. If False, play async.
    """
    if not SOUND_ENABLED:
        return
    
    path = _get_sfx_path(filename)
    if not os.path.exists(path):
        print(f"Warning: Sound file not found: {path}")
        return
    
    try:
        sound = pygame.mixer.Sound(path)
        sound.play()
        if block:
            time.sleep(sound.get_length())
    except pygame.error as e:
        print(f"Warning: Could not play sound: {e}")


def play_gunshot(block=True):
    """Play gunshot sound effect."""
    _play('single-pistol-gunshot.mp3', block)


def play_dryfire(block=True):
    """Play dry fire/click sound effect."""
    _play('revolver-dryfire.mp3', block)


def play_spin(block=True):
    """Play drum spin sound effect."""
    _play('revolver-spin.mp3', block)


def play_cock(block=True):
    """Play revolver cocking sound effect."""
    _play('revolver-cocking.mp3', block)


def play_holster(block=True):
    """Play holster pistol sound effect."""
    _play('holster-pistol.mp3', block)


def play_shells_drop(block=True):
    """Play shells hitting ground sound effect."""
    _play('shells-hitting-ground.mp3', block)


def play_cock_alt(block=True):
    """Play alternative cocking sound effect."""
    _play('revolvercock.mp3', block)


if __name__ == '__main__':
    print("Testing sound effects...")
    print("1. Cocking...")
    play_cock()
    print("2. Spinning...")
    play_spin()
    print("3. Dry fire (click)...")
    play_dryfire()
    print("4. Gunshot!")
    play_gunshot()
    print("5. Shells dropping...")
    play_shells_drop()
    print("Done!")
