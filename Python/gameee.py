import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 1
JUMP_STRENGTH = 15
PLAYER_SPEED = 5
ENEMY_SPEED = 2
PROJECTILE_SPEED = 7
PLAYER_PROJECTILE_SPEED = 10

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Clone with WASD Controls")
clock = pygame.time.Clock()

# Player Projectile class
class PlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 5))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PLAYER_PROJECTILE_SPEED
        
    def update(self):
        self.rect.x += self.speed
        # Remove if off screen
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT - 100)
        self.velocity_y = 0
        self.on_ground = False
        self.health = 100
        self.shoot_cooldown = 0
        
    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        # Handle shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Check if player is on the ground
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
        # Prevent player from going off the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            
    def jump(self):
        if self.on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.on_ground = False
            
    def move_left(self):
        self.rect.x -= PLAYER_SPEED
        
    def move_right(self):
        self.rect.x += PLAYER_SPEED
        
    def move_up(self):
        # This could be used for climbing ladders in a more advanced version
        pass
        
    def move_down(self):
        # This could be used for crouching or climbing down in a more advanced version
        pass
        
    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20  # Cooldown period in frames
            return PlayerProjectile(self.rect.right, self.rect.centery)
        return None

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - 90
        self.speed = ENEMY_SPEED
        self.shoot_timer = 0
        self.shoot_delay = 60  # frames between shots
        
    def update(self):
        self.rect.x -= self.speed
        
        # Shoot projectiles
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            return True  # Indicate that enemy should shoot
        return False
        
    def shoot(self):
        return Projectile(self.rect.left, self.rect.centery)

# Projectile class (enemy projectiles)
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PROJECTILE_SPEED
        
    def update(self):
        self.rect.x -= self.speed
        # Remove if off screen
        if self.rect.right < 0:
            self.kill()

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create sprites
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_projectiles = pygame.sprite.Group()
player_projectiles = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create ground
ground = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
all_sprites.add(ground)
platforms.add(ground)

# Create some platforms
platform_list = [
    (100, 400, 100, 20),
    (300, 300, 100, 20),
    (500, 200, 100, 20),
    (200, 150, 100, 20)
]

for plat in platform_list:
    p = Platform(*plat)
    all_sprites.add(p)
    platforms.add(p)

# Enemy spawn timer
enemy_spawn_timer = 0
enemy_spawn_delay = 180  # frames between enemy spawns

# Game loop
running = True
while running:
    # Keep loop running at the right speed
    clock.tick(60)
    
    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.jump()
            if event.key == pygame.K_RETURN:
                projectile = player.shoot()
                if projectile:
                    player_projectiles.add(projectile)
                    all_sprites.add(projectile)
    
    # Get pressed keys for continuous movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move_left()
    if keys[pygame.K_d]:
        player.move_right()
    if keys[pygame.K_w]:
        pass  # Jump is handled in KEYDOWN
    if keys[pygame.K_s]:
        pass  # Could be used for crouching
    
    # Spawn enemies
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= enemy_spawn_delay:
        enemy_spawn_timer = 0
        enemy = Enemy()
        enemies.add(enemy)
        all_sprites.add(enemy)
    
    # Update
    all_sprites.update()
    
    # Enemy shooting
    for enemy in enemies:
        if enemy.update():  # Returns True when it's time to shoot
            projectile = enemy.shoot()
            enemy_projectiles.add(projectile)
            all_sprites.add(projectile)
    
    # Check for collisions with platforms
    if player.velocity_y > 0:  # Only check when falling
        hits = pygame.sprite.spritecollide(player, platforms, False)
        if hits:
            player.rect.bottom = hits[0].rect.top
            player.velocity_y = 0
            player.on_ground = True
    
    # Check for player hit by enemy projectiles
    hits = pygame.sprite.spritecollide(player, enemy_projectiles, True)
    for hit in hits:
        player.health -= 10
        if player.health <= 0:
            running = False
    
    # Check for enemy hit by player projectiles
    hits = pygame.sprite.groupcollide(enemies, player_projectiles, True, True)
    for enemy in hits:
        pass  # You could add score here
    
    # Remove enemies that go off screen
    for enemy in enemies:
        if enemy.rect.right < 0:
            enemy.kill()
    
    # Draw / render
    screen.fill(BLUE)
    all_sprites.draw(screen)
    
    # Draw health bar
    pygame.draw.rect(screen, RED, (10, 10, player.health, 20))
    pygame.draw.rect(screen, WHITE, (10, 10, 100, 20), 2)
    
    # Flip the display
    pygame.display.flip()

pygame.quit()
sys.exit()