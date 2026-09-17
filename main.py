from flyfood import calc_flyfood
import time
from rich import print

def main():
    """
    Função principal que executa o cálculo da melhor rota e imprime os resultados.
    """

    inicio = time.perf_counter()
    rota, custo = calc_flyfood('matrizes/matrix2.txt')
    fim = time.perf_counter()
    tempo_exec = fim - inicio

    print(f'A melhor rota vai ser: [blue]{rota}[/blue]')
    print(f'O custo da rota vai ser: [yellow]{custo}[/yellow]')
    print(f"Tempo de execução: [green]{tempo_exec:.6f}[/green] segundos")

if __name__ == "__main__":
    main()