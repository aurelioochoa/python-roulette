import unittest
import os
import revolver
import graphics
import soundEffects
from player import Player
from crupier import Crupier
from logger import Logger

# Aliases for test logging helpers
log_test = Logger.Tests.log_test
log_info = Logger.Tests.log_info
log_drum = Logger.Tests.log_drum
log_result = Logger.Tests.log_result
log_pass_fail = Logger.Tests.log_pass_fail
count_bullets = Logger.Tests.count_bullets


# === Revolver Tests ===

class TestRevolver(unittest.TestCase):
    
    def setUp(self):
        self.revolver = revolver.Revolver()

    # === Initialization Tests ===
    
    def test_01_init_empty_drum(self):
        """Test that revolver initializes with empty drum (all None)"""
        log_test("1 Testing empty drum initialization")
        log_drum("Drum state", self.revolver.drum)
        self.assertEqual(self.revolver.drum, [None, None, None, None, None, None])

    def test_02_get_empty_chambers(self):
        """Test getting list of empty chambers"""
        log_test("2 Testing get_empty_chambers")
        log_info("Empty chambers", self.revolver.get_empty_chambers())
        self.assertEqual(self.revolver.get_empty_chambers(), [0, 1, 2, 3, 4, 5])

        self.revolver.load_bullet(2)
        log_drum("After loading pos 2 -> chamber 3", self.revolver.drum)
        log_info("Empty chambers", self.revolver.get_empty_chambers())
        self.assertEqual(self.revolver.get_empty_chambers(), [0, 1, 3, 4, 5])

    # === Loading Tests ===
    
    def test_03_load_bullet(self):
        """Test loading a bullet at a specific position"""
        log_test("3 Testing load_bullet at position 2 -> chamber 3")
        self.revolver.load_bullet(2)
        log_drum("Drum state", self.revolver.drum)
        self.assertTrue(self.revolver.drum[2])

    def test_04_load_bullet_already_loaded_raises(self):
        """Test that loading into occupied chamber raises error"""
        log_test("4 Testing load_bullet raises on occupied chamber")
        self.revolver.load_bullet(0)
        log_drum("Drum state", self.revolver.drum)
        with self.assertRaises(ValueError):
            self.revolver.load_bullet(0)
        log_info("Result", "ValueError raised as expected")

    def test_05_load_bullets_in_order(self):
        """Test loading multiple bullets in order"""
        bulletsToLoad = 3
        log_test(f"5 Testing load_bullets_in_order({bulletsToLoad})")
        self.revolver.load_bullets_in_order(bulletsToLoad)
        log_drum("Drum state", self.revolver.drum)
        self.assertEqual(self.revolver.drum, [True, True, True, None, None, None])

    def test_06_load_bullets_randomly(self):
        """Test that random loading adds correct number of bullets"""
        print("---")
        for sample in range(3):
            self.setUp()
            bulletsToLoad = 2
            log_test(f"6 Testing load_bullets_randomly({bulletsToLoad}) (sample {sample + 1}/3)")
            self.revolver.load_bullets_randomly(bulletsToLoad)
            log_drum("Drum state", self.revolver.drum)
            log_info("Bullets loaded", count_bullets(self.revolver.drum))
            self.assertEqual(count_bullets(self.revolver.drum), bulletsToLoad)
        print("---")
        
    # === Unloading Tests ===

    def test_07_unload_bullet(self):
        """Test unloading a bullet from chamber"""
        log_test("7 Testing unload_bullet -> chamber 1")
        self.revolver.load_bullet(0)
        log_drum("After loading", self.revolver.drum)
        self.revolver.unload_bullet(0)
        log_drum("After unloading", self.revolver.drum)
        self.assertIsNone(self.revolver.drum[0])

    def test_08_unload_drum(self):
        """Test dumping all chambers"""
        log_test("8 Testing unload_drum")
        self.revolver.load_bullets_in_order(4)
        log_drum("Before dump", self.revolver.drum)
        self.revolver.unload_drum()
        log_drum("After dump", self.revolver.drum)
        self.assertEqual(self.revolver.drum, [None, None, None, None, None, None])

    def test_09_speed_reload(self):
        """Test speed reload fills all chambers"""
        log_test("9 Testing speed_reload")
        self.revolver.load_bullet(0)
        log_drum("Before speed reload", self.revolver.drum)
        self.revolver.speed_reload()
        log_drum("After speed reload", self.revolver.drum)
        self.assertEqual(self.revolver.drum, [True, True, True, True, True, True])

    # === Trigger Tests ===

    def test_10_pull_trigger_loaded_chamber(self):
        """Test pulling trigger on loaded chamber"""
        log_test("10 Testing pull_trigger on loaded chamber")
        self.revolver.load_bullet(0)
        log_drum("Drum state", self.revolver.drum, self.revolver.activeChamberPosition)
        result = self.revolver.pull_trigger()
        log_drum("After trigger", self.revolver.drum, self.revolver.activeChamberPosition)
        log_result("Trigger", result)
        self.assertTrue(result)

    def test_11_pull_trigger_empty_chamber(self):
        """Test pulling trigger on empty chamber"""
        log_test("11 Testing pull_trigger on empty chamber")
        log_drum("Drum state", self.revolver.drum, self.revolver.activeChamberPosition)
        result = self.revolver.pull_trigger()
        log_drum("After trigger", self.revolver.drum, self.revolver.activeChamberPosition)
        log_result("Trigger", result)
        self.assertIsNone(result)

    def test_12_pull_trigger_sets_fired(self):
        """Test that firing sets chamber to False (fired)"""
        log_test("12 Testing that firing sets chamber to False (fired)")
        self.revolver.load_bullet(0)
        log_drum("Before firing", self.revolver.drum, self.revolver.activeChamberPosition)
        log_result("Trigger", self.revolver.pull_trigger())
        log_drum("After firing", self.revolver.drum, self.revolver.activeChamberPosition)
        self.assertFalse(self.revolver.drum[0])

    # === Drum Rotation Tests ===

    def test_13_rotate_drum_counter_clockwise(self):
        """Test drum rotation"""
        log_test("13 Testing rotate_drum_counter_clockwise")
        self.revolver.load_bullet(1)
        log_drum("Loaded pos 1", self.revolver.drum, self.revolver.activeChamberPosition)
        self.revolver.rotate_drum_counter_clockwise()
        log_drum("After rotate", self.revolver.drum, self.revolver.activeChamberPosition)
        result = self.revolver.pull_trigger()
        log_drum("After trigger", self.revolver.drum, self.revolver.activeChamberPosition)
        log_result("Trigger after 1 rotation", result)
        self.assertTrue(result)

    def test_14_rotate_drum_counter_clockwise_wraps_around(self):
        """Test drum rotation wraps at position 6"""
        log_test("14 Testing drum wrap-around after 6 rotations")
        log_drum("Initial", self.revolver.drum, self.revolver.activeChamberPosition)
        for i in range(6):
            self.revolver.rotate_drum_counter_clockwise()
            log_drum(f"After rotation {i+1}", self.revolver.drum, self.revolver.activeChamberPosition)
        self.revolver.load_bullet(0)
        log_drum("Loaded pos 0", self.revolver.drum, self.revolver.activeChamberPosition)
        result = self.revolver.pull_trigger()
        log_drum("After trigger", self.revolver.drum, self.revolver.activeChamberPosition)
        log_result("Trigger", result)
        self.assertTrue(result)

    def test_15_free_spin_drum(self):
        """Test that free spin drum works without error"""
        log_test("15 Testing free_spin_drum")
        self.revolver.load_bullet(0)
        log_drum("Before spin", self.revolver.drum, self.revolver.activeChamberPosition)
        self.revolver.free_spin_drum()
        log_drum("After spin", self.revolver.drum, self.revolver.activeChamberPosition)
        log_info("Spin", "completed")


