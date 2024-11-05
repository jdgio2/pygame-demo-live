import pygame
import random
import math

# setup stuff
pygame.init()
pygame.display.set_caption("Pygame Demo") 
screen = pygame.display.set_mode((1078, 728)) # screen size
clock = pygame.time.Clock() # ticks
running = True # when False, quits game
dt = 0 # delta time, for making movement consistent even if frame rate is bad
difficulty = 1

class Player:
    def __init__(self, pos=pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)):
        self.pos = pos
        self.body = pygame.Rect(*pos, 20, 20)
    def render(self, surf):
        self.body.topleft = (self.pos.x, self.pos.y) # repeatedly update the position of the player
        pygame.draw.rect(surf, "green", self.body) # draw to screen

class Enemy:
    def __init__ (self):
        self.size = random.randint(20, 50)
        self.pos = pygame.Vector2(random.randint(0, screen.get_width() - 10 + self.size), -self.size)
        self.speed = random.randint(200, 350) + (difficulty * 10)
    def fall(self):
        self.pos.y += self.speed * dt
    def render(self, surf):
        pygame.draw.rect(surf, "red", (*self.pos, self.size, self.size))

level_counter = pygame.font.SysFont('Arial', 48)
player = Player()
enemies = []

while running:
    # makes the X button actually work
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    difficulty += 0.004 # we increase the difficulty with each frame

    # shows the difficulty that we're on
    level_surface = level_counter.render(f'Level {math.floor(difficulty)}', True, "black")
    screen.blit(level_surface, (0,0))
    
    # enemy spawn rate increases with difficulty
    if len(enemies) < 50 and random.randint(1, int(30//difficulty)) == 1: # 1/30 initial chance of spawning an enemy
        enemies.append(Enemy())
    for enemy in enemies.copy(): # copy array to avoid weird stuff happening when same enemy is accessed
        enemy.fall()
        enemy.render(screen)

        # detect collisions with player, if collision then you lose
        enemy_rect = pygame.Rect(enemy.pos.x, enemy.pos.y, enemy.size, enemy.size)
        if player.body.colliderect(enemy_rect):
            print("Game Over")
            running = False

        # destroy enemy when goes off screen
        if enemy.pos.y > screen.get_height():
            enemies.remove(enemy)

    # player movement, speed increases slightly with difficulty
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.pos.y -= (300 + (difficulty * 10)) * dt
    if keys[pygame.K_s]:
        player.pos.y += (300 + (difficulty * 10)) * dt
    if keys[pygame.K_a]:
        player.pos.x -= (300 + (difficulty * 10)) * dt
    if keys[pygame.K_d]:
        player.pos.x += (300 + (difficulty * 10)) * dt

    player.render(screen)

    pygame.display.flip() # actually renders the stuff that gets drawn to the screen

    dt = clock.tick(60) / 1000 # since clock.tick returns time in ms since last frame, we divide by 1000 to get deltatime

pygame.quit()