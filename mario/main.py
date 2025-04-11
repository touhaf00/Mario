import sys
import pygame
from camera import Camera
from mario import Mario
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, FPS
from plateform import Platform
from enemy import Enemy
from level_manager import get_level_data

# Initialisation de Pygame et du mixer
pygame.init()
pygame.mixer.init()

# Configuration de la fenêtre et de l'horloge
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Game")
clock = pygame.time.Clock()

# Chargement des sons
try:
    jump_sound = pygame.mixer.Sound("sounds/jump.mp3")
    death_sound = pygame.mixer.Sound("sounds/death.mp3")
    coin_sound = pygame.mixer.Sound("sounds/coin.mp3")
    win_sound = pygame.mixer.Sound("sounds/win.mp3")
except Exception as e:
    print(f"Erreur lors du chargement des sons : {e}")
    jump_sound = death_sound = coin_sound = win_sound = None


# --------------------------------------------------
# Écran de démarrage
# --------------------------------------------------
def start_screen():
    bg = pygame.image.load("assets/bg.png").convert()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.mixer.music.load("sounds/start.mp3")
    pygame.mixer.music.play(-1)

    font = pygame.font.SysFont('Arial', 40)
    titre = font.render("Mario Clone", True, (255, 255, 0))
    prompt = font.render("Appuyez sur ENTREE pour jouer", True, (255, 255, 255))

    waiting = True
    while waiting:
        screen.blit(bg, (0, 0))
        screen.blit(titre, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4))
        screen.blit(prompt, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.mixer.music.stop()
                waiting = False


# --------------------------------------------------
# Classe pour les blocs (deux types : normal et mystery)
# --------------------------------------------------
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type="normal", size=50):
        super().__init__()
        self.block_type = block_type
        if self.block_type == "mystery":
            self.image = pygame.image.load("assets/mystery.png").convert_alpha()
        else:
            self.image = pygame.image.load("assets/block.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.used = False  # Le bloc n'a pas encore été activé


# --------------------------------------------------
# Classe pour le champignon (mushroom)
# --------------------------------------------------
class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/mushroom.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.speed = 2  # Vitesse horizontale du champignon

    def update(self, surfaces):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.rect.x += self.speed
        # Le champignon peut atterrir sur n'importe quelle surface (plateformes et blocs)
        for surface in surfaces:
            if self.rect.colliderect(surface.rect) and self.vel_y >= 0:
                self.rect.bottom = surface.rect.top
                self.vel_y = 0


# --------------------------------------------------
# Classe pour l'objectif (goal)
# --------------------------------------------------
class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y, width=50, height=70):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 215, 0))  # Couleur or pour l'objectif
        self.rect = self.image.get_rect(topleft=(x, y))


# --------------------------------------------------
# Génération du niveau à partir des données
# --------------------------------------------------
def generate_level(level_data):
    platform_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()

    # Réinitialiser la liste des plateformes (statique dans Platform)
    Platform.all_platforms.clear()

    # Création des plateformes
    for x, y, width, height in level_data["platforms"]:
        plat = Platform(x, y, width, height)
        platform_group.add(plat)

    # Décalage pour faire flotter les blocs
    BLOCK_OFFSET = 150
    # Les blocs du niveau sont définis comme dictionnaires :
    # {"pos": (x, y), "type": "normal" ou "mystery"}
    for block_data in level_data.get("blocks", []):
        x, y = block_data["pos"]
        block_type = block_data.get("type", "normal")
        y = y - BLOCK_OFFSET  # Décalage vertical pour que le bloc "flotte"
        block = Block(x, y, block_type)
        block_group.add(block)

    # Création des ennemis (vitesse horizontale par défaut = 2)
    for enemy_info in level_data.get("enemies", []):
        x, y = enemy_info["pos"]
        patrol_range = enemy_info["range"]
        enemy = Enemy(x, y, 2, patrol_range)
        enemy_group.add(enemy)

    # Création de l'objectif
    goal = Goal(*level_data["goal"])

    return platform_group, enemy_group, block_group, goal


# --------------------------------------------------
# Calcul de la taille du monde (pour la caméra)
# --------------------------------------------------
def compute_world_size(level_data):
    max_x = 0
    max_y = SCREEN_HEIGHT  # Au moins la hauteur de l'écran
    for x, y, width, height in level_data["platforms"]:
        max_x = max(max_x, x + width)
        max_y = max(max_y, y + height)
    for block_data in level_data.get("blocks", []):
        x, y = block_data["pos"]
        max_x = max(max_x, x + 50)
        max_y = max(max_y, (y - 150) + 50)
    goal_x, goal_y = level_data["goal"]
    max_x = max(max_x, goal_x + 50)
    max_y = max(max_y, goal_y + 70)
    return max_x + 100, max(max_y, SCREEN_HEIGHT)


