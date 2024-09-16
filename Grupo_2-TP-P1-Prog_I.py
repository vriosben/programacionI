# Trabajo Práctico Cuatrimestral // Proyecto Grupal (1° Parte) - 2° Cuatrimestre 2024
# Asignatura: Programación I | Algoritmos y Estructuras de Datos I
# Integrantes: Di Corrado, Candela; Morello Flores, María Laura; Ríos Benítez, Nancy Valeria
''' Especificaciones:
        → Objetivo: Sopa de Letras
    Características:    
        → Pedirle al usuario que ingrese "Y" para empezar a jugar, "N" para terminar.
        → Elegir el tamaño de la matriz según el nivel de dificultad:
            * Fácil (8x8)
            * Medio (12x12)
            * Difícil (18x18)
        → Elegir las palabras aleatorias a esconder según la categoría y el tamaño:
            * Ciudades
            * Animales
            * Tragos
        → Esconder las palabras aleatoriamente en la matriz, de manera horizontal o vertical.
        → Rellenar las palabras restantes con letras random.
        → Mostrar la sopa y las palabras a buscar para empezar a jugar.
        → Solicitar las palabras encontradas por el usuario.
        → Informar el estado actual del juego después de cada palabra encontrada.
        → El usuario debe encontrar todas las palabras o ingresar "N" si desea finalizar el juego antes.
        → Informar al usuario la ubicación de las respuestas y el número de palabras encontradas, si decide finalizar antes. '''

import random
import string

# Inicia el juego y le consulta al usuario si desea continuar, la categoría y la dificultad
def iniciarJuego():
    opcionesJuego = ['Y', 'N']
    mensaje = "¿Está listo para comenzar a jugar?\n(Ingrese 'Y' para continuar o 'N' para detener el juego en cualquier momento): "
    respuesta = pedirRespuesta(mensaje, opcionesJuego)

    if respuesta == 'Y':
        categoria = elegirCategoria()
        dificultad = elegirDificultad()
        print(f"Ha elegido la categoría '{categoria}' con dificultad '{dificultad}'. ¡Comience a jugar!")
        return categoria, dificultad
    else:
        print("El juego ha finalizado.")
        return None, None

# Solicita una respuesta válida al usuario
def pedirRespuesta(mensaje, opciones):
    while True:
        respuesta = input(mensaje).strip().upper()
        if respuesta in opciones:
            return respuesta
        print(f"Por favor, ingrese una opción válida: {', '.join(opciones)}")

# Permite al usuario elegir una categoría
def elegirCategoria():
    categorias = ['A', 'C', 'T']
    mensaje = "Ingrese la categoría.\nPuede elegir entre: A (Animales), C (Ciudades), T (Tragos): "
    return pedirRespuesta(mensaje, categorias)

# Permite al usuario elegir un nivel de dificultad
def elegirDificultad():
    dificultades = ['F', 'M', 'D']
    mensaje = "Introduzca el nivel de dificultad.\nPuede elegir entre: F (Fácil), M (Medio), D (Difícil): "
    return pedirRespuesta(mensaje, dificultades)

# Crea la matriz con letras aleatorias
def crearMatriz(dificultad):
    tamaños = {'F': 8, 'M': 12, 'D': 18}
    tamaño = tamaños[dificultad]

    matriz = []
    for fila in range(tamaño):
        matriz.append([])
        for columna in range(tamaño):
            matriz[fila].append(random.choice(string.ascii_uppercase))
    return matriz