# === Graphics Tests ===

class TestGraphics(unittest.TestCase):

    # === get_chamber_symbol Tests ===

    def test_16_get_chamber_symbol_empty(self):
        """Test that None returns empty space"""
        log_test("16 Testing get_chamber_symbol with None (empty)")
        result = graphics.get_chamber_symbol(None)
        log_pass_fail("Symbol", ' ', result)
        self.assertEqual(result, ' ')

    def test_17_get_chamber_symbol_live(self):
        """Test that True returns 'O' (live bullet)"""
        log_test("17 Testing get_chamber_symbol with True (live)")
        result = graphics.get_chamber_symbol(True)
        log_pass_fail("Symbol", 'O', result)
        self.assertEqual(result, 'O')

    def test_18_get_chamber_symbol_fired(self):
        """Test that False returns '@' (fired)"""
        log_test("18 Testing get_chamber_symbol with False (fired)")
        result = graphics.get_chamber_symbol(False)
        log_pass_fail("Symbol", '@', result)
        self.assertEqual(result, '@')

    # === display_drum Tests ===

    def test_19_display_drum_empty(self):
        """Test display_drum with empty drum (visual check)"""
        log_test("19 Testing display_drum with empty drum")
        drum = [None, None, None, None, None, None]
        log_info("Drum state", drum)
        print()
        graphics.display_drum(drum)
        self.assertTrue(True)

    def test_20_display_drum_loaded(self):
        """Test display_drum with loaded chambers"""
        log_test("20 Testing display_drum with loaded chambers")
        drum = [True, True, True, None, None, None]
        log_info("Drum state", drum)
        print()
        graphics.display_drum(drum)
        self.assertTrue(True)

    def test_21_display_drum_mixed(self):
        """Test display_drum with mixed states"""
        log_test("21 Testing display_drum with mixed states (empty, live, fired)")
        drum = [None, True, False, None, True, False]
        log_info("Drum state", drum)
        print()
        graphics.display_drum(drum)
        self.assertTrue(True)

    def test_22_display_drum_full(self):
        """Test display_drum with all chambers loaded"""
        log_test("22 Testing display_drum with full drum")
        drum = [True, True, True, True, True, True]
        log_info("Drum state", drum)
        print()
        graphics.display_drum(drum)
        self.assertTrue(True)

    def test_23_display_drum_all_fired(self):
        """Test display_drum with all chambers fired"""
        log_test("23 Testing display_drum with all fired")
        drum = [False, False, False, False, False, False]
        log_info("Drum state", drum)
        print()
        graphics.display_drum(drum)
        self.assertTrue(True)


