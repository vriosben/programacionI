import random

def crear_matriz():
# Crear la matriz
    matriz = []
    largo = 5
    for fila in range(largo):
        matriz.append([])
        for columna in range(largo):
            matriz[fila].append("*")
    return matriz

def mostrar_matriz(matriz):
# Mostrar la matriz
    for fila in range(len(matriz)):
        for columna in range(len(matriz)):
            print(matriz[fila][columna], end="     ")
        print("\n")

def esconder_palabra(palabra, matriz, coord_ocupadas):
# Esconde una palabra
    # Segun posicion sera horizontal o vertical
    # Seleccionar primera coordenada: primera fila y columna a esconder. 
    coord_palabra = []
    posicion = random.randint(0,1)
    if posicion == 0:
    #Si posicion es 0, esconde horizontal
        # Genera primera coordenada aleatoria: fila y columna
        fila_coord = random.randint(0, len(matriz)-1)
        columna_coord = random.randint(0, len(matriz)-len(palabra))
        # Genera el resto coordenadas de la palabra
        for i in range(len(palabra)): 
            coord_palabra.append((fila_coord, columna_coord + i))
    else:
    #Si posicion es 1, esconde vertical
        # Genera primera coordenada aleatoria: fila y columna
        fila_coord = random.randint(0, len(matriz)-len(palabra))
        columna_coord = random.randint(0, len(matriz)-1)
        # Genera el resto coordenadas de la palabra
        for i in range(len(palabra)): 
            coord_palabra.append((fila_coord + i, columna_coord))
    
    # Verificar si las coordenadas estan libres antes de esconder la palabra
    # Con la intereseccion de la lista de coordenadas de la palabra convertida en conjunto y el conjunto de todas las coordenadas ocupadas veo si hay elementos repetidos.
    if not set(coord_palabra) & coord_ocupadas:
    # Si las coordenadas estan libres, esconder cada letra empezando por la primera coordenada. 
        for letra in palabra:
            if posicion == 0: 
            # Si es horizontal, voy aumentando la columna. La fila es la misma.   
                matriz[fila_coord][columna_coord] = letra
                columna_coord += 1        
            else:
            # Si es vertical, voy aumentando la fila. La columna es la misma.  
                matriz[fila_coord][columna_coord] = letra
                fila_coord += 1
        return coord_palabra, posicion 
    # Si no estan libres, vuelvo a intentar esconder en otras coordenadas aleatorias llamando otra vez la funcion
    else:
        return esconder_palabra(palabra, matriz, coord_ocupadas)
       
def guardar_respuesta(coord_palabra,posicion):
    # Guardo las respuestas a medida que escondo las palabras para despues compararlas con las ingresadas por el usuario
    # Armo un diccionario con las respuestas. Sera un diccionario con un diccionario anidado adentro por cada palabra y su informacion 
    palabra = {}
    
    if posicion == 0:
        direccion = "h"
    else:
        direccion = "v"

    fila_inicial,columna_inicial = coord_palabra[0]

    palabra["direccion"] = direccion
    palabra["fila_inicial"] = fila_inicial
    palabra["columna_inicial"] = columna_inicial
    palabra["coordenadas"] = coord_palabra

    return palabra

def mostrar_respuestas(respuestas):
    # Muestra el diccionario de respuestas. No tiene mucha utilidad pero veo si todo esta guardado ok
    for palabra in respuestas.keys():
        print(palabra)
        for dato,valor in respuestas[palabra].items():
            print(f"\t{dato}: {valor}")

def main():
    # Creo la sopa
    sopa = crear_matriz()
    # guardo todas las coordenadas con palabras para no sobreescribir
    coord_ocupadas = set()
    # palabras a esconder
    palabras = ["gato", "pato", "ave"]
    # datos de donde quedaron escondidas las palabras
    respuestas = {}
    # Recorro cada palabra a esconder
    for palabra in palabras:
        # Obtengo las coordenas de la palabra ya escondida y su posicion
        coord_palabra,posicion = esconder_palabra(palabra,sopa,coord_ocupadas)
        # Agrego la respuesta de esa palabra al diccionario
        respuestas[palabra] = guardar_respuesta(coord_palabra,posicion)
        # Incluyo las coordenas de la palabra en el conjunto de coordenas ocupadas para no sobreescribir
        coord_ocupadas.update(coord_palabra)

    # La sopa
    mostrar_matriz(sopa)

    # Ejemplo de como se podria pedir la respuesta. Iria en otra funcion. Estaria bueno marcar en la sopa como que ya la encontro y mostrar la sopa actualizada con esa palabra en mayuscula por ejemplo o algo asi. Poder decirle cuantas palabras faltan,preguntarle si encontro otra palabra etc,etc. 
    palabra_encontrada = input("Que palabra encontraste? ").lower()
    if palabra_encontrada in respuestas:
        fila_inicial = int(input("En que fila inicia la palabra? del 1 al 5: "))
        fila_inicial -=1
        columna_inicial = int(input("En que columna inicia la palabra? del 1 al 5: "))
        columna_inicial -=1
        direccion = input("Que direccion tiene? h para horizontal, v para vertical:").lower()
        if respuestas[palabra_encontrada]["direccion"] == direccion and respuestas[palabra_encontrada]["fila_inicial"] == fila_inicial and respuestas[palabra_encontrada]["columna_inicial"] == columna_inicial:
            print("Correcto! ")
        else:
            print("Incorrecto! ")
    else:
        print("No esta la palabra")

    # mostrar_respuestas(respuestas)
main()