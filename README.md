# 🚣 Problema da Travessia - Lobo, Cabra e Alface

## 📋 Descrição

Este projeto implementa o clássico **Problema da Travessia** usando conceitos de **Teoria da Computação** e **Autômatos Finitos**. O problema consiste em transportar um lobo, uma cabra e um alface de uma margem do rio para a outra, usando um barco que comporta apenas o fazendeiro e mais um item por vez.

### 🎯 Objetivo
Levar todos os elementos (lobo, cabra, alface) da margem esquerda para a margem direita sem que:
- O lobo coma a cabra (quando estão juntos sem o fazendeiro)
- A cabra coma o alface (quando estão juntos sem o fazendeiro)

## 🏗️ Estrutura do Projeto

### Arquivos Principais

- **`travessia.py`** - Classe principal que gerencia o estado do jogo
- **`automato.py`** - Implementação do autômato finito e algoritmos de busca
- **`app.py`** - Interface web interativa usando Streamlit

## 🔧 Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit** - Interface web interativa
- **Dataclasses** - Estruturas de dados imutáveis
- **Collections** - Algoritmos de busca (BFS)
- **SVG** - Geração de diagramas de estados


## 🧮 Representação de Estados

Os estados são codificados como strings de 4 bits **FLCA**, onde:
- **F** = Fazendeiro (0=esquerda, 1=direita)
- **L** = Lobo (0=esquerda, 1=direita)
- **C** = Cabra (0=esquerda, 1=direita)
- **A** = Alface (0=esquerda, 1=direita)

### Exemplos:
- `"0000"` - Estado inicial (todos na esquerda)
- `"1111"` - Estado final (todos na direita)
- `"1010"` - Fazendeiro e cabra na direita, lobo e alface na esquerda

## 🤖 Autômato Finito Determinístico (AFD)

### Definição Formal
**M = ⟨K, Σ, δ, q₀, F⟩**

- **K** - Conjunto de estados seguros + estado-poço ⊥
- **Σ** - Alfabeto de ações {F, FL, FC, FA}
- **δ** - Função de transição
- **q₀** - Estado inicial "0000"
- **F** - Estado de aceitação {"1111"}

## 📊 Funcionalidades da Interface

### Controles Principais
- **🔁 Reiniciar** - Volta ao estado inicial
- **↩️ Desfazer** - Desfaz último movimento
- **💡 Solução Ótima** - Aplica automaticamente a melhor solução
- **Velocidade da Animação** - Controla velocidade das transições

### Visualizações
1. **Estado Atual** - Mostra posição de cada elemento
2. **Diagrama de Estados** - Grafo SVG interativo dos estados seguros
3. **Histórico** - Lista dos últimos movimentos realizados
4. **Definição Formal** - Mostra os componentes do AFD

## 🎨 Características do Diagrama

- **Nó Azul** - Estado atual
- **Nó Verde** - Estado objetivo (1111)
- **Aresta Azul** - Última ação executada
- **Layout em Camadas** - Estados organizados por distância do inicial

## 🧪 Exemplos de Uso

### Solução Clássica
1. `FC` - Leva cabra para direita
2. `F` - Volta sozinho
3. `FL` - Leva lobo para direita
4. `FC` - Volta com cabra
5. `FA` - Leva alface para direita
6. `F` - Volta sozinho
7. `FC` - Leva cabra para direita


## 🔬 Conceitos Teóricos Aplicados

### 1. **Modelagem por Estados**
Cada configuração do problema é um estado único no autômato.

### 2. **Transições Determinísticas** 
Cada ação em um estado leva a exatamente um próximo estado.

### 3. **Estados de Rejeição**
Estados inseguros levam ao estado-poço ⊥.

### 4. **Busca em Grafos**
BFS garante encontrar solução com menor número de passos.


## 🚀 Extensões Possíveis

- Implementar outros algoritmos de busca (DFS, A*)
- Adicionar variações do problema (mais itens, barco maior)
- Implementar autômato não-determinístico (AFN)
- Adicionar análise de complexidade temporal
- Exportar diagramas em outros formatos

## 🎓 Aplicação Educacional

Este projeto é ideal para:
- **Disciplinas de Teoria da Computação**
- **Estudo de Autômatos Finitos**
- **Algoritmos de Busca em Grafos**
- **Modelagem Computacional de Problemas**

## 📚 Bibliografia

- **Sipser, M.** - Introduction to the Theory of Computation
- **Hopcroft, J.** - Introduction to Automata Theory, Languages, and Computation
- Problema clássico de **Alcuin de York** (século VIII)

## 📄 Licença

Este projeto é desenvolvido para fins educacionais.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Adicionar novas funcionalidades
- Melhorar a documentação

---

**Desenvolvido para fins educacionais em Teoria da Computação** 🎓


