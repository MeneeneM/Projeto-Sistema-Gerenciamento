import customtkinter as ctk
import json
import os
import tkinter.messagebox as mbox

def janela_historico_acessos(usuario_logado):
    caminho_acessos = "Acesso.json"

    if not os.path.exists(caminho_acessos):
        mbox.showerror("Erro", "Arquivo de acessos não encontrado!")
        return

    with open(caminho_acessos, "r", encoding="utf-8") as arquivo:
        acessos = json.load(arquivo)

    cargo_usuario = usuario_logado.get("cargo", "")
    nome_usuario = usuario_logado.get("nome", "")

    # Gerente vê todos, demais veem apenas os próprios
    if cargo_usuario != "Gerente":
        acessos = [a for a in acessos if a.get("nome") == nome_usuario]

    # Criação da janela
    janela = ctk.CTkToplevel()
    janela.title("Histórico de Acessos")
    janela.geometry("900x450")

    # Frame principal
    frame = ctk.CTkFrame(janela)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    titulo = ctk.CTkLabel(frame, text="Histórico de Acessos", font=("Arial", 20, "bold"))
    titulo.pack(pady=10)

    # Cabeçalhos da "tabela"
    header_frame = ctk.CTkFrame(frame)
    header_frame.pack(fill="x", padx=10)

    headers = ["Usuário", "Nome", "Cargo", "Entrada", "Saída"]
    col_widths = [120, 180, 120, 180, 180]

    for i, h in enumerate(headers):
        label = ctk.CTkLabel(
            header_frame, 
            text=h, 
            font=("Arial", 13, "bold"),
            text_color="white",
            anchor="w",
            width=col_widths[i]
        )
        label.grid(row=0, column=i, padx=5, pady=5, sticky="w")

    # Frame rolável para os registros
    scroll_frame = ctk.CTkScrollableFrame(frame, width=850, height=300)
    scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Exibir registros
    if acessos:
        for acesso in reversed(acessos):
            usuario = acesso.get("usuario", "")
            nome = acesso.get("nome", "")
            cargo = acesso.get("cargo", "")
            entrada = acesso.get("data_hora", "—")
            saida = acesso.get("data_hora_saida", "—")

            linha = ctk.CTkFrame(scroll_frame)
            linha.pack(fill="x", padx=5, pady=2)

            valores = [usuario, nome, cargo, entrada, saida]
            for i, v in enumerate(valores):
                label = ctk.CTkLabel(
                    linha, 
                    text=v, 
                    font=("Arial", 12),
                    anchor="w",
                    width=col_widths[i]
                )
                label.grid(row=0, column=i, padx=5, pady=2, sticky="w")
    else:
        ctk.CTkLabel(scroll_frame, text="Nenhum acesso registrado.", font=("Arial", 13)).pack(pady=10)

    janela.grab_set()
