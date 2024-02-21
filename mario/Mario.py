import pygame
from pygame import sprite
from Plateform import Plateform
import os


pygame.mixer.init()



# Loading assets
MARIO_IMG = pygame.image.load(os.path.join('assets', 'mario.png'))
BACKGROUND_IMG = pygame.image.load(os.path.join('assets', 'bg.png'))
ENEMY_IMG = pygame.image.load(os.path.join('assets', 'enemy.png'))
JUMP_SOUND = pygame.mixer.Sound(os.path.join('sounds', 'jump.mp3'))
COIN_SOUND = pygame.mixer.Sound(os.path.join('sounds', 'coin.mp3'))
DEATH_SOUND = pygame.mixer.Sound(os.path.join('sounds', 'death.mp3'))

class Mario(sprite.Sprite):  # Classe de Mario (hérite de la classe Sprite)

    def __init__(self, img, pos, rot, scale):
        super().__init__()

        # Variables d'etat
        self.__is_life = True
        self.__is_fall = False
        self.__times_since_last_input = 0

        # Variables de deplacement
        self.__speed = [500, 500] # [vitesse horizontale, vitesse verticale]
        self.__vel = [0, 0] # [vitesse horizontale, vitesse verticale]
        self.__lerping_time = 1 # Temps en secondes pour que Mario s'arrete completement

        # Variables pour les graphismes
        self.__transform = [pos, rot, scale] # [position, rotation, echelle], que des listes de 2 elements (vecteurs 2D)
        self.__image = img
        self.__rect = self.__image.get_rect()

        # Variable pour les key events
        self.__keys = {
            # <nom de la touche>: [<fonction>, [<key event>, <key event>, ...]]
            "left": [self.go_left, [pygame.K_LEFT, pygame.K_q]],
            "right": [self.go_right, [pygame.K_RIGHT, pygame.K_d]],
            "jump": [self.jump, [pygame.K_SPACE, pygame.K_z, pygame.K_UP]],
        }

    ########## Getters ##########
    @property
    def is_life(self):
        return self.__is_life

    @property
    def is_fall(self):
        return self.__is_fall

    @property
    def x_speed(self):
        return self.__speed[0]

    @property
    def y_speed(self):
        return self.__speed[1]

    @property
    def speed(self):
        return self.__speed

    @property
    def x_vel(self):
        return self.__vel[0]

    @property
    def y_vel(self):
        return self.__vel[1]

    @property
    def vel(self):
        return self.__vel

    @property
    def lerping_time(self):
        return self.__lerping_time

    @property
    def x_pos(self):
        return self.__transform[0][0]

    @property
    def y_pos(self):
        return self.__transform[0][1]

    @property
    def pos(self):
        return self.__transform[0]

    @property
    def rot(self):
        return self.__transform[1]

    @property
    def scale(self):
        return self.__transform[2]

    @property
    def transform(self):
        return self.__transform

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    ########## Setters ##########
    @speed.setter
    def speed(self, speed):
        self.__speed = speed

    @x_speed.setter
    def x_speed(self, x_speed):
        self.__speed[0] = x_speed

    @y_speed.setter
    def y_speed(self, y_speed):
        self.__speed[1] = y_speed

    @vel.setter
    def vel(self, vel):
        self.__vel = vel

    @x_vel.setter
    def x_vel(self, x_vel):
        self.__vel[0] = x_vel

    @y_vel.setter
    def y_vel(self, y_vel):
        self.__vel[1] = y_vel

    @pos.setter
    def pos(self, pos):
        self.__transform[0] = pos

    @x_pos.setter
    def x_pos(self, x_pos):
        self.__transform[0][0] = x_pos

    @y_pos.setter
    def y_pos(self, y_pos):
        self.__transform[0][1] = y_pos

    @rot.setter
    def rot(self, rot):
        self.__transform[1] = rot

    @scale.setter
    def scale(self, scale):
        self.__transform[2] = scale

    @transform.setter
    def transform(self, transform):
        self.__transform = transform

    @image.setter
    def image(self, image):
        self.__image = image

    @rect.setter
    def rect(self, rect):
        self.__rect = rect

    ########## Methodes ##########
    # Methode pour faire sauter Mario
    def jump(self):
        if not self.__is_fall:
            self.y_vel = -self.y_speed
            self.__is_fall = True
            JUMP_SOUND.play()

    # Methode pour faire aller Mario a gauche
    def go_left(self):
        self.x_vel = -self.x_speed

    # Methode pour faire aller Mario a droite
    def go_right(self):
        self.x_vel = self.x_speed

    # Methode pour faire arreter Mario
    def stand(self):
        self.x_vel = 0

    # Méthode pour faire arrêter Mario avec un lerp sur x secondes
    def stand_lerp(self, dt, x):
        self.__times_since_last_input += dt
        t = min(self.__times_since_last_input / x, 1.0)  # Limiter le facteur de progression à 1.0
        self.x_vel = self.lerp(self.x_vel, 0, t)

    def lerp(self, start, end, t):
        return start + (end - start) * t

    def update(self, dt):
      if not self.__is_life:
        self.__is_fall = True
        self.rect.y += 20
        return

    # Check if Mario is on top of an enemy
      for enemy in enemy_generator.enemies:
        if pygame.sprite.collide_rect(self, enemy):
            if self.y_vel > 0 and self.rect.bottom <= enemy.rect.top:
                # Mario is on top of the enemy, kill the enemy
                enemy.is_life = False
                self.y_vel = -self.y_speed  # Add a bounce effect
            else:
                # Mario is not on top, which means it's a side or bottom collision, so lose a life
                self.__is_life = False
                DEATH_SOUND.play()



        
        # On écoute les evenements de clavier
        frame_keys = pygame.key.get_pressed()
        is_key_pressed = False

        # Debug : si au moins une touche est pressee, on affiche la touche
        print([key for key in self.__keys if frame_keys[self.__keys[key][1][0]] or frame_keys[self.__keys[key][1][1]]])

        # On execute les fonctions associees aux touches pressees. Si aucune touche n'est pressee, on fait arreter Mario
        for key in self.__keys:
            if frame_keys[self.__keys[key][1][0]] or frame_keys[self.__keys[key][1][1]]:
                self.__keys[key][0]()
                is_key_pressed = True
                self.__times_since_last_input = 0

        if not is_key_pressed:
            self.stand_lerp(dt, self.lerping_time)

        # On met a jour la position de Mario
        self.x_pos += self.x_vel * dt
        self.y_pos += self.y_vel * dt

        # On met a jour le rectangle de collision
        self.update_collision()

    def update_collision(self):
        # On ajuste la position du rectangle de collision
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        # On ajuste la taille du rectangle de collision
        self.rect.width = self.image.get_width() * self.scale
        self.rect.height = self.image.get_height() * self.scale

    def draw(self, screen):
        # On dessine Mario a la position transformee, Mario regarde la direction dans laquelle il va
        screen.blit(pygame.transform.flip(pygame.transform.rotozoom(self.__image, self.rot, self.scale), self.x_vel < 0, False), self.pos)
        # On dessine le rectangle de collision
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)


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
                self.rect.y += self.fall_speed  # Fall down
            else:
                self.__is_fall = False
                self.rect.y -= self.fall_speed  # Move up

        # Check if the enemy is below the screen, set is_life to False
        if self.rect.y > 600:
            self.is_life = False

        # Check if the enemy has touched Mario, stop moving
        if pygame.sprite.collide_rect(self, mario):
            if mario.y_vel >= 0 and mario.rect.bottom <= self.rect.centery:
                mario.__is_life = True
            elif mario.is_fall:
                self.is_life = False
                mario.__is_life= True
            else:
        # Mario touched an enemy, lose a life
                mario.is_life = False   
                DEATH_SOUND.play()

    def update_position(self):
        self.rect.x -= self.speed

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
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption('Super Mario Bros - Test Mario and Enemy')

    running = True
    delta_time = 0

    mario = Mario(pygame.image.load("assets/mario.png"), [0, 400], 0, 0.3)
    enemy_generator = EnemyGenerator(screen_width=1200, enemy_y=400, enemy_speed=3, spawn_delay=3000, scale=0.1)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(mario)

    # Add platforms
    Plateform(0, 550, 850, 50)
    Plateform(900, 450, 500, 25)

    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        delta_time = clock.get_time() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((135, 206, 250))

        # Update and draw Mario
        mario.update(delta_time)
        mario.draw(screen)
                     
        # Update and draw enemies
        enemy_generator.update()
        enemy_generator.draw(screen)

        # Draw platforms
        Plateform.draw_all(screen)

        pygame.display.flip()

    pygame.quit()

