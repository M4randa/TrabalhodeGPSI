def gerar_siglas(frase):
    # DICIONÁRIO : Lista de exclusão para que a sigla foque
    # apenas em palavras com valor semântico (substantivos/adjetivos).
    preposicoes = [
        "DE", "DO", "DA", "DOS", "DAS", "E", "O", "A",
        "OS", "AS", "EM", "UM", "UMA", "COM", "PARA"
    ]

    # 1. NORMALIZAÇÃO:
    # upper():ignora diferença entre maiúsculominúsculo.
    # strip(): Remove espaços acidentais no início/fim.
    # split(): Transforma a string em lista, usando espaços como delimitadores.
    palavras = frase.upper().strip().split()

    # 2. FILTRAGEM E EXTRAÇÃO (List Comprehension):
    # Para cada palavra 'p', verificamos se ela não é uma preposição.
    # Se for válida, pegamos apenas o caractere de índice [0] (a inicial).
    letras = [p[0] for p in palavras if p not in preposicoes]

    # 3. TRATAMENTO DE EXCEÇÃO (Fallback):
    # Caso a frase contenha APENAS preposições (ex: "O e A"),
    # a lista 'letras' estaria vazia. Este bloco evita que o retorno seja nulo,
    # gerando a sigla com todas as iniciais disponíveis.
    if not letras:
        letras = [p[0] for p in palavras]

    # 4. JUNÇÃO: Aglutina as letras da lista em uma única string.
    return "".join(letras)