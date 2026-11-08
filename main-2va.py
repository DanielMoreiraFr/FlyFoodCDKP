import time
from rich import print
from rich.panel import Panel
from va2.ag import algoritmo_genetico

# troque aqui o arquivo que quiser testar (rode sempre da raiz do projeto)
ARQUIVO = 'matrizes/edgesbrasil58.tsp'

# True = abre o gráfico em tempo real; False = sem gráfico (use para medir o tempo)
MOSTRAR_GRAFICO = True

# melhores custos conhecidos (TSPLIB) para mostrar o erro percentual
OTIMOS = {'edgesbrasil58.tsp': 25395, 'brazil58.tsp': 25395}

# paciencia: reinicia a populacao se ficar N geracoes sem melhorar (guarda o melhor ja achado)
# log_a_cada: de quantas em quantas geracoes imprime o progresso e atualiza o gráfico
PARAMS_MAPA = dict(tam_pop=200, geracoes=10000, taxa_mutacao=0.3, log_a_cada=500)
PARAMS_TSP = dict(tam_pop=100, geracoes=10000, taxa_mutacao=0.4, paciencia=400, log_a_cada=250)


def main():
    """
    Função principal que executa o algoritmo genético (mapa .txt ou .tsp) e imprime os resultados.
    """
    nome = ARQUIVO.split('/')[-1]  # so o nome do arquivo, sem a pasta
    print(f'[purple]Calculando a melhor rota para [cyan]{nome}[/cyan] (algoritmo genético)...[/purple]')
    params = PARAMS_TSP if nome.endswith('.tsp') else PARAMS_MAPA

    ao_atualizar = None
    if MOSTRAR_GRAFICO:
        from va2.grafico import criar_grafico  # so importa o matplotlib se o gráfico estiver ligado
        ao_atualizar = criar_grafico(OTIMOS.get(nome))

    inicio = time.perf_counter()
    rota, custo = algoritmo_genetico(ARQUIVO, ao_atualizar=ao_atualizar, **params)
    tempo_exec = time.perf_counter() - inicio

    linha_custo = f'Custo: [yellow]{custo}[/yellow]'
    if nome in OTIMOS:
        erro = (custo - OTIMOS[nome]) / OTIMOS[nome] * 100
        linha_custo += f'  (ótimo conhecido: {OTIMOS[nome]}, {erro:.2f}% acima)'

    aviso_tempo = ' (inclui o gráfico)' if MOSTRAR_GRAFICO else ''
    print(Panel(
        f'Melhor caminho: [blue]{rota}[/blue]\n'
        f'{linha_custo}\n'
        f'Tempo de execução{aviso_tempo}: [green]{tempo_exec:.6f}[/green] segundos',
        title=f'[bold]Algoritmo Genético - {nome}[/bold]',
        border_style='cyan',
        expand=False,
    ))

    if MOSTRAR_GRAFICO:
        from va2.grafico import manter_aberto
        manter_aberto()  # mantém a janela aberta até você fechar


if __name__ == "__main__":
    main()