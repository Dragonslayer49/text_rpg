from colorama import Fore, Style
import pygame

pygame.init()
class Enemy:
    def __init__(self, species, health, attackPower):
        self.species = species
        self.health = int(health)
        self.attackPower = int(attackPower)

    def takeDamage(self, damage):
        self.health -= max(0, damage)
        pygame.mixer.Sound("enemy_growl.wav").play()

    def showHP(self):
        print(f"{Fore.BLUE} {self.species} has: {self.health} HP left {Style.RESET_ALL}")

    def attack(self, player):
        player.takeDamage(self.attackPower)

    def isAlive(self):
        if self.health <= 0:
            return False

        elif self.health > 0:
            return True
