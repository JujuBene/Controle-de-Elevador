import tkinter as tk
from elevador_gui import ElevadorGUI  # Importa a interface do elevador
# from maquina_doces_gui import MaquinaDocesGUI # Importe a sua máquina de doces aqui quando estiver pronta
from vending_machine_interface import VendingMachineGUI

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Trabalho de Autômatos - Menu")
        
        # Define o tamanho da janela
        largura = 500
        altura = 450
        
        # Chama a função de centralizar
        self.centralizar_janela(self.root, largura, altura)
        
        self.root.configure(bg="#2c3e50")
        self.criar_widgets()

    def centralizar_janela(self, janela, largura, altura):
        # Obtém as dimensões da tela do seu monitor
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()

        # Calcula a posição X e Y para o centro
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)

        # Define a geometria: "Largura x Altura + X + Y"
        janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    def criar_widgets(self):
        label_titulo = tk.Label(
            self.root, 
            text="Selecione o Sistema", 
            font=("Verdana", 22, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
            pady=20 
        )
        label_titulo.pack()

        self.frame_botoes = tk.Frame(self.root, bg="#2c3e50")
        self.frame_botoes.pack(expand=True, pady=0) 

        estilo_botoes = {
            "font": ("Verdana", 12, "bold"),
            "width": 25,
            "height": 2,
            "bd": 6,             
            "relief": "raised",  
            "cursor": "hand2"
        }

        # Botão Máquina de Doces
        self.btn_doces = tk.Button(
            self.frame_botoes, 
            text="MÁQUINA DE DOCES", 
            bg="#27ae60", 
            fg="white",
            activebackground="#2ecc71",
            activeforeground="white",
            command=self.abrir_doces, # Chama a função que abre o case
            **estilo_botoes
        )
        self.btn_doces.pack(pady=10)

        # Botão Controle de Elevador
        self.btn_elevador = tk.Button(
            self.frame_botoes, 
            text="CONTROLE DE ELEVADOR", 
            bg="#2980b9", 
            fg="white",
            activebackground="#3498db",
            activeforeground="white",
            command=self.abrir_elevador, # Chama a função que abre o elevador
            **estilo_botoes
        )
        self.btn_elevador.pack(pady=10)

        # Eventos de Hover
        self.btn_doces.bind("<Enter>", lambda e: self.btn_doces.config(bg="#2ecc71"))
        self.btn_doces.bind("<Leave>", lambda e: self.btn_doces.config(bg="#27ae60"))
        self.btn_elevador.bind("<Enter>", lambda e: self.btn_elevador.config(bg="#3498db"))
        self.btn_elevador.bind("<Leave>", lambda e: self.btn_elevador.config(bg="#2980b9"))

    def abrir_doces(self):
        # Cria uma nova janela (Toplevel) para não fechar o menu
        janela_vendingmachine = tk.Toplevel(self.root)
        # MaquinaDocesGUI(nova_janela) # Ative quando o arquivo estiver pronto
        VendingMachineGUI(janela_vendingmachine) # Inicia a interface que fizemos antes
        print("Interface da Máquina de Doces iniciada.")

    def abrir_elevador(self):
        # Toplevel cria uma janela independente da principal
        janela_elevador = tk.Toplevel(self.root)
        ElevadorGUI(janela_elevador) # Inicia a interface que fizemos antes
        print("Interface do Elevador iniciada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()