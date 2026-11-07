"""Operador de cruzamento: Order Crossover (OX)."""
import random


def _gerar_filho_ox(pai1, pai2, a, b):
    """Copia o trecho [a, b] de pai1 e completa com os genes de pai2, em ordem circular."""
    n = len(pai1)
    filho = [None] * n
    filho[a:b + 1] = pai1[a:b + 1]
    copiados = set(pai1[a:b + 1])
    # genes do segundo pai, a partir do corte, sem os ja copiados
    resto = [g for g in pai2[b + 1:] + pai2[:b + 1] if g not in copiados]
    for k, gene in enumerate(resto):
        filho[(b + 1 + k) % n] = gene  # preenche circularmente
    return filho


def cruzamento_ox(pai1, pai2):
    """Order Crossover (OX): gera 2 filhos validos a partir de 2 pais.

    Args:
        pai1, pai2: permutacoes das entregas
    Returns:
        (filho1, filho2)
    """
    a, b = sorted(random.sample(range(len(pai1)), 2))  # corte do trecho copiado
    return _gerar_filho_ox(pai1, pai2, a, b), _gerar_filho_ox(pai2, pai1, a, b)