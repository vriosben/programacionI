# Trabajo Práctico Cuatrimestral // Proyecto Grupal (2° Parte) - 2° Cuatrimestre 2024
# Asignatura: Programación I | Algoritmos y Estructuras de Datos I
# Integrantes: Di Corrado, Candela; Morello Flores, María Laura; Ríos Benítez, Nancy Valeria
''' Especificaciones:
        → Objetivo: Sopa de Letras
    Características:    
        → Pedirle al usuario que ingrese "Y" para empezar a jugar o "Ctrl + C" para salir. 
        → Podrá salir con "Ctrl + C" en cualquier momento del juego y se guardará el estado del juego.
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
        → El usuario debe encontrar todas las palabras o ingresar "R" si desea rendirse y finalizar el juego antes.
        → Informar al usuario la ubicación de las respuestas si decide finalizar antes. 
        → Tanto el encontrar todas las palabras como al rendirse, se muestra la cantidad de palabras encontradas y la puntuación obtenida. 
        → Si el jugador obtiene una puntuación maxima, se registra en el ranking de puntuaciones.
        → Antes de finalizar, se le da la opcion al jugador de ver el ranking de puntuaciones.
        → El jugador tendrá la opcion de retomar el juego previo si decidio salir mediante "Ctrl + C" antes de rendirse o encontrar todas las palabras.
        → Extra para el programador: log que registra los errores que afectaron al jugador. 
        '''
import random
import string
import traceback
import json

class PalabraEncontradaError(Exception):
    pass

class PalabraInvalidaError(Exception):
    pass

class archivoPalabrasError(Exception):
    pass

# Inicia el juego y le consulta al usuario si desea continuar, la categoría y la dificultad
def iniciarJuego():
    opcionesJuego = ['Y']
    mensaje = "¿Está listo para comenzar a jugar?\n(Ingrese 'Y' para continuar o 'ctrl+c' para salir del juego en cualquier momento): "
    respuesta = pedirRespuesta(mensaje, opcionesJuego)

    if respuesta == 'Y':
        categoria = elegirCategoria()
        dificultad = elegirDificultad()
        print(f"Ha elegido la categoría '{categoria}' con dificultad '{dificultad}'. ¡Comience a jugar!")
        return categoria, dificultad

# Solicita una respuesta válida al usuario
def pedirRespuesta(mensaje, opciones):
    respuesta = input(mensaje).strip().upper()
    try:
        if respuesta in opciones:   
            return respuesta
        else:                       
            print(f"Por favor, ingresa una opción válida: {', '.join(opciones)}")
        return pedirRespuesta(mensaje, opciones)
    except RecursionError as e:
        registrarError(e)
        print("Demasiados intentos fallidos.")

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
    palabras = leerJson('palabras.json')
    if not palabras:
        raise archivoPalabrasError("No se pudo inicializar el juego porque ocurrió un error al acceder al archivo de palabras. ")
    
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
    try:
        posicion = random.randint(0, 1)
        
        if posicion == 0:  # Horizontal
            filaCoord = random.randint(0, len(matriz) - 1)
            columnaCoord = random.randint(0, len(matriz) - len(palabra))
            coordPalabra = [(filaCoord, columnaCoord + i) for i in range(len(palabra))] 
        else:  # Vertical
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
    except RecursionError as e:
        registrarError(e)
        print("Demasiados intentos fallidos.")

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
def pedirPalabra(matriz, palabrasTotales, palabrasEncontradas):
    palabraUsuario = input("¿Qué palabra encontraste? (O ingrese 'R' para rendirte, 'ctrl+c' para salir y continuar más tarde): ").strip().upper()
    
    if palabraUsuario not in palabrasTotales and palabraUsuario != 'R':
        raise PalabraInvalidaError(f"La palabra ingresada '{palabraUsuario}' no es una de las pabras ocultas en la sopa de letras. Reintentar.")

    if palabraUsuario in palabrasEncontradas:
        raise PalabraEncontradaError(f"La palabra ingresada '{palabraUsuario}' ya fue encontrada. Reintentar.")   
    
    if palabraUsuario == 'R':
        return palabraUsuario, None

    else:
        opcionesFilaColumna = [str(i + 1) for i in range(len(matriz))]
        direccion = pedirRespuesta("¿Es horizontal (H) o vertical (V)?: ", ['H', 'V']).upper()
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

# Finaliza el juego, mostrando las palabras encontradas y la puntuación final. Actualiza el ranking de puntuaciones y limpia el estado del juego guardado.
def finalizarJuego(palabrasEncontradas, palabrasTotales, intentos, dificultad):
    puntuacion = puntuar(palabrasEncontradas, palabrasTotales, intentos, dificultad)
    print(f"El juego ha terminado.\nTotal de palabras encontradas: {len(palabrasEncontradas)}/{len(palabrasTotales)}")
    print(f"Puntuación final: {puntuacion}")
    try:
        comprobarHighscores(puntuacion)
        mostrarHighscores()
    except (ValueError, TypeError, IndexError) as e:
        print("Hay un problema con el ranking de puntuaciones. Imposible guardar o acceder al ranking. Intente más tarde.")
        registrarError(e)
    finally:
        limpiarEstado() 

