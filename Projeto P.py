import pygame
from Player_sprite import Samurai, Mago
from gerador import gerar_siglas

# Inicialização obrigatória do Pygame para ativar som, vídeo e eventos
pygame.init()
largura, altura = 800, 500
tela = pygame.display.set_mode([largura, altura])  # Cria a janela (Surface principal)
pygame.display.set_caption("GRS - Samurai vs Mago")

# Carregamento de Backgrounds (Cenários estáticos)
# .convert() otimiza a imagem para o mesmo formato de pixels da tela, melhorando a performance
bg = pygame.image.load(r"C:\Users\goatm\PyCharmMiscProject\JOGO\test_2.png").convert()
bg = pygame.transform.scale(bg, (largura, altura))
bg_gameover = pygame.image.load(r"C:\Users\goatm\PyCharmMiscProject\JOGO\Game Over super Mario screen.jpg"  ).convert()
bg_gameover = pygame.transform.scale(bg_gameover, (largura, altura))
bg_win = pygame.image.load(r"C:\Users\goatm\PyCharmMiscProject\JOGO\you win.png").convert()
bg_win = pygame.transform.scale(bg_win, (largura, altura))

# Configuração de Texto e Tempo
# pygame.font.SysFont: Carrega fontes do sistema. bold=True ativa o negrito.
fonte = pygame.font.SysFont("Courier New", 22, bold=True)
relogio = pygame.time.Clock()  # Objeto para sincronizar o tempo e limitar o FPS

# --- SISTEMA DE AUDIO (PLAYLIST) ---
pygame.mixer.init()
playlist = [
    r"C:\Users\goatm\PyCharmMiscProject\Musicas\School-Spirit.ogg",
    r"C:\Users\goatm\PyCharmMiscProject\Musicas\Spider-Dance.ogg",
    r"C:\Users\goatm\PyCharmMiscProject\Musicas\Kanye-West-Bittersweet-Poetry-_feat.-John-Mayer_-_Bonus-Track_-_HIGHEST-QUALITY-ON-YOUTUBE_.ogg",
    r"C:\Users\goatm\PyCharmMiscProject\Musicas\Death-By-Glamour.ogg",
]
idx_musica = 0  # Índice que aponta para a música atual na lista


def tocar_musica(n):
    """Lógica para carregar e iniciar uma música da lista"""
    pygame.mixer.music.load(playlist[n])
    pygame.mixer.music.set_volume(0.4)  # Define o volume entre 0.0 e 1.0
    pygame.mixer.music.play(-1)  # -1 força a música a repetir em loop infinito


tocar_musica(idx_musica)  # Inicia a primeira trilha sonora

# --- ORGANIZAÇÃO DOS SPRITES ---
# pygame.sprite.Group(): Contentor que permite gerir múltiplos sprites como uma unidade
todos_sprites = pygame.sprite.Group()
player = Samurai(todos_sprites)
mago_npc = Mago(todos_sprites)

# Variáveis Globais de Controle de Jogo
estado = "MENU_INICIAL"  # Máquina de estados: controla em que tela o jogo está
opcao_sim = True  # Alternador para o menu de desistência (SIM/NÃO)
fases_gerar = 3  # Contador de quantas frases o jogador precisa escrever
perguntas_respondidas = 0  # Contador de progresso no desafio final
erros = 0  # Contador de erros; se chegar a 2, resulta em Game Over
input_usuario = ""  # String dinâmica que recebe a entrada do teclado
frase_atual, sigla_esperada = "", ""  # Variáveis temporárias para o desafio atual

# Lista de Tuplas: Estrutura fixa para armazenar o banco de dados de siglas
banco_questoes = [
    ("World Wide Web", "WWW"), ("Personal Computer", "PC"),
    ("HyperText Markup Language", "HTML"), ("Graphics Interchange Format", "GIF"),
    ("Unidentified Flying Object", "UFO"), ("Central Processing Unit", "CPU"),
    ("United Nations", "UN")
]


def desenha_caixa(texto, subtexto=""):
    """Renderiza a Interface de Usuário (HUD) na parte superior do ecrã"""
    # .draw.rect: Desenha retângulos (Superfície, Cor, [X, Y, Largura, Altura])
    pygame.draw.rect(tela, (255, 255, 255), [45, 20, 710, 110])  # Borda externa
    pygame.draw.rect(tela, (0, 0, 0), [50, 25, 700, 100])  # Preenchimento interno

    # .render transforma a string Python numa superfície de imagem desenhável
    img = fonte.render(texto, True, (255, 255, 255))
    tela.blit(img, (70, 40))  # .blit desenha uma superfície sobre a outra nas coordenadas indicadas
    if subtexto:
        img2 = fonte.render(subtexto, True, (255, 255, 0))
        tela.blit(img2, (70, 80))


