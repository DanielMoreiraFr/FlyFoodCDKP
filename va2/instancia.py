"""Leitura da instância (mapa FlyFood .txt ou TSPLIB .tsp) e montagem das distâncias."""
import math
from va1.flyfood import ler_mapa, calcular_distancia

ORIGEM = 0  # nó de partida e de chegada do ciclo (R no mapa, cidade 1 no .tsp)


def construir_matriz_distancias(ponto_r, entregas):
    """Converte o mapa de entregas em dicionario de distancias (i, j).

    Args:
        ponto_r: coordenadas de R (ex: (0, 0))
        entregas: dicionario {nome: coordenadas} (ex: {'A': (2, 1)})
    Returns:
        (distancias, nomes): dicionario {(i, j): peso} simetrico e
        dicionario {numero: nome} (R = 0, entregas = 1..n)
    """
    nomes = {ORIGEM: 'R'}
    coords = {ORIGEM: ponto_r}
    for numero, nome in enumerate(entregas, start=1):
        nomes[numero] = nome
        coords[numero] = entregas[nome]

    distancias = {}
    for i in coords:
        for j in coords:
            if i != j:
                distancias[(i, j)] = calcular_distancia(coords[i], coords[j])
    return distancias, nomes


def _separar_cabecalho(texto):
    """Separa o cabecalho da TSPLIB (se houver) do trecho com os pesos.

    Returns:
        (dimensao, texto_pesos): dimensao e None quando nao ha DIMENSION
    """
    if 'EDGE_WEIGHT_SECTION' not in texto:
        return None, texto

    cabecalho, corpo = texto.split('EDGE_WEIGHT_SECTION', 1)
    dimensao = None
    for linha in cabecalho.splitlines():
        chave, _, valor = linha.partition(':')
        chave, valor = chave.strip(), valor.strip()
        if chave == 'DIMENSION':
            dimensao = int(valor)
        elif chave == 'EDGE_WEIGHT_FORMAT' and valor != 'UPPER_ROW':
            raise ValueError(f'Formato {valor} nao suportado (so UPPER_ROW)')
    return dimensao, corpo.split('EOF')[0]


def _montar_distancias_upper_row(pesos, dimensao):
    """Preenche {(i, j): peso} (simetrico) a partir dos pesos acima da diagonal."""
    distancias = {}
    k = 0
    for i in range(dimensao - 1):
        for j in range(i + 1, dimensao):
            distancias[(i, j)] = distancias[(j, i)] = pesos[k]
            k += 1
    return distancias


def ler_tsp(caminho_arquivo):
    """Le um arquivo .tsp com pesos explicitos no formato UPPER_ROW.

    Aceita o arquivo completo da TSPLIB (com cabecalho NAME/DIMENSION/...) e
    tambem o arquivo "puro", so com os numeros (como o edgesbrasil58.tsp).
    A quantidade de cidades vem de DIMENSION ou e deduzida da quantidade de pesos.

    Args:
        caminho_arquivo: arquivo .tsp
    Returns:
        (distancias, nomes): dicionario {(i, j): peso} simetrico e dicionario
        {numero: nome}. A cidade 1 do arquivo vira o no 0 (origem do ciclo) e
        as demais viram 1..n-1; os nomes preservam a numeracao original.
    """
    with open(caminho_arquivo) as arq:
        dimensao, texto_pesos = _separar_cabecalho(arq.read())

    pesos = [int(p) for p in texto_pesos.split()]
    if dimensao is None:  # n*(n-1)/2 pesos -> n
        dimensao = round((1 + math.sqrt(1 + 8 * len(pesos))) / 2)
    if len(pesos) != dimensao * (dimensao - 1) // 2:
        raise ValueError(f'{caminho_arquivo}: {len(pesos)} pesos nao batem com {dimensao} cidades')

    distancias = _montar_distancias_upper_row(pesos, dimensao)
    nomes = {i: str(i + 1) for i in range(dimensao)}
    return distancias, nomes


def carregar_instancia(caminho_arquivo):
    """Escolhe o leitor pela extensao: .tsp (pesos explicitos) ou .txt (mapa FlyFood).

    Args:
        caminho_arquivo: arquivo da instancia
    Returns:
        (distancias, nomes) com o no 0 como origem do ciclo
    """
    if str(caminho_arquivo).lower().endswith('.tsp'):
        return ler_tsp(caminho_arquivo)
    ponto_r, entregas = ler_mapa(caminho_arquivo)
    return construir_matriz_distancias(ponto_r, entregas)