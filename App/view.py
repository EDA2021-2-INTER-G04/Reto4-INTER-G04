"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
"""


import sys
import config
import threading
import time
from App import controller
from DISClib.ADT import stack
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

citiesFile = "worldcities-utf8.csv"

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Crear analizador")
    print("2- Cargar archivos")
    print("3- Encontrar puntos de interconexión aérea")
    print("4- Encontrar clústeres de tráfico aéreo")
    print("5- Encontrar la ruta más corta entre ciudades")
    print("6- Utilizar las millas de viajero ")
    print("7- Cuantificar el efecto de un aeropuerto cerrado ")
    print("0- Salir")
    print("*******************************************")

def optionTwo(analyzer):
    print("\nCargando información...")
    start_time = time.process_time()
    print("Seleccione el tamaño de la muestra")
    print("1- Small")
    print("2- 5%")
    print("3- 10%")
    print("4- 20%")
    print("5- 30%")
    print("6- 50%")
    print("7- 80%")
    print("8- Large")
    sample = int(input())
    airportsFile = controller.selectSample(sample)[0]
    routesFile = controller.selectSample(sample)[1]
    controller.loadData(analyzer, airportsFile, routesFile, citiesFile)
    numAirports = controller.mapSize(analyzer["airportsByIATA"])
    numDiRoutes = controller.totalConnections(analyzer["routes"])
    numNoRoutes = controller.totalConnections(analyzer["roundTrip"])
    numCities = controller.mapSize(analyzer["cities"])
    numDiVertices = controller.numVertices(analyzer["routes"])
    numNoVertices = controller.numVertices(analyzer["roundTrip"])
    print('\nNumero de aeropuertos: ' + str(numAirports))
    print("\nNúmero de vértices en el digrafo: " + str(numDiVertices))
    print('Numero de conexiones en el digrafo: ' + str(numDiRoutes))
    print("\nNúmero de vértices en el grafo no dirigido: " + str(numNoVertices))
    print("Número de conexiones en el grafo no dirigido: " + str(numNoRoutes))
    print("\nNúmero de ciudades: " + str(numCities))
    controller.printFirstLastAirports(analyzer)
    controller.printFirstLastCities(analyzer)
    print('\nEl limite de recursion actual: ' + str(sys.getrecursionlimit()))
    stop_time = time.process_time()
    elapsed_time_ms = (stop_time-start_time)*1000
    print("\nLa operación tardó ", elapsed_time_ms, " ms.")

def optionThree(analyzer):
    start_time = time.process_time()
    controller.findInterconection(analyzer)
    stop_time = time.process_time()
    elapsed_time_ms = (stop_time-start_time)*1000
    print("\nLa operación tardó ", elapsed_time_ms, " ms.")

def optionFour(analyzer):
    start_time = time.process_time()
    controller.findClusters(analyzer)
    stop_time = time.process_time()
    elapsed_time_ms = (stop_time-start_time)*1000
    print("\nLa operación tardó ", elapsed_time_ms, " ms.")

def optionFive(analyzer):
    start_time = time.process_time()
    controller.minRoute(analyzer) 
    stop_time = time.process_time()
    elapsed_time_ms = (stop_time-start_time)*1000
    print("\nLa operación tardó ", elapsed_time_ms, " ms.")   

def optionSeven(analyzer):
    start_time = time.process_time()
    controller.closedAirport(analyzer) 
    stop_time = time.process_time()
    elapsed_time_ms = (stop_time-start_time)*1000
    print("\nLa operación tardó ", elapsed_time_ms, " ms.")

def optionSix(analyzer):
    start_time = time.process_time()
    departure = input("Ingrese el código IATA del aeropuerto de partida: ")
    miles = float(input("Ingrese la cantidad de millas de viajero disponibles: "))
    controller.travelerMiles(analyzer, departure, miles)
    stop_time = time.process_time()
    print("\nLa operación tardó ", (stop_time-start_time)*1000, " ms.")
"""
Menu principal
"""
def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs[0]) == 1:
            print("\nInicializando....")
            analyzer = controller.init()

        elif int(inputs[0]) == 2:
            optionTwo(analyzer)

        elif int(inputs[0]) == 3:
            optionThree(analyzer)
            pass

        elif int(inputs[0]) == 4:
            optionFour(analyzer)
            pass

        elif int(inputs[0]) == 5:
            optionFive(analyzer)

        elif int(inputs[0]) == 6:
            optionSix(analyzer)

        elif int(inputs[0]) == 7:
            optionSeven(analyzer)
        
        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()

