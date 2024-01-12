import random
import Character
import Enemy


# komentarz se jest tu

def enemyLib(filename):
    enemies = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            species, health, attackPower = line.strip().split(',')
        enemy = Enemy.Enemy(species, health, attackPower)
        enemies.append(enemy)
    return enemies


name = input("write your name")
chosingC = input("choose your class:1-Knight 2-Mage 3-Archer")
player = Character.Character(name, chosingC)


class StartingArea:
    def __init__(self):
        self.player = player
        self.current_location = "Entrance"
        self.locations = {
            "Entrance":   [['You find yourself at an entrance to the forest'], ["North Path", "South Path"]],
            "North Path": [['While walking you see a cave'], ["cave", "North"]],
            "South Path": [['You see a river'], ["river", "South"]],

        }
        self.tutorial_location = "house"
        self.tutorial_locations = {
            "House": ["Forest"]
        }

    def tutorial(self):
        choice = input("would you like to do a tutorial? Y/N")
        if choice == "Y":
            enemies = enemyLib("monsters.txt")
            enemy = random.choice(enemies)
            print("You find yourself at a village, You see a smoke in the distance")
            print("1-check out the smoke")
            print("2-rest at your house")
            print("3-go to the forest")
            choice = input()
            match choice:
                case "1":
                    print("you see soldiers attacking a nearby village")
                    print("while you looked at the soldiers one noticed you and started going your way")
                    print("1-prepare for battle")
                    print("2-run away")
                    choice = input()
                    if choice == "1":
                        self.fight(enemy)
                case "2":
                    print("while resting a soldier went into you house with a sword in his hand")
                case "3":
                    print()

        else:
            self.navigate()

    def navigate(self):
        while player.isAlive():
            available_paths = self.locations[self.current_location][1]
            print("".join(self.locations[self.current_location][0]))
            print("Available paths:", ", ".join(self.locations[self.current_location][1]))
            print("")
            print("write inventory to Check Inventory")
            print("q to Quit")
            choice = input()
            if choice in available_paths:
                self.current_location = choice
                self.handle_event()
            match choice:
                case "1":
                    self.walk()
                case "Inventory":
                    player.show_weapon()
                    break
                case "3":
                    break

            if not player.isAlive():
                print("Game Over! ")
                break

    def handle_event(self):
        event = random.randint(1, 10)
        if event > 0:
            self.encounter()
        else:
            print("you walked without problems.")

    def encounter(self):

        enemies = enemyLib("monsters.txt")
        enemy = random.choice(enemies)
        print("you see a ", enemy.species, " in the distance")
        print("1-fight him")
        print("2-try to sneak past")
        choice = input()
        if choice == "2":
            success = random.randint(1, 10)
            if success > 1:  # potem zmienic zeby byla szansa na atak przeciwnika
                print("you successfully evaded ", enemy.species)
        elif choice == "1":
            self.fight(enemy)

    def fight(self, enemy):
        while player.isAlive() & enemy.isAlive():
            print("you attack", enemy.species)
            player.attack(enemy)
            enemy.showHP()
            if enemy.health < 1:
                print("you defeated", enemy.species)
                player.loot_enemy()
                print("Do you want to use a health potion? (Y/N): ")
                choice = input().lower()
                if choice == "y":
                    player.use_health_potion()
                break
            print(enemy.species, " attacks you")
            player.showHP()
            enemy.attack(player)

        if not player.isAlive():
            print("Game Over! You have been defeated.")
        else:
            self.navigate()


gaming = StartingArea()
gaming.tutorial()
