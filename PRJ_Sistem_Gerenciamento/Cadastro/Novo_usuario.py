import json
import Cadastro.Formatacao as Formatacao
import customtkinter as ctk
import re
import tkinter.messagebox as mbox

def janela_cadastro(app):

    janela_cadastro = ctk.CTkToplevel(app)
    janela_cadastro.title("Cadastro de Novo Usuário")
    janela_cadastro.geometry("1050x600")
    janela_cadastro.grab_set()

    # Função salvar Json
    def salvar_json(dados):
        caminho = "Cadastro_Usuario.json"

        with open(caminho, "r", encoding="utf-8") as arquivo:
            usuarios = json.load(arquivo)

        if usuarios:
            ultimo_id = max(int(u.get("id", 0)) for u in usuarios)
            novo_id = ultimo_id + 1
        else:
            novo_id = 1

        dados["id"] = novo_id
        usuarios.append(dados)

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

    # Função Validar e salvar 
    def salvar_dados():
        nome = campo_Nome.get()
        usuario = campo_novo_usuario.get()
        email = campo_email.get()
        telefone = campo_telefone.get()
        nascimento = campo_dtNascimento.get()
        cpf = campo_CPF.get()
        cep = campo_CEP.get()
        senha = campo_nova_senha.get()
        confirmar = campo_confirmar_senha.get()
        cargo = combo_cargo.get()

        # Verificações básicas
        if not nome or not usuario or not email or not senha or not cargo:
            mbox.showwarning("Atenção", "Preencha todos os campos obrigatórios!")
            return

        # E-mail
        padrao_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(padrao_email, email):
            mbox.showerror("Erro", "E-mail inválido!")
            return

        # Telefone
        padrao_telefone = r"^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$"
        if not re.match(padrao_telefone, telefone):
            mbox.showerror("Erro", "Telefone inválido! Use o formato (XX) XXXXX-XXXX")
            return

        # CPF
        padrao_cpf = r"^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$"
        if not re.match(padrao_cpf, cpf):
            mbox.showerror("Erro", "CPF inválido! Use o formato XXX.XXX.XXX-XX")
            return

        # CEP
        padrao_cep = r"^\d{5}-?\d{3}$"
        if not re.match(padrao_cep, cep):
            mbox.showerror("Erro", "CEP inválido! Use o formato 00000-000")
            return

        # Senhas
        if senha != confirmar:
            mbox.showerror("Erro", "As senhas não coincidem!")
            return
        
        if not Formatacao.senha_valida(senha):
            mbox.showerror("Erro", Formatacao.mensagem_senha(senha))
            return

        # Dados do usuário
        dados_usuario = {
            "nome": nome,
            "usuario": usuario,
            "email": email,
            "telefone": telefone,
            "data_nascimento": nascimento,
            "cpf": cpf,
            "cep": cep,
            "senha": senha,
            "cargo": cargo
        }

        salvar_json(dados_usuario)
        mbox.showinfo("Sucesso", f"Usuário {usuario} cadastrado com sucesso!")
        janela_cadastro.destroy()

    # Layout
    for i in range(4):
        janela_cadastro.columnconfigure(i, weight=1)

    titulo = ctk.CTkLabel(
        janela_cadastro,
        text="Cadastro de Novo Usuário",
        font=("Arial", 22, "bold"),
        text_color="white"
    )
    titulo.grid(row=0, column=0, columnspan=4, pady=(20, 10))

    # Campos
    # Nome
    label_Nome = ctk.CTkLabel(janela_cadastro, text="Nome:", font=("Arial", 16))
    label_Nome.grid(row=1, column=0, sticky="w", padx=20, pady=10)
    campo_Nome = ctk.CTkEntry(janela_cadastro, placeholder_text="Digite o nome completo", width=300, height=35)
    campo_Nome.grid(row=1, column=1, sticky="w", padx=10, pady=10)

    #Novo Usuario
    label_novo_usuario = ctk.CTkLabel(janela_cadastro, text="Usuário:", font=("Arial", 16))
    label_novo_usuario.grid(row=1, column=2, sticky="w", padx=20, pady=10)
    campo_novo_usuario = ctk.CTkEntry(janela_cadastro, placeholder_text="Digite o usuário", width=300, height=35)
    campo_novo_usuario.grid(row=1, column=3, sticky="w", padx=10, pady=10)

    # Email
    label_email = ctk.CTkLabel(janela_cadastro, text="E-mail:", font=("Arial", 16))
    label_email.grid(row=2, column=0, sticky="w", padx=20, pady=10)
    campo_email = ctk.CTkEntry(janela_cadastro, placeholder_text="Digite o e-mail", width=300, height=35)
    campo_email.grid(row=2, column=1, sticky="w", padx=10, pady=10)
    campo_email.bind("<KeyRelease>", Formatacao.validar_email)

    # Telefone
    label_telefone = ctk.CTkLabel(janela_cadastro, text="Telefone:", font=("Arial", 16))
    label_telefone.grid(row=2, column=2, sticky="w", padx=20, pady=10)
    campo_telefone = ctk.CTkEntry(janela_cadastro, placeholder_text="(XX) XXXXX-XXXX", width=300, height=35)
    campo_telefone.grid(row=2, column=3, sticky="w", padx=10, pady=10)
    campo_telefone.bind("<KeyRelease>", Formatacao.formatar_telefone)

    # Data de nascimento
    label_dtNascimento = ctk.CTkLabel(janela_cadastro, text="Data de Nascimento:", font=("Arial", 16))
    label_dtNascimento.grid(row=3, column=0, sticky="w", padx=20, pady=10)
    campo_dtNascimento = ctk.CTkEntry(janela_cadastro, placeholder_text="DD/MM/AAAA", width=200, height=35)
    campo_dtNascimento.grid(row=3, column=1, sticky="w", padx=10, pady=10)
    campo_dtNascimento.bind("<KeyRelease>", Formatacao.formatar_data)

    # CPF
    label_CPF = ctk.CTkLabel(janela_cadastro, text="CPF:", font=("Arial", 16))
    label_CPF.grid(row=4, column=0, sticky="w", padx=20, pady=10)
    campo_CPF = ctk.CTkEntry(janela_cadastro, placeholder_text="XXX.XXX.XXX-XX", width=200, height=35)
    campo_CPF.grid(row=4, column=1, sticky="w", padx=10, pady=10)
    campo_CPF.bind("<KeyRelease>", Formatacao.formatar_cpf)

    # CEP
    label_CEP = ctk.CTkLabel(janela_cadastro, text="CEP:", font=("Arial", 16))
    label_CEP.grid(row=5, column=0, sticky="w", padx=20, pady=10)
    campo_CEP = ctk.CTkEntry(janela_cadastro, placeholder_text="00000-000", width=200, height=35)
    campo_CEP.grid(row=5, column=1, sticky="w", padx=10, pady=10)
    campo_CEP.bind("<KeyRelease>", Formatacao.formatar_cep)

    # Cargo (NOVO)
    label_cargo = ctk.CTkLabel(janela_cadastro, text="Cargo:", font=("Arial", 16))
    label_cargo.grid(row=5, column=2, sticky="w", padx=20, pady=10)

    combo_cargo = ctk.CTkComboBox(
        janela_cadastro,
        values=[
            "Gerente",
            "Segurança Administrativo",
            "Estagiário",
            "Secretárias",
            "Pesquisador",
            "Gestão",
            "Operador de T.I."
        ],
        width=300,
        height=35
    )
    combo_cargo.grid(row=5, column=3, sticky="w", padx=10, pady=10)
    combo_cargo.set("Selecione o cargo")

    # Senha
    label_nova_senha = ctk.CTkLabel(janela_cadastro, text="Senha:", font=("Arial", 16))
    label_nova_senha.grid(row=3, column=2, sticky="w", padx=20, pady=10)
    campo_nova_senha = ctk.CTkEntry(janela_cadastro, placeholder_text="Digite a senha", show="*", width=300, height=35)
    campo_nova_senha.grid(row=3, column=3, sticky="w", padx=10, pady=10)

    # Confirmar Senha
    label_confirmar_senha = ctk.CTkLabel(janela_cadastro, text="Confirmar Senha:", font=("Arial", 16))
    label_confirmar_senha.grid(row=4, column=2, sticky="w", padx=20, pady=10)
    campo_confirmar_senha = ctk.CTkEntry(janela_cadastro, placeholder_text="Digite novamente", show="*", width=300, height=35)
    campo_confirmar_senha.grid(row=4, column=3, sticky="w", padx=10, pady=10)

    #Botão Salvar
    botao_salvar = ctk.CTkButton(
        janela_cadastro,
        text="Salvar",
        font=("Arial", 14),
        command=salvar_dados,
        width=150,
        height=35
    )
    botao_salvar.grid(row=6, column=0, columnspan=4, pady=30)

    # Rodapé
    divisor = ctk.CTkLabel(
        janela_cadastro,
        text="──────────  © 2025 Sistema de Gerenciamento  ──────────",
        font=("Arial", 12, "italic"),
        text_color="gray70"
    )
    divisor.grid(row=7, column=0, columnspan=4, pady=(135, 10))
