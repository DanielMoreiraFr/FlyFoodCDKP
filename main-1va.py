import time
from rich import print
from rich.panel import Panel
from va1.flyfood import calc_flyfood

def main():
    """
    Função principal que executa o cálculo da melhor rota (força bruta) e imprime os resultados.
    """
    arquivo = 'matrizes/matriz7.txt'  # troque para a matriz que quiser

    print(f'[purple]Calculando a melhor rota para o FlyFood (força bruta)...[/purple]')
    inicio = time.perf_counter()
    rota, custo = calc_flyfood(arquivo)
    tempo_exec = time.perf_counter() - inicio

    print(Panel(
        f'Melhor caminho: [blue]R {rota} R[/blue]\n'
        f'Custo: [yellow]{custo}[/yellow]\n'
        f'Tempo de execução: [green]{tempo_exec:.6f}[/green] segundos',
        title='[bold]Força Bruta[/bold]',
        border_style='purple',
        expand=False,
    ))

if __name__ == "__main__":
    main()