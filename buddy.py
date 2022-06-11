
#Pregunta 3 Parcial 1 CI3641
#Elaborado por Roberto Gamboa 16-10394

# Implementacion de la tecnica de alocacion de memoria Buddy System
# Implementacion basada en la hallada en
# https://www.geeksforgeeks.org/buddy-memory-allocation-program-set-1-allocation/ y en
# https://www.geeksforgeeks.org/buddy-memory-allocation-program-set-2-deallocation/

# Se trata de una tecnica que maneja la memoria dividiendo sus bloques en potencias de 2
# Y cuando se libera un bloque, se combina con otro bloque adyacente (si esta libre)
# para crear bloques de mayor capacidad

import math

class Buddy(object):

    # Se recibe el numero de bloques a manejar, como el numero debe ser una potencia de dos,
    # se le aplica log base 2 al numero recibido para obtener la potencia de 2 mas cercana a ese numero
    # esto se hace ya que a la hora de dividir los bloques, se hace en potencias de 2.
    # y nos indica hasta cuantas veces se pueden dividir los bloques en bloques mas pequeños
    # Tambien se crean diccionarios para almacenar que bloques se encuentran ocupados
    # y que bloques se encuentran libres
    
    def __init__(self,bloques) -> None:
        
        self.cantidadBloques = math.floor(math.log2(bloques))

        # Ademas se crea un diccionario donde se guardara como clave el nombre de cada persona que reseve espacio
        # y como valor asignado a esa clave, la cantidad de bloques que dicha persona reservo
        self.bloquesEnUso = {}

        # Se crea una lista para almacenar los bloques libres
        # Se crean a su vez tantas listas vacias como cantidad de bloques se vayan a manejar
        self.bloquesLibres = [[] for i in range(0,self.cantidadBloques+1)]
        # Se agrega a la lista el primer bloque, dicho bloque es del tamaño maximo permitido ( 2 ** cantidadBloques )
        # y se dividira en bloques mas pequeños a medida que se requiera para almacenar datos 
        self.bloquesLibres[len(self.bloquesLibres)-1].append(Bloque(0,2**self.cantidadBloques - 1))
    
    # Funciones para reservar memoria
    # Recibe el nombre del usuario que solicita la memoria
    # Y la cantidad de memoria que solicita
    def reservar(self,nombre,memoria):
        

        # Primero se verifica en el diccionario que guarda la informacion de los bloques en uso
        # Si el usuario ya tiene asignada memoria, no se asigna nada
        if nombre in self.bloquesEnUso.keys():
            string = "\nEl usuario " + nombre + " ya tiene espacio asignado."
            print(string)
            return string

        # Se verifica si lo que solicita el usuario es mayor que 0
        if memoria == 0:
            string = "\nNo se ha solicitado memoria"
            print(string)
            return string
        
        # Luego se verifica si el espacio que se pide esta disponible
        if memoria > (2**self.cantidadBloques):
            string = "\nNo hay espacio suficiente que asignar"
            print(string)
            print("Se puede asignar un valor dentro del siguiente intervalo : " +str((1,2**self.cantidadBloques)))
            print("Esto sin tomar en cuenta los bloques ya asignados")
            return string
        
        # Se calcula en cual nivel se le debe asignar memoria al usuario
        # con la funcion math.ceil se retorna la potencia de dos mas cercana a lo solicitado
        # para evitar asignar demasiada memoria de mas
        posicion = math.ceil(math.log2(memoria))

        # Se examina el nivel de los bloques obtenido antes
        # Si se encuentran bloques libres se eliminan de la lista y se asignan al usuario
        # Se agrega al diccionario el nombre del usuario y el bloque que se le asigno
        # Caso contrario se debe buscar en un nivel superior si hay algun bloque disponible y dividirlo
        if len(self.bloquesLibres[posicion]) > 0:
            
            bloque = self.bloquesLibres[posicion].pop(0)
            self.bloquesEnUso[nombre] = bloque
            string = "Se le ha asignado el bloque " + str(bloque) + " al usuario " + nombre
            print(string)
            return string
        # Como no hay bloques del tamaño requerido, se busca en un nivel superior hasta encontrar alguno

        nivel = posicion + 1

        # Se itera hasta conseguir un nivel con bloques disponibles
        # O hasta que se recorra toda la lista de bloques libres
        while nivel != len(self.bloquesLibres):

            if len(self.bloquesLibres[nivel]) > 0 :
                break
            
            nivel += 1

        # Si nivel es igual al tamaño de la lista, significa que se recorrio toda la lista sin encontrar
        # algun bloque libre            
        if nivel == len(self.bloquesLibres):
            print("No hay espacio suficiente para asignar")
            return
        
        # Caso contrario se debe dividir el bloque encontrado para poder asignarle el espacio requerido al usuario

        bloqueDiv = self.bloquesLibres[nivel].pop(0)
        #self.bloquesLibres[nivel].remove(0)

        # Se divide el bloque encontrado y se generan dos nuevos bloques
        # uno de ellos se agrega a la lista de bloques libres ya que el otro se va a utilizar
        # Este proceso se repite hasta llegar al nivel adecuado para la memoria que requiera el usuario
        while nivel > posicion:
            b1,b2 = bloqueDiv.dividir()
            self.bloquesLibres[nivel-1].append(b2)
            bloqueDiv = b1
            nivel-=1
        
        # En este punto ya se obtuvo el bloque del tamaño requerido, se le asigna al usuario
        # y se guarda la informacion en el diccionario
        self.bloquesEnUso[nombre] = bloqueDiv
        string = "Se le ha asignado el bloque " + str(bloqueDiv) + " al usuario " + nombre
        print(string)
        return string

    # Funcion para unir un bloque con su compañero cuando se requiera un bloque de tamaño mayor
    # Para facilitar la tarea de unir bloques a traves de distintos niveles, se usa una funcion recursiva
    def unirBloques(self,bloque_a_fundir):
        
        # Caso base,
        if bloque_a_fundir == None:
            return
        else:
            inicio , final = bloque_a_fundir.direcciones()
            # Se calcula la posicion de la lista en la que se encuentra el bloque
            posicion = math.ceil(math.log2(bloque_a_fundir.capacidad))
            
            # Ahora calculamos la buddyAddress y el buddyNumber del bloque que queremos unir
            buddyNumber = inicio / bloque_a_fundir.capacidad
            

            # Luego dependiendo de si el buddyNumber es par o impar, hallamos la buddyAddress
            if buddyNumber % 2 == 0:
                buddyAddress = inicio + bloque_a_fundir.capacidad
            else:
                buddyAddress = inicio - bloque_a_fundir.capacidad
                
            
            bloque_unido = None

            # Ahora se busca en la lista de bloques libres al mismo nivel que el bloque actual
            # si este tiene un buddy
        
            for indice, bloque in enumerate(self.bloquesLibres[posicion]):
                inicioB , finalB = bloque.direcciones()
                if inicioB == buddyAddress:
                    if buddyNumber % 2 == 0:
                        bloque_unido = Bloque(inicio,finalB)
                        self.bloquesLibres[posicion+1].append(bloque_unido)
                    else:
                        bloque_unido = Bloque(inicioB,final)
                        self.bloquesLibres[posicion+1].append(bloque_unido)
                
                    self.bloquesLibres[posicion].pop()
                    self.bloquesLibres[posicion].pop(indice)
                    break
                
            self.unirBloques(bloque_unido)

    # Funcion que recibe el nombre del usuario que desea liberar los bloques reservados
    def liberar(self,nombre):

        # Se busca en el diccionario el bloque correspondiente al usuario
        bloque = self.bloquesEnUso.get(nombre,None)

        if bloque == None:
            string = "El usuario " + nombre + " no tiene asignada memoria"
            print(string)
            return string
        
        # Ahora se obtiene el nivel en el que se encuentra el bloque
        posicion = math.ceil(math.log2(bloque.capacidad))
        self.bloquesLibres[posicion].append(bloque)

        self.unirBloques(bloque)

        self.bloquesEnUso.pop(nombre)
        string = "Se ha liberado el bloque asignado al usuario " + nombre
        print(string)
        return string

    # Muestra visualmente el estado de los bloques, los que se encuentran libres y los que se encuentran reservados
    def imprimir(self):
        
        string_libres = ""
        print("\nBloques libres: ")
        for nivel in self.bloquesLibres:
            for bloque in nivel:
                string_libres += str(bloque) + "\n"
        if len(string_libres) == 0:
            print("No hay bloques libres")
        else:
            print(string_libres)
        
        print("\nBloques reservados: ")
        string_en_uso = ""
        for nombre in list(self.bloquesEnUso.keys()):
            bloque = self.bloquesEnUso[nombre]
            string_en_uso += str(bloque) + ", Usuario : " + nombre + "\n"
        if len(string_en_uso) == 0:
            print("No hay bloques reservados en este momento\n")
        else:
            print(string_en_uso + "\n")

        return


