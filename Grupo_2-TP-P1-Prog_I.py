# Trabajo Práctico Cuatrimestral // Proyecto Grupal (1° y 2° Parte) - 2° Cuatrimestre 2024
# Asignatura: Programación I | Algoritmos y Estructuras de Datos I
# Integrantes: Di Corrado, Candela; Morello Flores, María Laura; Ríos Benítez, Nancy Valeria
''' Especificaciones:
        → Objetivo: Sopa de Letras

    Características:
        → Pedirle al usuario que ingrese "Y" para empezar a jugar o "Ctrl + C" para salir.
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
        → Mostrar la sopa y las palabras a buscar para comenzar a jugar.
        → Solicitar las palabras encontradas por el usuario.
        → Informar el estado actual del juego después de cada palabra encontrada.
        → El usuario debe encontrar todas las palabras o ingresar "Ctrl + C" si desea salir antes del juego.
        → Informar al usuario la ubicación de las respuestas y el número de palabras encontradas, si decide finalizar antes. '''

import random
import string
import traceback
import json

class PalabraEncontradaError(Exception):
    pass

class PalabraInvalidaError(Exception):
    pass

class DatoVacioError(Exception):
    pass

# Inicia el juego y le consulta al usuario si desea continuar, la categoría y la dificultad
def iniciarJuego():
    opcionesJuego = ["Y"]
    mensaje = "¿Está listo para comenzar a jugar?\nIngrese 'Y' para continuar o 'Ctrl + C' para detener el juego en cualquier momento: "
    respuesta = pedirRespuesta(mensaje, opcionesJuego)

    if respuesta == "Y":
        categoria = elegirCategoria()
        dificultad = elegirDificultad()
        print(f"Ha elegido la categoría '{categoria}' con dificultad '{dificultad}'. ¡Comience a jugar!")
        return categoria, dificultad

# Solicita una respuesta válida al usuario
def pedirRespuesta(mensaje, opciones):
    respuesta = input(mensaje).strip().upper()
    if respuesta in opciones:
        return respuesta
    else:
        print(f"Por favor, ingrese una opción válida: {", ".join(opciones)}")
        return pedirRespuesta(mensaje, opciones)

# Permite al usuario elegir una categoría
def elegirCategoria():
    categorias = ["A", "C", "T"]
    mensaje = "Ingrese la categoría.\nPuede elegir entre: A (Animales), C (Ciudades) o T (Tragos): "
    return pedirRespuesta(mensaje, categorias)

# Permite al usuario elegir un nivel de dificultad
def elegirDificultad():
    dificultades = ["F", "M", "D"]
    mensaje = "Introduzca el nivel de dificultad.\nPuede elegir entre: F (Fácil), M (Medio) o D (Difícil): "
    return pedirRespuesta(mensaje, dificultades)

# Crea la matriz con letras aleatorias
def crearMatriz(dificultad):
    tamaños = {"F": 8, "M": 12, "D": 18}
    tamaño = tamaños[dificultad]

    matriz = []
    for fila in range(tamaño):
        matriz.append([])
        for columna in range(tamaño):
            matriz[fila].append(random.choice(string.ascii_uppercase))
    return matriz

# Se le asignan palabras a la matriz, según la categoría; las oculta y devuelve las respuestas.
def generarJuego(matriz, categoria):
    palabras = leerJSON("palabras.json")
    if palabras is None:
        raise DatoVacioError("El juego no se ha podido incializar porque es imposible acceder al archivo de palabras.")

    for item in palabras:
        if item["categoria"] == categoria:
            palabrasCategoria = item["palabras"]

    palabrasEscondidas = list(seleccionarPalabras(palabrasCategoria, matriz))

    coordOcupadas = set()
    respuestas = {}

    for palabra in palabrasEscondidas:
        coordPalabra, posicion = esconderPalabra(palabra, matriz, coordOcupadas)
        respuestas[palabra] = guardarRespuesta(coordPalabra, posicion)
    return respuestas

