import customtkinter as ctk
import tkinter as tk
import json
import os

# Caminho do arquivo de usuários
CAMINHO_USUARIOS = os.path.join("Cadastro_Usuario.json")

def janela_gerenciar(cargo_usuario):
    # Permissão mínima para abrir a janela
    if cargo_usuario not in ["Gerente", "Gestão", "Operador de T.I"]:
        ctk.CTkLabel(text="Acesso negado").pack()
        return

    janela = ctk.CTkToplevel()
    janela.title("Usuários Cadastrados")
    janela.geometry("800x450")

    ctk.set_appearance_mode("dark")

    # garante arquivo
    if not os.path.exists(CAMINHO_USUARIOS):
        with open(CAMINHO_USUARIOS, "w", encoding="utf-8") as f:
            json.dump([], f)

    def carregar_usuarios():
        with open(CAMINHO_USUARIOS, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    # Frame container
    frame_container = ctk.CTkFrame(janela)
    frame_container.pack(fill="both", expand=True, padx=10, pady=10)

    # usamos tk.Canvas para create_window estável
    canvas = tk.Canvas(frame_container, bg="#2b2b2b", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(frame_container, orientation="vertical", command=lambda *args: canvas.yview(*args))
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    frame_lista = ctk.CTkFrame(canvas)
    frame_lista_id = canvas.create_window((0, 0), window=frame_lista, anchor="nw")

    # atualiza scrollregion quando conteúdo muda
    def atualizar_scroll(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
    frame_lista.bind("<Configure>", atualizar_scroll)

    # ajusta largura do frame interno com o canvas
    def ajustar_largura(event):
        canvas.itemconfigure(frame_lista_id, width=event.width)
    canvas.bind("<Configure>", ajustar_largura)

    # monta tabela
    def atualizar_tabela():
        for w in frame_lista.winfo_children():
            w.destroy()

        usuarios = carregar_usuarios()

        if not usuarios:
            vazio = ctk.CTkLabel(frame_lista, text="Nenhum usuário cadastrado.", text_color="gray")
            vazio.pack(pady=20)
            frame_lista.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            return

        # cabeçalhos
        cabecalhos = ["Usuário", "Nome", "Cargo"]
        for i, cab in enumerate(cabecalhos):
            lbl = ctk.CTkLabel(frame_lista, text=cab, font=("Arial", 14, "bold"), text_color="lightblue")
            lbl.grid(row=0, column=i, padx=10, pady=5, sticky="w")

        # linhas
        for i, usuario in enumerate(usuarios, start=1):
            ctk.CTkLabel(frame_lista, text=usuario.get("usuario", ""), font=("Arial", 13)).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(frame_lista, text=usuario.get("nome", ""), font=("Arial", 13)).grid(row=i, column=1, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(frame_lista, text=usuario.get("cargo", ""), font=("Arial", 13)).grid(row=i, column=2, padx=10, pady=5, sticky="w")

        frame_lista.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    # botões
    frame_botoes = ctk.CTkFrame(janela)
    frame_botoes.pack(fill="x", pady=5)

    ctk.CTkButton(frame_botoes, text="Atualizar Lista", width=150, command=atualizar_tabela).pack(side="left", padx=20)

    # inicializa
    atualizar_tabela()
