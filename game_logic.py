import pygame
import random
from data_handler import save_logs

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SPACE INVADERS")

background = pygame.image.load("assets/images/background.webp").convert()
background = pygame.transform.scale(background, (800, 600))
player_image = pygame.image.load("assets/images/spaceInvader.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 50))
asteroid_image = pygame.image.load("assets/images/asteroid.png").convert_alpha()
asteroid_image = pygame.transform.scale(asteroid_image, (50, 50))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        self.speed = 5
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.level = 1
        self.shots = 1

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_delay:
            self.last_shot = now
            bullets = []
            for i in range(self.shots):
                bullet = Bullet(self.rect.centerx - 15 + (i * 30), self.rect.top)
                bullets.append(bullet)
            return bullets
        return []

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroid_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.level = 1
        self.speed = random.randint(3, 5) + (0.5 * self.level)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)

    def reset_position(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)

def start_game(screen, clock):
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    bullets = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    for i in range(5):
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

    score = 0
    game_over = False

    while not game_over:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_logs(score, {"level": player.level})
                return score
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                save_logs(score, {"level": player.level})
                return score

        all_sprites.update()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            new_bullets = player.shoot()
            for bullet in new_bullets:
                all_sprites.add(bullet)
                bullets.add(bullet)

        if pygame.sprite.spritecollide(player, obstacles, False):
            game_over = True
            save_logs(score, {"level": player.level})
            return score

        for bullet in bullets:
            collided_obstacles = pygame.sprite.spritecollide(bullet, obstacles, True)
            if collided_obstacles:
                score += 10
                bullet.kill()
                
                obstacle = Obstacle()
                obstacle.level = player.level
                all_sprites.add(obstacle)
                obstacles.add(obstacle)

        level_threshold = player.level * 100
        if score >= level_threshold:
            player.level += 1
            player.shots = min(player.shots + 1, 3)
            player.shoot_delay = max(250 - (player.level * 20), 150)
            
            for obstacle in obstacles:
                obstacle.level = player.level
                obstacle.speed = random.randint(3, 5) + (0.5 * obstacle.level)

        all_sprites.draw(screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {player.level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))

        pygame.display.flip()
        clock.tick(FPS)

    save_logs(score, {"level": player.level})
    return score
