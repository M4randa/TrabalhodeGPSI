"""
GESTOR DE NOMES - SISTEMA SIMPLES
Gerencia nomes, favoritos e categorias. Salva em arquivo JSON.
Sistema CRUD completo com persistência, histórico e interface CLI.
"""
import json  # JSON: Formato leve de dados, parecido com dicionário Python
from datetime import datetime  # Para timestamps no histórico
import pygame  # Biblioteca para reprodução de áudio

class GestorDeNomes:
    """
    Classe principal - Paradigma OOP (Programação Orientada a Objetos)
    Organiza dados (estado) e ações (comportamento) em um único lugar.
    'self' permite compartilhar variáveis entre todos os métodos da classe.
    """

    def __init__(self, arquivo='nomes.json'):
        """Construtor - Inicializa o sistema com estado vazio ou carregado"""
        self.arquivo = arquivo  # Nome do arquivo de persistência

        # ESTRUTURA DE DADOS PRINCIPAL - 4 componentes do sistema:
        self.nomes = []        # Banco de dados principal (lista simples)
        self.historico = []    # Log de auditoria (rastreabilidade)
        self.favoritos = []    # Subconjunto especial (filtro importante)
        self.categorias = {}   # Organização hierárquica (dicionário de listas)

        # 🎵 SISTEMA DE ÁUDIO - DECISÃO DE DESIGN
        pygame.mixer.init()  # Inicializa SOMENTE o mixer (mais eficiente)
        pygame.mixer.music.load("Roses.ogg")  # Formato OGG: livre, boa compressão
        pygame.mixer.music.play(-1)  # -1 = loop infinito (constante do Pygame)
        print("Roses,Kanye West")  # Feedback para usuário saber qual música

        self.carregar_dados()  # Carrega estado anterior (se existir)

    def carregar_dados(self):
        """
        CARREGAMENTO TOLERANTE A FALHAS
        Try/except silencioso: melhor começar vazio que travar o programa
        """
        try:
            # Gerenciador de contexto: fecha arquivo automaticamente
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)  # Converte JSON para dicionário Python

                # .get() com valor padrão: evita KeyError se chave não existir
                self.nomes = dados.get('nomes', [])
                self.historico = dados.get('historico', [])
                self.favoritos = dados.get('favoritos', [])
                self.categorias = dados.get('categorias', {})
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Primeira execução ou arquivo corrompido - inicia vazio

    def salvar_dados(self):
        """PERSISTÊNCIA COMPLETA - Salva todo o estado em arquivo JSON"""
        dados = {
            'nomes': self.nomes,
            'historico': self.historico,
            'favoritos': self.favoritos,
            'categorias': self.categorias
        }
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            # Parâmetros importantes:
            # indent=2: formatação bonita para debug humano
            # ensure_ascii=False: preserva acentos e caracteres especiais
            json.dump(dados, f, indent=2, ensure_ascii=False)

    def registrar_historico(self, acao):
        """RASTREABILIDADE - Cada ação gera um registro com timestamp"""
        # strftime: formata data/hora em formato brasileiro
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # f-string: formatação moderna e eficiente
        self.historico.append(f"[{timestamp}] {acao}")

    # ========== IMPLEMENTAÇÃO CRUD COMPLETA ==========
    # CRUD: Create, Read, Update, Delete - padrão fundamental de sistemas
    # Cada operação mapeada para um método específico
    # =================================================

    def adicionar_nome(self):
        """CREATE: Adiciona novo nome com validações"""
        print("\n" + "=" * 40)
        print(" ADICIONAR NOME ".center(40))  # .center(): interface alinhada

        nome = input("Nome: ").strip()  # .strip(): remove espaços desnecessários

        # VALIDAÇÕES IMPORTANTES:
        if not nome:  # Verifica string vazia
            print("ERRO: Nome vazio")
            return
        if nome in self.nomes:  # Verifica duplicidade
            print("ATENÇÃO: Nome já existe!")
            return

        self.nomes.append(nome)  # Adiciona ao banco principal

        # CATEGORIA OPCIONAL - usando setdefault()
        if self.categorias:
            print("Categorias:", list(self.categorias.keys()))
        cat = input("Categoria (Enter pular): ").strip()
        if cat:
            # setdefault(): cria lista se não existe, evita KeyError
            self.categorias.setdefault(cat, []).append(nome)

        # FAVORITO OPCIONAL - simples confirmação s/n
        if input("Favorito? (s/n): ").lower() == 's':
            self.favoritos.append(nome)

        self.registrar_historico(f"Adicionou: {nome}")
        self.salvar_dados()  # Persiste após cada alteração importante
        print(f"✓ {nome} adicionado!")  # ✓ Unicode para feedback visual

    def remover_nome(self):
        """DELETE: Remove completamente, limpando todas as referências"""
        print("\n" + "=" * 40)
        print(" REMOVER NOME ".center(40))

        if not self.nomes:  # Verificação de lista vazia
            print("Lista vazia!")
            return

        # INTERFACE NUMERADA - enumerate() com start=1
        for i, nome in enumerate(self.nomes, 1):  # Começa em 1 (mais amigável)
            print(f"{i}. {nome}")

        try:
            escolha = int(input("Número: ")) - 1  # Converte para índice 0-based

            # VALIDAÇÃO DE ÍNDICE - evita IndexError
            if 0 <= escolha < len(self.nomes):
                removido = self.nomes.pop(escolha)  # pop(): remove por índice

                # LIMPEZA DE REFERÊNCIAS CRUZADAS:
                if removido in self.favoritos:
                    self.favoritos.remove(removido)  # remove(): por valor

                # Remove de todas as categorias
                for lista in self.categorias.values():
                    if removido in lista:
                        lista.remove(removido)

                self.registrar_historico(f"Removeu: {removido}")
                self.salvar_dados()
                print(f"✓ {removido} removido!")

        except (ValueError, IndexError):  # Captura múltiplos erros
            print("ERRO: Digite um número válido")

    def listar_nomes(self):
        """READ: Visualização flexível com múltiplas ordenações"""
        print("\n" + "=" * 40)
        print(" LISTAR NOMES ".center(40))

        if not self.nomes:
            print("Nenhum nome cadastrado")
            return

        print("1. Ordem normal  2. A-Z  3. Z-A  4. Favoritos")
        opcao = input("Opção: ").strip()

        lista_exibir = self.nomes.copy()  # .copy(): evita modificar original

        # SISTEMA DE FILTROS/ORDENAÇÃO:
        if opcao == '2':
            lista_exibir = sorted(lista_exibir)  # sorted(): retorna nova lista
        elif opcao == '3':
            lista_exibir = sorted(lista_exibir, reverse=True)
        elif opcao == '4':
            lista_exibir = self.favoritos  # Referência direta (já é lista)

        # EXIBIÇÃO RICA COM METADADOS:
        print("\n" + "-" * 40)
        for i, nome in enumerate(lista_exibir, 1):
            favorito = "*" if nome in self.favoritos else " "  # Operador ternário
            categoria = ""

            # Busca categoria do nome (break otimiza performance)
            for cat, lista in self.categorias.items():
                if nome in lista:
                    categoria = f" ({cat})"  # f-string com expressão
                    break

            print(f"{favorito} {i}. {nome}{categoria}")
        print(f"Total: {len(lista_exibir)}")  # f-string com função len()

    def procurar_nome(self):
        """READ: Sistema de busca com 3 algoritmos diferentes"""
        print("\n" + "=" * 40)
        print(" PROCURAR NOME ".center(40))

        print("1. Por texto  2. Por inicial  3. Por categoria")
        tipo = input("Tipo: ").strip()
        encontrados = []  # Lista de tuplas (índice, nome)

        # ALGORITMO 1: Busca por substring (case-insensitive)
        if tipo == '1':
            texto = input("Texto: ").lower()
            for i, nome in enumerate(self.nomes):
                if texto in nome.lower():  # .lower(): busca case-insensitive
                    encontrados.append((i + 1, nome))  # +1 para índice amigável

        # ALGORITMO 2: Busca por primeira letra
        elif tipo == '2':
            letra = input("Inicial: ").upper()
            for i, nome in enumerate(self.nomes):
                if nome and nome[0].upper() == letra:  # Verifica se nome não é vazio
                    encontrados.append((i + 1, nome))

        # ALGORITMO 3: Busca por categoria
        elif tipo == '3':
            if self.categorias:
                print("Categorias:", list(self.categorias.keys()))
                cat = input("Categoria: ")
                if cat in self.categorias:
                    for nome in self.categorias[cat]:
                        i = self.nomes.index(nome)  # .index(): busca posição
                        encontrados.append((i + 1, nome))

        # APRESENTAÇÃO DE RESULTADOS:
        if encontrados:
            print(f"\n{len(encontrados)} resultado(s):")
            for num, nome in encontrados:
                print(f"{num}. {nome}")
        else:
            print("Nenhum resultado")

    def editar_nome(self):
        """UPDATE: Modificação com atualização de todas as referências"""
        print("\n" + "=" * 40)
        print(" EDITAR NOME ".center(40))

        if not self.nomes:
            print("Lista vazia!")
            return

        for i, nome in enumerate(self.nomes, 1):
            print(f"{i}. {nome}")

        try:
            escolha = int(input("Número: ")) - 1
            if 0 <= escolha < len(self.nomes):
                antigo = self.nomes[escolha]
                novo = input(f"Novo nome ({antigo}): ").strip()  # f-string com variável

                if novo:
                    self.nomes[escolha] = novo  # Atualização direta

                    # ATUALIZAÇÃO DE REFERÊNCIAS CRUZADAS:
                    if antigo in self.favoritos:
                        idx = self.favoritos.index(antigo)  # Encontra posição
                        self.favoritos[idx] = novo  # Substitui

                    # Atualiza em todas as categorias
                    for lista in self.categorias.values():
                        if antigo in lista:
                            idx = lista.index(antigo)
                            lista[idx] = novo

                    self.registrar_historico(f"Editou: {antigo} → {novo}")
                    self.salvar_dados()
                    print("✓ Nome atualizado!")

        except (ValueError, IndexError):
            print("ERRO: Número inválido")

    def gerenciar_favoritos(self):
        """SUBSISTEMA: Gerencia lista especial de favoritos"""
        print("\n" + "=" * 40)
        print(" FAVORITOS ".center(40))

        if self.favoritos:
            print("Atuais:")
            for i, nome in enumerate(self.favoritos, 1):
                print(f"{i}. {nome}")

        print("\n1. Adicionar  2. Remover  3. Voltar")
        opcao = input("Opção: ").strip()

        if opcao == '1':
            # LIST COMPREHENSION: nomes que NÃO são favoritos
            nao_fav = [n for n in self.nomes if n not in self.favoritos]

            if nao_fav:
                for i, nome in enumerate(nao_fav, 1):
                    print(f"{i}. {nome}")
                try:
                    idx = int(input("Número: ")) - 1
                    if 0 <= idx < len(nao_fav):
                        self.favoritos.append(nao_fav[idx])
                        self.salvar_dados()
                        print("✓ Adicionado!")
                except (ValueError, IndexError):
                    print("ERRO: Número inválido")

        elif opcao == '2' and self.favoritos:
            try:
                idx = int(input("Número para remover: ")) - 1
                if 0 <= idx < len(self.favoritos):
                    removido = self.favoritos.pop(idx)  # pop(): remove por índice
                    self.salvar_dados()
                    print(f"✓ {removido} removido!")
            except (ValueError, IndexError):
                print("ERRO: Número inválido")

    def gerenciar_categorias(self):
        """SUBSISTEMA: Gerencia organização hierárquica"""
        print("\n" + "=" * 40)
        print(" CATEGORIAS ".center(40))

        if self.categorias:
            for cat, nomes in self.categorias.items():
                print(f"\n{cat}: {len(nomes)} nome(s)")  # f-string com contagem
                for nome in nomes:
                    print(f"  - {nome}")

        print("\n1. Nova categoria  2. Remover categoria")
        print("3. Add nome  4. Remove nome  5. Voltar")
        opcao = input("Opção: ").strip()

        # ESTRUTURA CONDICIONAL PARA GESTÃO DE CATEGORIAS
        # Cada opção do menu de categorias é tratada com lógica específica
        if opcao == '1':  # Opção 1: Criar nova categoria
            # Solicita nome da nova categoria
            cat = input("Nome da categoria: ").strip()  # .strip() remove espaços em branco desnecessários

            # VALIDAÇÃO: Verifica se o usuário digitou algo (não string vazia)
            if cat:  # if cat é equivalente a if cat != ""
                # CRIAÇÃO: Inicializa nova chave no dicionário com lista vazia como valor
                self.categorias[cat] = []  # Sintaxe dicionario[chave] = valor

                # PERSISTÊNCIA: Salva imediatamente após alteração importante
                self.salvar_dados()  # Garante que dados não sejam perdidos em caso de crash

                # FEEDBACK: f-string com interpolação de variável e formatação clara
                print(f"✓ Categoria '{cat}' criada!")  # Unicode ✓ para feedback visual positivo

        elif opcao == '2' and self.categorias:  # Opção 2: Remover categoria (se existirem)
            # CONDIÇÃO DUPLA: and garante que só executa se houver categorias
            # EVITA ERRO: Não tenta mostrar keys() de dicionário vazio

            # VISUALIZAÇÃO: Converte dict_keys para lista para exibição amigável
            print("Categorias:", list(self.categorias.keys()))  # .keys() retorna view, convertemos para lista

            # ENTRADA DO USUÁRIO: Solicita qual categoria remover
            cat = input("Remover qual: ").strip()  # Strip novamente para limpeza

            # VERIFICAÇÃO DE EXISTÊNCIA: Evita KeyError ao tentar remover chave inexistente
            if cat in self.categorias:  # Operador 'in' verifica se chave existe no dicionário

                # REMOÇÃO: del remove a chave COMPLETAMENTE do dicionário
                del self.categorias[cat]  # Sintaxe: del dict[chave] - apaga chave e valor

                # PERSISTÊNCIA: Salva após alteração destrutiva
                self.salvar_dados()

                # FEEDBACK: Confirmação com nome da categoria removida
                print(f"✓ Categoria '{cat}' removida!")

        elif opcao == '3' and self.categorias:  # Opção 3: Adicionar nome a categoria existente
            # VALIDAÇÃO: Garante que há categorias para escolher

            # VISUALIZAÇÃO DE OPÇÕES: Mostra categorias disponíveis
            print("Categorias:", list(self.categorias.keys()))

            # ESCOLHA DA CATEGORIA: Usuário seleciona qual categoria usar
            cat = input("Adicionar em qual: ").strip()

            # VERIFICAÇÃO: Confirma que categoria existe
            if cat in self.categorias:  # Previne KeyError ao acessar self.categorias[cat]

                # LISTAGEM DE NOMES DISPONÍVEIS: enumerate com start=1 para interface amigável
                for i, nome in enumerate(self.nomes, 1):  # i começa em 1, não 0
                    print(f"{i}. {nome}")  # f-string para formatação limpa

                try:  # BLOCO TRY: Protege contra entrada inválida do usuário
                    # CONVERSÃO: Transforma string em inteiro e ajusta para índice 0-based
                    idx = int(input("Número do nome: ")) - 1  # -1 converte de "humano" para "Python"

                    # VALIDAÇÃO DE ÍNDICE: Verifica se está dentro dos limites da lista
                    if 0 <= idx < len(self.nomes):  # Intervalo inclusivo-exclusivo [0, len())

                        # PREVENÇÃO DE DUPLICATAS: Verifica se nome já não está na categoria
                        if self.nomes[idx] not in self.categorias[cat]:  # Operador 'not in'

                            # ADIÇÃO: .append() adiciona ao final da lista da categoria
                            self.categorias[cat].append(self.nomes[idx])  # Acessa nome pelo índice

                            # PERSISTÊNCIA: Salva após adição
                            self.salvar_dados()

                            # FEEDBACK: Confirmação genérica (sem mostrar qual nome)
                            print("✓ Adicionado!")
                        # NOTA: Se já existir, não faz nada (silenciosamente)

                except (ValueError,
                        IndexError):  # CAPTURA MÚLTIPLA: ValueError (int() falhou) e IndexError (índice fora)
                    print("ERRO: Número inválido")  # Mensagem de erro genérica mas informativa

        elif opcao == '4' and self.categorias:  # Opção 4: Remover nome de categoria específica
            # VALIDAÇÃO DUPLA: Garante que há categorias E que a escolhida não é vazia

            # VISUALIZAÇÃO DE CATEGORIAS: Mostra opções disponíveis
            print("Categorias:", list(self.categorias.keys()))

            # ESCOLHA DA CATEGORIA: Usuário seleciona de onde remover
            cat = input("Remover de qual: ").strip()

            # VERIFICAÇÃO DUPLA: 1) Categoria existe, 2) Categoria não está vazia
            if cat in self.categorias and self.categorias[cat]:  # and avalia ambas condições
                # self.categorias[cat] é truthy se lista não vazia

                # LISTAGEM DE NOMES NA CATEGORIA: enumerate específico para essa lista
                for i, nome in enumerate(self.categorias[cat], 1):  # start=1 novamente
                    print(f"{i}. {nome}")  # Mostra apenas nomes que estão na categoria

                try:  # BLOCO TRY PARA TRATAMENTO DE ERROS
                    # CONVERSÃO E AJUSTE DE ÍNDICE
                    idx = int(input("Número: ")) - 1  # -1 para índice 0-based

                    # VALIDAÇÃO DE ÍNDICE DENTRO DA CATEGORIA ESPECÍFICA
                    if 0 <= idx < len(self.categorias[cat]):  # Usa len() da lista específica

                        # REMOÇÃO E CAPTURA DO VALOR: .pop() remove E retorna o elemento
                        removido = self.categorias[cat].pop(idx)  # .pop(índice) - mais específico que .remove()

                        # PERSISTÊNCIA: Salva após remoção
                        self.salvar_dados()

                        # FEEDBACK ESPECÍFICO: Mostra qual nome foi removido
                        print(f"✓ {removido} removido!")  # Interpola nome removido na mensagem

                except (ValueError, IndexError):  # CAPTURA DUPLA: Entrada não numérica ou índice inválido
                    print("ERRO: Número inválido")
    def ver_historico(self):
        """AUDITORIA: Mostra últimas ações do sistema"""
        print("\n" + "=" * 40)
        print(" HISTÓRICO ".center(40))

        if self.historico:
            # SLICING: [-10:] pega os últimos 10 elementos
            for acao in self.historico[-10:]:  # Mostra apenas últimos 10 registros
                print(acao)
        else:
            print("Nenhuma ação registrada")

    def estatisticas(self):
        """ANALÍTICA: Métricas e insights sobre os dados"""
        print("\n" + "=" * 40)
        print(" ESTATÍSTICAS ".center(40))

        print(f"Nomes: {len(self.nomes)}")
        print(f"Favoritos: {len(self.favoritos)}")
        print(f"Categorias: {len(self.categorias)}")
        print(f"Ações: {len(self.historico)}")

        if self.nomes:
            # max/min com key=len: encontra maior/menor por comprimento
            maior = max(self.nomes, key=len)
            menor = min(self.nomes, key=len)
            print(f"\nMais longo: {maior} ({len(maior)} letras)")
            print(f"Mais curto: {menor} ({len(menor)} letras)")

    def humanizar_nome(self):
        """PROCESSAMENTO DE TEXTO: Formata nomes para padrão capitalizado"""
        print("\n" + "=" * 40)
        print(" HUMANIZAR NOME ".center(40))

        nome = input("Nome para formatar: ").strip()
        if nome:
            # Algoritmo de capitalização:
            palavras = nome.split()  # split(): divide por espaços
            # GENERATOR EXPRESSION: eficiente para processamento
            formatado = " ".join(p.capitalize() for p in palavras)

            print(f"Original: {nome}")
            print(f"Formatado: {formatado}")

            if input("\nAdicionar à lista? (s/n): ").lower() == 's':
                if formatado not in self.nomes:
                    self.nomes.append(formatado)
                    self.registrar_historico(f"Humanizou: {formatado}")
                    self.salvar_dados()
                    print("✓ Adicionado!")

    def limpar_lista(self):
        """OPERAÇÃO DESTRUTIVA: Limpeza completa com confirmação rigorosa"""
        print("\n" + "=" * 40)
        print(" LIMPAR TUDO ".center(40))

        print("ATENÇÃO: Isso apaga TUDO!")
        # Confirmação explícita: evita acidentes
        if input("Digite 'APAGAR' para confirmar: ") == "APAGAR":
            self.nomes = []
            self.favoritos = []
            self.categorias = {}
            self.historico = []
            self.salvar_dados()
            print("✓ Todos os dados apagados!")

    def menu(self):
        """LOOP PRINCIPAL: Interface de linha de comando interativa"""
        while True:  # Loop infinito até sair() chamar exit()
            print("\n" + "=" * 40)
            print(" GESTOR DE NOMES ".center(40))
            print("=" * 40)
            print("🎵 Roses - Kanye West (loop infinito)")
            print("-" * 40)

            # LISTA DE OPÇÕES - fácil de manter e estender
            opcoes = [
                "1. Adicionar nome",
                "2. Remover nome",
                "3. Listar nomes",
                "4. Procurar nome",
                "5. Editar nome",
                "6. Gerenciar favoritos",
                "7. Gerenciar categorias",
                "8. Ver histórico",
                "9. Estatísticas",
                "10. Humanizar nome",
                "11. Limpar tudo",
                "12. Sair"
            ]

            for op in opcoes:
                print(op)

            print("=" * 40)
            escolha = input("Opção: ").strip()

            # DICIONÁRIO DE AÇÕES - padrão Command/Dispatcher
            # Mapeia strings para métodos, evitando if/elif gigante
            acoes = {
                '1': self.adicionar_nome,
                '2': self.remover_nome,
                '3': self.listar_nomes,
                '4': self.procurar_nome,
                '5': self.editar_nome,
                '6': self.gerenciar_favoritos,
                '7': self.gerenciar_categorias,
                '8': self.ver_historico,
                '9': self.estatisticas,
                '10': self.humanizar_nome,
                '11': self.limpar_lista,
                '12': self.sair
            }

            if escolha in acoes:
                acoes[escolha]()  # Executa método dinamicamente
            else:
                print("ERRO: Opção inválida!")

    def sair(self):
        """SHUTDOWN: Encerramento seguro com persistência"""
        print("\n" + "=" * 40)
        self.salvar_dados()  # Garante que nada seja perdido
        pygame.mixer.music.stop()  # 🎵 Para a música
        print("Dados salvos. Até logo!")
        exit()  # Encerra o programa completamente


# ================================================
# PONTO DE ENTRADA DO PROGRAMA
# ================================================
if __name__ == "__main__":
    """
    CONVENÇÃO PYTHON: __name__ == "__main__"
    Permite que o arquivo seja tanto executado quanto importado como módulo.
    Se executado diretamente: python gestor.py → roda o sistema
    Se importado: import gestor → só carrega, não executa automaticamente
    """
    sistema = GestorDeNomes()  # Cria instância do sistema
    sistema.menu()  # Inicia o loop principal