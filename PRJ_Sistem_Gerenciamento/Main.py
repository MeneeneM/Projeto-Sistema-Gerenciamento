import customtkinter as ctk
import tkinter as tk
import json
import os
import tkinter.messagebox as mbox
from Cadastro.Novo_usuario import janela_cadastro
from Alterar_Cadastro import janela_gerenciar

# Configurações gerais
ctk.set_appearance_mode("dark")

# Interface principal
app = ctk.CTk()
app.title("Sistema de Gerenciamento - Histórico de Acessos")
app.geometry("1050x600")

ACESSOS = "Acesso.json"

# Funções 
def carregar_acessos():
    if not os.path.exists(ACESSOS):
        with open(ACESSOS, "w", encoding="utf-8") as f:
            json.dump([], f)

    # garante conteúdo inicial
    if os.path.getsize(ACESSOS) == 0:
        with open(ACESSOS, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(ACESSOS, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def atualizar_tabela():
    # limpa conteúdo do frame_tabela
    for widget in frame_tabela.winfo_children():
        widget.destroy()

    acessos = carregar_acessos()

    if not acessos:
        vazio = ctk.CTkLabel(frame_tabela, text="Nenhum acesso registrado ainda.", font=("Arial", 14), text_color="gray")
        vazio.pack(pady=20)
        # atualiza scrollregion
        frame_tabela.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        return

    # Cabeçalhos da tabela
    cabecalhos = ["Usuário", "Nome", "Cargo", "Data e Hora"]
    for i, texto in enumerate(cabecalhos):
        lbl = ctk.CTkLabel(frame_tabela, text=texto, font=("Arial", 16, "bold"), text_color="lightblue")
        lbl.grid(row=0, column=i, padx=20, pady=10, sticky="w")

    # Linhas da tabela
    for linha, acesso in enumerate(acessos, start=1):
        ctk.CTkLabel(frame_tabela, text=acesso.get("usuario", ""), font=("Arial", 14)).grid(row=linha, column=0, sticky="w", padx=20, pady=5)
        ctk.CTkLabel(frame_tabela, text=acesso.get("nome", ""), font=("Arial", 14)).grid(row=linha, column=1, sticky="w", padx=20, pady=5)
        ctk.CTkLabel(frame_tabela, text=acesso.get("cargo", ""), font=("Arial", 14)).grid(row=linha, column=2, sticky="w", padx=20, pady=5)
        ctk.CTkLabel(frame_tabela, text=acesso.get("data_hora", ""), font=("Arial", 14)).grid(row=linha, column=3, sticky="w", padx=20, pady=5)

    # Ajusta e atualiza área de rolagem
    frame_tabela.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def limpar_historico():
    resposta = mbox.askyesno("Confirmação", "Tem certeza que deseja apagar o histórico de acessos?")
    if resposta:
        with open(ACESSOS, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo)
        atualizar_tabela()
        mbox.showinfo("Sucesso", "Histórico apagado com sucesso!")

# Ultimo acesso 
cargo_usuario = ""
if os.path.exists(ACESSOS) and os.path.getsize(ACESSOS) > 0:
    with open(ACESSOS, "r", encoding="utf-8") as arquivo:
        try:
            dados_acesso = json.load(arquivo)
            if isinstance(dados_acesso, list) and len(dados_acesso) > 0:
                ultimo_acesso = dados_acesso[-1]
                cargo_usuario = ultimo_acesso.get("cargo", "")
            elif isinstance(dados_acesso, dict):
                cargo_usuario = dados_acesso.get("cargo", "")
        except json.JSONDecodeError:
            cargo_usuario = ""
else:
    cargo_usuario = ""

def tem_permissao(cargo):
    cargos_permitidos = ["Gerente", "Gestão", "Operador de T.I"]
    return cargo in cargos_permitidos

# Scrollable table
frame_tabela_container = ctk.CTkFrame(app)
frame_tabela_container.pack(pady=10, fill="both", expand=True)

canvas = tk.Canvas(frame_tabela_container, bg="#2b2b2b", highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ctk.CTkScrollbar(frame_tabela_container, orientation="vertical", command=lambda *args: (canvas.yview(*args)))
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

frame_tabela = ctk.CTkFrame(canvas)
frame_tabela_id = canvas.create_window((0, 0), window=frame_tabela, anchor="nw")

def atualizar_scroll(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))
frame_tabela.bind("<Configure>", atualizar_scroll)

def ajustar_largura(event):
    canvas.itemconfigure(frame_tabela_id, width=event.width)
canvas.bind("<Configure>", ajustar_largura)

# Botões
frame_botoes = ctk.CTkFrame(app)
frame_botoes.pack(fill="x", pady=10)

# Atualizar
ctk.CTkButton(
    frame_botoes, 
    text="Atualizar", 
    font=("Arial", 14), 
    width=150, 
    command=atualizar_tabela).pack(side="left", padx=30, pady=10)

# Limpar
ctk.CTkButton(
    frame_botoes, 
    text="Limpar Histórico", 
    font=("Arial", 14), 
    width=150, 
    fg_color="red", 
    hover_color="#a30000", 
    command=limpar_historico).pack(side="left", padx=10, pady=10)

# Permissões: Gerenciar
if tem_permissao(cargo_usuario):
    ctk.CTkButton(
        frame_botoes, 
        text="Cadastrar Usuário", 
        font=("Arial", 14), 
        width=150, 
        command=lambda: janela_cadastro(app)).pack(side="left", padx=10, pady=10)

    ctk.CTkButton(frame_botoes, 
        text="Gerenciar Usuários", 
        font=("Arial", 14), 
        width=200, 
        command=lambda: janela_gerenciar(cargo_usuario)).pack(side="left", padx=10, pady=10)

else:
    aviso = ctk.CTkLabel(
        app, 
        text="Acesso restrito: apenas Gerente, Gestão e Operador de T.I podem cadastrar ou gerenciar usuários.", 
        text_color="red", 
        font=("Arial", 14))
    aviso.pack(pady=10)

# Rodapé
rodape = ctk.CTkLabel(
    app, 
    text="──────────  © 2025 Sistema de Gerenciamento  ──────────", 
    font=("Arial", 12, "italic"), 
    text_color="gray70")
rodape.pack(side="bottom", pady=10)

# Inicializa tabela
atualizar_tabela()
app.mainloop()