# === Sound Effects Tests ===

class TestSoundEffects(unittest.TestCase):

    def test_24_sfx_dir_exists(self):
        """Test that sound effects directory exists"""
        log_test("24 Testing SFX_DIR exists")
        log_info("SFX_DIR", soundEffects.SFX_DIR)
        exists = os.path.isdir(soundEffects.SFX_DIR)
        log_pass_fail("Directory exists", True, exists)
        self.assertTrue(exists)

    def test_25_get_sfx_path(self):
        """Test _get_sfx_path returns correct path"""
        log_test("25 Testing _get_sfx_path")
        path = soundEffects._get_sfx_path('test.mp3')
        expected_end = os.path.join('sfx', 'test.mp3')
        log_info("Path", path)
        log_info("Ends with", expected_end)
        self.assertTrue(path.endswith(expected_end))

    def test_26_gunshot_file_exists(self):
        """Test gunshot sound file exists"""
        log_test("26 Testing gunshot file exists")
        path = soundEffects._get_sfx_path('single-pistol-gunshot.mp3')
        exists = os.path.exists(path)
        log_info("Path", path)
        log_pass_fail("File exists", True, exists)
        self.assertTrue(exists)

    def test_27_dryfire_file_exists(self):
        """Test dryfire sound file exists"""
        log_test("27 Testing dryfire file exists")
        path = soundEffects._get_sfx_path('revolver-dryfire.mp3')
        exists = os.path.exists(path)
        log_info("Path", path)
        log_pass_fail("File exists", True, exists)
        self.assertTrue(exists)

    def test_28_spin_file_exists(self):
        """Test spin sound file exists"""
        log_test("28 Testing spin file exists")
        path = soundEffects._get_sfx_path('revolver-spin.mp3')
        exists = os.path.exists(path)
        log_info("Path", path)
        log_pass_fail("File exists", True, exists)
        self.assertTrue(exists)

    def test_29_cock_file_exists(self):
        """Test cocking sound file exists"""
        log_test("29 Testing cocking file exists")
        path = soundEffects._get_sfx_path('revolver-cocking.mp3')
        exists = os.path.exists(path)
        log_info("Path", path)
        log_pass_fail("File exists", True, exists)
        self.assertTrue(exists)

    def test_30_holster_file_exists(self):
        """Test holster sound file exists"""
        log_test("30 Testing holster file exists")
        path = soundEffects._get_sfx_path('holster-pistol.mp3')
        exists = os.path.exists(path)
        log_info("Path", path)
        log_pass_fail("File exists", True, exists)
        self.assertTrue(exists)

    def test_31_shells_drop_file_exists(self):
        """Test shells drop sound file exists"""
        log_test("31 Testing shells drop file exists")
        path = soundEffects._get_sfx_path('shells-hitting-ground.mp3')
        exists = os.path.exists(path)
        log_info("Path", path)
        log_pass_fail("File exists", True, exists)
        self.assertTrue(exists)

    def test_32_sound_enabled_flag(self):
        """Test SOUND_ENABLED flag is defined"""
        log_test("32 Testing SOUND_ENABLED flag")
        log_info("SOUND_ENABLED", soundEffects.SOUND_ENABLED)
        self.assertIsInstance(soundEffects.SOUND_ENABLED, bool)

    def test_33_play_functions_callable(self):
        """Test all play functions are callable"""
        log_test("33 Testing play functions are callable")
        functions = [
            ('play_gunshot', soundEffects.play_gunshot),
            ('play_dryfire', soundEffects.play_dryfire),
            ('play_spin', soundEffects.play_spin),
            ('play_cock', soundEffects.play_cock),
            ('play_holster', soundEffects.play_holster),
            ('play_shells_drop', soundEffects.play_shells_drop),
            ('play_cock_alt', soundEffects.play_cock_alt),
        ]
        for name, func in functions:
            log_info(name, "callable" if callable(func) else "NOT callable")
            self.assertTrue(callable(func))


