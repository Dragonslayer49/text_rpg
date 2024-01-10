import random


#test
# masz małego
class Character:
    def __init__(self, name, characterClass):
        self.name = name
        self.characterClass = characterClass
        self.level = 5
        self.exp = 0
        self.health = 100
        self.strength = random.randint(8, 12)
        self.dexterity = random.randint(8, 12)
        self.inteligence = random.randint(8, 12)
        self.constitution = random.randint(8, 12)
        self.inventory = {
            "weapon": None,
            "armor": None,
            "health_potion": 3
        }
        match characterClass:
            case "Knight" | "1":
                self.strength = random.randint(8, 12) + 3
                self.inventory["weapon"] = {"type": "Sword", "attack": 10}
            case "Mage" | "2":
                self.inteligence = random.randint(8, 12) + 3
                self.inventory["weapon"] = {"type": "Wand", "attack": 8}
            case "Archer" | "3":
                self.dexterity = random.randint(8, 12) + 3
                self.inventory["weapon"] = {"type": "Bow", "attack": 12}

    def showstats(self):
        print(f"Name: {self.name}")
        print(f"Class: {self.characterClass}")
        print(f"Level: {self.level}")
        print(f"Health: {self.health}")
        print(f"Strength: {self.strength}")
        print(f"Dexterity: {self.dexterity}")
        print(f"Intelligence: {self.inteligence}")
        print(f"Constitution: {self.constitution}")
        print(f"Weapon: {self.inventory['weapon']}")
        self.show_weapon()

    def show_weapon(self):
        weapon = self.inventory["weapon"]
        if weapon:
            print(f"Weapon: Type: {weapon['type']}, Attack: {weapon['attack']}")
        else:
            print("No weapon equipped")

    def Getexp(self, exp):
        self.exp += exp
        if self.exp >= 100:
            print("you leveled up!")
            self.level += 1
            self.exp = 0

    def takeDamage(self, damage):
        self.health -= damage

    def showHP(self):
        print(f"You have: {self.health}")

    def attack(self, enemy):
        weapon = self.inventory["weapon"]
        weapon_type = weapon["type"]
        weapon_attack = weapon["attack"]

        if weapon_type == "Sword":
            damage = self.strength * weapon_attack
        elif weapon_type == "Wand":
            damage = self.inteligence * weapon_attack
        elif weapon_type == "Bow":
            damage = self.dexterity * weapon_attack
        else:
            print("Unknown weapon type")
            return

        enemy.takeDamage(damage)
        print(f"You attacked with {weapon_type} and dealt {damage} damage!")

    def loot_enemy(self):
        loot_chance = random.randint(1, 100)
        if loot_chance <= 50:
            new_weapon = self.loot_item("weapon")
            if new_weapon:
                print(f"You found a {new_weapon['type']} with {new_weapon['attack']} attack!")
                self.ask_equip_weapon(new_weapon)
        elif loot_chance <= 80:
            self.loot_health_potion()
        else:
            print("You didn't find any loot this time")

    def loot_item(self, item_type):
        items = {
            "weapons": [
                {"type": "Sword", "attack": 15},
                {"type": "Wand", "attack": 12},
                {"type": "Bow", "attack": 14},
                {"type": "Sword", "attack": 20},
                {"type": "Wand", "attack": 18},
                {"type": "Bow", "attack": 22},
                {"type": "Sword", "attack": 25},
                {"type": "Wand", "attack": 23},
                {"type": "Bow", "attack": 22},
                {"type": "Sword", "attack": 26},
                {"type": "Wand", "attack": 27},
                {"type": "Bow", "attack": 28}
            ],
        }

        chosen_item_list = items.get(item_type, [])
        if chosen_item_list:
            chosen_item = random.choice(chosen_item_list)
            print(f"You found a {chosen_item['type']} with {chosen_item['attack']} attack!")
            return chosen_item
        else:
            print(f"No {item_type} found.")
            return None

    def loot_health_potion(self):
        print("You found a health potion!")
        self.inventory["health_potion"] += 1

    def add_weapon_to_inventory(self, new_weapon):
        current_weapon = self.inventory["weapon"]
        if current_weapon:
            print(f"You already have a {current_weapon['type']} with {current_weapon['attack']} attack.")
            choice = input("Do you want to keep the old weapon? (Y/N): ").lower()
            if choice == "n":
                self.equip_weapon(new_weapon)
            else:
                print("You kept the old weapon.")
        else:
            self.equip_weapon(new_weapon)

    def equip_weapon(self, weapon):
        self.inventory["weapon"] = weapon
        print(f"You have equipped {weapon['type']}")

    def ask_equip_weapon(self, new_weapon):
        print(f"You found a {new_weapon['type']} with {new_weapon['attack']} attack!")
        choice = input(f"Do you want to equip the {new_weapon['type']}? (Y/N): ").lower()
        if choice == "y":
            self.add_weapon_to_inventory(new_weapon)
        else:
            print("You chose not to equip the new weapon.")

    def use_health_potion(self):
        if self.inventory["health_potion"] > 0:
            self.health += 20
            self.inventory["health_potion"] -= 1
            print(f"You have used a health potion. Current health: {self.health}")
        else:
            print("You don't have any health potions left.")

    def isAlive(self):
        if self.health <= 0:
            return False

        elif self.health > 0:
            return True