# --------------------------------------------------
# Boucle de jeu principale
# --------------------------------------------------
def game_loop(level_index=0):
    level_data = get_level_data(level_index)
    if level_data is None:
        print("Aucune donnée de niveau trouvée !")
        pygame.quit()
        sys.exit()

    # Générer les objets du niveau
    platform_group, enemy_group, block_group, goal = generate_level(level_data)
    powerup_group = pygame.sprite.Group()  # Groupe des power-ups (champignons)

    # Pour que Mario et les autres puissent se poser sur tous les objets (plateformes + blocs)
    union_group = pygame.sprite.Group()
    for sprite in platform_group.sprites():
        union_group.add(sprite)
    for sprite in block_group.sprites():
        union_group.add(sprite)

    mario = Mario(start_pos=level_data["player_start"])
    world_width, world_height = compute_world_size(level_data)
    camera = Camera(world_width, world_height)

    running = True
    level_complete = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mario.jump()
                    if jump_sound:
                        jump_sound.play()

        # Mise à jour des entités en utilisant union_group pour les collisions
        mario.update(union_group)
        enemy_group.update(union_group)
        powerup_group.update(union_group)
        camera.update(mario)

        # Si Mario tombe hors de la zone de jeu, jouer le son de défaite
        if mario.rect.top > SCREEN_HEIGHT + 100:
            print("[DEBUG] Mario est tombé dans le vide !")
            if death_sound:
                death_sound.play()
            mario.health = 0

        # Collision entre Mario et les ennemis
        for enemy in enemy_group.sprites():
            if not enemy.alive() or enemy.dead:
                continue
            if mario.rect.colliderect(enemy.rect):
                if mario.vel_y > 0 and (mario.rect.bottom - enemy.rect.top) < 20:
                    print(f"[DEBUG] Ennemi {enemy.id} écrasé")
                    enemy.kill()
                    enemy_group.remove(enemy)
                    mario.vel_y = -10
                    mario.rect.bottom = enemy.rect.top
                    mario.invulnerable = True
                    mario.invulnerable_timer = 20
                    if coin_sound:
                        coin_sound.play()
                else:
                    if not mario.invulnerable:
                        print(f"[DEBUG] Mario touché par l'ennemi {enemy.id}. Vies avant : {mario.health}")
                        mario.health -= 1
                        print(f"[DEBUG] Nouvelles vies : {mario.health}")
                        mario.invulnerable = True
                        mario.invulnerable_timer = 80
                        if mario.rect.centerx < enemy.rect.centerx:
                            mario.rect.x -= 30
                        else:
                            mario.rect.x += 30
                        mario.rect.y -= 20
                        # Jouer le son de défaite si Mario n'a plus de vies
                        if mario.health <= 0 and death_sound:
                            death_sound.play()

        # Activation des blocs lorsqu'ils sont frappés par le dessous par Mario
        for block in block_group:
            if (not block.used) and mario.vel_y < 0 and mario.rect.colliderect(block.rect):
                if abs(mario.rect.top - block.rect.bottom) < 10:
                    block.used = True
                    if block.block_type == "mystery":
                        # Pour un bloc mystery, changer l'image et générer un champignon
                        block.image.fill((128, 128, 128))
                        mushroom = Mushroom(block.rect.x, block.rect.y - 40)
                        powerup_group.add(mushroom)
                        if coin_sound:
                            coin_sound.play()
                    # Pour un bloc normal, vous pouvez ajouter d'autres effets

        # Collecte d'un champignon par Mario
        for powerup in powerup_group.copy():
            if mario.rect.colliderect(powerup.rect):
                powerup_group.remove(powerup)
                mario.health += 1  # Augmente la vie, par exemple
                # Activation du bonus : Mario grandit et saute plus haut pendant quelques instants
                mario.powered_up = True
                mario.power_up_timer = 300  # Environ 5 secondes (300 frames)
                print("[DEBUG] Mario a collecté un champignon et passe en mode power-up !")
                if coin_sound:
                    coin_sound.play()

        # Vérification de l'arrivée à l'objectif
        if mario.rect.colliderect(goal.rect):
            print("[DEBUG] Niveau complété !")
            if win_sound:
                win_sound.play()
            pygame.time.delay(2000)
            level_complete = True
            running = False

        if mario.health <= 0:
            running = False

        # Rendu
        screen.fill((135, 206, 250))  # Fond bleu ciel
        for plat in platform_group:
            screen.blit(plat.image, camera.apply(plat))
        for enemy in enemy_group:
            screen.blit(enemy.image, camera.apply(enemy))
        for block in block_group:
            screen.blit(block.image, camera.apply(block))
        for powerup in powerup_group:
            screen.blit(powerup.image, camera.apply(powerup))
        screen.blit(goal.image, camera.apply(goal))
        screen.blit(mario.image, camera.apply(mario))

        # Affichage du nombre de vies
        font = pygame.font.SysFont('Arial', 20)
        health_text = font.render(f"Vies : {mario.health}", True, (255, 0, 0))
        screen.blit(health_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    if level_complete:
        game_complete_screen()
    else:
        game_over_screen(level_index)


# --------------------------------------------------
# Écran de Game Over
# --------------------------------------------------
def game_over_screen(current_level):
    font = pygame.font.SysFont('Arial', 40)
    go_text = font.render("GAME OVER", True, (255, 0, 0))
    retry_text = font.render("Appuyez sur 'P' pour recommencer ou 'Q' pour quitter", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(go_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
    screen.blit(retry_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_loop(current_level)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


# --------------------------------------------------
# Écran de Fin de Niveau
# --------------------------------------------------
def game_complete_screen():
    font = pygame.font.SysFont('Arial', 40)
    complete_text = font.render("NIVEAU COMPLETÉ !", True, (0, 255, 0))
    next_text = font.render("Appuyez sur 'N' pour le niveau suivant ou 'Q' pour quitter", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(complete_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
    screen.blit(next_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    new_level = 1
                    from level_manager import levels
                    if new_level >= len(levels):
                        new_level = 0
                    game_loop(new_level)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


# --------------------------------------------------
# Lancement du jeu
# --------------------------------------------------
if __name__ == '__main__':
    start_screen()
    game_loop(0)
