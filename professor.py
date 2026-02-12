import pygame
from config import *


class Professor(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        try:
            f_idle = pygame.image.load("JOGO/gangster-pixel-character-sprite-sheets-pack/Gangsters_3/Idle_2.png")
            f_run = pygame.image.load("JOGO/gangster-pixel-character-sprite-sheets-pack/Gangsters_3/Run.png")
            f_jump = pygame.image.load("JOGO/gangster-pixel-character-sprite-sheets-pack/Gangsters_3/Jump.png")
            self.frames_idle = self._corta(f_idle, 14)
            self.frames_run = self._corta(f_run, 10)
            self.frames_jump = self._corta(f_jump, 10)
        except:
            surf = pygame.Surface((150, 150))
            surf.fill((100, 100, 200))
            pygame.draw.circle(surf, (255, 255, 255), (75, 50), 30)
            pygame.draw.rect(surf, (255, 255, 255), (50, 80, 50, 60))
            self.frames_idle = [surf]
            self.frames_run = [surf]
            self.frames_jump = [surf]

        self.frames_atuais = self.frames_idle
        self.index = 0
        self.image = self.frames_atuais[self.index]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.timer = 0
        self.direcao = "R"
        self.vel_y = 0
        self.no_chao = False
        self.pulando = False

    def _corta(self, folha, col):
        lista = []
        w = folha.get_width() // col
        h = folha.get_height()
        for i in range(col):
            sub = folha.subsurface((i * w, 0, w, h))
            lista.append(pygame.transform.scale(sub, (150, 150)))
        return lista

    def update(self):
        keys = pygame.key.get_pressed()
        movendo = False
        antiga_anim = self.frames_atuais
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= 5;
            self.direcao = "L";
            movendo = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += 5;
            self.direcao = "R";
            movendo = True
        if self.pulando:
            self.frames_atuais = self.frames_jump
        elif movendo:
            self.frames_atuais = self.frames_run
        else:
            self.frames_atuais = self.frames_idle
        if self.frames_atuais != antiga_anim: self.index = 0
        self.timer += 1
        if self.timer >= 6:
            self.index = (self.index + 1) % len(self.frames_atuais)
            self.timer = 0
        self.image = self.frames_atuais[self.index]
        if self.direcao == "L": self.image = pygame.transform.flip(self.image, True, False)
        self.vel_y += 0.8
        self.rect.y += self.vel_y
        if self.rect.bottom >= 540:
            self.rect.bottom = 540;
            self.vel_y = 0;
            self.no_chao = True;
            self.pulando = False
        if (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.no_chao:
            self.vel_y = -8;
            self.pulando = True
