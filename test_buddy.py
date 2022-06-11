#Pregunta 3 Parcial 1 CI3641
#Elaborado por Roberto Gamboa 16-10394

import unittest
from buddy import Buddy

buddy = Buddy(500)

# Se emplea la libreria unittest para las pruebas unitarias
# Solo se prueban las funciones asignar y liberar
# Ya que ellas llaman a las demas funciones a su vez

# para ejecutar las pruebas y calcular la cobertura ejecutar el siguiente comando:
# coverage run -m unittest test_buddy.py
# Luego se puede acceder al reporte de la cobertura con el comando
# coverage report
# En el reporte de cobertura se evidencia que la misma es menor al 80%
# Esto se debe a que no se realizan pruebas sobre la funcion imprimir
class TestBuddy(unittest.TestCase):

    def test_asignar_0(self):
        buddy.imprimir()
        self.assertEqual(buddy.reservar('p0',0) , '\nNo se ha solicitado memoria')
    
    def test_asignar_menor(self):
        self.assertEqual(buddy.reservar('p1',5) , "Se le ha asignado el bloque [Inicio : 0, Fin : 7] al usuario p1")

    def test_asignar_mayor(self):
        self.assertEqual(buddy.reservar('p2',400) , "\nNo hay espacio suficiente que asignar")
    
    def test_reasignar(self):
        self.assertEqual(buddy.reservar('p1',20) , "\nEl usuario p1 ya tiene espacio asignado.")

    def test_liberar_sin(self):
        self.assertEqual(buddy.liberar('p3') , "El usuario p3 no tiene asignada memoria")
    
    def test_liberar_con(self):
        buddy.reservar('p4',5)
        self.assertEqual(buddy.liberar('p4') , "Se ha liberado el bloque asignado al usuario p4")
    
    def test_liberar_g(self):
        buddy.reservar('p5',40)
        self.assertEqual(buddy.liberar('p5') , "Se ha liberado el bloque asignado al usuario p5")
    


if __name__ == '__main__':
    unittest.main()
