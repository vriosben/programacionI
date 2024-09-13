# Se comienza el juego, le pido al usuario que elija si quiere jugar, le pregunto la categoria y la dificultad. Si no quiere jugar termina el juego
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

# Esta es una función que analiza la respuesta ingresada por el usuario sea válida para que no ingrese un valor incorrecto
# El upper() lo usamos para convertir todo en mayúculas para que sea uniforme
# El strip() lo usamos para eliminar cualquier espacio que el usuario pueda usar
# Imprimimos todo lo que el usuario seleccionó y que ponga una opción válida

def pedirRespuesta(mensaje, opciones):

    while True:
        respuesta = input(mensaje).strip().upper()
        if respuesta in opciones:
            return respuesta
        print(f"Por favor, ingresa una opción válida: {', '.join(opciones)}")

# Acá le pedimos al usuario que seleccione una categoría válida

def elegirCategoria():

    categoria = ['A', 'C', 'T']
    mensaje = "Ingresa la categoría:\nPodes elegir entre: A(ANIMALES), C(CIUDADES), T(TRAGOS): "
    return pedirRespuesta(mensaje, categoria)

# Acá le pedimos al usuario que seleccione un nivel válido

def elegirDificultad():
    """
    Solicita al usuario que elija un nivel de dificultad válido.
    """
    dificultad = ['F', 'M', 'D']
    mensaje = "Ingresa el nivel de dificultad:\nPuedes elegir entre: F (Fácil), M (Medio), D (Difícil): "
    return pedirRespuesta(mensaje, dificultad)



# Creo la matriz en base a la dificultad que el usuario eligió
# Fácil: 8x8, Medio: 16x16, Difícil: 32x32
# Comienzo la matriz con todas las posiciones con *

def crearMatriz(dificultad):

    largo = {'F': 8, 'M': 16, 'D': 32}
    tamaño = largo[dificultad] 
    
    matriz = []
    for fila in range(tamaño):
        matriz.append([])
        for columna in range(tamaño):
            matriz[fila].append("*")
    
    return matriz

# Defino la matriz en base a la categoría

def categoriaMatriz(matriz, categoria):

    palabras = {
        'A': ['GATO', 'PERRO', 'PEZ'],
        'C': ['QUITO', 'PARIS', 'SEUL'],
        'T': ['GIN', 'RON', 'VODKA']
    }
    palabrasEscondidas = palabras.get(categoria, [])

    for elemento in palabrasEscondidas:
        esconderPalabra(matriz, elemento)
    
# Acá escondo las palabras en la matriz que cree







#

# Llamada a la función principal para iniciar el juego
categoria, dificultad = iniciarJuego()


