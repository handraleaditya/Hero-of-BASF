# Python CLI text game "Hero of BASF"
# Author : Aditya Handrale


import time # for adding delay (sleep) between dialogue
import random # used to handle crit chance and random monster turn
import textwrap # used to wrap text around console, for aesthetic purposes
import cmd 
import sys # for handling system commands like sys.exit() for quitting game
import os # used to clear the console

### Game Settings ###
screen_width = 150


"""
Main character base class from which Hero, Orc and Dragon will be inherited
 Contains attributes like Name, HP (health points), DMG (damage) and CRIT (critical damage chance) 
 And methods like attack() to attack, is_critical() to calculate critical chance, reduce_hp() to reduce health
"""
class Character:
    def __init__(self, name = "", health_points = 0, base_damage = 0, crit_chance= 0.0):
        self.name = name 
        self.health_points = health_points
        self.base_damage = base_damage
        self.crit_chance = crit_chance

    # function used to attack a monster/player
    def attack(self, target):
        # check if damage is critical, multiply by 2, else use normal damage
        if self.is_critical():
            damage = self.base_damage * 2
            print("A CRITICAL HIT!")
        else: 
            damage = self.base_damage
        # reduce target HP according to calculated damage    
        target.reduce_hp(damage)
        return damage

    # check if the new attack is a critical attack or a normal attack using crit chance attribute
    def is_critical(self):
        # return either True or False
        # ex: random_random generates value b/w 0 to 1, if it is greater than crit chance register as a critical hit
        return random.random() < self.crit_chance

    # function to reduce HP after taking damage, HP should not go below 0 
    def reduce_hp(self, damage):
        self.health_points = max(0, self.health_points - damage)


"""
Creating children classes for hero, orc and dragon inherited from Character using super() and initializing them
"""
class Hero(Character):
    def __init__(self):
        super().__init__("HERO", health_points=35, base_damage=2, crit_chance=0.2)

class Orc(Character):
    def __init__(self):
        super().__init__("ORC", health_points=7, base_damage=1, crit_chance=0.5)

class Dragon(Character):
    def __init__(self):
        super().__init__("DRAGON", health_points=20, base_damage=3, crit_chance=0.4)


