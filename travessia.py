
from dataclasses import dataclass, field

@dataclass
class Travessia:
    margem_esquerda: set = field(default_factory=lambda: {'lobo', 'cabra', 'alface'})
    margem_direita: set = field(default_factory=set)
    posicao_barco: str = 'esquerda'  # 'esquerda' ou 'direita'

   
    def exibir_estado(self):
        margem_e_str = ", ".join(sorted(list(self.margem_esquerda))) or "Vazio"
        margem_d_str = ", ".join(sorted(list(self.margem_direita))) or "Vazio"

        print("\n" + "="*50)
        if self.posicao_barco == 'esquerda':
            print(f"Margem Esquerda: [ {margem_e_str} ]  <BARCO> ~~~~~~~ Margem Direita: [ {margem_d_str} ]")
        else:
            print(f"Margem Esquerda: [ {margem_e_str} ] ~~~~~~~ <BARCO>  Margem Direita: [ {margem_d_str} ]")
        print("="*50 + "\n")

    def movimento_valido(self):
        f_direita = (self.posicao_barco == 'direita')

        esquerda = set(self.margem_esquerda)
        direita = set(self.margem_direita)

        
        def inseguro(conjunto_sem_fazendeiro: set):
            return (('lobo' in conjunto_sem_fazendeiro and 'cabra' in conjunto_sem_fazendeiro) or
                    ('cabra' in conjunto_sem_fazendeiro and 'alface' in conjunto_sem_fazendeiro))

        lado_sem_fazendeiro = direita if f_direita else esquerda
        return not inseguro(lado_sem_fazendeiro)

    def mover_console(self, item: str) -> bool:
        """Versão antiga: entrada textual; mantida por compatibilidade."""
        origem = self.margem_esquerda if self.posicao_barco == 'esquerda' else self.margem_direita

        if item != 'nenhum' and item not in origem:
            print(f"*** ERRO: '{item}' não está na margem de partida! ***")
            return False

        if item != 'nenhum':
            origem.remove(item)


        self.posicao_barco = 'direita' if self.posicao_barco == 'esquerda' else 'esquerda'

        destino = self.margem_esquerda if self.posicao_barco == 'esquerda' else self.margem_direita
        if item != 'nenhum':
            destino.add(item)

        if not self.movimento_valido():
            print(f"*** MOVIMENTO INVÁLIDO! Alguém seria comido. Tente novamente. ***")
         
            if item != 'nenhum':
                destino.remove(item)
                origem.add(item)
            self.posicao_barco = 'direita' if self.posicao_barco == 'esquerda' else 'esquerda'
            return False

        return True

  
    def estado_bits(self) -> str:
        """Codifica como 'F L C A' (0=esq, 1=dir)."""
        def bit(nome: str) -> int:
            return 1 if nome in self.margem_direita else 0
        F = 1 if self.posicao_barco == 'direita' else 0
        L = bit('lobo')
        C = bit('cabra')
        A = bit('alface')
        return f"{F}{L}{C}{A}"

    def reset(self):
        self.margem_esquerda = {'lobo', 'cabra', 'alface'}
        self.margem_direita = set()
        self.posicao_barco = 'esquerda'

    def problema_resolvido(self) -> bool:
        return len(self.margem_direita) == 3

    def mover_por_acao(self, acao: str) -> tuple[bool, str]:
        """
        Ações:
          F  -> fazendeiro atravessa sozinho
          FL -> leva lobo
          FC -> leva cabra
          FA -> leva alface
        Retorna (ok, mensagem).
        """
        if acao not in {"F", "FL", "FC", "FA"}:
            return False, "Ação inválida."

      
        if acao == "FL":
            passageiro = "lobo"
        elif acao == "FC":
            passageiro = "cabra"
        elif acao == "FA":
            passageiro = "alface"

        origem = self.margem_esquerda if self.posicao_barco == 'esquerda' else self.margem_direita
        destino = self.margem_direita if self.posicao_barco == 'esquerda' else self.margem_esquerda

        if passageiro and passageiro not in origem:
            return False, f"'{passageiro}' não está na mesma margem do fazendeiro."

       
        if passageiro:
            origem.remove(passageiro)
        self.posicao_barco = 'direita' if self.posicao_barco == 'esquerda' else 'esquerda'
        if passageiro:
           
            novo_destino = self.margem_direita if self.posicao_barco == 'direita' else self.margem_esquerda
            novo_destino.add(passageiro)

       
        if not self.movimento_valido():
           
            if passageiro:
                novo_destino.remove(passageiro)
                origem.add(passageiro)
            self.posicao_barco = 'direita' if self.posicao_barco == 'esquerda' else 'esquerda'
            return False, "Movimento inválido: alguém seria comido."

        return True, "Movimento realizado."
