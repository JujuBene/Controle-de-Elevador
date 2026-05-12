import tkinter as tk
from vending_machine_interface import VendingMachineGUI

# -------------------------------------------------------------------------
# PONTO DE ENTRADA DO SISTEMA (MAIN)
# -------------------------------------------------------------------------

# 1. Inicialização da instância principal do Tkinter (root)
# Representa a janela principal onde o "mundo" da nossa Vending Machine existirá.
root = tk.Tk()

# 2. Instanciação da Classe de Interface
# Aqui conectamos a lógica do AFD (VendingMachine) com a visualização (GUI).
# O objeto 'app' gerencia todos os estados visuais e transições de áudio.
app = VendingMachineGUI(root)

# 3. Execução do Loop Principal (Mainloop)
# Este método é o que mantém a janela aberta e "escutando" os eventos.
# Na perspectiva de Autômatos, é aqui que a máquina fica no 'Estado de Espera'
# aguardando os símbolos de entrada (cliques nas notas ou teclado).
root.mainloop()