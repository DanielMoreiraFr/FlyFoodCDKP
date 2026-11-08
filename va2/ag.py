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


def _nova_populacao(tam_pop, qtde, distancias):
    """Cria uma populacao aleatoria e calcula o custo de cada individuo."""
    populacao = inicializaPopulacao(tam_pop, qtde)
    custos = calculaAptidao([_com_origem(ind) for ind in populacao], distancias)
    return populacao, custos


def _proxima_geracao(populacao, custos, distancias, taxa_mutacao):
    """Gera os filhos e aplica a selecao de sobreviventes (steady-state)."""
    filhos = _gerar_filhos(populacao, custos, taxa_mutacao)
    custos_filhos = calculaAptidao([_com_origem(f) for f in filhos], distancias)
    return selecao_sobreviventes(populacao, custos, filhos, custos_filhos, len(populacao))


def _resolver_caso_trivial(qtde, distancias, nomes):
    """Para 0 ou 1 entrega nao ha o que otimizar (o sorteio exige ao menos 2 genes)."""
    individuo = list(range(1, qtde + 1))
    custo = custoCaminho(_com_origem(individuo), distancias) if qtde else 0
    return _montar_rota(individuo, nomes), custo


def algoritmo_genetico(caminho_arquivo, tam_pop=100, geracoes=200, taxa_mutacao=0.1,
                       semente=None, log_a_cada=0, paciencia=0, ao_atualizar=None):
    """Resolve o FlyFood (.txt) ou um TSP com pesos explicitos (.tsp) com Algoritmo Genetico.

    O no 0 (R no mapa, cidade 1 no .tsp) fica fixo como origem; o AG evolui a ordem
    dos demais. Como o custo e um ciclo, fixar a origem nao perde nenhuma solucao.

    Args:
        caminho_arquivo: arquivo da instancia (.txt do mapa ou .tsp)
        tam_pop: tamanho da populacao
        geracoes: numero de geracoes
        taxa_mutacao: probabilidade de mutacao de cada filho
        semente: semente do random (None = aleatorio a cada execucao)
        log_a_cada: a cada N geracoes imprime o melhor custo e chama ao_atualizar (0 = nunca)
        paciencia: se a populacao ficar N geracoes sem melhorar, ela e reiniciada
            (o melhor ja encontrado e guardado). 0 = nunca reinicia
        ao_atualizar: funcao opcional (geracao, custos, melhor_custo, reinicios) chamada
            junto com o log, usada para o grafico em tempo real. None = desligado
    Returns:
        (rota_str, custo): rota completa, ja com a origem no comeco e no fim
    """
    if semente is not None:
        random.seed(semente)

    distancias, nomes = carregar_instancia(caminho_arquivo)
    qtde = len(nomes) - 1  # sem contar a origem
    if qtde <= 1:
        return _resolver_caso_trivial(qtde, distancias, nomes)

    populacao, custos = _nova_populacao(tam_pop, qtde, distancias)
    melhor, melhor_custo = populacao[0], custos[0]  # melhor de todas as populacoes
    melhor_da_populacao, geracoes_sem_melhora = custos[0], 0
    reinicios = 0

    for g in range(1, geracoes + 1):
        populacao, custos = _proxima_geracao(populacao, custos, distancias, taxa_mutacao)

        if custos[0] < melhor_custo:
            melhor, melhor_custo = populacao[0], custos[0]  # o melhor fica na posicao 0
        if custos[0] < melhor_da_populacao:
            melhor_da_populacao, geracoes_sem_melhora = custos[0], 0
        else:
            geracoes_sem_melhora += 1

        if paciencia and geracoes_sem_melhora >= paciencia:  # estagnou: recomeca do zero
            populacao, custos = _nova_populacao(tam_pop, qtde, distancias)
            melhor_da_populacao, geracoes_sem_melhora = custos[0], 0
            reinicios += 1

        if log_a_cada and g % log_a_cada == 0:
            print(f'[dim]Geração[/dim] [cyan]{g}[/cyan] [dim]| melhor custo:[/dim] [yellow]{melhor_custo}[/yellow]')
            if ao_atualizar:
                ao_atualizar(g, custos, melhor_custo, reinicios)

    return _montar_rota(melhor, nomes), melhor_custo