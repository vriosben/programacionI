# programacionI

Proyecto para la Materia Programación I de la UADE - 2° Cuatrimestre 2024

- Objetivo: Sopa de Letras

- Características: 
    - Pedirle al usuario que ingrese Y para empezar a jugar, N para terminar. 
    - Elegir el tamaño de la matriz según nivel de dificultad:
        - Fácil(8x8)
        - Medio(16x16)
        - Difícil(32x32)
    - Elegir las palabras aleatorias a esconder según categoría y tamaño: 
        - Ciudades
        - Animales
        - Tragos
    - Esconder las palabras aleatoriamente en la matriz, de manera horizontal o vertical. 
    - Rellenar las palabras restantes con letras random.
    - Mostrar la sopa y las palabras a buscar para empezar a jugar.
    - Pedir las palabras encontradas por el usuario. 
    - Informar el estado actual del juego después de cada palabra encontrada. 
    - El usuario debe encontrar todas las palabras o ingresar N si desea finalizar el juego antes.
    - Informar al usuario la ubicación de las respuestas y el número de palabras encontradas si decide finalizar antes.


    Pendiente:     
   
   PARTE 2 - Ideas para agregar:
    - Guardar todas las palabras de las categorias de la sopa.
    - Guardar un archivo con puntajes más altos que el usuario puede consultar.
    - Algo con recursión.
    


    PARTE 2 - Se agregó:

    - Exception KeyInterrupt para salir con ctrl c en cualquier momento. (FALTA ARREGLAR EL N que hace lo mismo)
    - Dos excepciones personalizadas nuevas: PalabraEncontradaError y PalabraInvalidaError, que suceden si el usuario responde con con palabra que ya encontró o que no está en la sopa, respectivamente.
    - Excepciones ValueError, TypeError, IndexError en main. Si alguno de estos errores ocurre, se guardan los detalles en un log de errores para que el programador pueda analizarlos y corregirlos.
    - Funciones leerJson, escribirJson y registrarError.
    - archivo log_errores.json

    - Guardar el estado de juego y cargar para retomar juego. LISTO
    - Funcion registrarEstado - para guardar todos los datos de la sopa en juego.
    - Funcion limpiarEstado - para borrar los datos guardados cuando el usuario se rinde.
    - Funcion detectarJuegoPrevio - revisa si hay un juego previo guardado y da la opcion de retomarlo o empezar otro.
    - Funcion iniciarJuegoPrevio - vuelve a cargar el juego que esta guardado.
    - archivo estado_sopa.json


    


 
