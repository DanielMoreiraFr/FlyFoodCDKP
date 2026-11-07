"""Seleção de pais (torneio) e de sobreviventes (steady-state)."""
import random


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
    for custo, individuo in juntos:
        chave = tuple(individuo)
        if chave not in vistos:  # so entra se ainda nao existe na populacao
            vistos.add(chave)
            nova_pop.append(individuo)
            novos_custos.append(custo)
        else:
            repetidos.append((custo, individuo))
        if len(nova_pop) == tamanho:
            break

    # mapas pequenos podem ter poucas permutacoes diferentes: completa com repetidos
    for custo, individuo in repetidos:
        if len(nova_pop) == tamanho:
            break
        nova_pop.append(individuo)
        novos_custos.append(custo)
    return nova_pop, novos_custos