# === Player Tests ===

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("TestPlayer")

    def test_34_player_init(self):
        """Test player initialization"""
        log_test("34 Testing Player initialization")
        log_info("Name", self.player.name)
        log_info("Lives", self.player.lives)
        log_info("Has revolver", self.player.revolverInHand is not None)
        self.assertEqual(self.player.name, "TestPlayer")
        self.assertEqual(self.player.lives, 3)
        self.assertIsNotNone(self.player.revolverInHand)

    def test_35_player_custom_lives(self):
        """Test player with custom lives"""
        log_test("35 Testing Player with custom lives")
        player = Player("CustomPlayer", lives=5)
        log_info("Lives", player.lives)
        self.assertEqual(player.lives, 5)

    def test_36_player_is_alive(self):
        """Test is_alive returns True when lives > 0"""
        log_test("36 Testing is_alive")
        log_info("Lives", self.player.lives)
        log_pass_fail("is_alive", True, self.player.is_alive())
        self.assertTrue(self.player.is_alive())

    def test_37_player_take_damage(self):
        """Test take_damage reduces lives by 1"""
        log_test("37 Testing take_damage")
        log_info("Lives before", self.player.lives)
        self.player.take_damage()
        log_info("Lives after", self.player.lives)
        self.assertEqual(self.player.lives, 2)

    def test_38_player_die(self):
        """Test die sets lives to 0"""
        log_test("38 Testing die")
        log_info("Lives before", self.player.lives)
        self.player.die()
        log_info("Lives after", self.player.lives)
        log_pass_fail("is_alive", False, self.player.is_alive())
        self.assertEqual(self.player.lives, 0)
        self.assertFalse(self.player.is_alive())

    def test_39_player_shoot_himself_empty(self):
        """Test shoot_himself with empty chamber"""
        log_test("39 Testing shoot_himself with empty chamber")
        log_info("Lives before", self.player.lives)
        log_drum("Drum state", self.player.revolverInHand.drum)
        self.player.shoot_himself()
        log_info("Lives after", self.player.lives)
        self.assertEqual(self.player.lives, 3)

    def test_40_player_shoot_himself_loaded(self):
        """Test shoot_himself with loaded chamber"""
        log_test("40 Testing shoot_himself with loaded chamber")
        self.player.revolverInHand.load_bullet(0)
        log_info("Lives before", self.player.lives)
        log_drum("Drum state", self.player.revolverInHand.drum)
        self.player.shoot_himself()
        log_info("Lives after", self.player.lives)
        self.assertEqual(self.player.lives, 2)

    def test_41_player_shoot_player(self):
        """Test shoot_player damages target"""
        log_test("41 Testing shoot_player")
        target = Player("Target")
        self.player.revolverInHand.load_bullet(0)
        log_info("Shooter lives", self.player.lives)
        log_info("Target lives before", target.lives)
        self.player.shoot_player(target)
        log_info("Target lives after", target.lives)
        self.assertEqual(target.lives, 2)
        self.assertEqual(self.player.lives, 3)

    def test_42_player_give_revolver_to_crupier(self):
        """Test give_revolver_to_crupier transfers revolver"""
        log_test("42 Testing give_revolver_to_crupier")
        crupier = Crupier(revolver=None)
        crupier.revolverInHand = None
        log_info("Player has revolver before", self.player.revolverInHand is not None)
        log_info("Crupier has revolver before", crupier.revolverInHand is not None)
        self.player.give_revolver_to_crupier(crupier)
        log_info("Player has revolver after", self.player.revolverInHand is not None)
        log_info("Crupier has revolver after", crupier.revolverInHand is not None)
        self.assertIsNone(self.player.revolverInHand)
        self.assertIsNotNone(crupier.revolverInHand)


