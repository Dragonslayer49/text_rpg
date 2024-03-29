import random
import Character
from Enemy import Enemy
from colorama import init, Fore
import pygame
import time

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
        self.tutorial_location = "Dark Cave"
        self.tutorial_locations = {
            "Dark Cave": [['You find yourself inside a cave to look around press l'],
                          ['Big Room'], [
                              'you can smell a foul stench coming from walls most likely decomposing bodies\n you see a faint light coming from the North\n to navigate between rooms enter the name of the next location/ Big Room']],
            "Big Room": [['You enter a Big Room\n if you ever dont know what to do enter help '],
                         ['Dark Cave', 'Small Tunnel'], [
                             'You can see a small hole on the wall.\n there is something rustling in there']],
            "Small Tunnel": [['You can see the exit'],
                             ['Exit', 'Small Tunnel'], [
                                 'You are almost free']],

        }

    def navigate(self):
        numerek = 0
        iloscprob = 0
        while player.isAlive():
            if self.current_location == "Cave Entrance":
                choice = input("would you like to enter this cave? Y/N")
                match choice:
                    case "Y":
                        self.cave()
                    case "N":
                        break
            if self.current_location == "River":
                choice = input("You see a fishing spot.\nwould you like to check it out? Y/N")
                match choice:
                    case "Y":
                        self.river()
                    case "N":
                        break

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
            elif choice == "stats" or choice == "Stats" or choice == "s":
                player.showstats()
            elif choice == "HP" or choice == "hp" or choice == "Hp":
                player.showHP()
            elif choice == "help":
                print(f"{Fore.GREEN}To go into any place write the name of the place")
                print(f"{Fore.BLUE}write Inventory to Check Inventory")
                print(f"{Fore.YELLOW}to look around or investigate write look or l")
                print(f"{Fore.YELLOW}to see your stats enter stats")
                print(f"{Fore.YELLOW}to see your health enter hp")
                print(f"{Fore.RED}q to Quit\n")
            else:
                print("invalid")
                iloscprob += 1
                if iloscprob >= 3:
                    print('if you dont know what to do write help')
                    iloscprob = 0

            if not player.isAlive():
                print(f"{Fore.RED}Game Over! ")
                break

    def handle_event(self):
        event = random.randint(1, 10)
        if event > 1:
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
        choice = 0
        while choice != "1" and choice != "2":
            choice = input()

        if choice == "2":
            success = random.randint(1, 10)
            if success > 1:  # potem zmienic zeby byla szansa na atak przeciwnik
                print(f"{Fore.BLUE}you successfully evaded ", enemy.species)
                self.navigate()
        elif choice == "1":
            self.fight(enemy)

    def fight(self, enemy):
        while player.isAlive() & enemy.isAlive():
            print(f"{Fore.LIGHTRED_EX}you attack", enemy.species)
            time.sleep(1)
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
            time.sleep(1)
            enemy.attack(player)

        if not player.isAlive():
            print(f"{Fore.RED}Game Over! You have been defeated.")
            pygame.mixer.Sound("death.wav").play()
            exit()

        else:
            self.navigate()

    def cave(self):
        print("you are walking through the cave until you see a big monster")
        print("the monster seems to be asleep near him you see a chest with gold")
        print("1-try to sneak past and get the gold\n2-atack the big monster\n3-escape while he still sleeps")
        choice = input()
        enemies = enemyLib("monsters.txt")
        boss = enemies[3]
        match choice:
            case '1':
                print(
                    "big monster seems to be in a very deep sleep and doesnt notice you taking the "
                    "chest\nunfortunately you didnt notice that the chest wast tied to the wall and you trip")
                print("big monster wakes up")
                self.bossfight(boss)
            case '2':
                print("Monster wakes up and starts to attack you")
                self.bossfight(boss)
            case '3':
                print("the monster seems to be in a very deep sleep and doesnt wake up while you escape")
                self.navigate()

    def bossfight(self, boss):

        while player.isAlive() & boss.isAlive():
            print(f"{Fore.LIGHTRED_EX}you attack", boss.species)
            time.sleep(1)
            player.attack(boss)
            boss.showHP()
            if boss.health < 1:
                print(f"{Fore.BLUE}you defeated", boss.species)
                print(f"{Fore.BLUE}you have {player.health} hp")
                pygame.mixer.Sound("victory.mp3").play()
                player.Getexp(boss.exp)
                player.loot_enemy()
                print(f"{Fore.CYAN}Do you want to use a health potion? (Y/N): ")
                choice = input().lower()
                if choice == "y":
                    player.use_health_potion()
                break
            print(boss.species, f"{Fore.RED} attacks you")
            player.showHP()
            time.sleep(1)
            boss.attack(player)

        if not player.isAlive():
            print(f"{Fore.RED}Game Over! You have been defeated.")
            pygame.mixer.Sound("death.wav").play()
            exit()
        else:
            print('with monsters death the cave starts shaking\n you manage to run out before its to late')
            del self.locations["Cave Entrance"]
            self.locations['ruined cave entrance'] = [['the cave you have been in seems to be blocked by rocks'],
                                                      ["North Path"]]
            self.locations["North Path"] = [['while walking through the path you see the ruined cave that you have '
                                             'been to'],
                                            ["Entrance", "ruined cave entrance"], ["the cave is now just a pile of "
                                                                                   "rocks"]]
            self.current_location = 'ruined cave entrance'
            self.navigate()

    def bossfightriver(self, boss):

        while player.isAlive() & boss.isAlive():
            print(f"{Fore.LIGHTRED_EX}you attack", boss.species)
            time.sleep(1)
            player.attack(boss)
            boss.showHP()
            if boss.health < 1:
                print(f"{Fore.BLUE}you defeated", boss.species)
                print(f"{Fore.BLUE}you have {player.health} hp")
                pygame.mixer.Sound("victory.mp3").play()
                player.Getexp(boss.exp)
                player.loot_enemy()
                print(f"{Fore.CYAN}Do you want to use a health potion? (Y/N): ")
                choice = input().lower()
                if choice == "y":
                    player.use_health_potion()
                break
            print(boss.species, f"{Fore.RED} attacks you")
            player.showHP()
            time.sleep(1)
            boss.attack(player)

        if not player.isAlive():
            print(f"{Fore.RED}Game Over! You have been defeated.")
            pygame.mixer.Sound("death.wav").play()
            exit()
        else:
            print('the rod breaks and monster lies dead')
            del self.locations["River"]
            self.locations["River Spot"] = [['You see a topielec dead body lying and a broken fishing rod'],
                                            ["South Path", "Cross Bridge"]]
            self.locations["South Path"] = [['you spot a broken fishing rod while walking through the path'],
                                            ["Entrance", "River Spot"]]
            self.locations["Cross Bridge"] = [['You cross the bridge and find a peaceful meadow'],
                                              ["River Spot", "Meadow"]]
            self.current_location = "River Spot"
            self.navigate()

    def river(self):
        print("You see a fishing rod near the river would you like to fish:\n1-yes\n2-no")
        choice = 0
        while choice != '1' and choice != '2':
            choice = input()

        if choice == '1':
            enemies = enemyLib("monsters.txt")
            boss = enemies[13]
            print("suddenly water monster comes out of the water and attacks you!!")
            cokolwiek = input("press anything to continue")
            self.bossfightriver(boss)
        elif choice == '2':
            self.navigate()

    def turtorial(self):
        numerek = 0
        while player.isAlive():
            if self.tutorial_location == "Small Tunnel":
                enemies = enemyLib("monsters.txt")
                enemy = enemies[6]
                self.fight(enemy)

            available_paths = self.tutorial_locations[self.tutorial_location][1]
            if numerek == 0:
                print("\n".join(self.tutorial_locations[self.tutorial_location][0]))
                print("Available paths:", ", ".join(self.tutorial_locations[self.tutorial_location][1]))
                numerek += 1

            choice = input()
            if choice in available_paths:
                self.tutorial_location = choice
                numerek = 0
            elif choice == "q":
                break
            elif choice == "l":
                print(str(self.tutorial_locations[self.tutorial_location][2]))
            elif choice == "Inventory" or choice == "i" or choice == "inventory":
                player.show_weapon()
            elif choice == "stats" or choice == "Stats" or choice == "s":
                player.showstats()
            elif choice == "HP" or choice == "hp" or choice == "Hp":
                player.showHP()
            elif choice == "help":
                print(f"{Fore.GREEN}To go into any place write the name of the place")
                print(f"{Fore.BLUE}write Inventory to Check Inventory")
                print(f"{Fore.YELLOW}to look around or investigate write look or l")
                print(f"{Fore.YELLOW}to see your stats enter stats")
                print(f"{Fore.YELLOW}to see your health enter hp")
                print(f"{Fore.RED}q to Quit\n")
            else:
                print("Invalid")

            if not player.isAlive():
                print(f"{Fore.RED}Game Over! ")
                break


gaming = StartingArea()
choice = input(f"{Fore.CYAN}would you like to do a tutorial? Y/N")
if choice == "Y":
    gaming.turtorial()
else:
    gaming.navigate()
