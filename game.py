import pygame
from player import Player
from monster import Alien, Monster, Mummy
from comet_event import CometFallEvent
from sound import Sound_Manager

class Game:

    def __init__(self):
        self.is_playing = False
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.comet_event = CometFallEvent(self)
        self.all_monsters = pygame.sprite.Group()
        self.sound_Manager = Sound_Manager()
        self.font = pygame.font.Font("assets/Font_medium.ttf", 25)
        self.score = 0
        self.pressed = {}

    def start(self):
        self.is_playing = True
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)
        self.spawn_monster(Alien)

    def add_score(self, points=2):
        self.score += points

    def game_over(self):
        self.all_monsters = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.comet_event.reset_percent()
        self.is_playing = False
        self.score = 0
        self.sound_Manager.play('game_over')

    def update(self, screen):
        score_text = self.font.render(f"Score:{self.score}", 1, (255, 0, 0))
        screen.blit(score_text, (20, 20))
        screen.blit(self.player.image, self.player.rect)

        self.player.update_health_bar(screen)

        self.comet_event.update_bar(screen)

        self.player.update_animation()

        for projectile in self.player.allprojectiles:
            projectile.move()

        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()

        for comet in self.comet_event.all_comets:
            comet.fall()

        self.player.allprojectiles.draw(screen)

        self.all_monsters.draw(screen)

        self.comet_event.all_comets.draw(screen)

        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x < 840:
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > -40:
            self.player.move_left()
        elif self.pressed.get(pygame.K_UP) and self.player.rect.y > -34:
            self.player.move_up()
        elif self.pressed.get(pygame.K_DOWN) and self.player.rect.y < 500:
            self.player.move_down()

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self, monster_class_name):
        monster = Mummy(self)
        self.all_monsters.add(monster_class_name.__call__(self))
