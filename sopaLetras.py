import random
import string

# Inicia el juego, pregunta al usuario sobre continuar, categoría y dificultad
def iniciarJuego():
    opcionesJuego = ['Y', 'N']
    mensaje = "Estás listo para comenzar a jugar?\n(Ingresá 'Y' para continuar, 'N' para parar el juego en cualquier momento): "
    respuesta = pedirRespuesta(mensaje, opcionesJuego)
    
    if respuesta == 'Y':
        categoria = elegirCategoria()
        dificultad = elegirDificultad()
        print(f"Has elegido la categoría '{categoria}' con dificultad '{dificultad}'. Comienza a jugar")
        return categoria, dificultad
    else:
        print("El juego terminó.")
        return None, None

# Pide una respuesta válida al usuario
def pedirRespuesta(mensaje, opciones):
    while True:
        respuesta = input(mensaje).strip().upper()
        if respuesta in opciones:
            return respuesta
        print(f"Por favor, ingresa una opción válida: {', '.join(opciones)}")

# Permite al usuario elegir una categoría
def elegirCategoria():
    categorias = ['A', 'C', 'T']
    mensaje = "Ingresa la categoría:\nPuedes elegir entre: A(ANIMALES), C(CIUDADES), T(TRAGOS): "
    return pedirRespuesta(mensaje, categorias)

# Permite al usuario elegir un nivel de dificultad
def elegirDificultad():
    dificultades = ['F', 'M', 'D']
    mensaje = "Ingresa el nivel de dificultad:\nPuedes elegir entre: F (Fácil), M (Medio), D (Difícil): "
    return pedirRespuesta(mensaje, dificultades)

# Crea una matriz con letras aleatorias
def crearMatriz(dificultad):
    tamaños = {'F': 8, 'M': 16, 'D': 32}
    tamaño = tamaños[dificultad] 
    
    matriz = []
    for _ in range(tamaño):
        fila = [random.choice(string.ascii_uppercase) for _ in range(tamaño)]
        matriz.append(fila)
    
    return matriz

# Asigna palabras a la matriz según la categoría y las esconde
def categoriaMatriz(matriz, categoria):
    palabrasCategoria = {
        'A': ['GATO', 'PERRO', 'PEZ'],
        'C': ['QUITO', 'PARIS', 'SEUL'],
        'T': ['GIN', 'RON', 'VODKA']
    }
    
    palabrasEscondidas = palabrasCategoria.get(categoria, [])
    coord_ocupadas = set()
    respuestas = {}

    for palabra in palabrasEscondidas:
        coord_palabra, posicion = esconder_palabra(palabra, matriz, coord_ocupadas)
        respuestas[palabra] = guardar_respuesta(coord_palabra, posicion)
    
    return respuestas

# Esconde una palabra en la matriz
def esconder_palabra(palabra, matriz, coord_ocupadas):
    coord_palabra = []
    posicion = random.randint(0, 1)
    
    if posicion == 0:  # Horizontal
        fila_coord = random.randint(0, len(matriz) - 1)
        columna_coord = random.randint(0, len(matriz) - len(palabra))
        coord_palabra = [(fila_coord, columna_coord + i) for i in range(len(palabra))]
    else:  # Vertical
        fila_coord = random.randint(0, len(matriz) - len(palabra))
        columna_coord = random.randint(0, len(matriz) - 1)
        coord_palabra = [(fila_coord + i, columna_coord) for i in range(len(palabra))]
    
    if not set(coord_palabra) & coord_ocupadas:
        for i, letra in enumerate(palabra):
            fila, columna = coord_palabra[i]
            matriz[fila][columna] = letra
        
        coord_ocupadas.update(coord_palabra)
        return coord_palabra, posicion
    else:
        return esconder_palabra(palabra, matriz, coord_ocupadas)

# Guarda la respuesta sobre dónde se escondió la palabra
def guardar_respuesta(coord_palabra, posicion):
    respuesta = {}
    
    direccion = "h" if posicion == 0 else "v"
    fila_inicial, columna_inicial = coord_palabra[0]

    respuesta["direccion"] = direccion
    respuesta["fila_inicial"] = fila_inicial
    respuesta["columna_inicial"] = columna_inicial
    respuesta["coordenadas"] = coord_palabra

    return respuesta

# Muestra la matriz en un formato legible
def mostrar_matriz(matriz):
    for fila in matriz:
        print(' '.join(fila))
    print()

# Función para comprobar la respuesta del usuario
def comprobar_respuesta(respuesta_usuario, respuestas, palabra):
    if palabra in respuestas:
        datos_correctos = respuestas[palabra]
        direccion = "h" if datos_correctos["direccion"] == "h" else "v"
        fila_inicial = datos_correctos["fila_inicial"]
        columna_inicial = datos_correctos["columna_inicial"]
        
        if (respuesta_usuario["direccion"] == direccion and
            respuesta_usuario["fila_inicial"] == fila_inicial and
            respuesta_usuario["columna_inicial"] == columna_inicial):
            return True
        
    return False

# Función principal para ejecutar el juego
def main():
    categoria, dificultad = iniciarJuego()
    if categoria and dificultad:
        matriz = crearMatriz(dificultad)
        respuestas = categoriaMatriz(matriz, categoria)
        mostrar_matriz(matriz)
        
        palabras_encontradas = set()
        palabras_totales = set(respuestas.keys())
        
        while palabras_encontradas != palabras_totales:
            palabra_usuario = input("¿Qué palabra encontraste? (O ingresa 'N' para salir): ").strip().upper()
            
            if palabra_usuario == 'N':
                print("El juego ha terminado.")
                return
            
            if palabra_usuario in palabras_totales - palabras_encontradas:
                direccion = pedirRespuesta("¿Es horizontal (h) o vertical (v)? ", ['H', 'V']).lower()
                fila_inicial = int(input("¿Cuál es la posición de la fila inicial? "))
                columna_inicial = int(input("¿Cuál es la posición de la columna inicial? "))
                
                respuesta_usuario = {
                    "direccion": direccion,
                    "fila_inicial": fila_inicial,
                    "columna_inicial": columna_inicial
                }
                
                if comprobar_respuesta(respuesta_usuario, respuestas, palabra_usuario):
                    print("¡Correcto!")
                    palabras_encontradas.add(palabra_usuario)
                else:
                    print("Respuesta incorrecta. Inténtalo de nuevo.")
            else:
                print("Palabra no válida o ya encontrada. Inténtalo de nuevo.")
        
        print("¡Felicidades! Has encontrado todas las palabras.")

main()
