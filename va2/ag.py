import random
from va1.flyfood import ler_mapa, calcular_distancia
from rich import print


def custoCaminho(permutacao, dicDistancias):
    """Soma o custo entre nos consecutivos e do ultimo de volta ao primeiro.

    Args:
        permutacao: lista de nos (ex: [0, 3, 1, 2])
        dicDistancias: dicionario {(i, j): peso}
    Returns:
        custo total do ciclo
    """
    soma = 0
    for i in range(len(permutacao) - 1):
        soma += dicDistancias[(permutacao[i], permutacao[i + 1])]
    soma += dicDistancias[(permutacao[-1], permutacao[0])]
    return soma

def inicializaPopulacao(tamanho, qtdeCidades):
    """Cria 'tamanho' permutacoes aleatorias de 1..qtdeCidades.

    Args:
        tamanho: tamanho da populacao
        qtdeCidades: quantidade de cidades/entregas
    Returns:
        lista de listas (permutacoes)
    """
    lista = []
    for i in range(tamanho):
        individuo = list(range(1, qtdeCidades + 1))
        random.shuffle(individuo)
        lista.append(individuo)
    return lista

def calculaAptidao(populacao, dicDistancias):
    """Calcula o custo de cada individuo (menor = melhor).

    Args:
        populacao: lista de permutacoes
        dicDistancias: dicionario {(i, j): peso}
    Returns:
        lista de custos na mesma ordem da populacao
    """
    listaAptidao = []
    for elem in populacao:
        listaAptidao.append(custoCaminho(elem, dicDistancias))
    return listaAptidao

def construir_matriz_distancias(ponto_r, entregas):
    """Converte o mapa de entregas em dicionario de distancias (i, j).

    Args:
        ponto_r: coordenadas de R (ex: (0, 0))
        entregas: dicionario {nome: coordenadas} (ex: {'A': (2, 1)})
    Returns:
        (distancias, nomes): dicionario {(i, j): peso} simetrico e
        dicionario {numero: nome} (R = 0, entregas = 1..n)
    """
    nomes = {0: 'R'}
    coords = {0: ponto_r}
    for numero, nome in enumerate(entregas, start=1):
        nomes[numero] = nome
        coords[numero] = entregas[nome]

    distancias = {}
    for i in coords:
        for j in coords:
            if i != j:
                distancias[(i, j)] = calcular_distancia(coords[i], coords[j])
    return distancias, nomes

def torneio(populacao, custos):
    """Selecao de pais por torneio com K=2 (vence o menor custo).

    Args:
        populacao: lista de individuos
        custos: lista de custos na mesma ordem da populacao
    Returns:
        o individuo vencedor
    """
    i, j = random.sample(range(len(populacao)), 2)
    return populacao[i] if custos[i] <= custos[j] else populacao[j]

def cruzamento_ox(pai1, pai2):
    """Order Crossover (OX): gera 2 filhos validos a partir de 2 pais.

    Args:
        pai1, pai2: permutacoes das entregas
    Returns:
        (filho1, filho2)
    """
    n = len(pai1)
    a, b = sorted(random.sample(range(n), 2))  # corte do trecho copiado

    def gerar_filho(p1, p2):
        filho = [None] * n
        filho[a:b+1] = p1[a:b+1]  # copia o trecho do primeiro pai
        # genes do segundo pai, a partir do corte, sem os ja copiados
        resto = [g for g in p2[b+1:] + p2[:b+1] if g not in filho[a:b+1]]
        for k, gene in enumerate(resto):
            filho[(b + 1 + k) % n] = gene  # preenche circularmente
        return filho

    return gerar_filho(pai1, pai2), gerar_filho(pai2, pai1)

def mutacao_insert(individuo):
    """Remove um elemento de uma posicao e o insere em outra.

    Args:
        individuo: permutacao das entregas
    Returns:
        novo individuo mutado
    """
    novo = individuo[:]
    i, j = random.sample(range(len(novo)), 2)
    novo.insert(j, novo.pop(i))
    return novo

def mutacao_inversao(individuo):
    """Inverte a ordem dos elementos entre duas posicoes sorteadas.

    Args:
        individuo: permutacao das entregas
    Returns:
        novo individuo mutado
    """
    novo = individuo[:]
    i, j = sorted(random.sample(range(len(novo)), 2))
    novo[i:j+1] = reversed(novo[i:j+1])
    return novo

def mutacao(individuo, taxa_mutacao):
    """Com probabilidade taxa_mutacao, aplica insert, inversao ou swap (1/3 cada).

    Args:
        individuo: permutacao das entregas
        taxa_mutacao: probabilidade de mutar (0 a 1)
    Returns:
        individuo (mutado ou igual)
    """
    if random.random() < taxa_mutacao:
        operador = random.choice([mutacao_insert, mutacao_inversao, mutacao_swap])
        return operador(individuo)
    return individuo

