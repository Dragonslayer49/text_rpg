import random

#masz małego
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
        match characterClass:
            case "Knight" | "1":
                self.strength = random.randint(8, 12) + 3
            case "Mage" | "2":
                self.inteligence = random.randint(8, 12) + 3
            case "Archer" | "3":
                self.dexterity = random.randint(8, 12) + 3

    def showstats(self):
        print(f"Name: {self.name}")
        print(f"Class: {self.characterClass}")
        print(f"Level: {self.level}")
        print(f"Health: {self.health}")
        print(f"Strength: {self.strength}")
        print(f"Dexterity: {self.dexterity}")
        print(f"Intelligence: {self.inteligence}")
        print(f"Constitution: {self.constitution}")

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
        # tutaj trzeba bedzie dodac obliczenie ataku typu jak masz luk ktory ma base ap 10 to przemnozyc to z dexerity a jak miecz to z strength
        enemy.takeDamage(self.strength)

    def isAlive(self):
        if self.health <= 0:
            return False

        elif self.health > 0:
            return True