# === Crupier Tests ===

class TestCrupier(unittest.TestCase):

    def setUp(self):
        self.crupier = Crupier()

    def test_43_crupier_init(self):
        """Test crupier initialization"""
        log_test("43 Testing Crupier initialization")
        log_info("Name", self.crupier.name)
        log_info("Has revolver", self.crupier.revolverInHand is not None)
        self.assertEqual(self.crupier.name, "Crupier")
        self.assertIsNotNone(self.crupier.revolverInHand)

    def test_44_crupier_give_revolver_to_player(self):
        """Test give_revolver_to_player transfers revolver"""
        log_test("44 Testing give_revolver_to_player")
        player = Player("TestPlayer", revolver=None)
        player.revolverInHand = None
        log_info("Crupier has revolver before", self.crupier.revolverInHand is not None)
        log_info("Player has revolver before", player.revolverInHand is not None)
        self.crupier.give_revolver_to_player(player)
        log_info("Crupier has revolver after", self.crupier.revolverInHand is not None)
        log_info("Player has revolver after", player.revolverInHand is not None)
        self.assertIsNone(self.crupier.revolverInHand)
        self.assertIsNotNone(player.revolverInHand)

    def test_45_crupier_dump_and_load_single_bullet(self):
        """Test dump_and_load_single_bullet"""
        log_test("45 Testing dump_and_load_single_bullet")
        self.crupier.revolverInHand.load_bullets_in_order(3)
        log_drum("Before", self.crupier.revolverInHand.drum)
        self.crupier.dump_and_load_single_bullet()
        log_drum("After", self.crupier.revolverInHand.drum)
        self.assertEqual(count_bullets(self.crupier.revolverInHand.drum), 1)
        self.assertTrue(self.crupier.revolverInHand.drum[0])

    def test_46_crupier_dump_and_load_bullets_randomly(self):
        """Test dump_and_load_bullets_randomly"""
        log_test("46 Testing dump_and_load_bullets_randomly")
        log_drum("Before", self.crupier.revolverInHand.drum)
        self.crupier.dump_and_load_bullets_randomly(3)
        log_drum("After", self.crupier.revolverInHand.drum)
        self.assertEqual(count_bullets(self.crupier.revolverInHand.drum), 3)

    def test_47_crupier_setup_round_with_random_bullet_positions(self):
        """Test setup_round_with_random_bullet_positions"""
        log_test("47 Testing setup_round_with_random_bullet_positions")
        log_drum("Before", self.crupier.revolverInHand.drum)
        self.crupier.setup_round_with_random_bullet_positions(2)
        log_drum("After", self.crupier.revolverInHand.drum)
        self.assertEqual(count_bullets(self.crupier.revolverInHand.drum), 2)


# === Logger Tests ===

