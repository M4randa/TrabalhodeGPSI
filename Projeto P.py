import random

JOGADOR_SALDO = 100.00
JOGADOR_HISTORICO = ["Inicio da sessao: Saldo Inicial de 100.00"]

jogos_nomes = ["Elden Ring", "Cyberpunk 2077", "FIFA 25", "Hogwarts Legacy"]
jogos_precos = (60.00, 40.00, 70.00, 50.00)
jogos_estoque = [100, 50, 200, 75]


while True:
    print("\n===============================")
    print(" ***BEM-VINDO A LOJA JD***")
    print("===============================")

    print("SALDO ATUAL: " + str(round(JOGADOR_SALDO, 2)) + "")
    print("-------------------------------")
    print("3 Comprar Jogos")
    print("2- Ver Historico de Compras/Acoes")
    print("3- Adicionar Dinheiro")
    print("4- Gerir Stock (Admin)")
    print("5- Sair do Programa")
    print("-------------------------------")

    opcao_principal = input("Selecione uma opcao (1 a 5): ")

    if opcao_principal == "1":
        while True:
            print("\n-- Loja de Jogos --")
            print("SALDO ATUAL: " + str(round(JOGADOR_SALDO, 2)) + "")
            print("-------------------------------")

            for i in range(len(jogos_nomes)):
                print(str(i + 1) + "- " + jogos_nomes[i] + " | Preco: " + str(round(jogos_precos[i], 2)) + " | Em estoque: " + str(jogos_estoque[i]) + " unid.")

            print("0- Voltar ao menu principal")
            print("-------------------------------")

            try:
                escolha = int(input("Selecione o numero do item que deseja comprar (0 para sair): "))

                if escolha == 0:
                    break

                if 1 <= escolha <= len(jogos_nomes):
                    indice = escolha - 1
                    preco_item = jogos_precos[indice]
                    nome_item = jogos_nomes[indice]

                    if JOGADOR_SALDO >= preco_item:
                        if jogos_estoque[indice] > 0:
                            jogos_estoque[indice] -= 1
                            JOGADOR_SALDO -= preco_item
                            JOGADOR_HISTORICO.append("1 x " + nome_item)
                            print("\n✅ Compra efetuada com sucesso!")
                            print("Novo saldo: " + str(round(JOGADOR_SALDO, 2)) + "")
                        else:
                            print("\n❌ ERRO: Item sem estoque.")
                    else:
                        print("\n❌ ERRO: Saldo insuficiente. Precisa de " + str(round(preco_item, 2)) + "")
                else:
                    print("\n⚠️ Opcao invalida. Tente novamente.")
            except ValueError:
                print("\n⚠️ Entrada invalida. Digite um numero.")

    elif opcao_principal == "2":
        print("\n-- SEU HISTORICO DE ACOES --")
        if len(JOGADOR_HISTORICO) == 0:
            print("Nenhuma acao registada.")
        else:
            for item in JOGADOR_HISTORICO:
                print("- " + item)
        print("-------------------------------")

    elif opcao_principal == "3":
        print("\n-- ADICIONAR DINHEIRO --")
        valor_invalido = True
        while valor_invalido:
            valor_deposito_str = input("Digite o valor que deseja depositar: ")

            try:
                valor_deposito = float(valor_deposito_str)
                if valor_deposito > 0:
                    JOGADOR_SALDO += valor_deposito
                    JOGADOR_HISTORICO.append("DEPOSITO: Adicionado " + str(round(valor_deposito, 2)) + "")
                    print("\n✅ DEPOSITO BEM-SUCEDIDO! Adicionou " + str(round(valor_deposito, 2)) + ".")
                    print("Novo saldo: " + str(round(JOGADOR_SALDO, 2)) + "")
                    valor_invalido = False
                else:
                    print("⚠️ O valor deve ser positivo.")
            except ValueError:
                print("⚠️ Entrada invalida. Por favor, digite um numero valido.")

    elif opcao_principal == "4":
        while True:
            print("\n-- GESTAO DE STOCK (ADMIN) --")
            print("1- Gerir stock de Jogos")
            print("0- Voltar ao menu principal")
            print("-------------------------------")

            opcao_gestao = input("Selecione a categoria para gerir o stock (0 para voltar): ")

            if opcao_gestao == "1":
                while True:
                    print("\n--- Adicionar Stock: Jogos ---")
                    for i in range(len(jogos_nomes)):
                        print(str(i + 1) + "- " + jogos_nomes[i] + " | Stock Atual: " + str(jogos_estoque[i]))
                    print("0- Voltar")

                    try:
                        escolha = int(input("Selecione o item para adicionar stock (0 para voltar): "))
                        if escolha == 0:
                            break

                        if 1 <= escolha <= len(jogos_nomes):
                            indice = escolha - 1
                            quantidade_str = input("Quantas unidades deseja adicionar a '" + jogos_nomes[indice] + "'? ")
                            quantidade = int(quantidade_str)

                            if quantidade > 0:
                                jogos_estoque[indice] += quantidade
                                JOGADOR_HISTORICO.append("ADICIONADO STOCK: " + str(quantidade) + " unid. de " + jogos_nomes[indice])
                                print("\n✅ Stock atualizado. Novo stock de '" + jogos_nomes[indice] + "': " + str(jogos_estoque[indice]))
                            else:
                                print("⚠️ A quantidade deve ser positiva.")
                        else:
                            print("⚠️ Opcao invalida.")
                    except ValueError:
                        print("⚠️ Entrada invalida. Digite um numero inteiro.")
            elif opcao_gestao == "0":
                break
            else:
                print("\n❌ Opcao invalida.")

    elif opcao_principal == "5":
        print("\nObrigado por visitar a JD!")
        break
    else:
        print("\n❌ ERRO: Opcao invalida. Escolha um numero de 1 a 5.")

