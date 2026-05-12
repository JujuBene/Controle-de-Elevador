import tkinter as tk
from PIL import Image, ImageTk
from elevador_logic import ElevadorAFD

class ElevadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle do Elevador")
        
        # Dimensões do Elevador
        largura = 1000
        altura = 700
        
        # Centraliza
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)
        
        self.root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        
        self.root.configure(bg="#2c3e50")
        # ... restante do seu init (logic, imagens, layout)
        self.root.configure(bg="#2c3e50")

        self.logic = ElevadorAFD()
        
        # --- Configurações Visuais ---
        self.ALTURA_ANDAR = 150
        self.LARGURA_CABINE = 120
        self.ALTURA_CABINE = 130
        self.OFFSET_Y_PREDIO = 50
        self.X_CENTRO_PREDIO = 300

        # Carregar Gato
        try:
            img_original = Image.open("gato.png")
            self.img_gato = ImageTk.PhotoImage(img_original.resize((70, 70), Image.LANCZOS))
        except:
            self.img_gato = None

        self.y_andares = {
            3: self.OFFSET_Y_PREDIO + (0.5 * self.ALTURA_ANDAR),
            2: self.OFFSET_Y_PREDIO + (1.5 * self.ALTURA_ANDAR),
            1: self.OFFSET_Y_PREDIO + (2.5 * self.ALTURA_ANDAR),
            0: self.OFFSET_Y_PREDIO + (3.5 * self.ALTURA_ANDAR)
        }

        self.animando_porta = False
        self.percentual_porta = 1.0

        # Dicionário para guardar as referências dos botões e mudá-los de cor
        self.botoes_painel = {}

        self.criar_layout()
        self.desenhar_cabine_inicial()
        self.atualizar_display()

    def criar_layout(self):
        # --- Lado Esquerdo: Canvas com Cenário Completo ---
        self.canvas = tk.Canvas(self.root, width=600, height=700, bg="#ecf0f1", bd=0, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        x1_poco = self.X_CENTRO_PREDIO - 70
        x2_poco = self.X_CENTRO_PREDIO + 70
        
        # Poço do Elevador
        self.canvas.create_rectangle(x1_poco, self.OFFSET_Y_PREDIO, x2_poco, self.OFFSET_Y_PREDIO + (4*self.ALTURA_ANDAR), 
                                     fill="#95a5a6", outline="#7f8c8d", width=3)

        for andar in range(4):
            y_topo = self.OFFSET_Y_PREDIO + ((3-andar) * self.ALTURA_ANDAR)
            y_base = y_topo + self.ALTURA_ANDAR
            y_centro = self.y_andares[andar]

            # 1. Linhas dos Andares
            self.canvas.create_line(30, y_base, 570, y_base, fill="#bdc3c7", width=1, dash=(5,5))

            # 2. Janelas com Grades
            self.canvas.create_rectangle(50, y_centro-30, 130, y_centro+20, fill="#87ceeb", outline="#2c3e50", width=2)
            self.canvas.create_line(90, y_centro-30, 90, y_centro+20, fill="#2c3e50")
            self.canvas.create_line(50, y_centro-5, 130, y_centro-5, fill="#2c3e50")
            
            # 3. Vasos
            vx = x1_poco - 40
            self.canvas.create_polygon(vx-10, y_base, vx+10, y_base, vx+13, y_base-15, vx-13, y_base-15, fill="#a0522d")
            self.canvas.create_oval(vx-15, y_base-35, vx+15, y_base-10, fill="#228b22", outline="")

            # 4. Texto do Andar
            nome = "TÉRREO" if andar == 0 else f"{andar}º ANDAR"
            self.canvas.create_text(x1_poco - 20, y_centro, text=nome, anchor="e", font=("Arial", 10, "bold"), fill="#2c3e50")

            # 5. Quadros com Detalhes (Lado Direito)
            x1_q, x2_q = x2_poco + 40, x2_poco + 110
            y1_q, y2_q = y_centro - 25, y_centro + 25
            cx_q = (x1_q + x2_q) / 2
            cy_q = (y1_q + y2_q) / 2
            
            if andar == 0:
                self.canvas.create_rectangle(x1_q, y1_q, x2_q, y2_q, fill="white", outline="#d4af37", width=2)
                self.canvas.create_text(cx_q, cy_q, text="CERTIFICADO\nFELINA", font=("Times", 6, "bold"), fill="black")
            elif andar == 1:
                self.canvas.create_rectangle(x1_q, y1_q, x2_q, y2_q, fill="#3498db", outline="#2980b9", width=2)
                self.canvas.create_line(x1_q+5, cy_q+5, cx_q, cy_q-5, x2_q-5, cy_q+5, fill="white", smooth=True, width=2)
            elif andar == 2:
                self.canvas.create_rectangle(x1_q, y1_q, x2_q, y2_q, fill="#2ecc71", outline="#27ae60", width=2)
                self.canvas.create_polygon(x1_q+10, y2_q-5, cx_q, y1_q+5, x2_q-10, y2_q-5, fill="#1e8449", outline="#1e8449")
            elif andar == 3:
                self.canvas.create_rectangle(x1_q, y1_q, x2_q, y2_q, fill="#f1c40f", outline="#f39c12", width=2)
                self.canvas.create_oval(cx_q-12, cy_q-12, cx_q+12, cy_q+12, fill="#e67e22", outline="")

        # --- Painel Direito (Controlos) ---
        self.painel_controle = tk.Frame(self.root, bg="#34495e", width=400, bd=5, relief="raised")
        self.painel_controle.pack(side="right", fill="y", padx=10, pady=10)

        # Visor Principal (Onde as setas ▲▼ aparecerão)
        self.label_display = tk.Label(self.painel_controle, text="ELEVADOR PRONTO",
                                     font=("Courier", 14, "bold"), bg="#021e02", fg="#00ff41",
                                     width=30, height=3, bd=4, relief="sunken", justify="center")
        self.label_display.pack(pady=20, padx=10)
        
        self.create_control_panel_buttons()

    def create_control_panel_buttons(self):
        frame_botoes = tk.LabelFrame(self.painel_controle, text=" Painel Interno ", bg="#34495e", fg="white", font=("Arial", 12, "bold"))
        frame_botoes.pack(pady=30, padx=20)
        
        # Estilo base do botão (desligado)
        self.btn_style_off = {"font": ("Arial", 18, "bold"), "width": 4, "height": 2, "fg": "#333", "bg": "#bdc3c7", "relief": "raised", "bd": 4}
        
        # Criar e guardar os botões no dicionário para acesso fácil
        for r, botoes_linha in enumerate([["3", "2"], ["1", "T"]]):
            for c, texto in enumerate(botoes_linha):
                # Define o valor do andar (T=0)
                andar_val = 0 if texto == "T" else int(texto)
                
                btn = tk.Button(frame_botoes, text=texto, **self.btn_style_off, 
                                command=lambda a=andar_val: self.press_button(a))
                btn.grid(row=r, column=c, padx=15, pady=15)
                
                # Guarda a referência do botão usando o andar como chave
                self.botoes_painel[andar_val] = btn

  
    def desenhar_cabine_em_y(self, y_centro):
        """Desenha a cabine com a estética CLEAN e o risco simples do espelho."""
        # Limpa desenhos anteriores da cabine
        self.canvas.delete("cabine")
        
        # Define as bordas da cabine com base no centro fornecido
        x1, x2 = self.X_CENTRO_PREDIO - (self.LARGURA_CABINE/2), self.X_CENTRO_PREDIO + (self.LARGURA_CABINE/2)
        y1, y2 = y_centro - (self.ALTURA_CABINE/2), y_centro + (self.ALTURA_CABINE/2)

        # 1. Corpo Externo da Cabine
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#7f8c8d", outline="#333", width=2, tags="cabine")
        
        # 2. Luz Interna Amarela (Fixa no teto)
        self.canvas.create_rectangle(x1+20, y1+5, x2-20, y1+15, fill="#f1c40f", outline="", tags="cabine")
        
        # --- 3. ESPELHO (ESTÉTICA CLEAN RESTAURADA) ---
        # Fundo do espelho com o cinza mais claro e suave (#d1ccc0 conforme seu código resgatado)
        espelho_x1, espelho_y1 = x1+10, y1+20
        espelho_x2, espelho_y2 = x2-10, y2-15
        self.canvas.create_rectangle(espelho_x1, espelho_y1, espelho_x2, espelho_y2, 
                                     fill="#d1ccc0", outline="#a5b1c2", width=2, tags="cabine")
        
        # RISCO DE LUZ SIMPLES (A estética que você gosta)
        # Usando a linha branca simples e cheia no canto superior esquerdo
        self.canvas.create_line(espelho_x1+10, espelho_y1+10, espelho_x1+35, espelho_y1+35, 
                                fill="white", width=2, tags="cabine")

        # 4. Gato (Foto à frente do espelho)
        if self.img_gato:
            self.canvas.create_image(self.X_CENTRO_PREDIO, y2 - 40, image=self.img_gato, tags="cabine")

        # 5. Portas Metálicas Deslizantes (Por cima de tudo)
        lp = 60
        desloc = lp * self.percentual_porta
        
        # Porta Esquerda
        self.canvas.create_rectangle(x1, y1, x1+lp-desloc, y2, fill="#bdc3c7", outline="#7f8c8d", tags="cabine")
        # Porta Direita
        self.canvas.create_rectangle(x2-lp+desloc, y1, x2, y2, fill="#bdc3c7", outline="#7f8c8d", tags="cabine")

    def desenhar_cabine_inicial(self):
        self.desenhar_cabine_em_y(self.y_andares[self.logic.andar_atual])

    def atualizar_display(self):
        status = self.logic.obter_status_completo()
        self.label_display.config(text=status)

    def press_button(self, andar):
        if self.logic.movimento != "PARADO" or self.animando_porta: return
        
        # Se clicar no próprio andar, não faz nada
        if andar == self.logic.andar_atual: return

        # --- MELHORIA 3: ILUMINAR BOTÃO ---
        # Muda o fundo do botão para Amarelo Ouro e o alívio para 'sunken' (pressionado)
        if andar in self.botoes_painel:
            self.botoes_painel[andar].config(bg="#f1c40f", relief="sunken")

        # Processa a requisição na lógica
        acao = self.logic.processar_requisicao(andar)
        
        # Atualiza o visor (agora com ▲▼ se houver movimento)
        self.atualizar_display()
        
        if acao == "FECHANDO_PORTA": self.animar_porta_comando("FECHAR")
        elif acao == "INICIAR_MOVIMENTO":
            self.logic.definir_direcao()
            self.atualizar_display() # Atualiza para mostrar a seta antes de mover
            self.mover_cabine_ciclo()

    def animar_porta_comando(self, acao):
        self.animando_porta = True
        velocidade = 0.05
        if acao == "FECHAR":
            if self.percentual_porta > 0:
                self.percentual_porta -= velocidade
                self.logic.estado_porta = "FECHANDO"
                self.desenhar_cabine_em_y(self.y_andares[self.logic.andar_atual])
                self.atualizar_display()
                self.root.after(50, lambda: self.animar_porta_comando("FECHAR"))
            else:
                self.percentual_porta = 0
                self.logic.estado_porta = "FECHADA"
                self.animando_porta = False
                if self.logic.andar_destino is not None:
                    self.logic.definir_direcao()
                    self.atualizar_display()
                    self.mover_cabine_ciclo()
        else: # ABRIR
            if self.percentual_porta < 1.0:
                self.percentual_porta += velocidade
                self.logic.estado_porta = "ABRINDO"
                self.desenhar_cabine_em_y(self.y_andares[self.logic.andar_atual])
                self.atualizar_display()
                self.root.after(50, lambda: self.animar_porta_comando("ABRIR"))
            else:
                self.percentual_porta = 1.0
                self.logic.estado_porta = "ABERTA"
                self.animando_porta = False
                self.atualizar_display()

    def mover_cabine_ciclo(self):
        if self.logic.movimento == "PARADO": return
        y_origem = self.y_andares[self.logic.andar_atual]
        prox = self.logic.andar_atual + (1 if self.logic.movimento == "SUBINDO" else -1)
        y_destino = self.y_andares[prox]
        self.animar_deslocamento_suave(y_origem, y_destino)

    def animar_deslocamento_suave(self, y_start, y_end):
        passos = 40
        self.current_step = 0
        dy = (y_end - y_start) / passos
        def frame():
            if self.current_step <= passos:
                self.desenhar_cabine_em_y(y_start + (dy * self.current_step))
                self.current_step += 1
                self.root.after(25, frame)
            else:
                chegou = self.logic.chegou_no_andar()
                self.desenhar_cabine_em_y(self.y_andares[self.logic.andar_atual])
                self.atualizar_display() # Atualiza visor (pode remover a seta se parou)
                
                if chegou:
                    # --- MELHORIA 3: DESLIGAR BOTÃO ---
                    # Quando chega no destino, volta o botão à cor original
                    andar_chegada = self.logic.andar_atual
                    if andar_chegada in self.botoes_painel:
                        # Restaura o estilo original usando o dicionário guardado no __init__
                        self.botoes_painel[andar_chegada].config(**self.btn_style_off)
                    
                    self.root.after(500, lambda: self.animar_porta_comando("ABRIR"))
                else: 
                    self.mover_cabine_ciclo()
        frame()