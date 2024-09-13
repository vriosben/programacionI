# test_sopaLetras.py
import unittest
from unittest.mock import patch
from sopaLetras import pedirRespuesta, elegirCategoria, elegirDificultad, iniciarJuego, crearMatriz, categoriaMatriz

class TestSopaLetras(unittest.TestCase):


# Patch simula la entrada del usuario
    @patch('builtins.input', side_effect=['Y'])
    def test_iniciarJuego_continuar(self, mock_input):
        categoria, dificultad = iniciarJuego()
        self.assertIsNotNone(categoria)
        self.assertIsNotNone(dificultad)

    @patch('builtins.input', side_effect=['N'])
    def test_iniciarJuego_terminar(self, mock_input):
        categoria, dificultad = iniciarJuego()
        self.assertIsNone(categoria)
        self.assertIsNone(dificultad)

    @patch('builtins.input', side_effect=['A'])
    def test_elegirCategoria(self, mock_input):
        categoria = elegirCategoria()
        self.assertEqual(categoria, 'A')

    @patch('builtins.input', side_effect=['F'])
    def test_elegirDificultad(self, mock_input):
        dificultad = elegirDificultad()
        self.assertEqual(dificultad, 'F')

# En las siguientes funciones ya no ingresa directamente un valor, por lo cual 
# la función ya recibe argumentos
# El self es un método que accede a los atributos y métodos de la instancia actual  
    def test_crearMatriz(self):
        matriz = crearMatriz('F')
        esperado = [["*" for _ in range(8)] for _ in range(8)]
        self.assertEqual(matriz, esperado)
    

if __name__ == '__main__':
    unittest.main()
