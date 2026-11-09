import random


def torneio(populacao, custos):
    """Seleção de pais: sorteia 2 indivíduos (K=2) e vence o de menor custo."""
    i, j = random.sample(range(len(populacao)), 2)
    return populacao[i] if custos[i] <= custos[j] else populacao[j]


def selecao_sobreviventes(populacao, custos, filhos, custos_filhos, tamanho):
    """Steady-state: população e filhos competem e ficam os de menor custo, sem clones."""
    juntos = sorted(zip(custos + custos_filhos, populacao + filhos),
                    key=lambda par: par[0])  # do menor para o maior custo
    vistos = set()
    nova_pop, novos_custos, repetidos = [], [], []
    for custo, individuo in juntos:
        chave = tuple(individuo)
        if chave not in vistos:  # entra se ainda não existe na nova população
            vistos.add(chave)
            nova_pop.append(individuo)
            novos_custos.append(custo)
        else:
            repetidos.append((custo, individuo))
        if len(nova_pop) == tamanho:
            break

    # mapas pequenos têm poucas permutações diferentes: completa com os repetidos
    for custo, individuo in repetidos:
        if len(nova_pop) == tamanho:
            break
        nova_pop.append(individuo)
        novos_custos.append(custo)
    return nova_pop, novos_custos