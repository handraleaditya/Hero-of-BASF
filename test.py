# Sample Tests written for sanity checks
# Execute using "python -m unittest test.py"



import unittest # to write unit tests
from unittest.mock import patch # To mock output from random.random()
from main import Game, Hero, Orc, Dragon, Character # importing classes

class TestGame(unittest.TestCase):

    # Setting up characters
    def setUp(self):
        self.game = Game()
        self.hero = Character("HERO", health_points=35, base_damage=2, crit_chance=0.2)
        self.orc = Character("ORC", health_points=7, base_damage=1, crit_chance=0.5)            
        self.dragon = Character("DRAGON", health_points=20, base_damage=3, crit_chance=0.4)
  
    # Crit damage test
    def test_hero_crit_attack(self):
        # Mock the random function to always return 0.0 for crit chance so that its always a CRIT
        with patch('random.random', return_value=0.0):
            damage = self.hero.attack(self.orc)
            self.assertEqual(damage, 4)  # Crit damage always, should be 4

    # Non crit damage test
    def test_hero_base_attack(self):
        # Mock the random function to always return 1.0 for crit chance so that its never a CRIT
        with patch('random.random', return_value=1.0):
            damage = self.hero.attack(self.orc)
            self.assertEqual(damage, 2)  # Crit damage always, should be 4

    def test_orc_attack(self):
        # Mock the random function to always return 1.0 for crit chance
        with patch('random.random', return_value=1.0):
            hero = Hero()
            damage = self.game.orc.attack(hero)
            self.assertEqual(damage, 1)  # Non-crit damage

    def test_orc_crit_attack(self):
        # Mock the random function to always return 1.0 for crit chance
        with patch('random.random', return_value=0.0):
            hero = Hero()
            damage = self.game.orc.attack(hero)
            self.assertEqual(damage, 2)  # crit damage

    def test_dragon_crit_attack(self):
        # Mock the random function to always return 0.0 for crit chance
        with patch('random.random', return_value=0.0):
            hero = Hero()
            damage = self.game.dragon.attack(hero)
            self.assertEqual(damage, 6)  # Crit damage

    def test_dragon_base_attack(self):
        # Mock the random function to always return 1.0 for crit chance
        with patch('random.random', return_value=1.0):
            hero = Hero()
            damage = self.game.dragon.attack(hero)
            self.assertEqual(damage, 3)  #Non  Crit damage

    # To test function reduce HP
    def test_reduce_hp(self):
        character = Character("Test", 10, 2, 0.2)
        character.reduce_hp(3)
        self.assertEqual(character.health_points, 7)

 
if __name__ == '__main__':
    unittest.main()