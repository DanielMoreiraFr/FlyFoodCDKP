"""Gráfico em tempo real do A.G. (opcional: só é importado se o main pedir)."""
import matplotlib.pyplot as plt


def criar_grafico(otimo=None):
    """Abre a janela do gráfico e devolve a função que a atualiza.

    Esquerda: custo de cada indivíduo da população atual (menor = melhor).
    Direita: melhor custo e custo médio da população ao longo das gerações.

    Args:
        otimo: custo ótimo conhecido, desenhado como linha de referência (opcional)
    Returns:
        funcao atualizar(geracao, custos, melhor_custo, reinicios), para usar
        como o parametro ao_atualizar do algoritmo_genetico
    """
    plt.ion()
    fig, (ax_pop, ax_hist) = plt.subplots(1, 2, figsize=(12, 5))
    ax_pop.set_title('População atual (um custo por indivíduo)')
    ax_pop.set_xlabel('Indivíduo (do melhor ao pior)')
    ax_pop.set_ylabel('Custo')
    ax_hist.set_title('Evolução')
    ax_hist.set_xlabel('Geração')
    ax_hist.set_ylabel('Custo')

    linha_melhor, = ax_hist.plot([], [], color='tab:green', label='Melhor custo')
    linha_media, = ax_hist.plot([], [], color='tab:orange', label='Média da população')
    if otimo is not None:
        ax_hist.axhline(otimo, color='gray', linestyle='--', label=f'Ótimo ({otimo})')
    ax_hist.legend()

    barras = []  # criadas na primeira atualizacao (precisam do tamanho da populacao)
    geracoes, melhores, medias = [], [], []

    def atualizar(geracao, custos, melhor_custo, reinicios):
        ordenados = sorted(custos)
        if not barras:
            barras.extend(ax_pop.bar(range(len(ordenados)), ordenados, color='tab:blue'))
        for barra, custo in zip(barras, ordenados):
            barra.set_height(custo)
        referencia = otimo if otimo is not None else melhor_custo
        ax_pop.set_ylim(referencia * 0.95, max(ordenados) * 1.02)  # barras nao comecam do zero

        geracoes.append(geracao)
        melhores.append(melhor_custo)
        medias.append(sum(custos) / len(custos))
        linha_melhor.set_data(geracoes, melhores)
        linha_media.set_data(geracoes, medias)
        ax_hist.relim()
        ax_hist.autoscale_view()

        fig.suptitle(f'Geração {geracao} | melhor custo: {melhor_custo} | reinícios: {reinicios}')
        plt.pause(0.001)  # redesenha e processa eventos da janela

    return atualizar


def manter_aberto():
    """Deixa a janela aberta ao fim da execução (fecha quando o usuário fechar)."""
    plt.ioff()
    plt.show()