import pygame
from projectile import Projectile
import animation

class Player(animation.AnimateSprite ):
    def __init__(self, game):
        super().__init__('player')
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 20
        self.velocity = 5
        self.allprojectiles = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500

    def move_right(self):
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def move_up(self):
        self.rect.y -= self.velocity

    def move_down(self):
        self.rect.y += self.velocity

    def fire(self):
        self.allprojectiles.add(Projectile(self))
        self.start_animation()
        self.game.sound_Manager.play('tir')



    def damage(self, amount):
        if self.health - amount >= amount:
            self.health -= amount
        else:
            self.game.game_over()
    
    def update_animation(self):
        self.animate()

    def update_health_bar(self, surface):
        pygame.draw.rect(surface, (60, 63, 60), [
                         self.rect.x + 50, self.rect.y+5, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46),  [
                         self.rect.x + 50, self.rect.y+5, self.health, 5])
