import random
import Character
from Enemy import Enemy
from colorama import init, Fore
import pygame

pygame.init()


def enemyLib(filename):
    enemies = []
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                species, health, attackPower, exp = line.strip().split(',')
                enemy = Enemy(species, health, attackPower, exp)
                enemies.append(enemy)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{filename}' not found.")
    except Exception as e:
        print(f"{Fore.RED}Error reading '{filename}': {e}")

    return enemies



name = input(f"{Fore.CYAN}write your name:  ")
chosingC = input(f"{Fore.CYAN}choose your class:1-Knight 2-Mage 3-Archer ")
player = Character.Character(name, chosingC)


class StartingArea:
    def __init__(self):
        pygame.mixer.music.load("background.wav.wav")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        self.player = player
        self.current_location = "Entrance"
        self.locations = {
            "Entrance": [['You find yourself at the entrance of the forest, there are two paths before you'],
                         ["North Path", "South Path"], ["grass is very nice"]],
            "North Path": [['while walking through the path you see a abandoned cave entrance'],
                           ["Entrance", "Cave Entrance"], ["cave seems to emanate with bad energy"]],
            "South Path": [['you spot a river while walking through the path'], ["Entrance", "River"]],
            "Cave Entrance": [['You enter the dark cave'],
                              ["North Path", "Flower Garden"],
                              ['the rocks are very beautiful']],
            "River": [['You reach the river, a bridge is visible in the distance'], ["South Path", "Cross Bridge"]],
            "Cross Bridge": [['You cross the bridge and find a peaceful meadow'], ["River", "Meadow"]],
            "Meadow": [['You are in a beautiful meadow'], ["Entrance"], ["meadow is nice"]],
            "Flower Garden": [['you enter a beautiful garden'],
                              ["Meadow", "Cave Entrance"],
                              ['flowers are everywhere']],

        }
        self.tutorial_location = "house"
        self.tutorial_locations = {
            "House": ["Forest"]
        }

    def navigate(self):
        numerek = 0
        while player.isAlive():
            available_paths = self.locations[self.current_location][1]
            if numerek == 0:
                print("\n".join(self.locations[self.current_location][0]))
                print("Available paths:", ", ".join(self.locations[self.current_location][1]))
                numerek += 1
            choice = input()
            if choice in available_paths:
                self.current_location = choice
                self.handle_event()
            elif choice == "q":
                break
            elif choice == "l":
                print(self.locations[self.current_location][2])
            elif choice == "Inventory" or choice == "i" or choice == "inventory":
                player.show_weapon()
            elif choice == "help":
                print(f"{Fore.GREEN}To go into any place write the name of the place")
                print(f"{Fore.BLUE}write Inventory to Check Inventory")
                print(f"{Fore.YELLOW}to look around or investigate write look or l")
                print(f"{Fore.RED}q to Quit\n")
            else:
                print("Invalid")

            if not player.isAlive():
                print(f"{Fore.RED}Game Over! ")
                break

    def handle_event(self):
        event = random.randint(1, 10)
        if event > 9:
            self.encounter()
        else:
            print(f"{Fore.BLUE}you walked without problems.")
            self.navigate()

    def encounter(self):

        enemies = enemyLib("monsters.txt")
        enemy = random.choice(enemies)
        print(f"{Fore.BLUE}you see a ", enemy.species, " in the distance")
        print(f"{Fore.YELLOW}1-fight him")
        print(f"{Fore.BLUE}2-try to sneak past")
        choice = input()
        if choice == "2":
            success = random.randint(1, 10)
            if success > 1:  # potem zmienic zeby byla szansa na atak przeciwnika
                print(f"{Fore.BLUE}you successfully evaded ", enemy.species)
                self.navigate()
        elif choice == "1":
            self.fight(enemy)

    def fight(self, enemy):
        while player.isAlive() & enemy.isAlive():
            print(f"{Fore.LIGHTRED_EX}you attack", enemy.species)
            player.attack(enemy)
            enemy.showHP()
            if enemy.health < 1:
                print(f"{Fore.BLUE}you defeated", enemy.species)
                print(f"{Fore.BLUE}you have {player.health} hp")
                pygame.mixer.Sound("victory.mp3").play()
                player.Getexp(enemy.exp)
                player.loot_enemy()
                print(f"{Fore.CYAN}Do you want to use a health potion? (Y/N): ")
                choice = input().lower()
                if choice == "y":
                    player.use_health_potion()
                break
            print(enemy.species, f"{Fore.RED} attacks you")
            player.showHP()
            enemy.attack(player)

        if not player.isAlive():
            print(f"{Fore.RED}Game Over! You have been defeated.")
            pygame.mixer.Sound("death.wav").play()
        else:
            self.navigate()

    def cave(self):
        print("you are walking through the cave until you see a big monster")
        print("the monster seems to be asleep near him you see a chest with gold")
        print("1-try to sneak past and get the gold\n2-sneak atack the big monster\n3-escape while he still sleeps")
        choice = input()
        match choice:
            case '1':
                print(
                    "big monster seems to be in a very deep sleep and doesnt notice you taking the "
                    "chest\nunfortunately you didnt notice that the chest wast tied to the wall and you trip")
                print("big monster wakes up")
                self.bossfight()
            case '3':
                print("the monster seems to be in a very deep sleep and doesnt wake up while you escape")
                self.navigate()

    def bossfight(self):
        print("bossfight here")
        print('after defeating the boss you return to the cave entrance')
        self.locations['cave entrance']= [['the cave you have been in seems to be blocked by rocks'],
                                          ["North Path", "South Path"]]
        self.navigate()

    def river(self):
        print("river")

    def tutorial(self):
        choice = input(f"{Fore.CYAN}would you like to do a tutorial? Y/N")
        if choice == "Y":
            enemies = enemyLib("monsters.txt")
            enemy = random.choice(enemies)
            print(f"{Fore.GREEN}You find yourself at a village, You see a smoke in the distance")
            print(f"{Fore.CYAN}1-check out the smoke")
            print(f"{Fore.LIGHTGREEN_EX}2-rest at your house")
            print(f"{Fore.CYAN}3-go to the forest")
            choice = input()
            match choice:
                case "1":
                    print(f"{Fore.GREEN}you see soldiers attacking a nearby village")
                    print(f"{Fore.GREEN}while you looked at the soldiers one noticed you and started going your way")
                    print(f"{Fore.RED}1-prepare for battle")
                    print(f"{Fore.YELLOW}2-run away")
                    choice = input()
                    if choice == "1":
                        self.fight(enemy)
                case "2":
                    print(f"{Fore.GREEN}while resting a soldier went into you house with a sword in his hand")
                case "3":
                    print()

        else:
            self.navigate()


gaming = StartingArea()
gaming.tutorial()
