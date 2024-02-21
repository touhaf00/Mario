import pygame
import random
import Mario
import Plateform

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, scale):
        super().__init__()
        original_image = pygame.image.load("assets/enemy.png").convert_alpha()
        scaled_width = int(original_image.get_width() * scale)
        scaled_height = int(original_image.get_height() * scale)
        self.image = pygame.transform.scale(original_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()
        self.__is_life = True
        self.__is_fall = False
        self.rect.x = x
        self.rect.y = y - self.rect.bottom
        self.speed = speed
        self.fall_speed = 2
    @property
    def is_life(self):
        return self.__is_life

    @property
    def is_fall(self):
        return self.__is_fall

    @is_life.setter
    def is_life(self, value):
        self.__is_life = value

    def update(self):
        if not self.__is_life:
            self.__is_fall = True
            self.rect.y += self.fall_speed  # Fall down
        else:
            # Check if the enemy is falling
            if not Plateform.is_colliding_with(self.rect):
                self.__is_fall = True
                self.rect.y += 20  # Fall down
            else:
                self.__is_fall = False
                self.rect.y -= 20  # Move up

    def update_position(self):
        self.rect.x -= self.speed

        if pygame.sprite.collide_rect(self, mario):
            # Enemy has touched Mario, stop moving
            self.speed = 0


class EnemyGenerator:
    def __init__(self, screen_width, enemy_y, enemy_speed, spawn_delay, scale):
        self.screen_width = screen_width
        self.enemy_y = enemy_y  # Fixed Y position for all enemies
        self.enemy_speed = enemy_speed
        self.spawn_delay = spawn_delay
        self.scale = scale
        self.enemies = pygame.sprite.Group()
        self.last_spawn_time = 0

    def update(self):
        self.enemies.update()
        self.spawn_enemy()

        # Draw enemies
        for enemy in self.enemies:
            enemy.update()
            enemy.update_position()

            # Check if the enemy is below the screen, set is_life to False
            if enemy.rect.y > 600:
                enemy.is_life = False

    def draw(self, screen):
        self.enemies.draw(screen)

    def draw(self, screen):
        self.enemies.draw(screen)

    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_delay:
            enemy = Enemy(self.screen_width, self.enemy_y, self.enemy_speed, self.scale)
            self.enemies.add(enemy)
            self.last_spawn_time = current_time

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Adjust the parameters as needed
    enemy_generator = EnemyGenerator(screen_width=800, enemy_y=400, enemy_speed=5, spawn_delay=2000, scale=0.2)

    all_sprites = pygame.sprite.Group()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((135, 206, 250))

        enemy_generator.update()
        enemy_generator.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
