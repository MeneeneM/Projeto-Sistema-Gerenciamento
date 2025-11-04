import customtkinter as ctk
import json
import os
from Cadastro.Novo_usuario import janela_cadastro
from Alterar_Cadastro import janela_gerenciar
from Cadastro.Historico_Acessos import janela_historico_acessos
from Sobre import abrir_sobre
import datetime

# Configurações gerais
ctk.set_appearance_mode("dark")

# Interface principal
app = ctk.CTk()
app.title("Sistema de Gerenciamento")
app.geometry("900x600")

def desativar_botao_fechar():
    pass

app.protocol("WM_DELETE_WINDOW", desativar_botao_fechar)

# Funções auxiliares
def carregar_ultimo_usuario():
    if os.path.exists("Acesso.json") and os.path.getsize("Acesso.json") > 0:
        with open("Acesso.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            if isinstance(dados, list) and len(dados) > 0:
                return dados[-1]
    return {"usuario": "Desconhecido", "nome": "Usuário", "cargo": ""}

def tem_permissao(cargo):
    cargos_permitidos = ["Gerente", "Gestão", "Operador de T.I"]
    return cargo in cargos_permitidos

# Usuário logado
usuario_logado = carregar_ultimo_usuario()
cargo_usuario = usuario_logado.get("cargo", "")

# Funções do ComboBox
def menu_selecionado(opcao):
    if opcao == "Sobre":
        abrir_sobre()
    elif opcao == "Sair":
        sair_sistema()
        app.destroy()

def registrar_saida(usuario):
    if not os.path.exists("Acesso.json"):
        return

    with open("Acesso.json", "r", encoding="utf-8") as arquivo:
        acessos = json.load(arquivo)

    for acesso in reversed(acessos):
        if acesso.get("usuario") == usuario.get("usuario"):
            acesso["data_hora_saida"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            break

    with open("Acesso.json", "w", encoding="utf-8") as arquivo:
        json.dump(acessos, arquivo, indent=4, ensure_ascii=False)

def sair_sistema():
    registrar_saida(usuario_logado)
    app.destroy()

# Layout principal usando grid
app.grid_rowconfigure(0, weight=0)  # Linha do menu
app.grid_rowconfigure(1, weight=0)  # Saudação
app.grid_rowconfigure(2, weight=0)  # Mensagem de boas-vindas
app.grid_rowconfigure(3, weight=1)  # Espaço expansível
app.grid_rowconfigure(4, weight=0)  # Linha dos botões
app.grid_rowconfigure(5, weight=0)  # Linha do rodapé
app.grid_columnconfigure(0, weight=1)

# ComboBox de funções no topo
menu_funcoes = ctk.CTkOptionMenu(
    app,
    values=["Selecione", "Sobre", "Sair"],
    command=menu_selecionado,
    width=50,
    height=15,
    fg_color="#2b2b2b",
    button_color="#3a3a3a",
    button_hover_color="#505050",
    text_color="white"
)
menu_funcoes.set("Selecione")
menu_funcoes.grid(row=0, column=0, padx=(0,800))

# Saudação central
saudacao = ctk.CTkLabel(
    app,
    text=f"Olá, {usuario_logado.get('nome', 'Usuário')}",
    font=("Arial", 20, "bold"),
    text_color="gray"
)
saudacao.grid(row=1, column=0, pady=(10, 5))

# Mensagem de boas-vindas
mensagem_boas_vindas = ctk.CTkLabel(
    app,
    text="Bem-vindo ao sistema de gerenciamento",
    font=("Arial", 16),
    text_color="darkgray"
)
mensagem_boas_vindas.grid(row=2, column=0, pady=(0, 20))

# Frame de botões
frame_botoes = ctk.CTkFrame(app)
frame_botoes.grid(row=4, column=0, pady=20)

# Botões de ação
if tem_permissao(cargo_usuario):
    ctk.CTkButton(
        frame_botoes,
        text="Cadastrar Usuário",
        font=("Arial", 14),
        width=180,
        height=40,
        command=lambda: janela_cadastro(app)
    ).grid(row=0, column=0, padx=10, pady=10)

    ctk.CTkButton(
        frame_botoes,
        text="Gerenciar Usuários",
        font=("Arial", 14),
        width=180,
        height=40,
        command=lambda: janela_gerenciar(cargo_usuario)
    ).grid(row=0, column=1, padx=10, pady=10)
else:
    aviso = ctk.CTkLabel(
        frame_botoes,
        text="Acesso restrito: apenas Gerente, Gestão e Operador de T.I podem gerenciar usuários.",
        text_color="red",
        font=("Arial", 13)
    )
    aviso.grid(row=1, column=0, columnspan=5, pady=10)

ctk.CTkButton(
    frame_botoes,
    text="Histórico de Acessos",
    font=("Arial", 14),
    width=180,
    height=40,
    command=lambda: janela_historico_acessos(usuario_logado)
).grid(row=0, column=2, padx=10, pady=10)

ctk.CTkButton(
    frame_botoes,
    text="Sair",
    font=("Arial", 14),
    width=180,
    height=40,
    command=sair_sistema
).grid(row=0, column=3, padx=10, pady=10)

# Rodapé
rodape = ctk.CTkLabel(
    app,
    text="──────────  © 2025 Sistema de Gerenciamento  ──────────",
    font=("Arial", 12, "italic"),
    text_color="gray70"
)
rodape.grid(row=5, column=0, pady=10)

app.mainloop()
