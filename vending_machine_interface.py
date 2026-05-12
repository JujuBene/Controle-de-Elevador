import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import pygame
from vending_machine_logic import VendingMachine

class VendingMachineGUI:
    def __init__(self, root):
        # --- CONFIGURAÇÕES DA JANELA ---
        self.root = root
        self.root.title("Máquina de Doces")
        
        # 1. Definimos o tamanho desejado
        largura = 1100
        altura = 850
        
        # 2. Pegamos a largura e altura do seu monitor
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        
        # 3. Calculamos a posição para o centro
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)
        
        # 4. Aplicamos a geometria centralizada
        # O formato é: "LARGURAxALTURA+X+Y"
        self.root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        
        self.root.configure(bg="#1a1a1a") # Cor de fundo bem escura

        # --- RESTANTE DO SEU CÓDIGO (CARREGANDO SONS, etc) ---
        pygame.mixer.init()
        # ... (continua igual)
        self.root.configure(bg="#1a1a1a") # Cor de fundo bem escura

        # --- CARREGANDO OS SONS ---
        pygame.mixer.init() # Liga o sistema de áudio
        try:
            # Tenta carregar os arquivos de som das pastas
            self.som_venda = pygame.mixer.Sound("sounds/machine_drop.mp3")
            self.som_moeda = pygame.mixer.Sound("sounds/insert_coin.mp3")
            self.som_porta = pygame.mixer.Sound("sounds/coin_return.mp3")
        except:
            # Se não achar os sons, o programa não trava, apenas fica mudo
            self.som_venda = self.som_moeda = self.som_porta = None

        # --- CONECTANDO COM A LÓGICA ---
        self.vm = VendingMachine() # Aqui trazemos as regras do AFD (preços e saldo)
        self.produto_selecionado = None # Guarda qual doce você clicou
        self.botao_selecionado = None # Guarda qual botão deve piscar
        self.piscando = False # Controle para saber se o botão está piscando ou não

        # --- DESENHANDO A ESTRUTURA ---
        # Cria a "caixa" principal da máquina
        self.corpo_maquina = tk.Frame(root, bg="#34495e", bd=12, relief="raised")
        self.corpo_maquina.pack(expand=True, fill="both", padx=20, pady=20)

        # Cria o lado esquerdo (onde ficam os doces)
        self.vitrine = tk.Frame(self.corpo_maquina, bg="#dcdde1", bd=8, relief="sunken")
        self.vitrine.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        # Cria as 3 prateleiras horizontais
        self.prateleiras = []
        for i in range(3):
            p = tk.Frame(self.vitrine, bg="#ecf0f1", bd=2, relief="groove")
            p.pack(fill="both", expand=True, padx=5, pady=5)
            self.prateleiras.append(p)

        # Cria o painel da direita (onde ficam os botões e o dinheiro)
        self.painel_controle = tk.Frame(self.corpo_maquina, bg="#2c3e50", bd=4, relief="groove")
        self.painel_controle.pack(side="right", padx=20, pady=20, fill="y")

        # Display verde (o visor da máquina)
        self.label_display = tk.Label(self.painel_controle, text="INSIRA DINHEIRO",
                                     font=("Courier", 16, "bold"), bg="#021e02", fg="#00ff41",
                                     width=20, height=2, bd=4, relief="sunken")
        self.label_display.pack(pady=15, padx=10)

        # Texto que mostra o saldo em amarelo
        self.label_saldo = tk.Label(self.painel_controle, text="Saldo: R$ 0.00",
                                   font=("Arial", 14, "bold"), bg="#2c3e50", fg="#f1c40f")
        self.label_saldo.pack(pady=5)

        # --- ÁREA DO DINHEIRO ---
        frame_dinheiro = tk.LabelFrame(self.painel_controle, text=" Inserir Nota ", bg="#2c3e50", fg="white")
        frame_dinheiro.pack(pady=10, padx=10)
        for valor in [1, 2, 5]: # Cria os botões de R$1, R$2 e R$5 conforme o PDF
            tk.Button(frame_dinheiro, text=f"R$ {valor}", width=6, bg="#27ae60", fg="white",
                      font=("Arial", 9, "bold"), command=lambda v=valor: self.inserir(v)).pack(side=tk.LEFT, padx=3, pady=5)

        # --- TECLADO DE CÓDIGOS (A1, B2, etc) ---
        frame_selecao = tk.Frame(self.painel_controle, bg="#2c3e50")
        frame_selecao.pack(pady=10)
        codigos = [["A1","A2","A3","A4"], ["B1","B2","B3","B4"], ["C1","C2","C3","C4"]]
        self.botoes_teclado = {}
        for i, linha in enumerate(codigos):
            for j, codigo in enumerate(linha):
                # Cria cada botãozinho do teclado
                btn = tk.Button(frame_selecao, text=codigo, width=4, font=("Arial", 10, "bold"),
                                command=lambda c=codigo: self.selecionar(c))
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.botoes_teclado[codigo] = btn

        # Botão azul de confirmar
        self.botao_confirmar = tk.Button(self.painel_controle, text="CONFIRMAR COMPRA", width=22,
                                        bg="#2980b9", fg="white", font=("Arial", 10, "bold"),
                                        command=self.confirmar)
        self.botao_confirmar.pack(pady=5)

        # Botão vermelho de cancelar
        tk.Button(self.painel_controle, text="CANCELAR / TROCO", width=22, bg="#c0392b",
                  fg="white", font=("Arial", 10, "bold"), command=self.cancelar).pack(pady=5)

        # Espaço vazio para empurrar a porta para o fundo
        self.spacer = tk.Frame(self.painel_controle, bg="#2c3e50")
        self.spacer.pack(expand=True, fill="both")

        # --- COMPARTIMENTO DE SAÍDA ---
        self.compartimento = tk.Frame(self.painel_controle, bg="black", width=220, height=130, bd=4, relief="sunken")
        self.compartimento.pack(side="bottom", pady=20, padx=10)
        self.compartimento.pack_propagate(False) # Impede que a caixa mude de tamanho

        # A porta cinza "PUSH"
        self.porta = tk.Frame(self.compartimento, bg="#7f8c8d", width=180, height=80, 
                              bd=3, relief="raised", highlightbackground="#95a5a6", highlightthickness=2)
        self.porta.place(relx=0.5, rely=0.5, anchor="center")
        self.label_push = tk.Label(self.porta, text="PUSH", bg="#7f8c8d", fg="#2c3e50", font=("Arial", 10, "bold"))
        self.label_push.place(relx=0.5, rely=0.5, anchor="center")

        # Desenha os doces na vitrine
        self.labels_produtos = {}
        self.criar_produtos()
        self.atualizar_produtos_disponiveis()

    def criar_produtos(self):
        """ Carrega as fotos dos doces e coloca nas prateleiras """
        pasta = os.path.join(os.getcwd(), "images")
        imagens = {"A1":"cheetos.png", "A2":"coca_cola.png", "A3":"kitkat.png", "A4":"oreo.png",
                   "B1":"ovinhos.png", "B2":"pringles.png", "B3":"skittles.png", "B4":"snickers.png",
                   "C1":"suco_laranja.png", "C2":"tictac.png", "C3":"torcida.png", "C4":"trident.png"}
        
        self.imagens_guardadas = {}
        idx_prateleira = 0
        coluna = 0
        
        for codigo in sorted(self.vm.produtos.keys()):
            try:
                # Abre a imagem, muda o tamanho e prepara para o Tkinter
                img = Image.open(os.path.join(pasta, imagens[codigo])).resize((100, 100))
                foto = ImageTk.PhotoImage(img)
                self.imagens_guardadas[codigo] = foto
                prod = self.vm.produtos[codigo]
                
                # Cria o quadradinho com foto, preço e estoque
                label = tk.Label(self.prateleiras[idx_prateleira], image=foto, 
                                text=f"{codigo}\nR$ {prod['preco']:.2f}\nEst: {prod['estoque']}",
                                compound="top", bg="#ecf0f1", fg="#2c3e50", 
                                font=("Arial", 9, "bold"), padx=15, pady=5)
                label.pack(side="left", expand=True, padx=10)
                self.labels_produtos[codigo] = label
                
                # Organiza para pular de prateleira após 4 itens
                coluna += 1
                if coluna > 3:
                    coluna = 0
                    idx_prateleira += 1
            except: pass

    def atualizar_produtos_disponiveis(self):
        """ Muda a cor do doce se o dinheiro for suficiente (Ativa as opções) """
        for codigo, label in self.labels_produtos.items():
            prod = self.vm.produtos[codigo]
            label.config(text=f"{codigo}\nR$ {prod['preco']:.2f}\nEst: {prod['estoque']}")
            # Se o saldo for suficiente, o fundo fica cinza escuro (Ativo)
            if self.vm.saldo >= prod['preco'] and prod['estoque'] > 0:
                label.config(bg="#bdc3c7") 
            else:
                label.config(bg="#ecf0f1")

    def inserir(self, valor):
        """ Quando você clica no botão de dinheiro """
        self.vm.inserir_dinheiro(valor) # Avisa a lógica (AFD) que entrou dinheiro
        if self.som_moeda: self.som_moeda.play() # Toca o som de moeda
        self.label_display.config(text=f"CRÉDITO: R$ {self.vm.saldo:.2f}") 
        self.label_saldo.config(text=f"Saldo: R$ {self.vm.saldo:.2f}")
        self.atualizar_produtos_disponiveis() # Checa se algum doce "acendeu"

    def selecionar(self, codigo):
        """ Quando você digita o código do doce """
        if self.vm.produtos[codigo]["estoque"] == 0:
            self.label_display.config(text="ESGOTADO")
            return
        # Reseta o botão anterior se houver
        if self.botao_selecionado: self.botao_selecionado.config(bg="SystemButtonFace")
        self.piscando = False
        self.produto_selecionado = codigo
        self.botao_selecionado = self.botoes_teclado[codigo]
        self.label_display.config(text=f"ITEM: {codigo}")
        self.piscando = True
        self.piscar_led() # Começa a fazer o botão piscar

    def piscar_led(self):
        """ Faz o botão selecionado ficar trocando de cor """
        if not self.piscando or not self.botao_selecionado: return
        cor = "yellow" if self.botao_selecionado.cget("bg") != "yellow" else "SystemButtonFace"
        self.botao_selecionado.config(bg=cor)
        self.root.after(400, self.piscar_led) # Chama essa função de novo após 0.4 segundos

    def confirmar(self):
        """ O botão de compra final """
        if not self.produto_selecionado:
            self.label_display.config(text="SELECIONE ITEM")
            return
        
        codigo = self.produto_selecionado
        saldo_antes = self.vm.saldo
        preco_item = self.vm.produtos[codigo]["preco"]
        
        resultado = self.vm.comprar(codigo) # Pergunta para o AFD se pode comprar

        if resultado == "Saldo insuficiente":
            self.label_display.config(text="SALDO BAIXO")
        elif resultado == "Compra realizada":
            troco = saldo_antes - preco_item
            self.label_display.config(text="PROCESSANDO...")
            if self.som_venda: self.som_venda.play() # Som de queda
            
            self.animar_produto(codigo) # Inicia a animação visual
            self.vm.cancelar() # Zera o saldo na lógica
            self.label_saldo.config(text="Saldo: R$ 0.00")
            
            # Mostra o troco ou apenas que deu certo
            if troco > 0:
                if self.som_porta: self.som_porta.play()
                self.root.after(1200, lambda t=troco: self.label_display.config(text=f"TROCO: R$ {t:.2f}"))
            else:
                self.root.after(1200, lambda: self.label_display.config(text="COMPRA REALIZADA"))
            
            self.atualizar_produtos_disponiveis()
            self.resetar()

    def cancelar(self):
            """ Devolve o dinheiro e zera tudo, voltando ao início após 2 segundos """
            troco = self.vm.cancelar()
            
            if troco > 0:
                # Mostra o valor do troco e toca o som
                self.label_display.config(text=f"TROCO: R$ {troco:.2f}")
                if self.som_porta: self.som_porta.play()
                
                # AGUARDA 2 segundos e limpa o visor para o próximo usuário
                self.root.after(2000, lambda: self.label_display.config(text="INSIRA DINHEIRO"))
            else:
                # Se não tinha dinheiro, apenas cancela e volta rápido
                self.label_display.config(text="CANCELADO")
                self.root.after(1000, lambda: self.label_display.config(text="INSIRA DINHEIRO"))
                
            # Reseta o saldo visual na tela e os itens da vitrine
            self.label_saldo.config(text="Saldo: R$ 0.00")
            self.atualizar_produtos_disponiveis()
            self.resetar()

    def resetar(self):
        """ Limpa as variáveis de seleção """
        self.piscando = False
        if self.botao_selecionado: self.botao_selecionado.config(bg="SystemButtonFace")
        self.produto_selecionado = None

    def retirar_item(self, btn_item):
        """ Quando você clica no doce lá embaixo para pegá-lo """
        btn_item.destroy() # O doce some da mão do usuário
        self.porta.place(relx=0.5, rely=0.5, anchor="center") # A porta "PUSH" volta a aparecer
        self.label_display.config(text="DOCE RETIRADO")
        self.root.after(1500, lambda: self.label_display.config(text="INSIRA DINHEIRO"))

    def animar_produto(self, codigo):
        """ Faz a imagem do doce 'cair' na tela """
        foto = self.imagens_guardadas[codigo]
        label_queda = tk.Label(self.root, image=foto, bg="#ecf0f1", bd=0)
        label_queda.image = foto
        label_queda.place(x=300, y=200) # Posição inicial da queda

        def cair(y_pos):
            if y_pos < 620: # Enquanto não chegou no fundo
                label_queda.place(y=y_pos + 25) # Move 25 pixels para baixo
                self.root.after(30, lambda: cair(y_pos + 25)) # Repete rápido
            else:
                label_queda.destroy() # Apaga o doce que estava "no ar"
                self.porta.place_forget() # Esconde a porta cinza para mostrar o doce dentro
                
                # Cria o botão do doce dentro da bandeja preta
                item_retira = tk.Button(self.compartimento, image=foto, bg="black", bd=0,
                                       activebackground="black")
                item_retira.image = foto
                item_retira.config(command=lambda: self.retirar_item(item_retira))
                item_retira.place(relx=0.5, rely=0.5, anchor="center")

        cair(200)