# --- CICLO PRINCIPAL (GAME LOOP) ---
while True:
    # Gestão de Eventos: Captura entradas do utilizador do buffer do sistema
    eventos = pygame.event.get()
    for ev in eventos:
        if ev.type == pygame.QUIT:  # Evento de clicar no X da janela
            pygame.quit();
            exit()

        if ev.type == pygame.KEYDOWN:  # Evento de tecla pressionada
            # Lógica para alternar músicas
            if ev.key == pygame.K_n:
                # O operador % (módulo) garante que o índice volte a 0 ao passar do limite da lista
                idx_musica = (idx_musica + 1) % len(playlist)
                tocar_musica(idx_musica)

            if estado == "MENU_INICIAL":
                if ev.key == pygame.K_LEFT: opcao_sim = True
                if ev.key == pygame.K_RIGHT: opcao_sim = False
                if ev.key == pygame.K_RETURN:  # Enter confirma a opção
                    estado = "GAMEOVER" if opcao_sim else "ANDANDO"

            elif estado == "GERANDO":
                if ev.key == pygame.K_RETURN:
                    # QUANDO CLICAS ENTER, O PYTHON GERA A SIGLA NO CONSOLE
                    resultado_sigla = gerar_siglas(input_usuario)
                    print(f"  {resultado_sigla}")

                    fases_gerar -= 1
                    input_usuario = ""  # Limpa para a próxima

                    # APÓS 3 VEZES, MUDA PARA O QUIZ
                    if fases_gerar == 0:
                        estado = "DESAFIO"
                        frase_atual, sigla_esperada = banco_questoes[0]

                elif ev.key == pygame.K_BACKSPACE:
                    input_usuario = input_usuario[:-1]
                else:
                    input_usuario += ev.unicode.upper()

            elif estado == "DESAFIO":
                if ev.key == pygame.K_RETURN:
                    if input_usuario == sigla_esperada:
                        perguntas_respondidas += 1
                        if perguntas_respondidas == 7:
                            estado = "WIN"
                        else:
                            frase_atual, sigla_esperada = banco_questoes[perguntas_respondidas]
                    else:
                        erros += 1
                        if erros >= 2: estado = "GAMEOVER"
                    input_usuario = ""
                elif ev.key == pygame.K_BACKSPACE:
                    input_usuario = input_usuario[:-1]
                else:
                    input_usuario += ev.unicode.upper()

            # Lógica de Reinício (Botão R)
            if estado in ["GAMEOVER", "WIN"] and ev.key == pygame.K_r:
                estado = "MENU_INICIAL";
                fases_gerar = 3;
                perguntas_respondidas = 0
                erros = 0;
                input_usuario = ""
                player.vel_y = 0
                player.rect.midbottom = (150, 450)

                # --- ATUALIZAÇÃO DE LÓGICA ---
    if estado == "ANDANDO":
        todos_sprites.update()
        if pygame.sprite.collide_rect(player, mago_npc):
            estado = "GERANDO"

    if estado in ["MENU_INICIAL", "GERANDO", "DESAFIO"]:
        mago_npc.update()

    # --- DESENHO (RENDERIZAÇÃO) ---
    tela.fill((0, 0, 0))

    if estado in ["MENU_INICIAL", "ANDANDO", "GERANDO", "DESAFIO"]:
        tela.blit(bg, (0, 0))
        todos_sprites.draw(tela)

        if estado == "MENU_INICIAL":
            desenha_caixa("Desistir?", "   [SIM]      [NÃO]")
            seta = ">" if opcao_sim else "             >"
            tela.blit(fonte.render(seta, True, (255, 0, 0)), (70, 80))
        elif estado == "GERANDO":
            desenha_caixa(f"Mago: Eu sei gerar Siglas ({fases_gerar})", f"Texto: {input_usuario}")
        elif estado == "DESAFIO":
            desenha_caixa(f"Sigla de: {frase_atual}", f"Resp: {input_usuario}")

    elif estado == "GAMEOVER":
        tela.blit(bg_gameover, (0, 0))
    elif estado == "WIN":
        tela.blit(bg_win, (0, 0))

    pygame.display.update()
    relogio.tick(60)
