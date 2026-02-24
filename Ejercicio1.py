def is_even(k):
    return (k & 1) == 0

if __name__ == "__main__":
    numeros_prueba = [0, 1, 2, 10, 15, -4, -7]
    for n in numeros_prueba:
        resultado = is_even(n)
        print(f"¿Es {n} par? {resultado}")