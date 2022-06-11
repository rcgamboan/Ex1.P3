
# Archivo principal de la implementacion del Buddy System
# Se reciben los comandos del usuario desde la terminal
# Y se llaman a las funciones de la classe Buddy segun se requiera

import sys
from buddy import Buddy

if len(sys.argv) != 2:
    print("Para llamar al archivo utilice el siguiente formato: python3 main.py <numero_de_bloques>")
    sys.exit()

args = sys.argv
try:
    numero_bloques = int(args[1])
except:
    print("Numero de bloques invalido")
    print("Por favor introduzca como numero de bloques, un numero entero")
    sys.exit()

print("\n\nCliente que maneja la implementacion del Buddy System")
print("Implementado por Roberto Gamboa, 16-10394")

buddy = Buddy(numero_bloques)

print("\nA continuacion indique la operacion que quiere realizar")
print("Las operaciones disponibles son las siguientes: ")
print("\nRESERVAR <nombre> <cantidad>  (reserva <cantidad> de espacio al usuario <nombre>)")
print("LIBERAR <nombre>              (libera el espacio reservado por <nombre>)")
print("MOSTRAR                       (muestra los bloques libres y los reservados)")
print("SALIR                         (termina la ejecucion del programa)\n")
while True:

    comando = input("main> ")

    if comando == '':
        continue

    argumentos = comando.split()

    if argumentos[0] == "SALIR" or argumentos[0] == "salir":
        print("Se termina la ejecucion del programa")
        sys.exit()
    elif argumentos[0] == "RESERVAR" or argumentos[0] == "reservar":

        if len(argumentos) != 3:
            print("Formato invalido.")
        else:
            usuario = argumentos[1]
            try:
                bloques_a_reservar = int(argumentos[2])
            except:
                print("Cantidad de bloques invalida.")
                continue
            
            buddy.reservar(usuario,bloques_a_reservar)
    elif argumentos[0] == "LIBERAR" or argumentos[0] == "liberar":

        if len(argumentos) != 2:
            print("Formato invalido.")
        else:

            usuario = argumentos[1]
                
            buddy.liberar(usuario)
    elif argumentos[0] == "MOSTRAR" or argumentos[0] == "mostrar" :
            
        buddy.imprimir()
    else:
        print("Operacion no valida\n")

    