import sys
import pygame
from camera import Camera
import random
from mario import Mario
from config import *
from plateform import Platform
from enemy import Enemy

pygame.init()
pygame.mixer.init()

# Taille de la fenêtre d'affichage
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mario Game")
clock = pygame.time.Clock()

# Chargement des sons
jump_sound = pygame.mixer.Sound("sounds/jump.mp3")
death_sound = pygame.mixer.Sound("sounds/death.mp3")
coin_sound = pygame.mixer.Sound("sounds/coin.mp3")


def generate_fixed_level():
    """
    Création d'un niveau avec un sol découpé en segments et des plateformes en hauteur.
    Le niveau comporte aussi des ennemis fixes ayant un patrouille limitée sur leur plateforme.
    """
    platform_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    # Réinitialiser la liste statique des plateformes
    Platform.all_platforms.clear()

    # --- Plateformes du sol avec des vides ---
    # Chaque tuple est (x, y, largeur, hauteur)
    floor_segments = [
        (0, 560, 300, 40),    # Segment de sol de 0 à 300
        (500, 560, 400, 40),  # Segment de sol de 500 à 900, gap entre 300 et 500 (200 pixels)
        (1020, 560, 250, 40), # Segment de sol de 1020 à 1270, gap entre 900 et 1020 (120 pixels)
        (1300, 560, 300, 40)  # Segment de sol de 1300 à 1600, gap entre 1270 et 1300 (30 pixels)
    ]
    for seg in floor_segments:
        x, y, width, height = seg
        plat = Platform(x, y, width, height)
        platform_group.add(plat)

    # --- Plateformes en hauteur ---
    elevated_platforms = [
        (350, 450, 200, 20),
        (700, 400, 200, 20),
        (1050, 350, 200, 20),
        (1400, 300, 200, 20),
        (1700, 250, 200, 20)
    ]
    for seg in elevated_platforms:
        x, y, width, height = seg
        plat = Platform(x, y, width, height)
        platform_group.add(plat)

    # --- Création d'ennemis fixes répartis dans le niveau ---
    fixed_enemies = [
        (350, 400, 2, 100),
        (1050, 300, 2, 150),
        (1400, 250, 2, 80)
    ]
    for x, y, speed, patrol_range in fixed_enemies:
        enemy = Enemy(x, y, speed, patrol_range)
        enemy_group.add(enemy)

    return platform_group, enemy_group



def game_loop():
    mario = Mario()
    platform_group, enemy_group = generate_fixed_level()
    # La largeur du monde est augmentée pour correspondre à la carte étendue
    camera = Camera(1800, WINDOW_HEIGHT)

    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mario.jump()
                    # jump_sound.play()

        # Mise à jour des entités
        mario.update(platform_group)
        enemy_group.update(platform_group)
        camera.update(mario)

        # Détection si Mario tombe dans le vide (exemple : plus bas que WINDOW_HEIGHT + 100)
        if mario.rect.top > WINDOW_HEIGHT + 100:
            print("[DEBUG] Mario est tombé dans le vide")
            mario.health = 0  # Mario perd toutes ses vies

        # Calcul de la zone visible en fonction de la caméra
        visible_rect = pygame.Rect(-camera.camera.x, -camera.camera.y, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Détection de collisions pour chaque ennemi fixe
        for enemy in enemy_group.sprites():
            if not enemy.alive() or enemy.dead:
                continue
            if not enemy.rect.colliderect(visible_rect):
                continue
            if mario.rect.colliderect(enemy.rect):
                if mario.vel_y > 0 and (mario.rect.bottom - enemy.rect.top) < 20:
                    print(f"[DEBUG] Stomp sur ennemi {enemy.id}")
                    enemy.kill()
                    enemy_group.remove(enemy)
                    mario.vel_y = -10
                    mario.rect.bottom = enemy.rect.top
                    mario.invulnerable = True
                    mario.invulnerable_timer = 20
                    # coin_sound.play()
                else:
                    if not mario.invulnerable:
                        print(f"[DEBUG] Touché par ennemi {enemy.id} | Vie avant : {mario.health}")
                        mario.health -= 1
                        print(f"[DEBUG] Nouvelle vie : {mario.health}")
                        mario.invulnerable = True
                        mario.invulnerable_timer = 80
                        if mario.rect.centerx < enemy.rect.centerx:
                            mario.rect.x -= 30
                        else:
                            mario.rect.x += 30
                        mario.rect.y -= 20
                        # death_sound.play()

        if mario.health <= 0:
            running = False

        # Affichage
        screen.fill((135, 206, 250))
        for platform in platform_group:
            screen.blit(platform.image, camera.apply(platform))
        for enemy in enemy_group:
            screen.blit(enemy.image, camera.apply(enemy))
        screen.blit(mario.image, camera.apply(mario))

        # Affichage du nombre de vies
        font = pygame.font.SysFont('Arial', 20)
        health_text = font.render(f"Vies : {mario.health}", True, (255, 0, 0))
        screen.blit(health_text, (10, 10))
        pygame.display.flip()
        clock.tick(FPS)

    game_over_screen()


def game_over_screen():
    font = pygame.font.SysFont('Arial', 40)
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    play_again_text = font.render("Appuyez sur 'P' pour rejouer ou 'Q' pour quitter", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(game_over_text, (WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3))
    screen.blit(play_again_text, (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2))
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_loop()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


if __name__ == '__main__':
    game_loop()
