import math
from va1.flyfood import ler_mapa, calcular_distancia

ORIGEM = 0  # nó de partida e de chegada do ciclo (R no mapa, cidade 1 no .tsp)


def construir_matriz_distancias(ponto_r, entregas):
    """Converte o mapa do FlyFood em (distancias, nomes), com R = 0 e entregas = 1..n."""
    nomes = {ORIGEM: 'R'}  # número -> nome do ponto
    coords = {ORIGEM: ponto_r}
    for numero, nome in enumerate(entregas, start=1):
        nomes[numero] = nome
        coords[numero] = entregas[nome]

    distancias = {}  # {(i, j): peso}, nos dois sentidos
    for i in coords:
        for j in coords:
            if i != j:
                distancias[(i, j)] = calcular_distancia(coords[i], coords[j])
    return distancias, nomes


def _separar_cabecalho(texto):
    """Separa o cabeçalho da TSPLIB dos pesos e devolve (dimensao, texto_pesos).

    dimensao é None quando o arquivo não tem DIMENSION.
    """
    if 'EDGE_WEIGHT_SECTION' not in texto:
        return None, texto  # arquivo só com os números

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
    """Monta {(i, j): peso} nos dois sentidos a partir dos pesos acima da diagonal."""
    distancias = {}
    k = 0
    for i in range(dimensao - 1):
        for j in range(i + 1, dimensao):
            distancias[(i, j)] = distancias[(j, i)] = pesos[k]
            k += 1
    return distancias


def ler_tsp(caminho_arquivo):
    """Lê um .tsp com pesos UPPER_ROW e devolve (distancias, nomes).

    Aceita o arquivo completo da TSPLIB ou só os números (edgesbrasil58.tsp).
    A cidade 1 vira o nó 0 e as outras viram 1..n-1; os nomes mantêm a numeração original.
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
    """Escolhe o leitor pela extensão: .tsp (pesos) ou .txt (mapa do FlyFood)."""
    if str(caminho_arquivo).lower().endswith('.tsp'):
        return ler_tsp(caminho_arquivo)
    ponto_r, entregas = ler_mapa(caminho_arquivo)
    return construir_matriz_distancias(ponto_r, entregas)