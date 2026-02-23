lista_jogos = [
    (
        "GTA V",
        ("Ação", "Aventura", "Mundo Aberto"),
        ("PC", "PlayStation", "Xbox"),
        "17/09/2013",
        ("Single Player", "Multiplayer", "Online"),
        29.99,
        15
    ),
    (
        "Undertale",
        ("RPG", "Indie"),
        ("PC", "Switch"),
        "15/09/2015",
        ("Single Player",),
        9.99,
        30
    ),
    (
        "Minecraft",
        ("Sandbox", "Aventura", "Criativo"),
        ("PC", "PlayStation", "Xbox", "Switch"),
        "18/11/2011",
        ("Single Player", "Multiplayer", "Co-op"),
        19.99,
        50
    ),
    (
        "Red Dead Redemption 2",
        ("Ação", "Aventura", "Mundo Aberto"),
        ("PC", "PlayStation", "Xbox"),
        "26/10/2018",
        ("Single Player", "Multiplayer", "Online"),
        59.99,
        25
    ),
    (
        "EA FC 26",
        ("Esportes",),
        ("PC", "PlayStation", "Xbox"),
        "26/08/2025",
        ("Single Player", "Multiplayer", "Online"),
        79.99,
        28
    ),
    (
        "The Witcher 3: Wild Hunt",
        ("RPG", "Ação", "Fantasia"),
        ("PC", "PlayStation", "Xbox", "Switch"),
        "19/05/2015",
        ("Single Player",),
        19.99,
        13
    ),
    (
        "The Legend of Zelda: Ocarina of Time",
        ("Aventura", "Ação", "Fantasia"),
        ("Nintendo 64", "3DS"),
        "21/11/1998",
        ("Single Player",),
        39.99,
        8
    ),
    (
        "Dark Souls",
        ("RPG", "Ação", "Fantasia Sombria"),
        ("PC", "PlayStation", "Xbox"),
        "22/09/2011",
        ("Single Player", "Online", "Co-op"),
        29.99,
        12
    ),
    (
        "Half-Life 2",
        ("FPS", "Ação", "Sci-Fi"),
        ("PC", "Xbox", "Playstation"),
        "16/11/2004",
        ("Single Player",),

        9.99,
        20
    )
]


def listar_nomes(lista_jogos):
    print("\n" + "=" * 150)
    print("LISTA DE JOGOS".center(150))
    print("=" * 150)

    if not lista_jogos:
        print("Jogo indisponível")
        return

    while True:
        opcao = input("1.Normal 2.A-Z 3.Z-A 4.Genero 5.Plataforma 6.Data 7.Modos 8.Preco 9.Stock: ").strip()
        if opcao in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            break
        else:
            print("Número inválido. Tente novamente.")

    lista_exibir = lista_jogos.copy()

    if opcao == "1":
        lista_exibir = lista_exibir

    elif opcao == "2":
        lista_exibir = sorted(lista_exibir, key=lambda jogo: jogo[0])

    elif opcao == "3":
        lista_exibir = sorted(lista_exibir, key=lambda jogo: jogo[0], reverse=True)

    elif opcao == "4":
        lista_exibir = sorted(lista_exibir, key=lambda jogo: jogo[1][0])

    elif opcao == "5":
        lista_exibir = sorted(lista_exibir, key=lambda jogo: jogo[2][0])

    elif opcao == "6":
        lista_exibir = sorted(lista_exibir, key=lambda jogo: jogo[3].split("/")[::-1])

    elif opcao == "7":
        lista_exibir = sorted(lista_exibir, key=lambda jogo: ", ".join(jogo[4]))

    elif opcao == "8":
        lista_exibir = sorted(lista_exibir, key=lambda jogo: jogo[5])

    elif opcao == "9":
        lista_exibir = sorted(lista_exibir, key=lambda jogo: jogo[6])

    def cortar(texto, largura):
        texto = str(texto)
        if len(texto) <= largura:
            return texto
        return texto[:largura - 3] + "..."

    print("\n" + "-" * 170)
    print(f"| {'#':^3} | {'NOME':<30} | {'GÉNEROS':<30} | {'PLATAFORMAS':<30} | {'DATA':^12} | {'MODOS':<25} | {'PREÇO':^10} | {'STOCK':^7} |")
    print("-" * 170)

    for i, jogo in enumerate(lista_exibir, 1):
        nome = cortar(jogo[0], 30)
        generos = cortar(", ".join(jogo[1]), 30)
        plataformas = cortar(", ".join(jogo[2]), 30)
        data = jogo[3]
        modos = cortar(", ".join(jogo[4]), 25)
        preco = jogo[5]
        stock = jogo[6]

        print(f"| {i:^3} | {nome:<30} | {generos:<30} | {plataformas:<30} | {data:^12} | {modos:<25} | {preco:^10.2f} | {stock:^7} |")

    print("-" * 170)
    print(f"Total: {len(lista_exibir)}")