# Selecciona las palabras a esconder, según la matriz y la categoría
def seleccionarPalabras(palabrasCategoria, matriz):
    palabrasEscondidas = set()
    while len(palabrasEscondidas) != (len(matriz) // 2):
        indice = random.randint(0, len(palabrasCategoria) - 1)
        if len(palabrasCategoria[indice]) <= len(matriz):
            palabrasEscondidas.add(palabrasCategoria[indice])

    return palabrasEscondidas

# Esconde una palabra en la matriz
def esconderPalabra(palabra, matriz, coordOcupadas):
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
    else:
        return esconderPalabra(palabra, matriz, coordOcupadas)

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
        print(" ".join(fila))
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
def pedirPalabra(matriz, palabrasTotales, palabrasEncontradas):
    palabraUsuario = input("¿Qué palabra encontraste? (Ingrese 'R' para rendirse o 'Ctrl + C' para salir del juego): ").strip().upper()

    if palabraUsuario not in palabrasTotales and palabraUsuario != "R":
        raise PalabraInvalidaError(f"La palabra ingresada '{palabraUsuario}' no es una de las palabras ocultas en la sopa de letras. Reintentar.")

    if palabraUsuario in palabrasEncontradas:
        raise PalabraEncontradaError(f"La palabra ingresada '{palabraUsuario}' ya fue encontrada. Reintentar.")

    if palabraUsuario == "R":
        return palabraUsuario, None

    else:
        opcionesFilaColumna = [str(i + 1) for i in range(len(matriz))]
        direccion = pedirRespuesta("¿Es horizontal (H) o vertical (V)?: ", ["H", "V"]).upper()
        filaInicial = int(pedirRespuesta(f"¿En qué número de fila comienza? (1-{len(matriz)}): ", opcionesFilaColumna)) - 1
        columnaInicial = int(pedirRespuesta(f"¿En qué número de columna comienza? (1-{len(matriz)}): ", opcionesFilaColumna)) - 1

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

# Archivos JSON
def leerJSON(ubicacion):
    try:
        with open(ubicacion, "r") as f:
            contenido = f.read().strip()
            if not contenido:
                return []

            f.seek(0)
            return json.load(f)

    except FileNotFoundError:
        print("No se encuentra el archivo.")
        return None
    except json.JSONDecodeError:
        print("El formato JSON del archivo es inválido.")
        return None

def escribirJSON(ubicacion, datos):
    try:
        with open(ubicacion, "w") as f:
            json.dump(datos, f, indent = 4)
    except FileNotFoundError:
        print("No se encuentra el archivo.")

# Manejo de errores (Excepciones)
def registrarError(e, ubicacion = "log_errores.json"):
    errorInfo = traceback.format_exc()
    errorPila = traceback.extract_tb(e.__traceback__)

    error = {
            "tipo": e.__class__.__name__,
            "detalles": errorInfo,
            "ultima traza": {"linea": errorPila[-1].lineno,
                            "funcion": errorPila[-1].name,
                            "contexto": errorPila[-1].line.strip()}
            }

    listaErrores = leerJSON(ubicacion)
    if listaErrores is None:
        print("No se pudo guardar el error.")
        return

    listaErrores.append(error)
    escribirJSON(ubicacion, listaErrores)

# Se evalúa si existe una partida ya iniciada del juego
def detectarJuegoPrevio():
    juegoPrevio = leerJSON("estado_sopa.json")

    if juegoPrevio:
        mensaje = "Se ha encontrado un juego previo sin finalizar.\nIngrese 'V' para volver al juego anterior o 'N' para empezar un juego nuevo: "
        opcionesJuego = ["V", "N"]
        respuesta = pedirRespuesta(mensaje, opcionesJuego)
        return respuesta
    else:
        return "N"

# Se inicia la partida ya existente del juego
def iniciarJuegoPrevio():
    juegoPrevio = leerJSON("estado_sopa.json")
    matriz = juegoPrevio[0]["matriz"]
    respuestas = juegoPrevio[0]["respuestas"]
    matrizRespuestas = juegoPrevio[0]["matrizRespuestas"]
    palabrasTotales = set(juegoPrevio[0]["palabrasTotales"])
    palabrasEncontradas = set(juegoPrevio[0]["palabrasEncontradas"])
    return matriz, respuestas, matrizRespuestas, palabrasTotales, palabrasEncontradas

# Registra el estado actual de la sopa de letras
def registrarEstado(matriz, respuestas, matrizRespuestas, palabrasTotales, palabrasEncontradas):
    ubicacion = "estado_sopa.json"

    estadoJuego = [{
        "matriz": matriz,
        "respuestas": respuestas,
        "matrizRespuestas": matrizRespuestas,
        "palabrasTotales": list(palabrasTotales),
        "palabrasEncontradas": list(palabrasEncontradas)
    }]

    escribirJSON(ubicacion, estadoJuego)

# Realiza la limpieza de la sopa de letras; es decir, permite que esté disponible para iniciar una nueva partida
def limpiarEstado():
    ubicacion = "estado_sopa.json"
    try:
        with open(ubicacion, "w") as f:
            f.write("")
    except FileNotFoundError:
        print("No se pudo encontrar el archivo.")

# Programa Principal → Función para ejecutar el juego
def main():
    try:
        juego = detectarJuegoPrevio()
        if juego == "V":
            matriz, respuestas, matrizRespuestas, palabrasTotales, palabrasEncontradas = iniciarJuegoPrevio()
            mostrarEstadoJuego(palabrasTotales, palabrasEncontradas, matriz)
        else:
            categoria, dificultad = iniciarJuego()
            if categoria and dificultad:
                matriz = crearMatriz(dificultad)
                respuestas = generarJuego(matriz, categoria)
                palabrasTotales = set(respuestas.keys())
                matrizRespuestas = crearMatrizRespuesta(matriz, respuestas, palabrasTotales)
                palabrasEncontradas = set()

                registrarEstado(matriz, respuestas, matrizRespuestas, palabrasTotales, palabrasEncontradas)

                mostrarPalabrasEscondidas(palabrasTotales)
                mostrarMatriz(matriz)

        while palabrasEncontradas != palabrasTotales:
            try:
                palabraUsuario, respuestaUsuario = pedirPalabra(matriz, palabrasTotales, palabrasEncontradas)
            except (PalabraInvalidaError, PalabraEncontradaError) as e:
                print(e)
                continue

            if palabraUsuario == "R":
                finalizarJuego(palabrasEncontradas, palabrasTotales, matrizRespuestas)
                limpiarEstado()
                return

            if palabraUsuario in palabrasTotales - palabrasEncontradas:
                if comprobarRespuesta(respuestaUsuario, respuestas, palabraUsuario):
                    palabrasEncontradas.add(palabraUsuario)
                    for fila, columna in respuestas[palabraUsuario]["coordenadas"]:
                        matriz[fila][columna] = "-"
                    registrarEstado(matriz, respuestas, matrizRespuestas, palabrasTotales, palabrasEncontradas)
                    print("¡Correcto!")
                else:
                    print("Respuesta incorrecta. Inténtelo de nuevo.")

            else:
                print(f"Palabra no válida o ya encontrada. Inténtelo de nuevo.")

            mostrarEstadoJuego(palabrasTotales, palabrasEncontradas, matriz)
        print("¡Felicidades! Ha encontrado todas las palabras.")

    except DatoVacioError as e:
        print(e)

    except (ValueError, TypeError, IndexError) as e:
        print("Ocurrió un error inesperado. El juego se ha cerrado.")
        registrarError(e)

    except KeyboardInterrupt:
        print("\nHa abandonado el juego. ¡Adiós!")

main()