class VendingMachine:

    def __init__(self):
        # ==========================================
        # ESTADO INICIAL DO AFD (q0)
        # ==========================================
        # O estado é definido pelo saldo acumulado. 
        # S0: saldo = 0 (Ponto de partida)
        self.saldo = 0.0

        # ==========================================
        # CONFIGURAÇÃO DOS PRODUTOS (ESTADOS DE ACEITAÇÃO)
        # ==========================================
        # Retornando aos valores variados que você definiu:
        self.produtos = {
            "A1": {"preco": 7.50, "estoque": 5},
            "A2": {"preco": 6.00, "estoque": 5},
            "A3": {"preco": 5.50, "estoque": 5},
            "A4": {"preco": 4.00, "estoque": 5},
            "B1": {"preco": 3.50, "estoque": 5},
            "B2": {"preco": 8.00, "estoque": 5},
            "B3": {"preco": 5.00, "estoque": 5},
            "B4": {"preco": 6.50, "estoque": 5},
            "C1": {"preco": 4.50, "estoque": 5},
            "C2": {"preco": 3.00, "estoque": 5},
            "C3": {"preco": 2.50, "estoque": 5},
            "C4": {"preco": 2.00, "estoque": 5},
        }

    def inserir_dinheiro(self, valor):
        # ==========================================
        # FUNÇÃO DE TRANSIÇÃO (δ)
        # ==========================================
        # Quando o usuário insere uma nota (1, 2 ou 5),
        # a máquina muda para um novo estado de saldo.
        self.saldo += valor

    def comprar(self, codigo):
        # ==========================================
        # VERIFICAÇÃO DE ESTADO FINAL
        # ==========================================
        # Se o código não existir na nossa lista:
        if codigo not in self.produtos:
            return "Produto inválido"

        produto = self.produtos[codigo]

        # Se o estoque acabou:
        if produto["estoque"] <= 0:
            return "Sem estoque"

        # Verificando se o saldo atingiu a "Condição de Aceitação":
        if self.saldo < produto["preco"]:
            return "Saldo insuficiente"

        # Transição de Saída: O produto é liberado.
        self.saldo -= produto["preco"]
        produto["estoque"] -= 1

        return "Compra realizada"

    def cancelar(self):
        # ==========================================
        # TRANSIÇÃO DE RESET
        # ==========================================
        # Zera o saldo e retorna ao estado inicial (S0).
        troco = self.saldo
        self.saldo = 0
        return troco