import random


def _gerar_filho_ox(pai1, pai2, a, b):
    """Gera um filho: copia o trecho [a, b] do pai1 e completa com os genes do pai2."""
    n = len(pai1)
    filho = [None] * n
    filho[a:b + 1] = pai1[a:b + 1]  # trecho herdado do pai1
    copiados = set(pai1[a:b + 1])
    # genes do pai2 em ordem circular a partir do corte, sem os já copiados
    resto = [g for g in pai2[b + 1:] + pai2[:b + 1] if g not in copiados]
    for k, gene in enumerate(resto):
        filho[(b + 1 + k) % n] = gene  # preenche depois do trecho e volta ao início
    return filho


def cruzamento_ox(pai1, pai2):
    """Order Crossover (OX): devolve (filho1, filho2), ambos permutações válidas."""
    a, b = sorted(random.sample(range(len(pai1)), 2))  # pontos de corte
    return _gerar_filho_ox(pai1, pai2, a, b), _gerar_filho_ox(pai2, pai1, a, b)