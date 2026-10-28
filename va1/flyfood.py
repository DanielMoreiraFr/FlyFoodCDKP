def ler_mapa(mapa):
    """
    Lê o arquivo de mapa e retorna o ponto R e suas entregas, como um dict com as coordenadas de cada ponto de entrega

    Args:
        mapa (str): Caminho para o arquivo de mapa

    Returns:
        tuple: Ponto R (linha, coluna) e dict de entregas {ponto: (linha, coluna)}
    """
    with open(mapa, 'r') as m: # abre o arquivo passado como parametro com a função de read
        linhas = m.read().splitlines()

    n_linhas, n_colunas = map(int, linhas[0].split()) # pega as dimensões da matriz que ficaram na primeira lista pós splitlines

    ponto_r = None #vai ser reescrita com o ponto r informado no arquivo
    entregas = {}

    for line in range(n_linhas):
        elementos = linhas[line+1].split()

        for column in range(n_colunas):
            val = elementos[column]
            if val != '0': # nao faz nada se for vazio / 0
                if val == "R": # caso do ponto R
                    ponto_r = (line, column)
                else: # caso for uma das cidades de entrega A, B, C, D, ...
                    entregas[val] = (line, column) # da as coordenadas do ponto em específico

    return ponto_r, entregas


def calcular_distancia(p1, p2):
    """
    Calcula a distância entre dois pontos

    Args:
        p1 (tuple): Coordenadas do ponto 1 (linha, coluna)
        p2 (tuple): Coordenadas do ponto 2 (linha, coluna)

    Returns:
        int: Distância entre os dois pontos
    """
    return (abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])) # uso do valor absoluto para não ter caso de distancia negativa

def calcular_rota(rota, ponto_r, entregas):
    """
    Calcula o custo de uma rota para realizar um circuito completo de entregas

    Args:
        rota (tuple): Tupla com a ordem das entregas
        ponto_r (tuple): Coordenadas do ponto R
        entregas (dict): Dicionário com as coordenadas das entregas

    Returns:
        int: Custo da rota
    """
    custo = 0
    p_atual = ponto_r

    for ponto in rota:
        proximo_ponto = entregas[ponto]
        custo += calcular_distancia(p_atual, proximo_ponto)
        p_atual = proximo_ponto

    custo += calcular_distancia(p_atual, ponto_r) # volta pro ponto R
    return custo

def calc_flyfood(caminho_arquivo):
    """
    Resolve o problema de roteamento do flyfood com força bruta, testando todas as formas possíveis

    Args:
        caminho_arquivo (str): Caminho para o arquivo  .txt com a matriz

    Returns:
        tuple: Melhor rota (str) e custo da rota (int)
    """
    from itertools import permutations

    ponto_r, entregas = ler_mapa(caminho_arquivo)

    lista_entregas = list(entregas.keys()) # puxa apenas as chaves do dict para ter os nomes das entregas

    melhor_custo = float('inf')
    melhor_rota = None

    for rota in permutations(lista_entregas):
        custo_atual = calcular_rota(rota, ponto_r, entregas)

        if custo_atual < melhor_custo:
            melhor_custo = custo_atual
            melhor_rota = rota

    res = " ".join(melhor_rota) # join vai transformar a tupla das cidades da melhor rota em uma string da rota em questão
    return res, melhor_custo