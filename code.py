class Travessia:
    def __init__(self):
        self.margem_esquerda = {'lobo', 'cabra', 'alface'}
        self.margem_direita = set()
        self.posicao_barco = 'esquerda'

    def exibir_estado(self):
        margem_e_str = ", ".join(sorted(list(self.margem_esquerda))) or "Vazio"
        margem_d_str = ", ".join(sorted(list(self.margem_direita))) or "Vazio"
        
        print("\n" + "="*50)
        if self.posicao_barco == 'esquerda':
            print(f"Margem Esquerda: [ {margem_e_str} ]  <BARCO> ~~~~~~~ Margem Direita: [ {margem_d_str} ]")
        else:
            print(f"Margem Esquerda: [ {margem_e_str} ] ~~~~~~~ <BARCO>  Margem Direita: [ {margem_d_str} ]")
        print("="*50 + "\n")

    def movimento_valido(self, margem_avaliada):
        margem_oposta = self.margem_direita if margem_avaliada is self.margem_esquerda else self.margem_esquerda

        if 'lobo' in margem_oposta and 'cabra' in margem_oposta:
            return False

        if 'cabra' in margem_oposta and 'alface' in margem_oposta:
            return False
        return True

    def mover(self, item):
        origem = self.margem_esquerda if self.posicao_barco == 'esquerda' else self.margem_direita

        if item != 'nenhum' and item not in origem:
            print(f"*** ERRO: '{item}' não está na margem de partida! ***")
            return False

        if item != 'nenhum':
            origem.remove(item)
        
        if self.posicao_barco == 'esquerda':
            self.posicao_barco = 'direita'
        else:
            self.posicao_barco = 'esquerda'
            
        destino = self.margem_esquerda if self.posicao_barco == 'esquerda' else self.margem_direita
        if item != 'nenhum':
            destino.add(item)

        
        if not self.movimento_valido(destino):
            print(f"*** MOVIMENTO INVÁLIDO! Alguém seria comido. Tente novamente. ***")
           
            if item != 'nenhum':
                destino.remove(item)
                origem.add(item)

            if self.posicao_barco == 'esquerda':
                self.posicao_barco = 'direita'
            else:
                self.posicao_barco = 'esquerda'
            return False
            
        return True

    def problema_resolvido(self):
        return len(self.margem_direita) == 3

def jogar():
    jogo = Travessia()
  
    print("--- BEM-VINDO AO PROBLEMA DA TRAVESSIA ---")
    print("Objetivo: Levar o lobo, a cabra e a alface para a outra margem.")
    print("Regras:")
    print("1. O barco só leva um item por vez.")
    print("2. O lobo não pode ficar sozinho com a cabra.")
    print("3. A cabra não pode ficar sozinha com a alface.")
    
    while not jogo.problema_resolvido():
        jogo.exibir_estado()
        
        escolha = input("Quem (ou o que) você quer levar no barco? (lobo, cabra, alface, ou 'nenhum'): ").lower().strip()
        
        if escolha in ['lobo', 'cabra', 'alface', 'nenhum']:
            jogo.mover(escolha)
        else:
            print("*** Escolha inválida. Por favor, digite uma das opções. ***")

    print("\n🎉 PARABÉNS! VOCÊ RESOLVEU O PROBLEMA! 🎉")
    jogo.exibir_estado()

if __name__ == "__main__":
    jogar()
