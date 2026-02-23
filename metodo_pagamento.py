from faker import Faker
from faker_crypto import CryptoAddress
import random

fake = Faker("pt_PT")
fake.add_provider(CryptoAddress)


def gerar_numero_cartao_simulacao():
    """
    Gera um numero de cartao PARA SIMULACAO (nao-real e nao-aceitavel em pagamento).
    """
    digitos = [str(random.randint(0, 9)) for _ in range(16)]
    digitos[-1] = "0"  # torna ainda mais "cara de teste"
    return "".join(digitos)


def gerar_cartao_ficticio(nome_usuario):
    cartao = {
        "nome": nome_usuario,
        "numero": gerar_numero_cartao_simulacao(),
        "validade": fake.credit_card_expire(),
        "cvv": str(random.randint(100, 999))
    }
    return cartao


def pagar_com_cartao(nome):
    cartao = gerar_cartao_ficticio(nome)
    print("\n=== PAGAMENTO COM CARTAO (SIMULACAO) ===")
    print("Titular: {0}".format(cartao["nome"]))
    print("Numero:  {0}".format(cartao["numero"]))
    print("Validade:{0}".format(cartao["validade"]))
    print("CVV:     {0}".format(cartao["cvv"]))
    print("Status:  PAGO \n")


def pagar_com_paypal(nome):
    token = fake.uuid4()
    email = "{0}@gmail.com".format(nome.replace(" ", "").lower())

    print("\n=== PAGAMENTO COM PAYPAL ===")
    print("Email:   {0}".format(email))
    print("Token:   {0}".format(token))
    print("=== Status:  PAGO ====\n")


def pagar_em_dinheiro(nome):
    codigo = fake.bban()
    print("\n=== PAGAMENTO EM DINHEIRO  ===")
    print("Usuario: {0}".format(nome))
    print("Codigo:  {0}".format(codigo))
    print("Status:  PENDENTE\n")


def pagar_em_bitcoin(nome):
    token = fake.uuid4()
    endereco_btc = fake.bitcoin_address()

    print("\n=== PAGAMENTO EM BITCOIN  ===")
    print("Usuario:  {0}".format(nome))
    print("Endereco: {0}".format(endereco_btc))
    print("Token:    {0}".format(token))
    print("Status:   Pago\n")


def iniciar_checkout():
    nome_usuario = input("Digite o seu nome completo: ").strip()

    if nome_usuario == "" or not nome_usuario.replace(" ", "").isalpha():
        print("So podes digitar letras de A a Z no nome.")
        return

    print("\n=== INICIAR CHECKOUT ===")
    print("1 - cartao")
    print("2 - paypal")
    print("3 - dinheiro")
    print("4 - bitcoin")

    escolha = input("pagamento (1/2/3/4): ").strip()

    if escolha == "1":
        pagar_com_cartao(nome_usuario)
    elif escolha == "2":
        pagar_com_paypal(nome_usuario)
    elif escolha == "3":
        pagar_em_dinheiro(nome_usuario)
    elif escolha == "4":
        pagar_em_bitcoin(nome_usuario)
    else:
        print("\n=== OPCAO INVALIDA ===")


if __name__ == "__main__":
    iniciar_checkout()
