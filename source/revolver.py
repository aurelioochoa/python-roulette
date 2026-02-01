class Revolver:
    def __init__(self):
        self.drum = [
            None, None, 
            None, None, 
            None, None
            ]
        self.activeChamberPosition = 5

    def get_empty_chambers(self):
        """Returns a list of empty chambers."""
        emptyChambers = []
        for chamber in range(6):
            if self.drum[chamber] is None:
                emptyChambers.append(chamber)
        return emptyChambers

    def validate_bullet_count(self, bulletsToLoad):
        """Validates and adjusts bullet count based on empty chambers.
        If bullet count is greater than empty chambers, adjust bullet count to empty chambers.
        
        Returns:
            Tuple of (adjusted bullet count, list of empty chambers)
        """
        emptyChambers = self.get_empty_chambers()
        
        if bulletsToLoad > len(emptyChambers):
            print("Cannot load more bullets than empty chambers")
            print("Loading " + str(len(emptyChambers)) + " bullets instead")
            bulletsToLoad = len(emptyChambers)
        
        return bulletsToLoad, emptyChambers

    def load_bullet(self, chamber):
        """Loads a bullet into the specified chamber."""
        if self.drum[chamber] is not None:
            raise ValueError("Chamber already has a bullet")
        self.drum[chamber] = True

    def load_bullet_in_given_order(self, chambersToLoad):
        """Loads a bullets in a given order."""
        for chamber in chambersToLoad:
            self.load_bullet(chamber)

    def load_bullets_in_order(self, bulletsToLoad):
        """Loads a specified number of bullets into the revolver in order."""
        bulletsToLoad, emptyChambers = self.validate_bullet_count(bulletsToLoad)
        
        for bullet in range(bulletsToLoad):
            chamber = emptyChambers[bullet]
            self.load_bullet(chamber)
        return emptyChambers

    def load_bullets_randomly(self, bulletsToLoad):
        """Loads a specified number of bullets into the revolver randomly."""
        import random
        
        bulletsToLoad, emptyChambers = self.validate_bullet_count(bulletsToLoad)

        # Randomly select positions to load bullets
        randomEmptyChambersToLoad = random.sample(emptyChambers, bulletsToLoad)
        for chamber in randomEmptyChambersToLoad:
            self.load_bullet(chamber)

    def unload_bullet(self, chamber):
        """Unloads a bullet from the specified chamber."""
        self.drum[chamber] = None

    def unload_empty_cartidges(self):
        """Unloads all fired bullets from its chambers."""
        for chamber in range(6):
            if self.drum[chamber] is False:
                self.unload_bullet(chamber)

    def unload_bullets_in_given_order(self, chambersToUnload):
        """Unloads bullets from a given order."""
        for chamber in chambersToUnload:
            self.unload_bullet(chamber)

    def unload_drum(self):
        """Dumps all chambers, resetting the revolver."""
        self.drum = [None, None, None, None, None, None]

    def speed_reload(self):
        """Dumps current drum and loads all chambers with a bullet."""
        self.unload_drum()
        self.drum = [True, True, True, True, True, True]

    def rotate_drum_counter_clockwise(self):
        self.activeChamberPosition += 1
        if self.activeChamberPosition == 6:
            self.activeChamberPosition = 0

    def free_spin_drum(self):
        import random
        stepsToSpin = random.randint(10, 100)
        for step in range(stepsToSpin):
            self.rotate_drum_counter_clockwise()
        return stepsToSpin

    def pull_trigger(self):
        """Pulls the trigger and returns True if the chamber is loaded, False otherwise."""
        self.rotate_drum_counter_clockwise()
        isChamberLoaded = self.drum[self.activeChamberPosition]
        if isChamberLoaded:
            self.drum[self.activeChamberPosition] = False
        return isChamberLoaded

