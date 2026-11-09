import random
from rich import print

from va2.instancia import carregar_instancia, ORIGEM
from va2.populacao import custoCaminho, inicializaPopulacao, calculaAptidao
from va2.selecao import torneio, selecao_sobreviventes
from va2.cruzamento import cruzamento_ox
from va2.mutacao import mutacao


def _com_origem(individuo):
    """Põe a origem na frente; o custoCaminho já soma a volta até ela."""
    return [ORIGEM] + individuo


def _montar_rota(individuo, nomes):
    """Rota em texto, com a origem no começo e no fim."""
    return " ".join(nomes[g] for g in [ORIGEM] + individuo + [ORIGEM])


def _gerar_filhos(populacao, custos, taxa_mutacao):
    """Gera tantos filhos quanto o tamanho da população: torneio, OX e mutação."""
    filhos = []
    for _ in range(len(populacao) // 2):  # cada par de pais gera 2 filhos
        pai1 = torneio(populacao, custos)
        pai2 = torneio(populacao, custos)
        filho1, filho2 = cruzamento_ox(pai1, pai2)
        filhos.append(mutacao(filho1, taxa_mutacao))
        filhos.append(mutacao(filho2, taxa_mutacao))
    return filhos


def _nova_populacao(tam_pop, qtde, distancias):
    """Cria uma população aleatória e calcula o custo de cada indivíduo."""
    populacao = inicializaPopulacao(tam_pop, qtde)
    custos = calculaAptidao([_com_origem(ind) for ind in populacao], distancias)
    return populacao, custos


def _proxima_geracao(populacao, custos, distancias, taxa_mutacao):
    """Gera os filhos e escolhe os sobreviventes (steady-state)."""
    filhos = _gerar_filhos(populacao, custos, taxa_mutacao)
    custos_filhos = calculaAptidao([_com_origem(f) for f in filhos], distancias)
    return selecao_sobreviventes(populacao, custos, filhos, custos_filhos, len(populacao))


def _resolver_caso_trivial(qtde, distancias, nomes):
    """Com 0 ou 1 entrega não há o que otimizar (o sorteio de posições exige 2 genes)."""
    individuo = list(range(1, qtde + 1))
    custo = custoCaminho(_com_origem(individuo), distancias) if qtde else 0
    return _montar_rota(individuo, nomes), custo


def algoritmo_genetico(caminho_arquivo, tam_pop=100, geracoes=200, taxa_mutacao=0.1,
                       semente=None, log_a_cada=0, paciencia=0, ao_atualizar=None):
    """Roda o A.G. no FlyFood (.txt) ou no TSP (.tsp) e devolve (rota, custo).

    O nó 0 (R no mapa, cidade 1 no .tsp) fica fixo; o A.G. evolui a ordem dos outros.
    semente: fixa o random (None = muda a cada execução)
    log_a_cada: de N em N gerações imprime o progresso e chama ao_atualizar (0 = desligado)
    paciencia: reinicia a população após N gerações sem melhora (0 = nunca reinicia)
    ao_atualizar: função (geracao, custos, melhor_custo, reinicios) do gráfico (None = desligado)
    """
    if semente is not None:
        random.seed(semente)

    distancias, nomes = carregar_instancia(caminho_arquivo)
    qtde = len(nomes) - 1  # sem contar a origem
    if qtde <= 1:
        return _resolver_caso_trivial(qtde, distancias, nomes)

    populacao, custos = _nova_populacao(tam_pop, qtde, distancias)
    melhor, melhor_custo = populacao[0], custos[0]  # melhor entre todas as populações
    melhor_da_populacao, geracoes_sem_melhora = custos[0], 0
    reinicios = 0

    for g in range(1, geracoes + 1):
        populacao, custos = _proxima_geracao(populacao, custos, distancias, taxa_mutacao)

        if custos[0] < melhor_custo:
            melhor, melhor_custo = populacao[0], custos[0]  # a população vem ordenada
        if custos[0] < melhor_da_populacao:
            melhor_da_populacao, geracoes_sem_melhora = custos[0], 0
        else:
            geracoes_sem_melhora += 1

        if paciencia and geracoes_sem_melhora >= paciencia:  # estagnou: recomeça do zero
            populacao, custos = _nova_populacao(tam_pop, qtde, distancias)
            melhor_da_populacao, geracoes_sem_melhora = custos[0], 0
            reinicios += 1

        if log_a_cada and g % log_a_cada == 0:
            print(f'[dim]Geração[/dim] [cyan]{g}[/cyan] [dim]| melhor custo:[/dim] [yellow]{melhor_custo}[/yellow]')
            if ao_atualizar:
                ao_atualizar(g, custos, melhor_custo, reinicios)

    return _montar_rota(melhor, nomes), melhor_custo