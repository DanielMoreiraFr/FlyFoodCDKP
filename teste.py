def divisivel3(numero): 
    numero = abs(numero) # Casos base (números de um dígito) 
    if numero in (3, 6, 9, 0): 
        return True 
    elif numero < 10: 
        return False # Passo recursivo: soma dos dígitos 
    else:
        soma_digitos = sum(int(digito) for digito in str(numero))
    return divisivel3(soma_digitos)


res = divisivel3(12)
print(res)  # Saída: True, pois 123456789 é divisível por 3