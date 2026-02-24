import random

class Animal:
    def __init__(self):
        self.se_ha_movido = False

class Oso(Animal):
    def __str__(self):
        return "O"

class Pez(Animal):
    def __str__(self):
        return "P"

class Ecosistema:
    def __init__(self, tamano, num_osos, num_peces):
        self.tamano = tamano
        self.rio = [None] * tamano
        
        posiciones_vacias = list(range(tamano))
        random.shuffle(posiciones_vacias)
        
        for _ in range(num_osos):
            if posiciones_vacias:
                self.rio[posiciones_vacias.pop()] = Oso()
                
        for _ in range(num_peces):
            if posiciones_vacias:
                self.rio[posiciones_vacias.pop()] = Pez()

    def mostrar_rio(self):
        estado = "".join([str(animal) if animal is not None else "-" for animal in self.rio])
        print(estado)

    def obtener_posiciones_vacias(self):
        return [i for i, animal in enumerate(self.rio) if animal is None]

    def paso_de_tiempo(self):
        for animal in self.rio:
            if animal is not None:
                animal.se_ha_movido = False

        for i in range(self.tamano):
            animal_actual = self.rio[i]

            if animal_actual is None or animal_actual.se_ha_movido:
                continue

            movimiento = random.choice([-1, 0, 1])
            
            if movimiento == 0:
                animal_actual.se_ha_movido = True
                continue
                
            nueva_posicion = i + movimiento

            if 0 <= nueva_posicion < self.tamano:
                animal_objetivo = self.rio[nueva_posicion]

                if animal_objetivo is None:
                    self.rio[nueva_posicion] = animal_actual
                    self.rio[i] = None
                    animal_actual.se_ha_movido = True

                elif type(animal_actual) == type(animal_objetivo):
                    animal_actual.se_ha_movido = True
                    animal_objetivo.se_ha_movido = True
                    
                    posiciones_vacias = self.obtener_posiciones_vacias()
                    if posiciones_vacias:
                        nueva_pos = random.choice(posiciones_vacias)
                        if isinstance(animal_actual, Oso):
                            self.rio[nueva_pos] = Oso()
                        else:
                            self.rio[nueva_pos] = Pez()
                            
                else:
                    if isinstance(animal_actual, Oso):
                        self.rio[nueva_posicion] = animal_actual
                        self.rio[i] = None
                    else:
                        self.rio[i] = None
                        
                    animal_actual.se_ha_movido = True

if __name__ == "__main__":
    mi_ecosistema = Ecosistema(tamano=20, num_osos=3, num_peces=7)
    
    print("Estado inicial:")
    mi_ecosistema.mostrar_rio()
    print("-" * 25)
    
    pasos = 10
    for paso in range(1, pasos + 1):
        mi_ecosistema.paso_de_tiempo()
        print(f"Paso {paso}:")
        mi_ecosistema.mostrar_rio()