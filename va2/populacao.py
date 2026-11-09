import random


def custoCaminho(permutacao, dicDistancias):
    """Soma o custo entre nós consecutivos e do último de volta ao primeiro."""
    soma = 0
    for i in range(len(permutacao) - 1):
        soma += dicDistancias[(permutacao[i], permutacao[i + 1])]
    soma += dicDistancias[(permutacao[-1], permutacao[0])]  # volta ao nó inicial
    return soma


def inicializaPopulacao(tamanho, qtdeCidades):
    """Cria 'tamanho' permutações aleatórias de 1..qtdeCidades."""
    lista = []
    for _ in range(tamanho):
        individuo = list(range(1, qtdeCidades + 1))
        random.shuffle(individuo)
        lista.append(individuo)
    return lista


def calculaAptidao(populacao, dicDistancias):
    """Devolve o custo de cada indivíduo, na ordem da população (menor = melhor)."""
    return [custoCaminho(individuo, dicDistancias) for individuo in populacao]