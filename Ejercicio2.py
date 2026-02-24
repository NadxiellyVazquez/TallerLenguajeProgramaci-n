def minmax(data):
    if len(data) == 0:
        raise ValueError("La secuencia debe contener al menos un número.")
 
    min_val = data[0]
    max_val = data[0]

    for val in data:
        if val < min_val:
            min_val = val
            
        if val > max_val:
            max_val = val

    return (min_val, max_val)

if __name__ == "__main__":
    datos_prueba = [15, 3, 9, 22, -4, 8, 42, 0]
    resultado = minmax(datos_prueba)
    
    print(f"La secuencia es: {datos_prueba}")
    print(f"El mínimo y máximo son: {resultado}")