"""Game class has functions to display menu, title screen etc and runs the main gameplay loop"""
class Game:

    # populating the Game instance with the 3 characters
    def __init__(self):
        self.hero = Hero()
        self.orc = Orc()
        self.dragon = Dragon()

    # Title screen at the start of the game, contains the Menu. 
    # This will be the first thing printed on the console
    def title_screen(self):
        print("\n############################")
        print("# Welcome to Hero of BASF! #")
        print("############################\n")
        print("          - PLAY -          ")
        print("          - HELP -          ")
        print("          - QUIT -          ")
        print("\nCopyright © 2024 Aditya Handrale ")
        print("> Enter a choice")
        self.menu() # display the menu again


    # Menu to be shown at title screen the start of the game, has three options
    # 1. PLAY : Starts the game
    # 2. HELP : Displays the tutorial
    # 3. QUIT : Exits the game
    def menu(self):
        option = input("> ")
        if option.lower() == "play":
            self.start_game()
        elif option.lower() == "help":
            self.help()
        elif option.lower() == "quit":
            sys.exit()
        else:
            print("Please enter a valid choice")
            self.menu()


    # This is the help screen, which displays helpful tips on the main menu
    def help(self):
        print("\n\n############################")
        print("#        -TUTORIAL-        #")
        print("############################")
        print("- Use commands like 'attack orc' or 'attack dragon'")
        print("- Commands are case insensitive, use capital or lowercase")
        print("- Your objective is to defeat the monsters without running out of your HP")
        print("- Good luck and have fun!")
        self.title_screen()
        self.menu()





    def display_message(self,message):
        print(message)
        time.sleep(0.1)


    # function to display basic intro text, then start the gameplay loop
    def intro_text(self):
        self.display_message("\n*You wake up in a daze*")
        self.display_message("finding yourself in a dungeon...your head hurts and your armor is missing...")
        self.display_message("You dont remember anything... and suddenly hear a loud, primal, animalistic sound. It makes your bones shiver")
        self.display_message("You see a rusted SWORD (DMG - 2HP) in the corner of the dungeon, you go ahead and pick it up")
        self.display_message("\n* Two monsters are standing next to you, angry & ready to attack! an ORC (7HP) & a DRAGON (20HP)!  *")
        self.display_message("You can either attack the ORC ('attack orc') or the DRAGON('attack dragon')")
        self.gameplay_loop()

    # this is the main gameplay loop of the game
    def gameplay_loop(self):

        move_counter = 0
        while self.hero.health_points > 0 and (self.orc.health_points >0 or self.dragon.health_points>0):
            
            # Player turn
            # player attacks ORC or DRAGON
            self.display_message("Your turn")
            action = input("> ")
            move_counter += 1
            critical = self.hero.is_critical()
            if action.lower() == "attack orc":
                if self.orc.health_points == 0:
                    print("You hit the dead body of the ORC! nothing seems to happen")
                    continue
                target = "ORC"
                damage = self.hero.attack(self.orc)
                self.display_message(f"--- {self.hero.name} attacks {target} and reduces its HP by {damage}!")
                if self.orc.health_points == 0:
                    self.display_message("Hurray! The ORC was slain!")
                self.display_message(f"- {self.orc.name} has {self.orc.health_points} HP remaining ")
                self.display_message(f"- {self.dragon.name} has {self.dragon.health_points} HP remaining ")
                self.display_message(f"- {self.hero.name} has {self.hero.health_points} HP remaining \n")
            elif action.lower() == "attack dragon":
                if self.dragon.health_points == 0:
                    print("You hit the dead body of the DRAGON! nothing seems to happen")
                    continue
                target = "DRAGON"
                damage = self.hero.attack(self.dragon)
                self.display_message(f"--- {self.hero.name} attacks {target} and reduces its HP by {damage}!")

                if self.dragon.health_points == 0:
                    self.display_message("Hurray! The DRAGON was slain!")
                self.display_message(f"- {self.orc.name} has {self.orc.health_points} HP remaining ")
                self.display_message(f"- {self.dragon.name} has {self.dragon.health_points} HP remaining ")
                self.display_message(f"- {self.hero.name} has {self.hero.health_points} HP remaining \n")
            else:
                self.display_message("Invalid choice! please try again")
                continue

            # Monsters turn
            # selecting the enemy who will attack   
            # check if monsters are still alive, if both alive, choose random
            if self.orc.health_points > 0 and self.dragon.health_points > 0: 
                enemy = random.choice(['ORC','DRAGON'])
            # if one of only ORC is alive
            elif self.orc.health_points > 0:
                enemy = "ORC"
            # if only DRAGON is alive
            elif self.dragon.health_points > 0:
                enemy = "DRAGON"
            else:
                continue
            
            self.display_message("Enemy turn")
            if enemy == "ORC":
                damage = self.orc.attack(self.hero)
                self.display_message(f"--- {enemy} attacks {self.hero.name} and reduces its HP by {damage}!")
                self.display_message(f"- {self.orc.name} has {self.orc.health_points} HP remaining ")
                self.display_message(f"- {self.dragon.name} has {self.dragon.health_points} HP remaining ")
                self.display_message(f"- {self.hero.name} has {self.hero.health_points} HP remaining \n")

            if enemy == "DRAGON":
                damage = self.dragon.attack(self.hero)
                self.display_message(f"--- {enemy} attacks {self.hero.name} and reduces its HP by {damage}!")
                self.display_message(f"- {self.orc.name} has {self.orc.health_points} HP remaining ")
                self.display_message(f"- {self.dragon.name} has {self.dragon.health_points} HP remaining ")
                self.display_message(f"- {self.hero.name} has {self.hero.health_points} HP remaining \n")

        if self.hero.health_points <= 0:
            self.display_message("Uh Oh! You were slain by the monsters!\n\n")
            self.display_message("GAME OVER! LOSER!! You're fired! You failed to protect BASF! git gud and try again...\n\n")
            time.sleep(5)
            exit()
        else:
            self.display_message("\n\nCongratulations! You slayed both the monsters and protected BASF! You've been promoted to CEO!")
            self.display_message(f"Total moves : {move_counter}")
            salary_hike = move_counter * 6.9
            self.display_message(f"Salary hike (High score) : {salary_hike}%")
            self.display_message(f"The End! Try for a better score next time!\n\n")
            time.sleep(5)
            exit()

    def start_game(self):
        self.intro_text()
        self.gameplay_loop()


# runs the main function to start the game
if  __name__ == "__main__":
    os.system("cls") # clears the console
    game = Game() # create instance of Game class
    game.title_screen() # display the title screen