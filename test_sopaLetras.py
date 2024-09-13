# test_sopaLetras.py
import unittest
from unittest.mock import patch
from sopaLetras import pedirRespuesta, elegirCategoria, elegirDificultad, iniciarJuego

class TestSopaLetras(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
