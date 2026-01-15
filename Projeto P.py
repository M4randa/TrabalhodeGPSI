import os
import pygame
import time

# --- CONFIGURAÇÃO DE ÁUDIO ---
pygame.mixer.init()
# Certifique-se que o nome do ficheiro está exatamente igual à pasta
nome_musica = "Kanye-West-Graduation-01-10-Everything-I-Am.ogg"
caminho = os.path.join(r"C:\Users\goatm\PyCharmMiscProject", nome_musica)

try:
    if os.path.exists(caminho):
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.play(-1)  
        pygame.mixer.music.set_volume(0.3)  
        print("Som carregado com sucesso! SIUUUUUUU!\n")
    else:
        print(f"Aviso: Ficheiro não encontrado no caminho: {caminho}\n")
except Exception as e:
    print(f"Erro ao carregar som: {e}\n")

# --- LÓGICA DO GERADOR DE SIGLAS ---
print("=== GERADOR DE SIGLAS 2026 ===")

while True:
    frase = input("\nDigite uma frase para gerar a sigla (ou 'sair' para fechar): ")

    if not frase: # Evita erro se carregar no Enter sem escrever nada
        continue

    if frase.lower() == 'sair':
        break

    # Pega a primeira letra de cada palavra e coloca em maiúsculas
    palavras = frase.split()
    # Adicionada verificação para ignorar espaços extras
    sigla = "".join([palavra[0].upper() for palavra in palavras if palavra])

    print(f"A sua sigla é: {sigla}")
    print("SIUUUUUUUUUU!")

pygame.mixer.music.stop()
print("Programa finalizado.")
