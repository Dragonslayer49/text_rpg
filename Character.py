import random
from colorama import Fore, Style
import pygame
import numpy as np

# from rich.console import Console

pygame.init()


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
            case _:
                self.characterClass = "Knight"
                self.strength = random.randint(8, 12) + 3
                self.inventory["weapon"] = {"type": "Sword", "attack": 10}

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
        armor = self.inventory["armor"]

        if weapon:
            if "name" in weapon:
                print(f"{Fore.BLUE}Weapon: Type: {weapon['type']}, Name: {weapon['name']} Attack: {weapon['attack']}")
            else:
                print(f"{Fore.BLUE}Weapon: Type: {weapon['type']} Attack: {weapon['attack']}")
        else:
            print(f"{Fore.BLUE}No weapon equipped")

        if armor:
            print(f"{Fore.BLUE}Armor: Name: {armor['name']} Defense: {armor['defense']}")
        else:
            print(f"{Fore.BLUE}No armor equipped")

    def Getexp(self, exp):
        self.exp += exp
        if self.exp >= 100:
            self.strength += 2
            self.dexterity += 2
            self.inteligence += 3
            print("you leveled up!")
            self.level += 1
            self.exp = 0

    def takeDamage(self, damage):
        armor = self.inventory.get("armor", {"defense": 0})
        armor_defense = armor["defense"] if armor else 0
        total_damage = max(0, damage - armor_defense)
        self.health -= damage
        print(f"{Fore.YELLOW}You took {total_damage} damage!")

    def showHP(self):
        print(f"You have: {self.health}")

    def calculate_damage(self, enemy):
        weapon = self.inventory["weapon"]
        weapon_type = weapon["type"]
        weapon_attack = weapon["attack"]

        attribute_value = 0
        if weapon_type == "Sword":
            attribute_value = self.strength
        elif weapon_type == "Wand":
            attribute_value = self.inteligence
        elif weapon_type == "Bow":
            attribute_value = self.dexterity

        damage = np.multiply(np.multiply(0.1, attribute_value), weapon_attack)

        enemy.takeDamage(damage)
        print(f"{Fore.LIGHTRED_EX}You attacked with {weapon_type} and dealt {damage} damage!")

    def attack(self, enemy):
        self.calculate_damage(enemy)
        pygame.mixer.Sound("clash.wav").play()

    def loot_enemy(self):
        loot_chance = random.randint(1, 100)
        if loot_chance <= 50:
            new_weapon = self.loot_item("weapon")
            if new_weapon:
                self.ask_equip_weapon(new_weapon)
        elif loot_chance <= 80:
            new_armor = self.loot_item("armor")
            if new_armor:
                self.ask_equip_armor(new_armor)
        else:
            print(f"{Fore.GREEN}You didn't find any loot this time.")

    def loot_item(self, item_type):
        items = {
            "weapon": [
                {"type": "Sword", "name": "Broad Sword", "attack": 15},
                {"type": "Wand", "name": "Frost Wand", "attack": 12},
                {"type": "Bow", "name": "Crossbow", "attack": 14},
                {"type": "Sword", "name": "Long Sword", "attack": 20},
                {"type": "Wand", "name": "Fire Staff", "attack": 18},
                {"type": "Bow", "name": "Piercing Bow", "attack": 22},
                {"type": "Sword", "name": "Destroyer", "attack": 25},
                {"type": "Wand", "name": "Wand of Chaos", "attack": 23},
                {"type": "Bow", "name": "Bow of Decomposition", "attack": 22},
                {"type": "Sword", "name": "Excalibur", "attack": 26},
                {"type": "Wand", "name": "Holy Staff", "attack": 27},
                {"type": "Bow", "name": "Unholy Bow", "attack": 28}
            ],

            "armor": [
                {"name": "Leather Armor", "defense": 1},
                {"name": "Stone Armor", "defense": 2},
                {"name": "Plate Armor", "defense": 3},
                {"name": "Chainmail", "defense": 4},
                {"name": "Steel Plate", "defense": 5}

            ],
        }

        chosen_item_list = items.get(item_type, [])
        if chosen_item_list:
            chosen_item = random.choice(chosen_item_list)
            return chosen_item
        else:
            return None

    def loot_health_potion(self):
        print(f"{Fore.YELLOW}You found a health potion!")
        self.inventory["health_potion"] += 1

    def add_weapon_to_inventory(self, new_weapon):
        current_weapon = self.inventory["weapon"]
        if current_weapon:
            if "name" in current_weapon:
                print(
                    f"{Fore.LIGHTBLUE_EX}You already have a {current_weapon['type']} named {current_weapon['name']} with {current_weapon['attack']} attack.")
            else:
                print(
                    f"{Fore.LIGHTBLUE_EX}You already have a {current_weapon['type']} with {current_weapon['attack']} attack.")
            choice = input(f"{Fore.LIGHTGREEN_EX}Do you want to keep the old weapon? (Y/N): ").lower()
            if choice == "n":
                self.equip_weapon(new_weapon)
            else:
                print(f"{Fore.GREEN}You kept the old weapon.")
        else:
            self.equip_weapon(new_weapon)

    def ask_equip_armor(self, new_armor):
        print(f"{Fore.GREEN}You found armor named {new_armor['name']} with {new_armor['defense']} defense!")
        choice = input(f"{Fore.GREEN}Do you want to equip the {new_armor['name']}? (Y/N): ").lower()
        if choice == "y":
            self.equip_armor(new_armor)
            pygame.mixer.Sound("loot.wav").play()
        else:
            print(f"{Fore.YELLOW}You chose not to equip the new armor.")

    def equip_armor(self, armor):
        self.inventory["armor"] = armor
        print(f"{Fore.GREEN}You have equipped {armor['name']} with {armor['defense']} defense.")

    def equip_weapon(self, weapon):
        self.inventory["weapon"] = weapon
        print(f"{Fore.BLUE}You have equipped {weapon['type']}")

    def ask_equip_weapon(self, new_weapon):
        print(f"{Fore.BLUE}You found a {new_weapon['type']} with {new_weapon['attack']} attack!")
        choice = input(f"{Fore.BLUE}Do you want to equip the {new_weapon['type']}? (Y/N): ").lower()
        if choice == "y":
            self.equip_weapon(new_weapon)
            pygame.mixer.Sound("loot.wav").play()
        else:
            print(f"{Fore.YELLOW}You chose not to equip the new weapon.")

    def use_health_potion(self):
        if self.inventory["health_potion"] > 0:
            self.health += 20
            pygame.mixer.Sound("drinking.wav").play()
            self.inventory["health_potion"] -= 1
            print(f"{Fore.YELLOW}You have used a health potion. Current health: {self.health}")
        else:
            print(f"{Fore.GREEN}You don't have any health potions left.")

    def isAlive(self):
        if self.health <= 0:
            return False

        elif self.health > 0:
            return True
