import time
from rich import print
from rich.panel import Panel
from va2.ag import algoritmo_genetico_brasil58

OTIMO = 25395  # melhor custo conhecido do brazil58 (TSPLIB)

def main():
    """
    Executa o algoritmo genético no Brasil 58 e imprime os resultados.
    """
    arquivo = 'matrizes/edgesbrasil58.tsp'

    print('[purple]Calculando a melhor rota para o Brasil 58 [green](algoritmo genético)[/green]...[/purple]')
    inicio = time.perf_counter()
    rota, custo = algoritmo_genetico_brasil58(arquivo, tam_pop=300, geracoes=10000, taxa_mutacao=0.5)
    tempo_exec = time.perf_counter() - inicio

    erro = (custo - OTIMO) / OTIMO * 100

    print(Panel(
        f'Melhor caminho: [blue]{rota}[/blue]\n'
        f'Custo: [yellow]{custo}[/yellow]  (ótimo conhecido: {OTIMO}, {erro:.2f}% acima)\n'
        f'Tempo de execução: [green]{tempo_exec:.6f}[/green] segundos',
        title='[bold]Algoritmo Genético - Brasil 58[/bold]',
        border_style='cyan',
        expand=False,
    ))

if __name__ == "__main__":
    main()