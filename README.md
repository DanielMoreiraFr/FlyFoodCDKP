# 🛵 FlyFood - Otimização de Rotas de Entrega (CDKP)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-conclu%C3%ADdo-brightgreen.svg)

O **FlyFood** é uma solução em Python desenvolvida para resolver o problema de otimização de rotas de entregas autônomas em uma grade bidimensional (matriz). O objetivo principal é determinar o circuito de menor custo para que um drone parta do restaurante, visite todos os pontos de entrega cadastrados e retorne ao ponto de partida.

---

## 📌 Sobre o Problema

O projeto aborda uma variação do clássico **Problema do Caixeiro Viajante (TSP - *Traveling Salesperson Problem*)**, um problema NP-Difícil (*NP-Hard*).

- **Ponto de Origem ($R$):** Ponto de partida e retorno do drone (Restaurante).
- **Pontos de Entrega ($A, B, C, \dots$):** Locais na matriz onde o drone deve realizar entregas.
- **Métrica de Distância:** Utiliza a **Distância de Manhattan** (Geometria do Táxi), ideal para movimentação em grades ortogonais sem deslocamento diagonal:
  $$d(P_1, P_2) = |x_1 - x_2| + |y_1 - y_2|$$

---

## 🧠 Algoritmo e Complexidade

A solução foi implementada utilizando uma estratégia de **Força Bruta (Busca Exaustiva)**:

1. **Leitura do Mapa (`ler_mapa`):** Faz o *parsing* do arquivo `.txt`, identificando as dimensões da matriz, a coordenada do ponto $R$ e montando um dicionário com os pontos de entrega.
2. **Geração de Permutações:** Utiliza a função `itertools.permutations` para iterar por todas as possíveis sequências de visitação aos clientes.
3. **Cálculo de Custo (`calcular_rota`):** Somatório das distâncias de Manhattan entre os pontos consecutivos da rota, adicionando o retorno final ao ponto $R$.
4. **Seleção da Melhor Rota:** Mantém em memória a rota com menor custo total encontrado.

### Complexidade Computacional

- **Complexidade Temporal:** $\mathcal{O}(N! \cdot N)$, onde $N$ é o número de pontos de entrega. Devido ao crescimento fatorial $N!$, o algoritmo garante o ótimo global, mas possui restrição de escala para números elevados de entregas.
- **Complexidade Espacial:** $\mathcal{O}(N + M)$, onde $N$ é o número de entregas e $M$ as dimensões da matriz.

---

## 📁 Estrutura do Repositório

```text
FlyFoodCDKP/
│
├── flyfood.py           # Módulo principal com a lógica do algoritmo e funções de distância
├── main.py              # Script de execução e medição de tempo de desempenho
├── README.md            # Documentação do projeto
└── matrizes/            # Instâncias de teste em arquivos de texto (.txt)
    ├── matrix.txt       # Matriz 4x5
    ├── matrix2.txt      # Matriz 3x3
    ├── matrix3.txt      # Matriz 5x5
    ├── matrix4.txt      # Matriz 6x4
    ├── matrix5.txt      # Matriz 7x7
    ├── matrix6.txt      # Matriz 10x10
    └── matrix7.txt      # Matriz 12x12
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- Biblioteca `rich` (para formatação visual no terminal)

### Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/DanielMoreiraFr/FlyFoodCDKP.git
   cd FlyFoodCDKP
   ```

2. Instale as dependências necessárias:
   ```bash
   pip install rich
   ```

### Executando

Para rodar o projeto e verificar o resultado de uma matriz:

```bash
python main.py
```

---

## 🖥️ Exemplo de Saída

```text
A melhor rota vai ser: A B C
O custo da rota vai ser: 12
Tempo de execução: 0.000045 segundos
```

---

## 📄 Licença

Este projeto é voltado para fins acadêmicos e educacionais. Sinta-se à vontade para utilizar e modificar o código.