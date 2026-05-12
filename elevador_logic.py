# elevador_logic.py

class ElevadorAFD:
    def __init__(self):
        # ==========================================
        # ESTADOS INICIAIS DO AFD
        # ==========================================
        
        # Estado de Posição: 0 (Térreo), 1, 2, 3
        self.andar_atual = 0 
        
        # Estado da Porta: "FECHADA" ou "ABERTA"
        self.estado_porta = "ABERTA" # Inicia parado no térreo com porta aberta (Exemplo do PDF)
        
        # Estado de Movimento: "PARADO", "SUBINDO", "DESCENDO"
        self.movimento = "PARADO"
        
        self.andar_destino = None

    def processar_requisicao(self, andar_solicitado):
        """
        Função de Transição de Entrada (δ).
        Recebe o símbolo de entrada (botão pressionado) e define o próximo passo.
        """
        # Se já estamos no andar, não faz nada (talvez reabra a porta se estivesse fechando)
        if andar_solicitado == self.andar_atual:
            self.andar_destino = None
            return "Já está no andar"

        # Define o destino final
        self.andar_destino = andar_solicitado
        
        # Regra do AFD: Se vai se mover, o primeiro passo é fechar a porta.
        if self.estado_porta == "ABERTA":
            return "FECHANDO_PORTA"
        else:
            return "INICIAR_MOVIMENTO"

    def definir_direcao(self):
        """Define se sobe ou desce baseado no destino"""
        if self.andar_destino is None: return

        if self.andar_destino > self.andar_atual:
            self.movimento = "SUBINDO"
        elif self.andar_destino < self.andar_atual:
            self.movimento = "DESCENDO"

    def chegou_no_andar(self):
        """Atualiza estado ao chegar em um andar físico"""
        if self.movimento == "SUBINDO":
            self.andar_atual += 1
        elif self.movimento == "DESCENDO":
            self.andar_atual -= 1
            
        # Verifica se chegou ao destino final
        if self.andar_atual == self.andar_destino:
            self.movimento = "PARADO"
            self.andar_destino = None
            return True # Chegou no destino
        
        return False # Apenas passando pelo andar (requisito linear)

    def obter_status_completo(self):
        """Retorna o estado atual em MAIÚSCULAS com quebra de linha e setas"""
        desc_andar = "TÉRREO" if self.andar_atual == 0 else f"{self.andar_atual}º ANDAR"
        
        # Define a seta baseada no movimento atual
        seta = ""
        if self.movimento == "SUBINDO":
            seta = " ▲" # Seta para cima
        elif self.movimento == "DESCENDO":
            seta = " ▼" # Seta para baixo
            
        # Monta a string com a seta ao lado do andar
        status = f"ESTADO: {desc_andar}{seta}\nPORTA: {self.estado_porta.upper()}"
        return status