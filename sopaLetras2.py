import random
import string               # Esperar respuesta del profe si se puede usar o no. Usamos en crearMatriz()

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
    tamaños = {'F': 8, 'M': 12, 'D': 18}
    tamaño = tamaños[dificultad] 
    
    matriz = []
    for fila in range(tamaño):
        matriz.append([])
        for columna in range(tamaño):
            matriz[fila].append(random.choice(string.ascii_uppercase))        
    return matriz
    
# Asigna palabras a la matriz según la categoría y las esconde, devuelve las respuestas.
def generarJuego(matriz, categoria):                                     
    palabrasCategoria = {
        'A': ['GATO', 'PERRO', 'PEZ', 'CABALLO', 'VACA', 'OVEJA', 'PATO', 'GALLINA', 'LORO', 'PANDA', 'JIRAFA', 'LEON', 'TIGRE', 'ZEBRA', 'ELEFANTE', 'RINOCERONTE', 'OSO', 'COBRA', 'SERPIENTE', 'CANGREJO', 'TIBURON'],
        'C': ['QUITO', 'PARIS', 'SEUL', 'LONDRES', 'MADRID', 'BERLIN', 'ROMA', 'TOKIO', 'PEKIN', 'MEXICO', 'MOSCU', 'RIO', 'SANTIAGO', 'BOGOTA', 'CARACAS', 'EDINBURGO', 'BRASILIA', 'LISBOA', 'PRAGA', 'VIENA'],
        'T': ['GIN', 'RON', 'VODKA', 'TEQUILA', 'WHISKY', 'RUM', 'BRANDY', 'COGNAC', 'CHAMPAGNE', 'APEROL', 'MARTINI', 'MOJITO', 'DAIQUIRI', 'NEGRONI', 'MANHATTAN', 'DESTORNILLADOR', 'FERNET', 'SANGRIA', 'MARGARITA', 'CAIPIRINHA']
    }
    
    palabrasTotales = palabrasCategoria.get(categoria, [])    
    palabrasEscondidas = list(seleccionarPalabras(palabrasTotales, matriz))   

    coordOcupadas = set()
    respuestas = {}

    for palabra in palabrasEscondidas: 
        coordPalabra, posicion = esconderPalabra(palabra, matriz, coordOcupadas)     
        respuestas[palabra] = guardarRespuesta(coordPalabra, posicion)
    return respuestas

# Selecciona las palabras a esconder segun la matriz y categoria
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
        
        if posicion == 0:  # Horizontal
            filaCoord = random.randint(0, len(matriz) - 1)
            columnaCoord = random.randint(0, len(matriz) - len(palabra))
            coordPalabra = [(filaCoord, columnaCoord + i) for i in range(len(palabra))]   # lista de tuplas por comprension
        else:  # Vertical
            filaCoord = random.randint(0, len(matriz) - len(palabra))
            columnaCoord = random.randint(0, len(matriz) - 1)
            coordPalabra = [(filaCoord + i, columnaCoord) for i in range(len(palabra))]   # lista de tuplas por comprension
        
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

# Guarda la respuesta sobre dónde se escondió la palabra
def guardarRespuesta(coordPalabra, posicion):                          
    respuesta = {}
    
    direccion = "h" if posicion == 0 else "v"
    filaInicial, columnaInicial = coordPalabra[0]

    respuesta["direccion"] = direccion
    respuesta["filaInicial"] = filaInicial
    respuesta["columnaInicial"] = columnaInicial
    respuesta["coordenadas"] = coordPalabra

    return respuesta

# Muestra la matriz en un formato legible
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

# Crea una matriz donde solo se muestran las palabras escondidas y el resto *
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

# Informa el estado del juego: cantidad y palabras que falta encontrar, muestra el estado actual de la matriz.
def mostrarEstadoJuego(palabrasTotales, palabrasEncontradas, matriz):
    palabrasRestantes = palabrasTotales - palabrasEncontradas
    cantidadRestantes = len(palabrasRestantes)

    print(f"Palabras restantes: {cantidadRestantes}")
    mostrarPalabrasEscondidas(palabrasRestantes)
    mostrarMatriz(matriz)

# Funcion para pedir las respuestas del usuario
def pedirPalabra(matriz):
    palabraUsuario = input("¿Qué palabra encontraste? (O ingresa 'N' para salir): ").strip().upper()  
            
    if palabraUsuario == 'N':
        return palabraUsuario, None

    else:
        opcionesFilaColumna = [str(i + 1) for i in range(len(matriz))]
        direccion = pedirRespuesta("¿Es horizontal (h) o vertical (v)? ", ['H', 'V']).lower()      
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
        direccion = "h" if datosCorrectos["direccion"] == "h" else "v"        
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

# Función principal para ejecutar el juego
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
                    print("Respuesta incorrecta. Inténtalo de nuevo.")  

            else:
                print(f"Palabra no válida o ya encontrada. Inténtalo de nuevo.")

            mostrarEstadoJuego(palabrasTotales, palabrasEncontradas, matriz)       
        print("¡Felicidades! Has encontrado todas las palabras.")

main()