def selecao_sobreviventes(populacao, custos, filhos, custos_filhos, tamanho):
    """Steady-state sem clones: populacao + filhos competem, ficam os de menor custo.

    Args:
        populacao, custos: individuos atuais e seus custos
        filhos, custos_filhos: novos individuos e seus custos
        tamanho: tamanho original da populacao
    Returns:
        (nova_populacao, novos_custos)
    """
    juntos = sorted(zip(custos + custos_filhos, populacao + filhos),
                    key=lambda par: par[0])
    vistos = set()
    nova_pop, novos_custos, repetidos = [], [], []
    for c, ind in juntos:
        chave = tuple(ind)
        if chave not in vistos:  # so entra se ainda nao existe na populacao
            vistos.add(chave)
            nova_pop.append(ind)
            novos_custos.append(c)
        else:
            repetidos.append((c, ind))
        if len(nova_pop) == tamanho:
            break
    # mapas pequenos podem ter poucas permutacoes diferentes: completa com repetidos
    for c, ind in repetidos:
        if len(nova_pop) == tamanho:
            break
        nova_pop.append(ind)
        novos_custos.append(c)
    return nova_pop, novos_custos

def algoritmo_genetico(caminho_arquivo, tam_pop=100, geracoes=200, taxa_mutacao=0.1):
    """Resolve o FlyFood com Algoritmo Genetico.

    Args:
        caminho_arquivo: arquivo do mapa
        tam_pop: tamanho da populacao
        geracoes: numero de geracoes
        taxa_mutacao: probabilidade de mutacao de cada filho
    Returns:
        (rota_str, custo) no mesmo formato de calc_flyfood
    """
    ponto_r, entregas = ler_mapa(caminho_arquivo)
    distancias, nomes = construir_matriz_distancias(ponto_r, entregas)

    populacao = inicializaPopulacao(tam_pop, len(entregas))
    # [0] + individuo inclui R no inicio (e o retorno a R no custoCaminho)
    custos = calculaAptidao([[0] + ind for ind in populacao], distancias)

    for _ in range(geracoes):
        filhos = []
        for _ in range(tam_pop // 2):
            pai1 = torneio(populacao, custos)
            pai2 = torneio(populacao, custos)
            f1, f2 = cruzamento_ox(pai1, pai2)
            filhos.append(mutacao(f1, taxa_mutacao))
            filhos.append(mutacao(f2, taxa_mutacao))
        custos_filhos = calculaAptidao([[0] + f for f in filhos], distancias)
        populacao, custos = selecao_sobreviventes(populacao, custos, filhos,
                                                  custos_filhos, tam_pop)

    melhor = populacao[0]  # populacao ja esta ordenada por custo
    rota_str = " ".join(nomes[g] for g in melhor)
    return rota_str, custos[0]

def ler_brasil58(caminho_arquivo, qtde_cidades=58):
    """Le o arquivo edgesbrasil58.tsp (triangulo superior) em um dicionario.

    Args:
        caminho_arquivo: arquivo com os pesos
        qtde_cidades: numero de cidades (58)
    Returns:
        dicionario {(i, j): peso} simetrico, cidades de 1 a qtde_cidades
    """
    with open(caminho_arquivo) as arq:
        pesos = arq.read().split()  # todos os numeros em sequencia

    distancias = {}
    k = 0
    for i in range(1, qtde_cidades):
        for j in range(i + 1, qtde_cidades + 1):
            peso = int(pesos[k])
            k += 1
            distancias[(i, j)] = peso
            distancias[(j, i)] = peso
    return distancias

def algoritmo_genetico_brasil58(caminho_arquivo, tam_pop=100, geracoes=200, taxa_mutacao=0.1):
    """Resolve o TSP Brasil 58 com Algoritmo Genetico.

    Args:
        caminho_arquivo: arquivo edgesbrasil58.tsp
        tam_pop: tamanho da populacao
        geracoes: numero de geracoes
        taxa_mutacao: probabilidade de mutacao de cada filho
    Returns:
        (rota_str, custo) com as cidades de 1 a 58
    """
    qtde = 58
    distancias = ler_brasil58(caminho_arquivo, qtde)

    populacao = inicializaPopulacao(tam_pop, qtde)
    custos = calculaAptidao(populacao, distancias)  # sem R fixo

    for g in range(1, geracoes + 1):
        filhos = []
        for _ in range(tam_pop // 2):
            pai1 = torneio(populacao, custos)
            pai2 = torneio(populacao, custos)
            f1, f2 = cruzamento_ox(pai1, pai2)
            filhos.append(mutacao(f1, taxa_mutacao))
            filhos.append(mutacao(f2, taxa_mutacao))
        custos_filhos = calculaAptidao(filhos, distancias)
        populacao, custos = selecao_sobreviventes(populacao, custos, filhos,
                                                  custos_filhos, tam_pop)
        if g % 1000 == 0:  # mostra o progresso a cada 1000 geracoes
            print(f'[dim]Geração[/dim] [cyan]{g}[/cyan] [dim]| melhor custo:[/dim] [yellow]{custos[0]}[/yellow]')

    rota_str = " ".join(str(c) for c in populacao[0])
    return rota_str, custos[0]

def mutacao_swap(individuo):
    """Troca dois elementos de posicao.

    Args:
        individuo: permutacao das entregas
    Returns:
        novo individuo mutado
    """
    novo = individuo[:]
    i, j = random.sample(range(len(novo)), 2)
    novo[i], novo[j] = novo[j], novo[i]
    return novo