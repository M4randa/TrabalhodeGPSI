import os
import pygame
import tkinter as tk

from professor import Professor
from interface_tk import InovarInterface

# =============================
# CONFIG (não mexe nos paths)
# =============================
LARGURA, ALTURA = 1200, 650
FPS = 60

FUNDO_PATH = r"C:\Users\goatm\PyCharmMiscProject\JOGO\does-anyone-else-have-more-city-sprite-backgrounds-that-i-v0-lhybm358znge1.webp"
MUSICAS_DIR = r"C:\Users\goatm\PyCharmMiscProject\Musicas"

# =============================
# INIT PYGAME
# =============================
pygame.init()
pygame.mixer.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("🎓 Inovar Professor")
clock = pygame.time.Clock()

# =============================
# FUNDO
# =============================
fundo = pygame.image.load(FUNDO_PATH).convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

# =============================
# SPRITES
# =============================
todos = pygame.sprite.Group()
prof = Professor(300, 540, todos)

# =============================
# PLAYLIST (só mete as músicas na pasta e pronto)
# =============================

playlist = [
    r"C:\Users\goatm\PyCharmMiscProject\Musicas\Roses.ogg",
    r"C:\Users\goatm\PyCharmMiscProject\Musicas\Death-By-Glamour.ogg",
    r"C:\Users\goatm\PyCharmMiscProject\Musicas\School-Spirit.ogg"
]

musica_idx = 0

# Texto na tela com o nome da música (some depois de um tempo)
fonte_hud = pygame.font.Font(None, 30)
hud_musica = ""
hud_timer_ms = 0  # countdown
volume = 0.25  # começa baixo
pygame.mixer.music.set_volume(volume)

def tocar_musica(indice):
    global hud_musica, hud_timer_ms
    if not playlist:
        hud_musica = "Sem músicas na pasta /musicas"
        hud_timer_ms = 2500
        return musica_idx  # mantém o atual

    indice = indice % len(playlist)
    caminho = playlist[indice]

    pygame.mixer.music.load(caminho)
    pygame.mixer.music.play()

    nome = os.path.basename(caminho)
    hud_musica = f"Agora: {nome}"
    hud_timer_ms = 3000
    print(hud_musica)

    return indice

# Começa a tocar a primeira (se existir)
if playlist:
    musica_idx = tocar_musica(musica_idx)

# =============================
# LOOP
# =============================
rodando = True
while rodando:
    dt = clock.tick(FPS)  # tempo do frame em ms

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_h:
                root = tk.Tk()
                InovarInterface(root)
                root.mainloop()

            elif evento.key == pygame.K_n:
                musica_idx = tocar_musica(musica_idx + 1)

            elif evento.key == pygame.K_MINUS:
                volume = max(0.0, volume - 0.05)
                pygame.mixer.music.set_volume(volume)
                hud_musica = f"🔉 Volume: {int(volume * 100)}%"
                hud_timer_ms = 1500

            elif evento.key == pygame.K_i:
                volume = min(1.0, volume + 0.05)
                pygame.mixer.music.set_volume(volume)
                hud_musica = f"🔊 Volume: {int(volume * 100)}%"
                hud_timer_ms = 1500

    # Atualiza jogo (MAPA)
    todos.update()

    # Render
    tela.blit(fundo, (0, 0))
    todos.draw(tela)

    # HUD da música
    if hud_timer_ms > 0 and hud_musica:
        hud_timer_ms -= dt
        txt = fonte_hud.render(hud_musica, True, (255, 255, 255))
        # caixinha atrás (simples e legível)
        pygame.draw.rect(tela, (0, 0, 0), (10, 10, txt.get_width() + 16, txt.get_height() + 10))
        tela.blit(txt, (18, 15))

    pygame.display.flip()

pygame.quit()
