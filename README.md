# 🛵 FlyFood - Otimização de Rotas de Entrega (CDKP)

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-conclu%C3%ADdo-brightgreen.svg)

O **FlyFood** é uma solução em Python desenvolvida para resolver o problema de otimização de rotas de entregas autônomas em uma grade bidimensional (matriz). O objetivo principal é determinar o circuito de menor custo para que um drone parta do restaurante, visite todos os pontos de entrega cadastrados e retorne ao ponto de partida.

O projeto tem duas entregas:

| Entrega | Técnica | Pasta | Script |
|---|---|---|---|
| 1ª | Força Bruta (busca exaustiva) | `va1/` | `main-1va.py` |
| 2ª | Algoritmo Genético (A.G.) | `va2/` | `main-2va.py` |

---

## 📌 Sobre o Problema

O projeto aborda uma variação do clássico **Problema do Caixeiro Viajante (TSP - *Traveling Salesperson Problem*)**, um problema NP-Difícil (*NP-Hard*).

- **Ponto de Origem ($R$):** Ponto de partida e retorno do drone (Restaurante).
- **Pontos de Entrega ($A, B, C, \dots$):** Locais na matriz onde o drone deve realizar entregas.
- **Métrica de Distância:** Utiliza a **Distância de Manhattan** (Geometria do Táxi), ideal para movimentação em grades ortogonais sem deslocamento diagonal:
  $$d(P_1, P_2) = |x_1 - x_2| + |y_1 - y_2|$$

---

## 🧠 1ª Entrega: Força Bruta

A solução foi implementada utilizando uma estratégia de **Força Bruta (Busca Exaustiva)**:

1. **Leitura do Mapa (`ler_mapa`):** Faz o *parsing* do arquivo `.txt`, identificando as dimensões da matriz, a coordenada do ponto $R$ e montando um dicionário com os pontos de entrega.
2. **Geração de Permutações:** Utiliza a função `itertools.permutations` para iterar por todas as possíveis sequências de visitação aos clientes.
3. **Cálculo de Custo (`calcular_rota`):** Somatório das distâncias de Manhattan entre os pontos consecutivos da rota, adicionando o retorno final ao ponto $R$.
4. **Seleção da Melhor Rota:** Mantém em memória a rota com menor custo total encontrado.

### Complexidade Computacional

- **Complexidade Temporal:** $\mathcal{O}(N! \cdot N)$, onde $N$ é o número de pontos de entrega. Devido ao crescimento fatorial $N!$, o algoritmo garante o ótimo global, mas possui restrição de escala para números elevados de entregas.
- **Complexidade Espacial:** $\mathcal{O}(N + M)$, onde $N$ é o número de entregas e $M$ as dimensões da matriz.

---

## 🧬 2ª Entrega: Algoritmo Genético

A força bruta deixa de funcionar quando $N$ cresce: com 10 entregas são 3.628.800 rotas, com 12 são 479.001.600. Para a instância **brasil58** (TSPLIB, 58 cidades, ótimo conhecido de **25395**) seriam $57! \approx 4 \times 10^{76}$ rotas. Mesmo avaliando 1 bilhão de rotas por segundo, a busca levaria cerca de $10^{60}$ anos.

A 2ª entrega resolve o mesmo problema com um **Algoritmo Genético (A.G.)**, que explora o espaço de rotas por seleção, cruzamento e mutação. O A.G. não garante o ótimo, mas encontra rotas muito boas em segundos.

### Metas da entrega

- Calcular a função de aptidão usando a matriz de distâncias.
- Implementar operadores de cruzamento e mutação.
- Implementar a seleção de pais e a seleção de sobreviventes.
- Converter a matriz do FlyFood para o formato de matriz de distâncias usado no brasil58.
- Rodar o A.G. no FlyFood e comparar com a força bruta.
- Rodar o A.G. no brasil58 e comparar com o ótimo conhecido (25395).

### Componentes do A.G.

