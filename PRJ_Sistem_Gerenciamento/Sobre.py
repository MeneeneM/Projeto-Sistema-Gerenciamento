# Sobre.py
import customtkinter as ctk

def abrir_sobre():
    janela = ctk.CTkToplevel()  # Cria uma janela filha
    janela.title("Sobre")
    janela.geometry("600x400")
    
    ctk.CTkLabel(
        janela,
        text="Sistema de Gerenciamento\n© 2025",
        font=("Arial", 16),
        justify="center",
        text_color="darkgray"
    ).pack(expand=True, pady=30)

    ctk.CTkLabel(
        janela,
        text="Aplicativo Desenvolvido por:\n\nJoão Aylton Mariotto\n Matheus Araujo Guedes Silva\n Ryan cardoso\nPedro Henrique da Silva Pereira\nVictor Hugo Bahia Cardoso dos Santos",
        font=("Arial", 14),
        justify="center",
        text_color="gray"
    ).pack(expand=True)
    
    ctk.CTkButton(
        janela,
        text="Fechar",
        command=janela.destroy
    ).pack(pady=10)
    
    janela.mainloop()