# Clase que representa un bloque de memoria
# Recibe una direccion de inicio y de fin de memoria donde se aloja dicho bloque
class Bloque(object):

    # Se calcula la capacidad del bloque como la distancia entre las direcciones
    def __init__(self,dirInicio,dirFin) -> None:
        self.dirInicio = dirInicio
        self.dirFin = dirFin
        self.capacidad = dirFin - dirInicio + 1

    # Funcion para acceder a la direccion de inicio y fin del bloque
    def direcciones(self) :
        return self.dirInicio, self.dirFin

    def capacidad(self):
        return self.capacidad

    # Funcion para dividir el bloque en dos bloques con la mitad de la capacidad del bloque actual cada uno
    def dividir(self):

        inicio,final = self.direcciones()
        # Se retorna dos bloques B1 y B2 
        # tal que a B1 se le asignan las direcciones entre el inicio del bloque actual
        # y la mitad del mismo
        # y a B2 se le asigna desde la mitad +1 del bloque actual hasta el final.

        return Bloque(inicio,  inicio + (final - inicio)//2) , Bloque((inicio + (final - inicio+1)//2) , final)

    # Funcion que indica como se representa el bloque cuando se utiliza el metodo str() sobre el
    def __str__(self) -> str:
        inicio,final = self.direcciones()
        string = '[Inicio : ' + str(inicio) + ', Fin : ' + str(final) + ']'
        return string

