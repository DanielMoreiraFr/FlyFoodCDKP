"""Funções da aula: custo de um caminho, população inicial e aptidão."""
import random


def custoCaminho(permutacao, dicDistancias):
    """Soma o custo entre nos consecutivos e do ultimo de volta ao primeiro.

    Args:
        permutacao: lista de nos (ex: [0, 3, 1, 2])
        dicDistancias: dicionario {(i, j): peso}
    Returns:
        custo total do ciclo
    """
    soma = 0
    for i in range(len(permutacao) - 1):
        soma += dicDistancias[(permutacao[i], permutacao[i + 1])]
    soma += dicDistancias[(permutacao[-1], permutacao[0])]
    return soma


def inicializaPopulacao(tamanho, qtdeCidades):
    """Cria 'tamanho' permutacoes aleatorias de 1..qtdeCidades.

    Args:
        tamanho: tamanho da populacao
        qtdeCidades: quantidade de cidades/entregas
    Returns:
        lista de listas (permutacoes)
    """
    lista = []
    for _ in range(tamanho):
        individuo = list(range(1, qtdeCidades + 1))
        random.shuffle(individuo)
        lista.append(individuo)
    return lista


def calculaAptidao(populacao, dicDistancias):
    """Calcula o custo de cada individuo (menor = melhor).

    Args:
        populacao: lista de permutacoes
        dicDistancias: dicionario {(i, j): peso}
    Returns:
        lista de custos na mesma ordem da populacao
    """
    return [custoCaminho(individuo, dicDistancias) for individuo in populacao]