from pygame import sprite
import pygame


class Plateform(sprite.Sprite):
    __all_plateforms = []  # Liste statique de toutes les plateformes

    @staticmethod
    def get_all():
        return Plateform.__all_plateforms

    @staticmethod
    def update_all():
        for plateform in Plateform.__all_plateforms:
            plateform.update()

    @staticmethod
    def draw_all(screen):
        for plateform in Plateform.__all_plateforms:
            plateform.draw(screen)

    @staticmethod
    def add(plateform):
        Plateform.__all_plateforms.append(plateform)

    @staticmethod
    def remove(plateform):
        Plateform.__all_plateforms.remove(plateform)

    @staticmethod
    def clear():
        Plateform.__all_plateforms.clear()

    @staticmethod
    def is_colliding_with(rect):
        for plateform in Plateform.__all_plateforms:
            if plateform.rect.colliderect(rect):
                return True
        return False

    @staticmethod
    def is_sprite_colliding(sprite):
        for plateform in Plateform.__all_plateforms:
            if plateform.rect.colliderect(sprite.rect):
                return True
        return False

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 255, 100))
        # Collision
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        Plateform.add(self)

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    plateform1 = Plateform(0, 450, 25, 25)
    plateform2 = Plateform(25, 450, 25, 25)
    plateform3 = Plateform(100, 450, 25, 25)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill((0, 0, 0))
        Plateform.draw_all(screen)
        pygame.display.flip()
        clock.tick(60)
