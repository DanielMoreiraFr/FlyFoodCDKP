import random


def mutacao_insert(individuo):
    """Tira um elemento de uma posição e insere em outra."""
    novo = individuo[:]  # copia para não alterar o original
    i, j = random.sample(range(len(novo)), 2)
    novo.insert(j, novo.pop(i))
    return novo


def mutacao_inversao(individuo):
    """Inverte o trecho entre duas posições sorteadas."""
    novo = individuo[:]
    i, j = sorted(random.sample(range(len(novo)), 2))
    novo[i:j + 1] = reversed(novo[i:j + 1])
    return novo


def mutacao_swap(individuo):
    """Troca dois elementos de posição."""
    novo = individuo[:]
    i, j = random.sample(range(len(novo)), 2)
    novo[i], novo[j] = novo[j], novo[i]
    return novo


OPERADORES = [mutacao_insert, mutacao_inversao]  # para usar o swap, inclua mutacao_swap aqui


def mutacao(individuo, taxa_mutacao):
    """Com probabilidade taxa_mutacao, aplica um operador sorteado de OPERADORES."""
    if random.random() < taxa_mutacao:
        return random.choice(OPERADORES)(individuo)
    return individuo