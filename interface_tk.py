import tkinter as tk
# tkinter = biblioteca gráfica nativa do Python
# Cria janelas, botões, campos de texto (GUI)
# "as tk" = atalho para não escrever "tkinter" toda hora
# Exemplo: tk.Button() em vez de tkinter.Button()

from tkinter import ttk, messagebox, simpledialog
# ttk = widgets modernos e bonitos (Combobox, Notebook/abas)
# messagebox = caixas de diálogo (erro, confirmação, aviso)
# simpledialog = janelas pequenas para pedir input (editar nome, nota...)

import json

import os
# os = operações do sistema operacional
# Usado para verificar se arquivo existe, criar pastas, etc
# No código: os.path.exists(ARQUIVO_JSON) verifica se turma.json existe
import random

# Paleta de cores - tema escuro com alto contraste
bg, fg = "#1e1e1e", "white"
entry_bg, btn_bg = "#2d2d2d", "#3a3a3a"

# Regras de negócio - sistema de avaliação português
NOTA_MIN, NOTA_MAX = 0, 20
FALTAS_MIN, FALTAS_MAX = 0, 40
FALTAS_CHUMBO = 30

# Sistema de penalização progressivo
FALTA_MATERIAL_LIMITE = 2      # Acúmulo converte em falta de presença
FALTA_DISCIPLINAR_LIMITE = 3   # Acúmulo resulta em suspensão

DISCIPLINAS = [
    "Matemática", "Português", "História", "Geografia",
    "Física", "Química", "Biologia", "Inglês", "GPSI"
]

ARQUIVO_JSON = r"C:\Users\goatm\PyCharmMiscProject\JOGO\turma.json"


# Camada de persistência - padrão Repository para isolamento de dados
def garantir_json():
    """Inicialização lazy - cria arquivo apenas se necessário"""
    if not os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)


def salvar_turma(turma):
    """Persistência atômica - ensure_ascii=False suporta caracteres portugueses"""
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(turma, f, indent=4, ensure_ascii=False)


def calcular_situacao(nota, faltas):
    """Lógica de negócio centralizada - faltas têm precedência sobre nota"""
    if faltas > FALTAS_CHUMBO:
        return "Reprovado por faltas"
    if nota < 10:
        return "Reprovado por nota"
    return "Aprovado"


def carregar_turma():
    """
    Carregamento com migração automática de schema
    Compatibilidade retroativa - adiciona campos faltantes com valores padrão
    """
    garantir_json()
    with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
        turma = json.load(f)

    for a in turma:
        a.setdefault("disciplina", "—")
        a.setdefault("nota", 0)
        a.setdefault("faltas", 0)
        a.setdefault("falta_material", 0)
        a.setdefault("falta_disciplinar", 0)
        a.setdefault("suspenso", False)
        a["situacao"] = calcular_situacao(a["nota"], a["faltas"])

    return turma


# Validação de input - previne dados corrompidos
def nome_valido(nome: str) -> bool:
    """Aceita apenas letras e espaços - permite nomes compostos"""
    nome = nome.strip()
    if not nome:
        return False
    return all(p.isalpha() for p in nome.split())


def erro_nome():
    """Feedback com exemplo concreto para correção"""
    messagebox.showerror(
        "Nome inválido",
        "Só são permitidos nomes com letras e espaços.\nEx: Ana Clara, João Silva."
    )


