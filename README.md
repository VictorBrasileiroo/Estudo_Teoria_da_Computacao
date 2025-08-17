# Documentação - Problema da Travessia

## Visão Geral
A classe `Travessia` implementa o clássico problema lógico da travessia do rio, onde um fazendeiro precisa transportar um lobo, uma cabra e alface para o outro lado do rio, respeitando certas restrições.

## Classe Travessia

### Atributos

- **`margem_esquerda`** (`set`): Conjunto contendo os itens presentes na margem esquerda do rio
- **`margem_direita`** (`set`): Conjunto contendo os itens presentes na margem direita do rio  
- **`posicao_barco`** (`str`): String indicando a posição atual do barco ('esquerda' ou 'direita')

### Métodos

#### `__init__(self)`
**Descrição:** Construtor da classe que inicializa o estado inicial do problema.
- Todos os itens começam na margem esquerda
- Margem direita inicia vazia
- Barco começa na margem esquerda

#### `exibir_estado(self)`
**Descrição:** Exibe o estado atual do jogo de forma visual.
- Mostra os itens em cada margem
- Indica a posição do barco
- Formata a saída com separadores visuais

#### `movimento_valido(self, margem_avaliada)`
**Descrição:** Verifica se um movimento resulta em um estado válido do jogo.

**Parâmetros:**
- `margem_avaliada` (`set`): A margem que será avaliada após o movimento

**Retorna:** 
- `bool`: `True` se o movimento é válido, `False` caso contrário

**Regras verificadas:**
- Lobo não pode ficar sozinho com a cabra
- Cabra não pode ficar sozinha com a alface

#### `mover(self, item)`
**Descrição:** Executa o movimento de um item (ou movimento vazio) entre as margens.

**Parâmetros:**
- `item` (`str`): O item a ser movido ('lobo', 'cabra', 'alface', ou 'nenhum')

**Retorna:**
- `bool`: `True` se o movimento foi executado com sucesso, `False` caso contrário

**Processo:**
1. Verifica se o item está na margem de partida
2. Remove o item da origem (se não for 'nenhum')
3. Move o barco para a margem oposta
4. Adiciona o item ao destino (se não for 'nenhum')
5. Valida o movimento resultante
6. Desfaz o movimento se for inválido

#### `problema_resolvido(self)`
**Descrição:** Verifica se o problema foi resolvido.

**Retorna:**
- `bool`: `True` se todos os 3 itens estão na margem direita, `False` caso contrário

## Função Principal

### `jogar()`
**Descrição:** Função principal que gerencia o loop do jogo.

**Funcionalidades:**
- Exibe instruções iniciais
- Controla o loop principal do jogo
- Processa entrada do usuário
- Exibe mensagem de vitória

**Fluxo:**
1. Cria instância da classe Travessia
2. Exibe regras e objetivo
3. Loop até problema ser resolvido:
   - Exibe estado atual
   - Solicita entrada do usuário
   - Processa movimento
4. Exibe mensagem de sucesso

## Regras do Jogo

1. **Capacidade do barco:** Apenas um item por viagem
2. **Restrição lobo-cabra:** O lobo não pode ficar sozinho com a cabra
3. **Restrição cabra-alface:** A cabra não pode ficar sozinha com a alface
4. **Objetivo:** Transportar todos os itens para a margem direita

## Estados Válidos
O jogo verifica automaticamente se um estado é válido após cada movimento, impedindo configurações onde algum item seria "comido" por outro.
