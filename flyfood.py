def ler_mapa(mapa):
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
    return (abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])) # uso do valor absoluto para não ter caso de distancia negativa

def calcular_rota(rota, ponto_r, entregas):
    custo = 0
    p_atual = ponto_r

    for ponto in rota:
        proximo_ponto = entregas[ponto]
        custo += calcular_distancia(p_atual, proximo_ponto)
        p_atual = proximo_ponto

    custo += calcular_distancia(p_atual, ponto_r) # volta pro ponto R
    return custo

def calc_flyfood():
    pass