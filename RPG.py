import random
import Character
import Enemy
from colorama import init, Fore




def enemyLib(filename):
    enemies = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 3:
                species, health, attackPower = parts
                enemy = Enemy.Enemy(species, health, attackPower)
                enemies.append(enemy)
            else:
                print(f"Ignoring invalid line: {line}")
    return enemies


name = input(f"{Fore.CYAN}write your name:  ")
chosingC = input(f"{Fore.CYAN}choose your class:1-Knight 2-Mage 3-Archer ")
player = Character.Character(name, chosingC)


class StartingArea:
    def __init__(self):
        self.player = player
        self.current_location = "Entrance"
        self.locations = {
            "Entrance": [['You find yourself at the entrance of the forest, there are two paths before you'],
                         ["North Path", "South Path"]],
            "North Path": [['while walking through the path you see a abandoned cave entrance'],
                           ["Entrance", "Cave Entrance"]],
            "South Path": [['you spot a river while walking through the path'], ["Entrance", "River"]],
            "Cave Entrance": [['You enter the dark cave, a goblin blocks your way'],
                              ["North Path", "Fight Goblin", "South Path"]],
            "Fight Goblin": [['You are in a battle with a goblin'], ["Fight", "Flee"]],
            "River": [['You reach the river, a bridge is visible in the distance'], ["North Path", "Cross Bridge"]],
            "Cross Bridge": [['You cross the bridge and find a peaceful meadow'], ["River", "Meadow"]],
            "Meadow": [['You are in a beautiful meadow'], ["North Path", "South Path"]],
        }
        self.tutorial_location = "house"
        self.tutorial_locations = {
            "House": ["Forest"]
        }

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

    def navigate(self):
        while player.isAlive():
            available_paths = self.locations[self.current_location][1]
            print("\n".join(self.locations[self.current_location][0]))
            print("Available paths:", ", ".join(self.locations[self.current_location][1]))
            print(f"{Fore.BLUE}write Inventory to Check Inventory")
            print(f"{Fore.YELLOW}q to Quit\n")
            choice = input()
            if choice in available_paths:
                self.current_location = choice
                self.handle_event()
            elif choice == "q":
                break
            elif choice == "Inventory" or choice == "i" or choice == "inventory":
                player.show_weapon()
            else:
                print("Invalid")

            if not player.isAlive():
                print(f"{Fore.RED}Game Over! ")
                break

    def handle_event(self):
        event = random.randint(1, 10)
        if event > 1:
            self.encounter()
        else:
            print(f"{Fore.BLUE}you walked without problems.")

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
        else:
            self.navigate()


gaming = StartingArea()
gaming.tutorial()