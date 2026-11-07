import time
from rich import print
from rich.panel import Panel
from va2.ag import algoritmo_genetico

# troque aqui o arquivo que quiser testar (rode sempre da raiz do projeto)
ARQUIVO = 'matrizes/edgesbrasil58.tsp'

# melhores custos conhecidos (TSPLIB) para mostrar o erro percentual
OTIMOS = {'edgesbrasil58.tsp': 25395, 'brazil58.tsp': 25395}

PARAMS_MAPA = dict(tam_pop=200, geracoes=10000, taxa_mutacao=0.3, log_a_cada=500)
PARAMS_TSP = dict(tam_pop=200, geracoes=10000, taxa_mutacao=0.4, log_a_cada=500)


def main():
    """
    Função principal que executa o algoritmo genético (mapa .txt ou .tsp) e imprime os resultados.
    """
    nome = ARQUIVO.split('/')[-1]  # so o nome do arquivo, sem a pasta
    print(f'[purple]Calculando a melhor rota para [cyan]{nome}[/cyan] (algoritmo genético)...[/purple]')
    params = PARAMS_TSP if nome.endswith('.tsp') else PARAMS_MAPA

    inicio = time.perf_counter()
    rota, custo = algoritmo_genetico(ARQUIVO, **params)
    tempo_exec = time.perf_counter() - inicio

    linha_custo = f'Custo: [yellow]{custo}[/yellow]'
    if nome in OTIMOS:
        erro = (custo - OTIMOS[nome]) / OTIMOS[nome] * 100
        linha_custo += f'  (ótimo conhecido: {OTIMOS[nome]}, {erro:.2f}% acima)'

    print(Panel(
        f'Melhor caminho: [blue]{rota}[/blue]\n'
        f'{linha_custo}\n'
        f'Tempo de execução: [green]{tempo_exec:.6f}[/green] segundos',
        title=f'[bold]Algoritmo Genético - {nome}[/bold]',
        border_style='cyan',
        expand=False,
    ))


if __name__ == "__main__":
    main()