| Etapa | Implementação | Arquivo |
|---|---|---|
| Representação | Permutação das entregas. O nó 0 (R no mapa, cidade 1 no `.tsp`) fica fixo como origem | `ag.py` |
| Aptidão | Custo do ciclo completo, com retorno à origem. Quanto menor, melhor | `populacao.py` |
| Seleção de pais | Torneio com K=2: sorteia 2 indivíduos e vence o de menor custo | `selecao.py` |
| Cruzamento | Order Crossover (OX): gera 2 filhos válidos a partir de 2 pais | `cruzamento.py` |
| Mutação | **Insert** (obrigatória) e **inversão**, sorteadas com 50% cada. O `mutacao_swap` está implementado, mas fora da lista `OPERADORES` | `mutacao.py` |
| Seleção de sobreviventes | Steady-state: população anterior e filhos competem juntos e ficam os de menor custo, sem indivíduos repetidos | `selecao.py` |
| Reinício por estagnação | Se a população passa `paciencia` gerações sem melhorar, ela é recriada do zero. O melhor indivíduo já encontrado é guardado | `ag.py` |
| Leitura da instância | Mapa `.txt` do FlyFood (convertido para matriz de distâncias) ou `.tsp` da TSPLIB (formato `UPPER_ROW`) | `instancia.py` |
| Gráfico em tempo real | Janela opcional com o progresso da execução | `grafico.py` |

A cada geração, o A.G. executa:

1. Seleciona 2 pais por torneio.
2. Cruza os pais com OX e gera 2 filhos.
3. Aplica a mutação em cada filho, com probabilidade `taxa_mutacao`.
4. Calcula o custo dos filhos.
5. Junta população e filhos e mantém os de menor custo (steady-state).
6. Reinicia a população se ela estagnou.

O reinício foi incluído porque, nos testes, a população converge para um ótimo local entre as gerações 2000 e 3000 e as gerações seguintes não melhoram o resultado. Com vários reinícios, a mesma execução tenta chegar ao ótimo várias vezes.

### Parâmetros

Os parâmetros ficam no topo do `main-2va.py`:

```python
PARAMS_MAPA = dict(tam_pop=200, geracoes=10000, taxa_mutacao=0.3, log_a_cada=500)
PARAMS_TSP = dict(tam_pop=100, geracoes=10000, taxa_mutacao=0.4, paciencia=500, log_a_cada=250)
```

| Parâmetro | O que faz |
|---|---|
| `tam_pop` | Tamanho da população |
| `geracoes` | Número de gerações |
| `taxa_mutacao` | Probabilidade de mutação de cada filho (0 a 1) |
| `paciencia` | Gerações sem melhora até reiniciar a população (0 = nunca reinicia) |
| `log_a_cada` | De N em N gerações imprime o progresso e atualiza o gráfico (0 = desligado) |
| `semente` | Fixa o `random` para repetir uma execução (opcional) |

### Gráfico em tempo real

Com `MOSTRAR_GRAFICO = True` no `main-2va.py`, uma janela abre quando o A.G. começa a rodar:

- **Esquerda:** melhor custo de cada população. Cada reinício cria uma barra nova, e a barra fica verde quando chega ao ótimo.
- **Direita:** melhor custo encontrado ao longo das gerações, com a linha do ótimo conhecido.

O gráfico aumenta o tempo de execução. Para medir o tempo ou comparar com a força bruta, use `MOSTRAR_GRAFICO = False`. Nesse caso o `matplotlib` nem é importado.

### Resultados no brasil58

O A.G. é aleatório, então cada execução termina em um ponto diferente. Nos testes realizados durante o desenvolvimento, com 10000 gerações:

| Configuração | Execuções que chegaram a 25395 | Tempo por execução |
|---|---|---|
| `tam_pop=100`, `paciencia=400` | 8 de 10 | 15 s |
| `tam_pop=200`, `paciencia=500` | 15 de 17 | 29 s |

As execuções que não chegaram ao ótimo terminaram a menos de 1% dele (por exemplo, 25507 e 25622). Os tempos variam conforme a máquina. Para aumentar a chance de chegar ao ótimo, aumente `tam_pop` ou `geracoes`, com custo proporcional no tempo.

### Complexidade do A.G.

- **Complexidade Temporal:** $\mathcal{O}(G \cdot P \cdot N)$, onde $G$ é o número de gerações, $P$ o tamanho da população e $N$ o número de entregas. Cada geração calcula o custo de $P$ filhos, e cada custo soma $N$ distâncias. A ordenação dos sobreviventes soma $\mathcal{O}(P \log P)$ por geração.
- **Complexidade Espacial:** $\mathcal{O}(P \cdot N)$ para guardar a população, mais $\mathcal{O}(N^2)$ para o dicionário de distâncias.

