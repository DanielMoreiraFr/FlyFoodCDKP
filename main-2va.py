import os
import sys
import time
from rich import print
from rich.panel import Panel
from va2.ag import algoritmo_genetico

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# arquivo padrao; para trocar sem editar o codigo: python main-2va.py matrizes/matriz5.txt
ARQUIVO_PADRAO = 'matrizes/matriz10.txt'

# melhores custos conhecidos (TSPLIB) para mostrar o erro percentual
OTIMOS = {'edgesbrasil58.tsp': 25395, 'brazil58.tsp': 25395}

# parametros por tipo de instancia: o Brasil 58 precisa de bem mais do que os mapas pequenos
PARAMS_MAPA = dict(tam_pop=100, geracoes=200, taxa_mutacao=0.1)
PARAMS_TSP = dict(tam_pop=300, geracoes=10000, taxa_mutacao=0.5, log_a_cada=1000)

def resolver_caminho(caminho):
    """Aceita caminho absoluto, relativo a pasta atual ou relativo a pasta do projeto."""
    if os.path.isabs(caminho) or os.path.exists(caminho):
        return caminho
    return os.path.join(BASE_DIR, caminho)

def main():
    """
    Função principal que executa o algoritmo genético (mapa .txt ou .tsp) e imprime os resultados.
    """
    arquivo = 'matrizes/matriz9.txt'  # troque para a matriz que quiser
    nome = os.path.basename(arquivo)
    print(f'[purple]Calculando a melhor rota para [cyan]{nome}[/cyan] (algoritmo genético)...[/purple]')
    inicio = time.perf_counter()
    params = PARAMS_TSP if nome.endswith('.tsp') else PARAMS_MAPA

    rota, custo = algoritmo_genetico(arquivo, **params)
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