# Se le asignan palabras a la matriz, según la categoría; las oculta y devuelve las respuestas.
def generarJuego(matriz, categoria):
    palabrasCategoria = {
        'A': ['GATO', 'PERRO', 'PEZ', 'CABALLO', 'VACA', 'OVEJA', 'PATO', 'GALLINA', 'LORO', 'PANDA', 'JIRAFA', 'LEÓN', 'TIGRE', 'ZEBRA', 'ELEFANTE', 'RINOCERONTE', 'OSO', 'COBRA', 'SERPIENTE', 'CANGREJO', 'TIBURÓN'],
        'C': ['QUITO', 'PARÍS', 'SEÚL', 'LONDRES', 'MADRID', 'BERLÍN', 'ROMA', 'TOKIO', 'PEKÍN', 'MÉXICO', 'MOSCÚ', 'FLORIDA', 'FLORENCIA', 'BOGOTÁ', 'CARACAS', 'EDIMBURGO', 'BRASILIA', 'LISBOA', 'PRAGA', 'VIENA'],
        'T': ['GIN', 'RON', 'VODKA', 'TEQUILA', 'WHISKY', 'RUM', 'BRANDY', 'COGNAC', 'CHAMPAGNE', 'APEROL', 'MARTINI', 'MOJITO', 'DAIQUIRI', 'NEGRONI', 'MANHATTAN', 'DESTORNILLADOR', 'FERNET', 'SANGRÍA', 'MARGARITA', 'CAIPIRINHA']
    }

    palabrasTotales = palabrasCategoria.get(categoria, [])
    palabrasEscondidas = list(seleccionarPalabras(palabrasTotales, matriz))

    coordOcupadas = set()
    respuestas = {}

    for palabra in palabrasEscondidas:
        coordPalabra, posicion = esconderPalabra(palabra, matriz, coordOcupadas)
        respuestas[palabra] = guardarRespuesta(coordPalabra, posicion)
    return respuestas

