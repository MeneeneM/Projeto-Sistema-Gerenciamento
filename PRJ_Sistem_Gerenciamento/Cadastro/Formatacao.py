import customtkinter as ctk
import re
import tkinter.messagebox as mbox

# Funções de formatação

def formatar_telefone(telefone):
    texto = telefone.widget.get()
    texto = re.sub(r'\D', '', texto)
    if len(texto) > 11:
        texto = texto[:11]
    formatado = ""

    if len(texto) >= 2:
        formatado = f"({texto[:2]})"
        if len(texto) >= 7:
            formatado += f" {texto[2:7]}-{texto[7:]}"
        elif len(texto) > 2:
            formatado += f" {texto[2:]}"
    else:
        formatado = texto

    telefone.widget.delete(0, ctk.END)
    telefone.widget.insert(0, formatado)

def formatar_cpf(CPF):
    texto = re.sub(r'\D', '', CPF.widget.get())
    if len(texto) > 11:
        texto = texto[:11]
    formatado = ""

    if len(texto) > 9:
        formatado = f"{texto[:3]}.{texto[3:6]}.{texto[6:9]}-{texto[9:]}"
    elif len(texto) > 6:
        formatado = f"{texto[:3]}.{texto[3:6]}.{texto[6:]}"
    elif len(texto) > 3:
        formatado = f"{texto[:3]}.{texto[3:]}"
    else:
        formatado = texto

    CPF.widget.delete(0, ctk.END)
    CPF.widget.insert(0, formatado)

def formatar_cep(CEP):
    texto = re.sub(r'\D', '', CEP.widget.get())
    if len(texto) > 8:
        texto = texto[:8]
    formatado = ""

    if len(texto) > 5:
        formatado = f"{texto[:5]}-{texto[5:]}"
    else:
        formatado = texto

    CEP.widget.delete(0, ctk.END)
    CEP.widget.insert(0, formatado)

def formatar_data(data):
    texto = re.sub(r'\D', '', data.widget.get())
    if len(texto) > 8:
        texto = texto[:8]
    formatado = ""

    if len(texto) >= 4:
        formatado = f"{texto[:2]}/{texto[2:4]}"
        if len(texto) > 4:
            formatado += f"/{texto[4:]}"
    elif len(texto) > 2:
        formatado = f"{texto[:2]}/{texto[2:]}"
    else:
        formatado = texto

    data.widget.delete(0, ctk.END)
    data.widget.insert(0, formatado)

def validar_email(Email):
    texto = Email.widget.get()
    texto = texto.replace(" ", "")
    Email.widget.delete(0, ctk.END)
    Email.widget.insert(0, texto)

def senha_valida(senha):
    if len(senha) < 8:
        return False
    tem_maiuscula = tem_minuscula = tem_numero = tem_especial = False
    for c in senha:
        if c.isupper():
            tem_maiuscula = True
        elif c.islower():
            tem_minuscula = True
        elif c.isdigit():
            tem_numero = True
        elif c in "!@#$%&*()-_=+[].,":
            tem_especial = True
    return tem_maiuscula and tem_minuscula and tem_numero and tem_especial
    
def mensagem_senha(senha):
    if senha_valida(senha):
        return "Senha válida."
    else:
        return "Senha inválida. Precisa ter 8+ caracteres, letras maiúsculas e minúsculas, \
                números e caracteres especiais (!@#$%&*()-_=+[].,)."