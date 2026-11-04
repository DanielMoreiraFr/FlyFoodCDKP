import time
from rich import print
from rich.panel import Panel
from va2.ag import algoritmo_genetico

def main():
    """
    Função principal que executa o algoritmo genético e imprime os resultados.
    """
    arquivo = 'matrizes/matriz10.txt'  # troque para a matriz que quiser

    print(f'[purple]Calculando a melhor rota para o FlyFood [cyan](algoritmo genético)[/cyan]...[/purple]')
    inicio = time.perf_counter()
    rota, custo = algoritmo_genetico(arquivo)
    tempo_exec = time.perf_counter() - inicio

    print(Panel(
        f'Melhor caminho: [blue]R {rota} R[/blue]\n'
        f'Custo: [yellow]{custo}[/yellow]\n'
        f'Tempo de execução: [green]{tempo_exec:.6f}[/green] segundos',
        title='[bold]Algoritmo Genético[/bold]',
        border_style='cyan',
        expand=False,
    ))

if __name__ == "__main__":
    main()