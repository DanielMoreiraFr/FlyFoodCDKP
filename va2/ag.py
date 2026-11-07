"""Algoritmo Genético para o FlyFood (.txt) e para TSP com pesos explicitos (.tsp)."""
import random
from rich import print

from va2.instancia import carregar_instancia, ORIGEM
from va2.populacao import custoCaminho, inicializaPopulacao, calculaAptidao
from va2.selecao import torneio, selecao_sobreviventes
from va2.cruzamento import cruzamento_ox
from va2.mutacao import mutacao


def _com_origem(individuo):
    """Coloca a origem no inicio (o custoCaminho ja inclui o retorno a ela)."""
    return [ORIGEM] + individuo


def _montar_rota(individuo, nomes):
    """Rota completa em texto, com a origem no comeco e no fim."""
    return " ".join(nomes[g] for g in [ORIGEM] + individuo + [ORIGEM])


def _gerar_filhos(populacao, custos, taxa_mutacao):
    """Gera filhos suficientes para igualar o tamanho da populacao.

    Cada par: torneio (pais) -> OX (cruzamento) -> mutacao em cada filho.
    """
    filhos = []
    for _ in range(len(populacao) // 2):
        pai1 = torneio(populacao, custos)
        pai2 = torneio(populacao, custos)
        filho1, filho2 = cruzamento_ox(pai1, pai2)
        filhos.append(mutacao(filho1, taxa_mutacao))
        filhos.append(mutacao(filho2, taxa_mutacao))
    return filhos


def _resolver_caso_trivial(qtde, distancias, nomes):
    """Para 0 ou 1 entrega nao ha o que otimizar (o sorteio exige ao menos 2 genes)."""
    individuo = list(range(1, qtde + 1))
    custo = custoCaminho(_com_origem(individuo), distancias) if qtde else 0
    return _montar_rota(individuo, nomes), custo


def algoritmo_genetico(caminho_arquivo, tam_pop=100, geracoes=200, taxa_mutacao=0.1,
                       semente=None, log_a_cada=0):
    """Resolve o FlyFood (.txt) ou um TSP com pesos explicitos (.tsp) com Algoritmo Genetico.

    O no 0 (R no mapa, cidade 1 no .tsp) fica fixo como origem; o AG evolui a ordem
    dos demais. Como o custo e um ciclo, fixar a origem nao perde nenhuma solucao.

    Args:
        caminho_arquivo: arquivo da instancia (.txt do mapa ou .tsp)
        tam_pop: tamanho da populacao
        geracoes: numero de geracoes
        taxa_mutacao: probabilidade de mutacao de cada filho
        semente: semente do random (None = aleatorio a cada execucao)
        log_a_cada: imprime o melhor custo a cada N geracoes (0 = nao imprime)
    Returns:
        (rota_str, custo): rota completa, ja com a origem no comeco e no fim
    """
    if semente is not None:
        random.seed(semente)

    distancias, nomes = carregar_instancia(caminho_arquivo)
    qtde = len(nomes) - 1  # sem contar a origem
    if qtde <= 1:
        return _resolver_caso_trivial(qtde, distancias, nomes)

    populacao = inicializaPopulacao(tam_pop, qtde)
    custos = calculaAptidao([_com_origem(ind) for ind in populacao], distancias)

    for g in range(1, geracoes + 1):
        filhos = _gerar_filhos(populacao, custos, taxa_mutacao)
        custos_filhos = calculaAptidao([_com_origem(f) for f in filhos], distancias)
        populacao, custos = selecao_sobreviventes(populacao, custos, filhos,
                                                  custos_filhos, tam_pop)
        if log_a_cada and g % log_a_cada == 0:
            print(f'[dim]Geração[/dim] [cyan]{g}[/cyan] [dim]| melhor custo:[/dim] [yellow]{custos[0]}[/yellow]')

    melhor = populacao[0]  # o melhor sempre fica na posicao 0
    return _montar_rota(melhor, nomes), custos[0]