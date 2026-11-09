import matplotlib.pyplot as plt


def criar_grafico(otimo=None):
    """Abre a janela e devolve atualizar(geracao, custos, melhor_custo, reinicios).

    Esquerda: melhor custo de cada população (cada reinício cria uma barra).
    Direita: melhor custo ao longo das gerações.
    otimo: custo ótimo conhecido, desenhado como linha de referência (opcional).
    """
    plt.ion()  # modo interativo: a janela abre sem travar o programa
    fig, (ax_pop, ax_hist) = plt.subplots(1, 2, figsize=(12, 5))
    ax_pop.set_title('Melhor custo de cada população')
    ax_pop.set_xlabel('População (a última está em andamento)')
    ax_pop.set_ylabel('Custo')
    ax_hist.set_title('Evolução')
    ax_hist.set_xlabel('Geração')
    ax_hist.set_ylabel('Custo')

    linha_melhor, = ax_hist.plot([], [], color='tab:green', label='Melhor custo')
    if otimo is not None:
        ax_hist.axhline(otimo, color='gray', linestyle='--', label=f'Ótimo ({otimo})')
        ax_pop.axhline(otimo, color='gray', linestyle='--')
    ax_hist.legend()

    barras, rotulos, alturas = [], [], []  # uma barra por população (reinício)
    geracoes, melhores = [], []

    def _cor(custo):
        return 'tab:green' if custo == otimo else 'tab:blue'  # verde = chegou ao ótimo

    def atualizar(geracao, custos, melhor_custo, reinicios):
        melhor_populacao = min(custos)

        while len(barras) <= reinicios:  # população nova (ou reinício entre dois logs)
            posicao = len(barras)
            barras.append(ax_pop.bar(posicao, melhor_populacao)[0])
            rotulos.append(ax_pop.text(posicao, melhor_populacao, '', ha='center', va='bottom'))
            alturas.append(melhor_populacao)
        alturas[reinicios] = melhor_populacao

        barras[reinicios].set_height(melhor_populacao)
        barras[reinicios].set_color(_cor(melhor_populacao))
        rotulos[reinicios].set_position((reinicios, melhor_populacao))
        rotulos[reinicios].set_text(str(melhor_populacao))
        ax_pop.set_xticks(range(len(barras)), [str(i + 1) for i in range(len(barras))])
        referencia = otimo if otimo is not None else min(alturas)
        ax_pop.set_ylim(referencia * 0.99, max(alturas) * 1.01)  # barras não começam do zero

        geracoes.append(geracao)
        melhores.append(melhor_custo)
        linha_melhor.set_data(geracoes, melhores)
        ax_hist.relim()
        ax_hist.autoscale_view()

        fig.suptitle(f'Geração {geracao} | melhor custo: {melhor_custo} | reinícios: {reinicios}')
        fig.canvas.draw_idle()     # agenda o redesenho
        fig.canvas.flush_events()  # a janela executa o redesenho agora, antes de o A.G. seguir

    return atualizar


def manter_aberto():
    """Mantém a janela aberta ao fim da execução, até o usuário fechar."""
    plt.ioff()
    plt.show()