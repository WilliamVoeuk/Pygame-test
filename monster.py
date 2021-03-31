from player import Player
import pygame
import random
import animation


class Monster(animation.AnimateSprite):
    def __init__(self, game, name, size, offset=0):
        super().__init__(name, size)
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 1
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = 550 - offset
        self.loot_amount = 10
        self.start_animation()

    def set_speed(self, speed):
        self.default_speed = speed
        self.velocity = random.randint(1, 3)

    def set_loot_amount(self, amount):
        self.loot_amount = amount

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.rect.x = 900
            self.game.add_score(self.loot_amount)
            self.health = self.max_health
            self.velocity = random.randint(1, self.default_speed)

        if self.game.comet_event.is_full_loaded():
            self.game.all_monsters.remove(self)
            self.game.comet_event.attempt_fall()

    def update_animation(self):
        self.animate(loop=True)

    def update_health_bar(self, surface):
        pygame.draw.rect(surface, (60, 63, 60), [
                         self.rect.x + 20, self.rect.y-20, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46),  [
                         self.rect.x + 20, self.rect.y-20, self.health, 5])

    def forward(self):
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        else:
            self.game.player.damage(self.attack)
        if self.rect.x <= 0:
            self.rect.x = 900
            self.health = self.max_health
            self.rect.y = 550
            self.velocity = random.randint(1, 3)


class Mummy(Monster):
    def __init__(self, game):
        super().__init__(game, "mummy", (130, 130))
        self.set_speed(3)
        self.set_loot_amount(10)


class Alien(Monster):
    def __init__(self, game):
        super().__init__(game, "alien", (300, 300), random.randint(200, 540))
        self.health = 250
        self.max_health = 250
        self.set_speed(1)
        self.set_loot_amount(30)