# Selecciona las palabras a esconder, según la matriz y la categoría
def seleccionarPalabras(palabrasTotales, matriz):
    palabrasEscondidas = set()
    while len(palabrasEscondidas) != (len(matriz) // 2):
        indice = random.randint(0, len(palabrasTotales) - 1)
        if len(palabrasTotales[indice]) <= len(matriz):
            palabrasEscondidas.add(palabrasTotales[indice])

    return palabrasEscondidas

# Esconde una palabra en la matriz
def esconderPalabra(palabra, matriz, coordOcupadas):
    while True:
        posicion = random.randint(0, 1)

        if posicion == 0:   # Horizontal
            filaCoord = random.randint(0, len(matriz) - 1)
            columnaCoord = random.randint(0, len(matriz) - len(palabra))
            coordPalabra = [(filaCoord, columnaCoord + i) for i in range(len(palabra))]
        else:   # Vertical
            filaCoord = random.randint(0, len(matriz) - len(palabra))
            columnaCoord = random.randint(0, len(matriz) - 1)
            coordPalabra = [(filaCoord + i, columnaCoord) for i in range(len(palabra))]

        if not set(coordPalabra) & coordOcupadas:
            for letra in palabra:
                if posicion == 0:
                    matriz[filaCoord][columnaCoord] = letra
                    columnaCoord += 1
                else:
                    matriz[filaCoord][columnaCoord] = letra
                    filaCoord += 1

            coordOcupadas.update(coordPalabra)
            return coordPalabra, posicion

# Guarda la respuesta de la posición en la que está oculta la palabra
def guardarRespuesta(coordPalabra, posicion):
    respuesta = {}

    direccion = "H" if posicion == 0 else "V"
    filaInicial, columnaInicial = coordPalabra[0]

    respuesta["direccion"] = direccion
    respuesta["filaInicial"] = filaInicial
    respuesta["columnaInicial"] = columnaInicial
    respuesta["coordenadas"] = coordPalabra

    return respuesta

# Expone la matriz en un formato legible
def mostrarMatriz(matriz):
    print()
    for fila in matriz:
        print(' '.join(fila))
    print()

# Función para imprimir las palabras dentro de un conjunto
def mostrarPalabrasEscondidas(conjunto):
    print("\nPalabras escondidas:\n")
    for palabra in conjunto:
        print("\t", palabra)

# Crea una matriz donde sólo se muestran las palabras escondidas y el resto lo reemplaza con el asterisco (*)
def crearMatrizRespuesta(matriz, respuestas, palabrasTotales):
    matrizRespuestas = [list(fila) for fila in matriz]

    coordRespuestas = set()
    for palabra in palabrasTotales:
        coordRespuestas.update(respuestas[palabra]["coordenadas"])

    for fila in range(len(matrizRespuestas)):
        for columna in range(len(matrizRespuestas)):
            if (fila, columna) not in coordRespuestas:
                matrizRespuestas[fila][columna] = "*"

    return matrizRespuestas

# Informa la cantidad y las palabras que faltan encontrar y exhibe el estado actual de la matriz
def mostrarEstadoJuego(palabrasTotales, palabrasEncontradas, matriz):
    palabrasRestantes = palabrasTotales - palabrasEncontradas
    cantidadRestantes = len(palabrasRestantes)

    print(f"Palabras restantes: {cantidadRestantes}")
    mostrarPalabrasEscondidas(palabrasRestantes)
    mostrarMatriz(matriz)

# Función para solicitar las respuestas del usuario
def pedirPalabra(matriz):
    palabraUsuario = input("¿Qué palabra encontraste? (O ingrese 'N' para salir): ").strip().upper()

    if palabraUsuario == 'N':
        return palabraUsuario, None

    else:
        opcionesFilaColumna = [str(i + 1) for i in range(len(matriz))]
        direccion = pedirRespuesta("¿Es horizontal (H) o vertical (V)?: ", ['H', 'V']).upper()
        filaInicial = int(pedirRespuesta(f"¿En qué número de fila comienza?: (1-{len(matriz)}): ", opcionesFilaColumna)) - 1
        columnaInicial = int(pedirRespuesta(f"¿En qué número de columna comienza?: (1-{len(matriz)}): ", opcionesFilaColumna)) - 1

        respuestaUsuario = {
            "direccion": direccion,
            "filaInicial": filaInicial,
            "columnaInicial": columnaInicial
        }
        return palabraUsuario, respuestaUsuario

# Función para comprobar la respuesta del usuario
def comprobarRespuesta(respuestaUsuario, respuestas, palabra):
    if palabra in respuestas:
        datosCorrectos = respuestas[palabra]
        direccion = "H" if datosCorrectos["direccion"] == "H" else "V"
        filaInicial = datosCorrectos["filaInicial"]
        columnaInicial = datosCorrectos["columnaInicial"]

        if (respuestaUsuario["direccion"] == direccion and
            respuestaUsuario["filaInicial"] == filaInicial and
            respuestaUsuario["columnaInicial"] == columnaInicial):
            return True

    return False

# Informa las palabras encontradas y muestra las respuestas
def finalizarJuego(palabrasEncontradas, palabrasTotales, matrizRespuestas):
    print(f"El juego ha terminado.\nTotal de palabras encontradas: {len(palabrasEncontradas)}/{len(palabrasTotales)}")
    print("Respuestas: ")
    mostrarMatriz(matrizRespuestas)

# Programa Principal → Función para ejecutar el juego
def main():
    categoria, dificultad = iniciarJuego()
    if categoria and dificultad:
        matriz = crearMatriz(dificultad)
        respuestas = generarJuego(matriz, categoria)
        palabrasTotales = set(respuestas.keys())
        matrizRespuestas = crearMatrizRespuesta(matriz, respuestas, palabrasTotales)

        mostrarPalabrasEscondidas(palabrasTotales)
        mostrarMatriz(matriz)
        palabrasEncontradas = set()

        while palabrasEncontradas != palabrasTotales:
            palabraUsuario, respuestaUsuario = pedirPalabra(matriz)

            if palabraUsuario == 'N':
                finalizarJuego(palabrasEncontradas, palabrasTotales, matrizRespuestas)
                return

            if palabraUsuario in palabrasTotales - palabrasEncontradas:
                if comprobarRespuesta(respuestaUsuario, respuestas, palabraUsuario):
                    palabrasEncontradas.add(palabraUsuario)
                    for fila, columna in respuestas[palabraUsuario]["coordenadas"]:
                        matriz[fila][columna] = "-"
                    print("¡Correcto!")
                else:
                    print("Respuesta incorrecta. Inténtelo de nuevo.")

            else:
                print(f"Palabra no válida o ya encontrada. Inténtelo de nuevo.")

            mostrarEstadoJuego(palabrasTotales, palabrasEncontradas, matriz)
        print("¡Felicidades! Ha encontrado todas las palabras.")

main()