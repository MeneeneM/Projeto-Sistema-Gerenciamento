from Cadastro.Novo_usuario import janela_cadastro
import customtkinter as ctk
import json
import os
import tkinter.messagebox as mbox
import subprocess

# Configuração - aparência
ctk.set_appearance_mode("dark")

# Criação da janela principal
app = ctk.CTk()
app.title("Sistema de Gerenciamento")
app.geometry("900x600")

# Função para verificar Login
def verificar_login():
    usuario = campo_usuario.get()
    senha = campo_senha.get()

    if not usuario or not senha:
        mbox.showwarning("Atenção", "Preencha usuário e senha!")
        return

    caminho_usuarios = "Cadastro_Usuario.json"
    caminho_acessos = "Acesso.json"

    if not os.path.exists(caminho_usuarios):
        mbox.showerror("Erro", "Arquivo de usuários não encontrado!")
        return

    # Carrega usuários
    with open(caminho_usuarios, "r", encoding="utf-8") as f:
        usuarios = json.load(f)

    for u in usuarios:
        if u["usuario"] == usuario and u["senha"] == senha:
            mbox.showinfo("Sucesso", f"Bem-vindo, {u['nome']}!")

            from datetime import datetime
            hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            with open(caminho_acessos, "r", encoding="utf-8") as arq:
                acessos = json.load(arq)

            registro = {
                "usuario": u["usuario"],
                "nome": u["nome"],
                "cargo": u.get("cargo", "Não informado"),
                "data_hora": hora_atual
            }

            acessos.append(registro)

            with open(caminho_acessos, "w", encoding="utf-8") as arq:
                json.dump(acessos, arq, indent=4, ensure_ascii=False)

            # Fecha o login e abre a tela principal
            app.destroy()
            from Main import abrir_main
            abrir_main(u)
            return

    mbox.showerror("Erro", "Usuário ou senha incorretos!")

# Label - Bem-vindo
bem_vindo = ctk.CTkLabel(app, text="Bem - Vindo !", font=("Arial", 36))
bem_vindo.pack(pady=10, anchor="center")

bem_vindo2 = ctk.CTkLabel(app, text="Digite o Usuário e a Senha para acessar o sistema !", font=("Arial", 14), text_color="gray")
bem_vindo2.pack(pady=10, anchor="center")

# Campo Usuário
label_usuario = ctk.CTkLabel(app, text="Usuário:", font=("Arial", 16))
label_usuario.pack(pady=1, padx=100, anchor="w")

campo_usuario = ctk.CTkEntry(app, placeholder_text="Digite seu usuário", width=300, height=35)
campo_usuario.pack(pady=1, padx=100, anchor="w")

# Campo Senha
label_senha = ctk.CTkLabel(app, text="Senha:", font=("Arial", 16))
label_senha.pack(pady=20, padx=100, anchor="w")

campo_senha = ctk.CTkEntry(app, placeholder_text="Digite sua senha", show="*", width=300, height=35)
campo_senha.pack(pady=1, padx=100, anchor="w")

# Botão Login
botao_login = ctk.CTkButton(app, text="Login", font=("Arial", 14), command=verificar_login)
botao_login.pack(pady=20, padx=100, anchor="w")

# Rodapé
divisor = ctk.CTkLabel(
    app,
    text="──────────  © 2025 Sistema de Gerenciamento  ──────────",
    font=("Arial", 12, "italic"),
    text_color="gray70"
)
divisor.pack(side="bottom", pady=10)

# Iniciar app
app.mainloop()