# Lee un archivo JSON y devuelve el contenido como una lista. Si el archivo está vacío devuelve una lista vacia, si no existe o el formato está mal, maneja excepciones.
def leerJson(ubicacion):
    try:
        with open(ubicacion, 'r') as f:
            contenido = f.read().strip()
            if not contenido:  
                return []  
            
            f.seek(0)  
            return json.load(f) 

    except FileNotFoundError as e:
        print("No se pudo encontrar el archivo.") 
        return None
    
    except json.JSONDecodeError as e:
        print("El formato JSON del archivo es inválido.")
        return None
        
# Escribe los datos proporcionados en un archivo JSON
def escribirJson(ubicacion, datos):
   with open(ubicacion, 'w') as f:
        json.dump(datos, f, indent = 4)

# Registra un error en un archivo de log en formato JSON, incluyendo detalles sobre el tipo de error y su traza.
def registrarError(e):
    ubicacion = "log_errores.json"   
    errorInfo = traceback.format_exc()
    errorPila = traceback.extract_tb(e._traceback_)            
    
    error = {
            "tipo":e._class.name_ ,
            "detalles":errorInfo, 
            "ultima traza": {"linea": str(errorPila[-1].lineno),"funcion": errorPila[-1].name,"contexto": errorPila[-1].line.strip()}               
            }
    
    listaErrores = leerJson(ubicacion)
    if listaErrores is None:
        print("No se pudo guardar el error.")
        return
    listaErrores.append(error)

    escribirJson(ubicacion, listaErrores)


# Se evalúa si existe una partida ya iniciada del juego, revisando el archivo JSON de estado del juego. Si es así, pregunta al usuario si quiere continuar el juego anterior o comenzar uno nuevo.
def detectarJuegoPrevio():
    juegoPrevio = leerJson('estado_sopa.json')
    
    if juegoPrevio:
        mensaje = "Se ha encontrado un juego previo sin finalizar.\nIngrese 'V' para volver al juego anterior o 'N' para empezar un juego nuevo: "
        opcionesJuego = ['V','N']
        respuesta = pedirRespuesta(mensaje, opcionesJuego)
        return respuesta
    else:
        return 'N'

# Se inicia la partida ya existente del juego, restaurando el estado guardado en el archivo JSON.
def iniciarJuegoPrevio():
    juegoPrevio = leerJson('estado_sopa.json')
    matriz = juegoPrevio[0]["matriz"]
    respuestas = juegoPrevio[0]["respuestas"]
    matrizRespuestas = juegoPrevio[0]["matrizRespuestas"]
    palabrasTotales = set(juegoPrevio[0]["palabrasTotales"])
    palabrasEncontradas = set(juegoPrevio[0]["palabrasEncontradas"])
    dificultad = juegoPrevio[0]["dificultad"]
    intentos = int(juegoPrevio[0]["intentos"])
    return matriz, respuestas, matrizRespuestas, palabrasTotales, palabrasEncontradas, dificultad, intentos 

# Guarda el estado del juego en el archivo JSON.
def registrarEstado(matriz, respuestas, matrizRespuestas, palabrasTotales, palabrasEncontradas, dificultad, intentos):
    ubicacion = 'estado_sopa.json'

    estadoJuego = [{
        "matriz": matriz,
        "respuestas": respuestas,
        "matrizRespuestas":matrizRespuestas,
        "palabrasTotales": list(palabrasTotales),
        "palabrasEncontradas": list(palabrasEncontradas),
        "intentos":str(intentos),
        "dificultad":dificultad
    }]

    escribirJson(ubicacion, estadoJuego)

# Borra todo el estado del juego guardado en el archivo JSON.
def limpiarEstado():
    ubicacion = 'estado_sopa.json'
    
    with open(ubicacion, 'w') as f:
            f.write("") 

# Calcula la puntuación basada en el número de palabras encontradas, la cantidad de intentos y la dificultad del juego.
def puntuar(palabrasEncontradas, palabrasTotales, intentos, dificultad):
    aciertos = len(palabrasEncontradas)
    puntuacion = aciertos*100
    if aciertos == len(palabrasTotales):
        if intentos == aciertos:
            puntuacion += 1000
        elif intentos <= round(aciertos*1.5):  
            puntuacion += 500  
        elif intentos <= aciertos*2:
            puntuacion += 250  

    if dificultad == "M":
        puntuacion = puntuacion * 10
    if dificultad == "D":
        puntuacion = puntuacion * 20
  
    return puntuacion

