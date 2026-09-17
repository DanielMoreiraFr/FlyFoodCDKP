from flyfood import calc_flyfood
import time
from rich import print

def main():
    inicio = time.perf_counter()
    rota, custo = calc_flyfood('matrix4.txt')
    fim = time.perf_counter()
    tempo_exec = fim - inicio

    print(f'A melhor rota vai ser: [blue]{rota}[/blue]')
    print(f'O custo da rota vai ser: [yellow]{custo}[/yellow]')
    print(f"Tempo de execução: [green]{tempo_exec:.6f}[/green] segundos")

if __name__ == "__main__":
    main()