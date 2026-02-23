import json
import os
from datetime import datetime

from Dicionario_de_produtos import lista_jogos
from metodo_pagamento import iniciar_checkout

ARQ_STOCK = "stock_jogos.json"
ARQ_VENDAS = "vendas.json"
ARQ_CLIENTES = "clientes.json"
ARQ_USUARIOS = "usuarios.json"
ARQ_SESSOES = "sessoes.json"

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


# ----------------------------
# Utilitarios de terminal
# ----------------------------
def pausar():
    input("\nPressiona ENTER para continuar")


def agora_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ----------------------------
# JSON (persistencia)
# ----------------------------

def garantir_json(arquivo, default):
    if not os.path.exists(arquivo):
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4, ensure_ascii=False)


def carregar_json(arquivo, default):
    garantir_json(arquivo, default)
    with open(arquivo, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_json(arquivo, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


# ----------------------------
# Stock de jogos
# ----------------------------

def guardar_stock(jogos):
    dados = []
    for j in jogos:
        dados.append({
            "nome": j[0],
            "generos": list(j[1]),
            "plataformas": list(j[2]),
            "data": j[3],
            "modos": list(j[4]),
            "preco": j[5],
            "stock": j[6]
        })
    guardar_json(ARQ_STOCK, dados)


def carregar_stock():
    if not os.path.exists(ARQ_STOCK):
        guardar_stock(lista_jogos)

    dados = carregar_json(ARQ_STOCK, [])
    jogos = []

    for d in dados:
        jogos.append((
            d["nome"],
            tuple(d["generos"]),
            tuple(d["plataformas"]),
            d["data"],
            tuple(d["modos"]),
            float(d["preco"]),
            int(d["stock"])
        ))

    return jogos


# ----------------------------
# Usuarios / Clientes / Vendas
# ----------------------------

def carregar_usuarios():
    return carregar_json(ARQ_USUARIOS, {})


def guardar_usuarios(usuarios):
    guardar_json(ARQ_USUARIOS, usuarios)


def carregar_clientes():
    return carregar_json(ARQ_CLIENTES, [])


def guardar_clientes(clientes):
    guardar_json(ARQ_CLIENTES, clientes)


def carregar_vendas():
    return carregar_json(ARQ_VENDAS, [])


def guardar_vendas(vendas):
    guardar_json(ARQ_VENDAS, vendas)


def registar_login(nome, tipo):
    sessoes = carregar_json(ARQ_SESSOES, [])
    sessoes.append({
        "usuario": nome,
        "tipo": tipo,
        "login_at": agora_str()
    })
    guardar_json(ARQ_SESSOES, sessoes)


def registar_cliente(nome):
    clientes = carregar_clientes()
    if nome not in clientes:
        clientes.append(nome)
        guardar_clientes(clientes)


# ----------------------------
# Autenticacao
# ----------------------------

def registro_usuario(usuarios):
    
    print("\n" + "=" * 50)
    print("REGISTO DE NOVO UTILIZADOR".center(50))
    print("=" * 50)

    nome = input("Qual e o seu nome: ").strip()
    senha = input("Defina a sua senha: ").strip()

    if nome == "" or senha == "":
        print("\nERRO: Nome e senha nao podem ser vazios.")
        pausar()
        return usuarios

    if not nome.replace(" ", "").isalpha():
        print("\nERRO: O nome do usuario so pode conter letras (A-Z).")
        pausar()
        return usuarios

    if nome in usuarios:
        print("\nERRO: Esse usuario ja existe.")
        pausar()
        return usuarios

    usuarios[nome] = senha
    guardar_usuarios(usuarios)

    print("\nUsuario registrado com sucesso.")
    pausar()
    return usuarios


def login(usuarios):
    
    print("\n" + "=" * 50)
    print("LOGIN".center(50))
    print("=" * 50)

    login_user = input("Usuario: ").strip()
    login_senha = input("Senha: ").strip()

    if login_user == ADMIN_USER and login_senha == ADMIN_PASS:
        print("\nLogin admin realizado.")
        registar_login(login_user, "admin")
        pausar()
        return("admin", login_user)

    if login_user in usuarios and usuarios[login_user] == login_senha:
        print("\nLogin realizado. Bem-vindo, {}".format(login_user))
        registar_login(login_user, "cliente")
        registar_cliente(login_user)
        pausar()
        return ("cliente", login_user)

    print("\nERRO: Usuario ou senha incorretos.")
    pausar()
    return (None, None)


# ----------------------------
# Input seguro
# ----------------------------

def pedir_numero(msg, minimo, maximo):
    while True:
        x = input(msg).strip()
        if x.isdigit():
            x = int(x)
            if minimo <= x <= maximo:
                return x
        print("Numero invalido.")


def pedir_texto(msg):
    t = input(msg).strip()
    return t if t != "" else None


# ----------------------------
# Catalogo
# ----------------------------

def mostrar_catalogo(jogos):
    
    print("\n" + "=" * 170)
    print("CATALOGO DE JOGOS".center(170))
    print("=" * 170)

    print("-" * 170)
    print("| {0:^3} | {1:<30} | {2:<30} | {3:<30} | {4:^12} | {5:<25} | {6:^10} | {7:^7} |".format(
        "#", "NOME", "GENEROS", "PLATAFORMAS", "DATA", "MODOS", "PRECO", "STOCK"
    ))
    print("-" * 170)

    for i, j in enumerate(jogos, 1):
        nome = j[0]
        generos = ", ".join(j[1])
        plataformas = ", ".join(j[2])
        data = j[3]
        modos = ", ".join(j[4])
        preco = j[5]
        stock = j[6]

        if len(nome) > 30:
            nome = nome[:27] + "..."
        if len(generos) > 30:
            generos = generos[:27] + "..."
        if len(plataformas) > 30:
            plataformas = plataformas[:27] + "..."
        if len(modos) > 25:
            modos = modos[:22] + "..."

        print("| {0:^3} | {1:<30} | {2:<30} | {3:<30} | {4:^12} | {5:<25} | {6:^10.2f} | {7:^7} |".format(
            i, nome, generos, plataformas, data, modos, preco, stock
        ))

    print("-" * 170)
    pausar()


# ----------------------------
# Carrinho
# ----------------------------

def adicionar_ao_carrinho(carrinho, jogos):
    mostrar_catalogo(jogos)

    escolha = pedir_numero("Escolhe o numero do jogo: ", 1, len(jogos))
    jogo = jogos[escolha - 1]

    if jogo[6] <= 0:
        print("Sem stock.")
        pausar()
        return

    qtd = pedir_numero("Quantidade: ", 1, jogo[6])
    nome = jogo[0]
    preco = jogo[5]

    for item in carrinho:
        if item["nome"] == nome:
            nova_qtd = item["qtd"] + qtd
            if nova_qtd > jogo[6]:
                print("Nao tens stock para essa quantidade.")
                pausar()
                return
            item["qtd"] = nova_qtd
            print("Atualizado no carrinho.")
            pausar()
            return

    carrinho.append({"nome": nome, "preco": preco, "qtd": qtd})
    print("Adicionado ao carrinho.")
    pausar()


def ver_carrinho(carrinho):
    

    if not carrinho:
        print("\nCarrinho vazio.")
        pausar()
        return

    print("\n" + "=" * 70)
    print("CARRINHO".center(70))
    print("=" * 70)

    total = 0
    print("-" * 70)
    print("| {0:^3} | {1:<35} | {2:^5} | {3:^10} |".format("#", "JOGO", "QTD", "SUBTOTAL"))
    print("-" * 70)

    for i, item in enumerate(carrinho, 1):
        sub = item["preco"] * item["qtd"]
        total += sub
        nome = item["nome"]

        if len(nome) > 35:
            nome = nome[:32] + "..."

        print("| {0:^3} | {1:<35} | {2:^5} | {3:^10.2f} |".format(
            i, nome, item["qtd"], sub
        ))

    print("-" * 70)
    print("TOTAL: {0:.2f}EUR".format(total))
    pausar()


def remover_do_carrinho(carrinho):
    if not carrinho:
        print("\nCarrinho vazio.")
        pausar()
        return

    ver_carrinho(carrinho)
    escolha = pedir_numero("Remover qual item? ", 1, len(carrinho))
    removido = carrinho.pop(escolha - 1)
    print("Removido: {}".format(removido["nome"]))
    pausar()


def alterar_quantidade_carrinho(carrinho, jogos):
    if not carrinho:
        print("\nCarrinho vazio.")
        pausar()
        return

    ver_carrinho(carrinho)
    escolha = pedir_numero("Alterar qual item? ", 1, len(carrinho))
    item = carrinho[escolha - 1]

    stock_atual = 0
    for j in jogos:
        if j[0] == item["nome"]:
            stock_atual = j[6]
            break

    if stock_atual <= 0:
        print("Sem stock.")
        pausar()
        return

    nova_qtd = pedir_numero("Nova quantidade: ", 1, stock_atual)
    item["qtd"] = nova_qtd
    print("Quantidade atualizada.")
    pausar()


# ----------------------------
# Compra / Vendas
# ----------------------------

def atualizar_stock_por_compra(jogos, carrinho):
    for item in carrinho:
        for i in range(len(jogos)):
            if jogos[i][0] == item["nome"]:
                j = jogos[i]
                novo_stock = j[6] - item["qtd"]
                jogos[i] = (j[0], j[1], j[2], j[3], j[4], j[5], novo_stock)
                break
    return jogos


def registrar_venda(cliente_nome, carrinho, total, metodo):
    vendas = carregar_vendas()
    vendas.append({
        "cliente": cliente_nome,
        "itens": carrinho,
        "total": total,
        "metodo": metodo,
        "comprado_em": agora_str()
    })
    guardar_vendas(vendas)


def finalizar_compra_com_carrinho(carrinho, jogos, cliente_nome):
    

    if not carrinho:
        print("\nCarrinho vazio.")
        pausar()
        return jogos

    total = 0
    for item in carrinho:
        total += item["preco"] * item["qtd"]

    print("\n" + "=" * 50)
    print("FINALIZAR COMPRA".center(50))
    print("=" * 50)
    print("TOTAL A PAGAR: {0:.2f}EUR".format(total))

    confirma = input("\nConfirmar compra? (s/n): ").strip().lower()
    if confirma != "s":
        print("\nCompra cancelada.")
        pausar()
        return jogos

    print("\nMetodo:")
    print("1 - Dinheiro")
    print("2 - Cartao")
    print("3 - PayPal")
    print("4 - Bitcoin")

    m = input("Escolha: ").strip()

    if m == "1":
        metodo = "dinheiro"
    elif m == "2":
        metodo = "cartao"
    elif m == "3":
        metodo = "paypal"
    elif m == "4":
        metodo = "bitcoin"
    else:
        print("Opcao invalida.")
        pausar()
        return jogos

    jogos = atualizar_stock_por_compra(jogos, carrinho)
    guardar_stock(jogos)
    registrar_venda(cliente_nome, carrinho[:], total, metodo)

    iniciar_checkout()
    carrinho.clear()

    print("\nCompra finalizada com sucesso.")
    pausar()
    return jogos


def ver_minhas_compras(cliente_nome):
    
    vendas = carregar_vendas()
    minhas = [v for v in vendas if v["cliente"] == cliente_nome]

    if not minhas:
        print("\nAinda nao fizeste compras.")
        pausar()
        return

    print("\n" + "=" * 70)
    print("MINHAS COMPRAS".center(70))
    print("=" * 70)

    total_gasto = 0

    for i, v in enumerate(minhas, 1):
        total_gasto += v["total"]
        print("\n{0}. Total: {1:.2f}EUR | Metodo: {2} | Data: {3}".format(
            i, v["total"], v.get("metodo", "-"), v.get("comprado_em", "-")
        ))

        print("   Itens:")
        for item in v["itens"]:
            print("   - {0} x{1} = {2:.2f}EUR".format(
                item["nome"], item["qtd"], item["preco"] * item["qtd"]
            ))

    print("\n" + "=" * 70)
    print("TOTAL GASTO: {0:.2f}EUR".format(total_gasto))
    print("=" * 70)
    pausar()


# ----------------------------
# Pesquisa / Filtros / Ordenacao
# ----------------------------

def pesquisar_por_nome(jogos):
    
    termo = pedir_texto("Pesquisar nome: ")
    if termo is None:
        return jogos
    termo = termo.lower()
    return [j for j in jogos if termo in j[0].lower()]


def filtrar_por_categoria(jogos):
    
    termo = pedir_texto("Filtrar genero: ")
    if termo is None:
        return jogos
    termo = termo.lower()

    filtrado = []
    for j in jogos:
        generos = [g.lower() for g in j[1]]
        if termo in generos:
            filtrado.append(j)
    return filtrado


def filtrar_por_preco(jogos):
    
    minimo = input("Preco minimo: ").strip()
    maximo = input("Preco maximo: ").strip()

    try:
        minimo = float(minimo)
        maximo = float(maximo)
    except:
        print("Preco invalido.")
        pausar()
        return jogos

    return [j for j in jogos if minimo <= j[5] <= maximo]


def ordenar_normal(jogos):
    return jogos


def ordenar_az(jogos):
    return sorted(jogos, key=lambda j: j[0].lower())


def ordenar_za(jogos):
    return sorted(jogos, key=lambda j: j[0].lower(), reverse=True)


def ordenar_por_genero(jogos):
    return sorted(jogos, key=lambda j: j[1][0].lower())


def ordenar_por_plataforma(jogos):
    return sorted(jogos, key=lambda j: j[2][0].lower())


def ordenar_por_data(jogos):
    return sorted(jogos, key=lambda j: j[3].split("/")[::-1])


def ordenar_por_modos(jogos):
    return sorted(jogos, key=lambda j: ", ".join(j[4]).lower())


def ordenar_por_preco(jogos):
    return sorted(jogos, key=lambda j: j[5])


def ordenar_por_stock(jogos):
    return sorted(jogos, key=lambda j: j[6])


# ----------------------------
# Admin
# ----------------------------

def relatorio_vendas():
    
    vendas = carregar_vendas()

    if not vendas:
        print("\nSem vendas.")
        pausar()
        return

    print("\n" + "=" * 70)
    print("RELATORIO DE VENDAS".center(70))
    print("=" * 70)

    soma = 0
    for i, v in enumerate(vendas, 1):
        soma += v["total"]
        print("{0}. Cliente: {1} | Total: {2:.2f}EUR | Metodo: {3} | Em: {4}".format(
            i, v["cliente"], v["total"], v.get("metodo", "-"), v.get("comprado_em", "-")
        ))

    print("\n" + "=" * 70)
    print("TOTAL FATURADO: {0:.2f}EUR".format(soma))
    print("=" * 70)
    pausar()


def produto_mais_vendido():
    
    vendas = carregar_vendas()
    contagem = {}

    for v in vendas:
        for item in v["itens"]:
            nome = item["nome"]
            qtd = item["qtd"]
            contagem[nome] = contagem.get(nome, 0) + qtd

    if not contagem:
        print("\nSem vendas.")
        pausar()
        return

    mais = max(contagem, key=contagem.get)
    print("\nProduto mais vendido: {} ({} unidades)".format(mais, contagem[mais]))
    pausar()


def top_3_jogos():
    
    vendas = carregar_vendas()
    contagem = {}

    for v in vendas:
        for item in v["itens"]:
            nome = item["nome"]
            qtd = item["qtd"]
            contagem[nome] = contagem.get(nome, 0) + qtd

    if not contagem:
        print("\nSem vendas.")
        pausar()
        return

    top = sorted(contagem.items(), key=lambda x: x[1], reverse=True)[:3]

    print("\n" + "=" * 50)
    print("TOP 3 JOGOS MAIS VENDIDOS".center(50))
    print("=" * 50)

    for i, (nome, qtd) in enumerate(top, 1):
        print("{0}. {1} - {2} unidades".format(i, nome, qtd))

    print("=" * 50)
    pausar()


def ver_todos_clientes():
    
    clientes = carregar_clientes()

    if not clientes:
        print("\nSem clientes.")
        pausar()
        return

    print("\n" + "=" * 50)
    print("CLIENTES REGISTADOS".center(50))
    print("=" * 50)

    for i, c in enumerate(clientes, 1):
        print("{0}. {1}".format(i, c))

    print("=" * 50)
    print("Total: {0} clientes".format(len(clientes)))
    pausar()


def alterar_precos(jogos):
    mostrar_catalogo(jogos)
    escolha = pedir_numero("Qual jogo alterar preco? ", 1, len(jogos))
    jogo = jogos[escolha - 1]

    novo = input("Novo preco: ").strip()

    try:
        novo = float(novo)
    except:
        print("Preco invalido.")
        pausar()
        return jogos

    confirma = input("Confirmar alteracao? (s/n): ").strip().lower()
    if confirma != "s":
        print("Alteracao cancelada.")
        pausar()
        return jogos

    jogos[escolha - 1] = (jogo[0], jogo[1], jogo[2], jogo[3], jogo[4], novo, jogo[6])
    guardar_stock(jogos)

    print("Preco alterado.")
    pausar()
    return jogos


def gerir_stock(jogos):
    mostrar_catalogo(jogos)
    escolha = pedir_numero("Qual jogo alterar stock? ", 1, len(jogos))
    jogo = jogos[escolha - 1]

    novo = input("Novo stock: ").strip()

    if not novo.isdigit():
        print("Stock invalido.")
        pausar()
        return jogos

    novo = int(novo)

    if novo < 0:
        print("Stock nao pode ser negativo.")
        pausar()
        return jogos

    confirma = input("Confirmar alteracao? (s/n): ").strip().lower()
    if confirma != "s":
        print("Alteracao cancelada.")
        pausar()
        return jogos

    jogos[escolha - 1] = (jogo[0], jogo[1], jogo[2], jogo[3], jogo[4], jogo[5], novo)
    guardar_stock(jogos)

    print("Stock alterado.")
    pausar()
    return jogos


def produtos_stock_baixo(jogos):
    
    print("\n" + "=" * 50)
    print("PRODUTOS COM STOCK BAIXO (<10)".center(50))
    print("=" * 50)

    baixo = [j for j in jogos if j[6] < 10]

    if not baixo:
        print("\nNenhum produto com stock baixo.")
        pausar()
        return

    for j in baixo:
        print("- {0}: {1} unidades".format(j[0], j[6]))

    print("=" * 50)
    pausar()


# ----------------------------
# Menus
# ----------------------------

def menu_cliente(jogos, cliente_nome):
    carrinho = []

    while True:
        
        print("\n" + "=" * 50)
        print("LOJA DE JOGOS - CLIENTE".center(50))
        print("=" * 50)
        print("Usuario: {0}".format(cliente_nome))
        print("=" * 50)
        print("1 - Ver catalogo")
        print("2 - Carrinho")
        print("3 - Pesquisa/Filtros")
        print("4 - Minhas compras")
        print("5 - Sair da conta")
        print("=" * 50)

        op = input("Opcao: ").strip()

        if op == "1":
            mostrar_catalogo(jogos)

        elif op == "2":
            while True:
                
                print("\n" + "=" * 50)
                print("CARRINHO".center(50))
                print("=" * 50)
                print("1 - Adicionar ao carrinho")
                print("2 - Ver carrinho")
                print("3 - Remover do carrinho")
                print("4 - Alterar quantidade")
                print("5 - Finalizar compra")
                print("6 - Voltar")
                print("=" * 50)

                c = input("Opcao: ").strip()

                if c == "1":
                    adicionar_ao_carrinho(carrinho, jogos)
                elif c == "2":
                    ver_carrinho(carrinho)
                elif c == "3":
                    remover_do_carrinho(carrinho)
                elif c == "4":
                    alterar_quantidade_carrinho(carrinho, jogos)
                elif c == "5":
                    jogos = finalizar_compra_com_carrinho(carrinho, jogos, cliente_nome)
                elif c == "6":
                    break
                else:
                    print("Opcao invalida.")
                    pausar()

        elif op == "3":
            while True:
                2
                print("\n" + "=" * 50)
                print("PESQUISA/FILTROS".center(50))
                print("=" * 50)
                print("1 - Pesquisar por nome")
                print("2 - Filtrar por categoria")
                print("3 - Filtrar por preco")
                print("4 - Ordenar (Normal)")
                print("5 - Ordenar (A-Z)")
                print("6 - Ordenar (Z-A)")
                print("7 - Ordenar (Genero)")
                print("8 - Ordenar (Plataforma)")
                print("9 - Ordenar (Data)")
                print("10 - Ordenar (Modos)")
                print("11 - Ordenar (Preco)")
                print("12 - Ordenar (Stock)")
                print("13 - Voltar")
                print("=" * 50)

                p = input("Opcao: ").strip()

                if p == "1":
                    res = pesquisar_por_nome(jogos)
                    mostrar_catalogo(res)
                elif p == "2":
                    res = filtrar_por_categoria(jogos)
                    mostrar_catalogo(res)
                elif p == "3":
                    res = filtrar_por_preco(jogos)
                    mostrar_catalogo(res)
                elif p == "4":
                    res = ordenar_normal(jogos)
                    mostrar_catalogo(res)
                elif p == "5":
                    res = ordenar_az(jogos)
                    mostrar_catalogo(res)
                elif p == "6":
                    res = ordenar_za(jogos)
                    mostrar_catalogo(res)
                elif p == "7":
                    res = ordenar_por_genero(jogos)
                    mostrar_catalogo(res)
                elif p == "8":
                    res = ordenar_por_plataforma(jogos)
                    mostrar_catalogo(res)
                elif p == "9":
                    res = ordenar_por_data(jogos)
                    mostrar_catalogo(res)
                elif p == "10":
                    res = ordenar_por_modos(jogos)
                    mostrar_catalogo(res)
                elif p == "11":
                    res = ordenar_por_preco(jogos)
                    mostrar_catalogo(res)
                elif p == "12":
                    res = ordenar_por_stock(jogos)
                    mostrar_catalogo(res)
                elif p == "13":
                    break
                else:
                    print("Opcao invalida.")
                    pausar()

        elif op == "4":
            ver_minhas_compras(cliente_nome)

        elif op == "5":
            print("\nSaindo da conta...")
            pausar()
            break

        else:
            print("Opcao invalida.")
            pausar()

    return jogos


def menu_admin(jogos):
    while True:
        
        print("\n" + "=" * 50)
        print("PAINEL DE ADMINISTRADOR".center(50))
        print("=" * 50)
        print("1 - Relatorio vendas")
        print("2 - Produto mais vendido")
        print("3 - Top 3 jogos")
        print("4 - Ver clientes registados")
        print("5 - Alterar precos")
        print("6 - Gerir stock")
        print("7 - Alerta stock baixo")
        print("8 - Sair da conta")
        print("=" * 50)

        a = input("Opcao: ").strip()

        if a == "1":
            relatorio_vendas()
        elif a == "2":
            produto_mais_vendido()
        elif a == "3":
            top_3_jogos()
        elif a == "4":
            ver_todos_clientes()
        elif a == "5":
            jogos = alterar_precos(jogos)
        elif a == "6":
            jogos = gerir_stock(jogos)
        elif a == "7":
            produtos_stock_baixo(jogos)
        elif a == "8":
            print("\nSaindo da conta admin...")
            pausar()
            break
        else:
            print("Opcao invalida.")
            pausar()

    return jogos


# ----------------------------
# Programa principal
# ----------------------------

def main():
    jogos = carregar_stock()
    usuarios = carregar_usuarios()

    while True:
        
        print("\n" + "=" * 50)
        print("GAMES_EDUU".center(50))
        print("=" * 50)
        print("1 - Registrar novo usuario")
        print("2 - Login")
        print("3 - Sair")
        print("=" * 50)

        opcao = input("Opcao: ").strip()

        if opcao == "1":
            usuarios = registro_usuario(usuarios)

        elif opcao == "2":
            tipo, nome_logado = login(usuarios)

            if tipo == "admin":
                jogos = menu_admin(jogos)

            elif tipo == "cliente":
                jogos = menu_cliente(jogos, nome_logado)

        elif opcao == "3":
            
            print("\n" + "=" * 50)
            print("Obrigado por usar a Loja de Jogos!".center(50))
            print("Ate breve!".center(50))
            print("=" * 50)
            break

        else:
            print("\nOpcao invalida. Usa 1, 2 ou 3.")
            pausar()


if __name__ == "__main__":
    main()
