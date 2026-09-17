from flyfood import calc_flyfood

def main():
    rota, custo = calc_flyfood('matrix.txt')
    print(f'A melhor rota vai ser: {rota}')
    print(f'O custo da rota vai ser: {custo}')

if __name__ == "__main__":
    main()