O tempo cresce de forma linear com $N$, contra o crescimento fatorial da força bruta.

---

## 📁 Estrutura do Repositório

```text
FlyFoodCDKP/
│
├── va1/                      # 1ª entrega: força bruta
│   └── flyfood.py            # Leitura do mapa, distância de Manhattan e força bruta
│
├── va2/                      # 2ª entrega: algoritmo genético
│   ├── ag.py                 # Laço principal do A.G. e reinício por estagnação
│   ├── instancia.py          # Leitura do mapa .txt e do .tsp, e matriz de distâncias
│   ├── populacao.py          # Custo do caminho, população inicial e aptidão
│   ├── selecao.py            # Torneio (pais) e steady-state (sobreviventes)
│   ├── cruzamento.py         # Order Crossover (OX)
│   ├── mutacao.py            # Insert, inversão e swap
│   └── grafico.py            # Gráfico em tempo real (opcional)
│
├── main-1va.py               # Executa a força bruta e mede o tempo
├── main-2va.py               # Executa o A.G. e mede o tempo
├── requirements.txt          # Dependências (rich e matplotlib)
├── README.md                 # Documentação do projeto
└── matrizes/                 # Instâncias de teste
    ├── matrix.txt            # Matriz 4x5
    ├── matrix2.txt           # Matriz 3x3
    ├── matrix3.txt           # Matriz 5x5
    ├── matrix4.txt           # Matriz 6x4
    ├── matrix5.txt           # Matriz 7x7
    ├── matrix6.txt           # Matriz 10x10
    ├── matrix7.txt           # Matriz 12x12
    └── edgesbrasil58.tsp     # brasil58 (TSPLIB): pesos acima da diagonal
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.10 ou superior (testado com 3.14)
- Biblioteca `rich` (formatação visual no terminal)
- Biblioteca `matplotlib` (gráfico da 2ª entrega, só necessária com `MOSTRAR_GRAFICO = True`)

### Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/DanielMoreiraFr/FlyFoodCDKP.git
   cd FlyFoodCDKP
   ```

2. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```

### Executando a 1ª entrega (força bruta)

Para rodar o projeto e verificar o resultado de uma matriz:

```bash
python main-1va.py
```

### Executando a 2ª entrega (algoritmo genético)

Rode sempre a partir da raiz do projeto:

```bash
python main-2va.py
```

No topo do `main-2va.py`, troque o arquivo a testar:

```python
ARQUIVO = 'matrizes/edgesbrasil58.tsp'  # ou uma matriz .txt do FlyFood, como 'matrizes/matrix.txt'
MOSTRAR_GRAFICO = True                  # False = sem gráfico, mais rápido
```

Para comparar o A.G. com a força bruta no FlyFood, rode os dois scripts na mesma matriz `.txt` e compare rota, custo e tempo. Use `MOSTRAR_GRAFICO = False` nessa medição. A força bruta só termina em tempo razoável nas matrizes pequenas, e o brasil58 só roda no A.G.

---

## 🖥️ Exemplo de Saída

### 1ª entrega (força bruta)

```text
A melhor rota vai ser: A B C
O custo da rota vai ser: 12
Tempo de execução: 0.000045 segundos
```

### 2ª entrega (algoritmo genético, brasil58)

```text
Calculando a melhor rota para edgesbrasil58.tsp (algoritmo genético)...
Geração 250 | melhor custo: 30892
Geração 500 | melhor custo: 27822
...
╭─────────────── Algoritmo Genético - edgesbrasil58.tsp ───────────────╮
│ Melhor caminho: 1 18 44 24 58 5 23 57 12 27 43 49 47 51 52 10 35 41  │
│ 2 54 55 48 3 29 33 45 56 46 34 15 37 14 28 6 19 26 17 36 21 39 11 7  │
│ 31 38 42 16 22 8 4 50 53 20 32 9 25 40 13 30 1                       │
│ Custo: 25395  (ótimo conhecido: 25395, 0.00% acima)                  │
│ Tempo de execução: 26.960778 segundos                                │
╰──────────────────────────────────────────────────────────────────────╯
```

---

## 📄 Licença

Este projeto é voltado para fins acadêmicos e educacionais. Sinta-se à vontade para utilizar e modificar o código.