class InovarInterface:
    """
    Classe = MOLDE que define:
    - Quais DADOS guardar (turma, widgets, filtro...)
    - Quais AÇÕES fazer (adicionar, editar, remover...)
    self = referencia daquele objeto na classe
    """

    def __init__(self, janela):
        # ☝️ CONSTRUTOR = método especial que inicia o projeto
        # Roda AUTOMATICAMENTE quando você faz: InovarInterface(root)

        self.janela = janela           # Guarda referência da janela
        self.turma = carregar_turma()  # Carrega dados do JSON
        self.filtro = None             # Estado da busca
        # ☝️ Todos esses dados ficam SALVOS NO OBJETO

        tk.Label(
            janela, text="🎓 Sistema Inovar",
            font=("Arial", 26, "bold"), bg=bg, fg=fg
        ).pack(pady=15)

        self.notebook = ttk.Notebook(janela)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self._aba_alunos()
        self._aba_faltas()
        self._aba_estatisticas()

        self.atualizar_combos()
        self.atualizar_lista()
        self.atualizar_estatisticas()

    # Padrão DRY - factory methods para widgets padronizados
    def _entry(self, parent, texto, row):
        """Cria label + entry com layout e estilo consistentes"""
        tk.Label(parent, text=texto, font=("Arial", 12), bg=bg, fg=fg)\
            .grid(row=row, column=0, padx=10, pady=6, sticky="e")

        e = tk.Entry(parent, width=35, font=("Arial", 12),
                     bg=entry_bg, fg=fg, insertbackground=fg, relief="solid", bd=1)
        e.grid(row=row, column=1, padx=10, pady=6, sticky="w")
        return e

    def _botao(self, parent, texto, cmd, col):
        tk.Button(parent, text=texto, command=cmd,
                  bg=btn_bg, fg="white", font=("Arial", 12),
                  width=15, relief="flat", pady=5)\
            .grid(row=0, column=col, padx=6)

    def _nome_selecionado(self):
        """Extrai nome da linha selecionada (parsing: 'Nome | Disciplina | ...')"""
        sel = self.listbox.curselection()
        if not sel:
            return None
        linha = self.listbox.get(sel[0])
        return linha.split("|")[0].strip()

    def _limpar_campos(self):
        for e in (self.entry_nome, self.entry_disciplina, self.entry_nota, self.entry_faltas):
            e.delete(0, tk.END)

    def _aba_alunos(self):
        """
        CRUD completo - layout hierárquico:
        Busca → Formulário → Ações → Listagem
        """
        frame = tk.Frame(self.notebook, bg=bg)
        self.notebook.add(frame, text="👥 Alunos")

        # Sistema de busca client-side - filtra em memória sem recarregar JSON
        box_busca = tk.Frame(frame, bg=bg)
        box_busca.pack(fill="x", padx=10, pady=8)

        tk.Label(box_busca, text="Buscar:", font=("Arial", 12), bg=bg, fg=fg)\
            .pack(side="left", padx=(0, 8))

        self.entry_busca = tk.Entry(box_busca, width=35, font=("Arial", 12),
                                    bg=entry_bg, fg=fg, insertbackground=fg, relief="solid", bd=1)
        self.entry_busca.pack(side="left", padx=(0, 8))

        tk.Button(box_busca, text="🔎 Buscar", command=self.buscar,
                  bg=btn_bg, fg="white", font=("Arial", 12),
                  width=12, relief="flat").pack(side="left", padx=5)

        tk.Button(box_busca, text="🧹 Limpar", command=self.limpar_busca,
                  bg=btn_bg, fg="white", font=("Arial", 12),
                  width=12, relief="flat").pack(side="left", padx=5)

        form = tk.LabelFrame(frame, text=" Dados do Aluno ", bg=bg, fg=fg, font=("Arial", 14))
        form.pack(pady=10, padx=10, fill="x")

        self.entry_nome = self._entry(form, "Nome:", 0)
        self.entry_disciplina = self._entry(form, "Disciplina:", 1)
        self.entry_nota = self._entry(form, "Nota (0-20):", 2)
        self.entry_faltas = self._entry(form, "Faltas (0-40):", 3)

        box_btns = tk.Frame(frame, bg=bg)
        box_btns.pack(pady=10)

        self._botao(box_btns, "➕ Adicionar", self.adicionar, 0)
        self._botao(box_btns, "🎲 Gerar", self.gerar, 1)
        self._botao(box_btns, "✏️ Editar", self.editar, 2)
        self._botao(box_btns, "🗑️ Remover", self.remover, 3)
        self._botao(box_btns, "📊 Organizar", self.organizar, 4)

        self.listbox = tk.Listbox(frame, width=90, height=14, font=("Arial", 11),
                                 bg=entry_bg, fg=fg, selectbackground="#555555")
        self.listbox.pack(pady=10, padx=10)

    def atualizar_lista(self):
        """Renderiza view respeitando filtro ativo"""
        self.listbox.delete(0, tk.END)
        dados = self.filtro if self.filtro is not None else self.turma

        for a in dados:
            linha = f"{a['nome']} | {a['disciplina']} | Nota: {a['nota']} | Faltas: {a['faltas']} | {a['situacao']}"
            if a.get("suspenso"):
                linha += " | ⛔ SUSPENSO"
            self.listbox.insert(tk.END, linha)

    def atualizar_combos(self):
        """Sincroniza combobox da aba Faltas com lista de alunos"""
        nomes = [a["nome"] for a in self.turma]
        self.combo_faltas["values"] = nomes

    def buscar(self):
        """Filtro case-insensitive com substring matching"""
        termo = self.entry_busca.get().strip().lower()
        if not termo:
            self.filtro = None
        else:
            self.filtro = [a for a in self.turma if termo in a["nome"].lower()]
        self.atualizar_lista()

    def limpar_busca(self):
        self.entry_busca.delete(0, tk.END)
        self.filtro = None
        self.atualizar_lista()

    def adicionar(self):
        """
        CREATE - validação em camadas:
        1. Formato (nome válido)
        2. Obrigatoriedade (disciplina)
        3. Tipo e range (nota/faltas)
        """
        nome = self.entry_nome.get().strip()
        if not nome_valido(nome):
            erro_nome()
            return

        disc = self.entry_disciplina.get().strip()
        if not disc:
            messagebox.showerror("Erro", "Disciplina obrigatória (ou use 🎲 Gerar).")
            return

        try:
            nota = float(self.entry_nota.get())
            faltas = int(self.entry_faltas.get())
        except:
            messagebox.showerror("Erro", "Nota ou faltas inválidas.")
            return

        if not (NOTA_MIN <= nota <= NOTA_MAX):
            messagebox.showerror("Erro", "Nota fora do limite.")
            return

        if not (FALTAS_MIN <= faltas <= FALTAS_MAX):
            messagebox.showerror("Erro", "Faltas fora do limite.")
            return

        aluno = {
            "nome": nome,
            "disciplina": disc,
            "nota": nota,
            "faltas": faltas,
            "falta_material": 0,
            "falta_disciplinar": 0,
            "suspenso": False,
            "situacao": calcular_situacao(nota, faltas)
        }

        self.turma.append(aluno)
        salvar_turma(self.turma)

        self.filtro = None
        self._limpar_campos()
        self.atualizar_combos()
        self.atualizar_lista()
        self.atualizar_estatisticas()

    def gerar(self):
        """Geração procedural - notas tendendo a aprovação (7-20), faltas baixas (0-12)"""
        nome = self.entry_nome.get().strip()
        if not nome_valido(nome):
            erro_nome()
            return

        aluno = {
            "nome": nome,
            "disciplina": random.choice(DISCIPLINAS),
            "nota": round(random.uniform(7, 20), 1),
            "faltas": random.randint(0, 12),
            "falta_material": 0,
            "falta_disciplinar": 0,
            "suspenso": False
        }
        aluno["situacao"] = calcular_situacao(aluno["nota"], aluno["faltas"])

        self.turma.append(aluno)
        salvar_turma(self.turma)

        self.filtro = None
        self._limpar_campos()
        self.atualizar_combos()
        self.atualizar_lista()
        self.atualizar_estatisticas()

        messagebox.showinfo("Automático", f"{nome} gerado com sucesso!")

    def editar(self):
        """UPDATE - diálogos modais sequenciais com validação inline"""
        nome_sel = self._nome_selecionado()
        if not nome_sel:
            messagebox.showwarning("Aviso", "Selecione um aluno.")
            return

        aluno = next((a for a in self.turma if a["nome"] == nome_sel), None)
        if not aluno:
            return

        novo_nome = simpledialog.askstring("Editar", "Nome:", initialvalue=aluno["nome"])
        if novo_nome is not None:
            novo_nome = novo_nome.strip()
            if not nome_valido(novo_nome):
                erro_nome()
                return
            aluno["nome"] = novo_nome

        nova_disc = simpledialog.askstring("Editar", "Disciplina:", initialvalue=aluno["disciplina"])
        if nova_disc is not None and nova_disc.strip():
            aluno["disciplina"] = nova_disc.strip()

        nova_nota = simpledialog.askstring("Editar", "Nota (0-20):", initialvalue=str(aluno["nota"]))
        if nova_nota is not None:
            try:
                aluno["nota"] = float(nova_nota)
            except:
                messagebox.showerror("Erro", "Nota inválida.")
                return

        novas_faltas = simpledialog.askstring("Editar", "Faltas (0-40):", initialvalue=str(aluno["faltas"]))
        if novas_faltas is not None:
            try:
                aluno["faltas"] = int(novas_faltas)
            except:
                messagebox.showerror("Erro", "Faltas inválidas.")
                return

        aluno["situacao"] = calcular_situacao(aluno["nota"], aluno["faltas"])
        salvar_turma(self.turma)

        self.filtro = None
        self.atualizar_combos()
        self.atualizar_lista()
        self.atualizar_estatisticas()

    def remover(self):
        """DELETE - confirmação obrigatória para operações destrutivas"""
        nome_sel = self._nome_selecionado()
        if not nome_sel:
            messagebox.showwarning("Aviso", "Selecione um aluno.")
            return

        if not messagebox.askyesno("Confirmar", f"Remover {nome_sel}?"):
            return

        self.turma = [a for a in self.turma if a["nome"] != nome_sel]
        salvar_turma(self.turma)

        self.filtro = None
        self.atualizar_combos()
        self.atualizar_lista()
        self.atualizar_estatisticas()

    def organizar(self):
        """Ordenação alfabética case-insensitive"""
        self.turma.sort(key=lambda a: a["nome"].lower())
        salvar_turma(self.turma)
        self.filtro = None
        self.atualizar_lista()
        self.atualizar_estatisticas()

    def _aba_faltas(self):
        """
        Sistema disciplinar com penalização progressiva:
        Material: acumula → converte em falta → reseta
        Disciplinar: acumula → suspensão permanente
        """
        frame = tk.Frame(self.notebook, bg=bg)
        self.notebook.add(frame, text="🚫 Faltas")

        tk.Label(frame, text="Gestão de Faltas",
                 font=("Arial", 20, "bold"), bg=bg, fg=fg).pack(pady=15)

        box = tk.LabelFrame(frame, text=" Selecionar Aluno ", bg=bg, fg=fg, font=("Arial", 12))
        box.pack(pady=10, padx=20, fill="x")

        self.combo_faltas = ttk.Combobox(box, font=("Arial", 12), state="readonly", width=40)
        self.combo_faltas.pack(pady=10, padx=10)

        # Botões color-coded - amarelo (aviso) vs vermelho (grave)
        botoes = tk.Frame(frame, bg=bg)
        botoes.pack(pady=10)

        tk.Button(botoes, text="➕ Falta Material", command=lambda: self.registrar_falta("material"),
                  bg="#DAA520", fg="white", font=("Arial", 12), width=20, relief="flat", pady=5)\
            .grid(row=0, column=0, padx=8)

        tk.Button(botoes, text="➕ Falta Disciplinar", command=lambda: self.registrar_falta("disciplinar"),
                  bg="#DC143C", fg="white", font=("Arial", 12), width=20, relief="flat", pady=5)\
            .grid(row=0, column=1, padx=8)

        self.text_faltas = tk.Text(frame, width=80, height=14, font=("Arial", 11),
                                   bg=entry_bg, fg=fg)
        self.text_faltas.pack(pady=10, padx=20)

    def registrar_falta(self, tipo):
        """
        Escalada automática de penalizações:
        - Material: 2 faltas → 1 falta presença (reset contador)
        - Disciplinar: 3 faltas → suspensão (flag permanente)
        """
        nome = self.combo_faltas.get()
        if not nome:
            messagebox.showwarning("Aviso", "Selecione um aluno!")
            return

        aluno = next((a for a in self.turma if a["nome"] == nome), None)
        if not aluno:
            return

        if tipo == "material":
            aluno["falta_material"] += 1
            msg = f"{nome} recebeu falta de material ({aluno['falta_material']}/{FALTA_MATERIAL_LIMITE})."

            if aluno["falta_material"] >= FALTA_MATERIAL_LIMITE:
                aluno["faltas"] += 1
                aluno["falta_material"] = 0
                aluno["situacao"] = calcular_situacao(aluno["nota"], aluno["faltas"])
                msg += f"\n⚠️ Convertido em falta de presença. Total: {aluno['faltas']}."

        else:
            aluno["falta_disciplinar"] += 1
            msg = f"{nome} recebeu falta disciplinar ({aluno['falta_disciplinar']}/{FALTA_DISCIPLINAR_LIMITE})."

            if aluno["falta_disciplinar"] >= FALTA_DISCIPLINAR_LIMITE:
                aluno["suspenso"] = True
                msg += "\n🚨 Resultado: aluno suspenso."

        salvar_turma(self.turma)
        self.atualizar_lista()
        self.atualizar_estatisticas()
        self.atualizar_combos()
        self._mostrar_faltas(aluno, msg)

    def _mostrar_faltas(self, aluno, msg):
        """Feedback detalhado - contexto da ação + status completo"""
        self.text_faltas.delete("1.0", tk.END)
        self.text_faltas.insert(tk.END, msg + "\n\n")
        self.text_faltas.insert(tk.END, f"Aluno: {aluno['nome']}\n")
        self.text_faltas.insert(tk.END, f"📚 Material: {aluno['falta_material']}\n")
        self.text_faltas.insert(tk.END, f"⚠️ Disciplinar: {aluno['falta_disciplinar']}\n")
        self.text_faltas.insert(tk.END, f"🚫 Presença: {aluno['faltas']}\n")
        self.text_faltas.insert(tk.END, f"Status: {'⛔ SUSPENSO' if aluno.get('suspenso') else '✅ Regular'}\n")

    def _aba_estatisticas(self):
        # Cria a ABA "Estatísticas" dentro do Notebook (as abas do Tkinter).
        # Essa função só monta o VISUAL da aba (não calcula nada ainda).

        frame = tk.Frame(self.notebook, bg=bg)
        # tk.Frame = uma "caixa" onde colocamos widgets (Label, Button, Text...)
        # Aqui: o frame vai ficar DENTRO do notebook (abas)
        # bg=bg = fundo escuro

        self.notebook.add(frame, text="📊 Estatísticas")
        # Adiciona este frame como uma nova ABA do notebook
        # text="📊 Estatísticas" = nome que aparece na aba

        tk.Label(
            frame,
            text="Estatísticas da Turma",
            font=("Arial", 20, "bold"),
            bg=bg,
            fg=fg
        ).pack(pady=15)
        # tk.Label = texto na tela
        # frame = onde o texto vai aparecer
        # font = fonte, tamanho e negrito
        # bg = fundo do texto (escuro)
        # fg = cor do texto (branco)
        # pack(pady=15) = coloca o texto na tela com espaçamento vertical

        self.text_stats = tk.Text(
            frame,
            width=90,
            height=18,
            font=("Arial", 11),
            bg=entry_bg,
            fg=fg
        )
        # tk.Text = caixa de texto grande (tipo bloco)
        # width=90 = largura em "caracteres"
        # height=18 = altura em "linhas"
        # bg=entry_bg = cor do fundo (cinza escuro)
        # fg=fg = cor do texto (branco)
        #
        # self.text_stats = guardamos isso no "self" porque:
        # depois, noutra função (atualizar_estatisticas),
        # vamos fazer:
        # self.text_stats.delete(...)
        # self.text_stats.insert(...)

        self.text_stats.pack(pady=10, padx=10)
        # Mostra o Text na tela
        # pady = espaço vertical
        # padx = espaço horizontal

        tk.Button(
            frame,
            text="🔄 Atualizar",
            command=self.atualizar_estatisticas,
            bg=btn_bg,
            fg="white",
            font=("Arial", 12),
            width=20,
            relief="flat",
            pady=5
        ).pack(pady=8)
        # tk.Button = cria um botão
        #
        # text="🔄 Atualizar" = nome do botão
        #
        # command=self.atualizar_estatisticas
        # --> quando clicas no botão, ele chama:
        # self.atualizar_estatisticas()
        #
        # relief="flat" = botão moderno sem borda estranha
        # width=20 = largura
        # pady=5 = botão mais alto
        # pack(pady=8) = mostra o botão com espaçamento

    def atualizar_estatisticas(self):
        """Cálculo de métricas em única passagem O(n)"""
        total = len(self.turma)
        aprovados = sum(1 for a in self.turma if a["situacao"] == "Aprovado")
        reprovados = total - aprovados
        suspensos = sum(1 for a in self.turma if a.get("suspenso"))
        media = (sum(float(a["nota"]) for a in self.turma) / total) if total else 0.0

        # Agregação por disciplina
        por_disc = {}
        for a in self.turma:
            por_disc[a["disciplina"]] = por_disc.get(a["disciplina"], 0) + 1

        self.text_stats.delete("1.0", tk.END)
        self.text_stats.insert(tk.END, f"Total de alunos: {total}\n")
        self.text_stats.insert(tk.END, f"Aprovados: {aprovados}\n")
        self.text_stats.insert(tk.END, f"Reprovados: {reprovados}\n")
        self.text_stats.insert(tk.END, f"Suspensos: {suspensos}\n")
        self.text_stats.insert(tk.END, f"Média geral: {media:.2f}\n\n")

        self.text_stats.insert(tk.END, "Alunos por disciplina:\n")
        for disc in sorted(por_disc.keys(), key=str.lower):
            self.text_stats.insert(tk.END, f" - {disc}: {por_disc[disc]}\n")


if __name__ == "__main__":
    root = tk.Tk()
    InovarInterface(root)
    root.mainloop()