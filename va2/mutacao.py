"""Operadores de mutação: insert, inversão e swap."""
import random


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
    novo[i:j + 1] = reversed(novo[i:j + 1])
    return novo


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


OPERADORES = [mutacao_insert, mutacao_inversao]

def mutacao(individuo, taxa_mutacao):
    """Com probabilidade taxa_mutacao, aplica insert, inversao ou swap (1/3 cada).

    Args:
        individuo: permutacao das entregas
        taxa_mutacao: probabilidade de mutar (0 a 1)
    Returns:
        individuo (mutado ou igual)
    """
    if random.random() < taxa_mutacao:
        return random.choice(OPERADORES)(individuo)
    return individuo