class TestLogger(unittest.TestCase):

    def setUp(self):
        self.logger = Logger()

    def test_48_logger_init(self):
        """Test logger initialization"""
        log_test("48 Testing Logger initialization")
        log_info("Has _get_timestamp", hasattr(self.logger, '_get_timestamp'))
        log_info("Has history", hasattr(self.logger, 'history'))
        log_info("History empty", len(self.logger.history) == 0)
        self.assertTrue(callable(self.logger._get_timestamp))
        self.assertEqual(self.logger.history, [])

    def test_49_logger_info(self):
        """Test info logging"""
        log_test("49 Testing Logger.info")
        self.logger.info("Test message")
        log_info("History length", len(self.logger.history))
        self.assertEqual(len(self.logger.history), 1)
        self.assertEqual(self.logger.history[0][1], "INFO")
        self.assertEqual(self.logger.history[0][2], "Test message")

    def test_50_logger_action(self):
        """Test action logging"""
        log_test("50 Testing Logger.action")
        self.logger.action("Test action")
        log_info("Level", self.logger.history[0][1])
        self.assertEqual(self.logger.history[0][1], "ACTION")

    def test_51_logger_warning(self):
        """Test warning logging"""
        log_test("51 Testing Logger.warning")
        self.logger.warning("Test warning")
        log_info("Level", self.logger.history[0][1])
        self.assertEqual(self.logger.history[0][1], "WARNING")

    def test_52_logger_danger(self):
        """Test danger logging"""
        log_test("52 Testing Logger.danger")
        self.logger.danger("Test danger")
        log_info("Level", self.logger.history[0][1])
        self.assertEqual(self.logger.history[0][1], "DANGER")

    def test_53_logger_result(self):
        """Test result logging"""
        log_test("53 Testing Logger.result")
        self.logger.result("Test result")
        log_info("Level", self.logger.history[0][1])
        self.assertEqual(self.logger.history[0][1], "RESULT")

    def test_54_logger_player(self):
        """Test player logging"""
        log_test("54 Testing Logger.player")
        self.logger.player("Alice", "did something")
        log_info("Level", self.logger.history[0][1])
        log_info("Message", self.logger.history[0][2])
        self.assertEqual(self.logger.history[0][1], "[Alice]")
        self.assertEqual(self.logger.history[0][2], "did something")

    def test_55_logger_round(self):
        """Test round logging"""
        log_test("55 Testing Logger.round")
        self.logger.round(5)
        log_info("Level", self.logger.history[0][1])
        self.assertEqual(self.logger.history[0][1], "ROUND")
        self.assertIn("5", self.logger.history[0][2])

    def test_56_logger_game_over_with_winner(self):
        """Test game_over with winner"""
        log_test("56 Testing Logger.game_over with winner")
        self.logger.game_over("Alice")
        log_info("Level", self.logger.history[0][1])
        log_info("Message", self.logger.history[0][2])
        self.assertEqual(self.logger.history[0][1], "GAME OVER")
        self.assertIn("Alice", self.logger.history[0][2])

    def test_57_logger_game_over_no_winner(self):
        """Test game_over without winner"""
        log_test("57 Testing Logger.game_over without winner")
        self.logger.game_over()
        log_info("Level", self.logger.history[0][1])
        log_info("Message", self.logger.history[0][2])
        self.assertEqual(self.logger.history[0][1], "GAME OVER")
        self.assertIn("No survivors", self.logger.history[0][2])

    def test_58_logger_get_history(self):
        """Test get_history returns copy"""
        log_test("58 Testing Logger.get_history")
        self.logger.info("Message 1")
        self.logger.info("Message 2")
        history = self.logger.get_history()
        log_info("History length", len(history))
        self.assertEqual(len(history), 2)
        history.append("fake")
        self.assertEqual(len(self.logger.history), 2)

    def test_59_logger_clear_history(self):
        """Test clear_history empties history"""
        log_test("59 Testing Logger.clear_history")
        self.logger.info("Message 1")
        self.logger.info("Message 2")
        log_info("History before", len(self.logger.history))
        self.logger.clear_history()
        log_info("History after", len(self.logger.history))
        self.assertEqual(len(self.logger.history), 0)


if __name__ == '__main__':
    unittest.main()