# Comprueba si la puntuación del jugador está dentro de los primeros 5 en el ranking, y la registra si es necesario.
def comprobarHighscores(puntuacion):
    ubicacion = 'highscores.txt'

    with open(ubicacion, 'a') as f: 
        highscore = f"jugador;{puntuacion}\n"
        f.write(highscore)
    
    with open(ubicacion, 'r') as f: 
        highscores = f.readlines()
    
    if len(highscore) > 6 :
        highscores = highscores[:6] 
    
    if len(highscores) == 6:
        score6 = highscores[5].split(";")[1]
        score5 = highscores[4].split(";")[1]
        
        if score6 > score5: 
            jugador = input("¡Felicidades, has superado una puntuación del ranking!\nIngresa tu nombre para registrar tu nuevo record (se mostrarán hasta 15 caracteres): ")
            highscores[5] = f"{jugador};{puntuacion}\n"
            highscores[4] = highscores[5] 
        highscores = highscores[:5] 

    else:
        jugador = input("¡Felicidades, has ingresado en el ranking de puntuaciones!\nIngresa tu nombre para registrarlo (se mostrarán hasta 15 caracteres): ")
        highscores[-1] = f"{jugador};{puntuacion}\n"

    highscores = ordenarHighscores(highscores)
    
    with open(ubicacion, 'w') as f:
        for registro in highscores:
            f.write(registro)        
    
# Ordena el ranking de puntuaciones de mayor a menor en función de la puntuación.
def ordenarHighscores(highscores):
    for i in range(len(highscores)):
        for j in range(i + 1, len(highscores)):
            score1 = int(highscores[i].split(";")[1])
            score2 = int(highscores[j].split(";")[1])
            if score1 < score2:
                highscores[i], highscores[j] = highscores[j], highscores[i]
    return highscores 
         
# Muestra la tabla de puntuaciones del ranking, si el jugador decide verla.
def mostrarHighscores():
    ubicacion = 'highscores.txt'
    mensaje = "¿Quiere ver la tabla de Highscores?\n(Ingrese 'Y' para ver la tabla, 'N' en caso contrario): "
    opciones = ['Y','N']
    respuesta = pedirRespuesta(mensaje,opciones)

    if respuesta == 'Y':
        try:
            with open(ubicacion, 'r') as f:
                highscores = f.readlines()
        
        except FileNotFoundError as e:
            print("No se ha encontrado el ranking de puntuaciones.")
            registrarError(e)

        else:
            print("Ranking de Puntuaciones:")
            puesto = 1
            for registro in highscores:
                jugador,score = registro.strip().split(";") 
                print(f"Puesto {puesto}: {jugador[:15].ljust(15)} {score} puntos")
                puesto += 1 


# Programa Principal → Función para ejecutar el juego
def main():
    try:
        juego = detectarJuegoPrevio()
        if juego == 'V':
            matriz, respuestas, matrizRespuestas, palabrasTotales,palabrasEncontradas,dificultad,intentos = iniciarJuegoPrevio()
            mostrarEstadoJuego(palabrasTotales, palabrasEncontradas, matriz)

        else:
            categoria, dificultad = iniciarJuego()
            if categoria and dificultad:
                matriz = crearMatriz(dificultad)
                respuestas = generarJuego(matriz, categoria)
                palabrasTotales = set(respuestas.keys())
                matrizRespuestas = crearMatrizRespuesta(matriz, respuestas, palabrasTotales)
                palabrasEncontradas = set()
                intentos = 0

                registrarEstado(matriz, respuestas, matrizRespuestas, palabrasTotales, palabrasEncontradas, dificultad,intentos)

                mostrarPalabrasEscondidas(palabrasTotales)
                mostrarMatriz(matriz)

        while palabrasEncontradas != palabrasTotales:
            try:
                palabraUsuario, respuestaUsuario = pedirPalabra(matriz,palabrasTotales,palabrasEncontradas)
            except (PalabraInvalidaError,PalabraEncontradaError) as e:
                print(e)
                continue

            if palabraUsuario == 'R':
                print("Respuestas: ")
                mostrarMatriz(matrizRespuestas)
                finalizarJuego(palabrasEncontradas, palabrasTotales, intentos, dificultad)
                return

            if palabraUsuario in palabrasTotales - palabrasEncontradas:
                intentos += 1
                if comprobarRespuesta(respuestaUsuario, respuestas, palabraUsuario):
                    palabrasEncontradas.add(palabraUsuario)
                    for fila, columna in respuestas[palabraUsuario]["coordenadas"]:
                         matriz[fila][columna] = "-"
                    print("\n¡Correcto!")
                else:
                    print("\nRespuesta incorrecta. Inténtelo de nuevo.")
                registrarEstado(matriz, respuestas, matrizRespuestas, palabrasTotales, palabrasEncontradas, dificultad, intentos)

            mostrarEstadoJuego(palabrasTotales, palabrasEncontradas, matriz)
           
        print(f"¡Felicidades! Ha encontrado todas las palabras.")
        finalizarJuego(palabrasEncontradas, palabrasTotales, intentos, dificultad)

    except archivoPalabrasError as e:
        print(e)
        registrarError(e)

    except (ValueError, TypeError, IndexError) as e:
        print("Ocurrió un error inesperado. El juego se ha cerrado.")
        registrarError(e)

    except KeyboardInterrupt:
        print("\nHa abandonado el juego. Adios!")
            
main()