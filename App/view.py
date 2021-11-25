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

airportsFile = "airports_full.csv"
routesFile = "routes_full.csv"
citiesFile = "worldcities.csv"


# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Crear catálogo")
    print("2- Cargar archivos")
    print("3- Encontrar puntos de interconexión aérea")
    print("4- Encontrar clústeres de tráfico aéreo")
    print("5- Encontrar la ruta más corta entre ciudades")
    print("6- Utilizar las millas de viajero ")
    print("7- Cuantificar el efecto de un aeropuerto cerrado ")
    print("8- Comparar con servicio WEB externo")
    print("9- Visualizar gráficamente los requerimientos")
    print("0- Salir")
    print("*******************************************")


def optionTwo(analyzer):
    print("\nCargando información...")
    start_time = time.process_time()
    controller.loadData(analyzer, airportsFile, routesFile, citiesFile)
    numAirports = controller.mapSize(analyzer["airports"])
    numDiRoutes = controller.totalConnections(analyzer["routes"])
    numNoRoutes = controller.totalConnections(analyzer["roundTrip"])
    numCities = controller.mapSize(analyzer["cities"])
    numDiVertices = controller.numVertices(analyzer["routes"])
    numNoVertices = controller.numVertices(analyzer["roundTrip"])
    print('\nNumero de aeropuertos: ' + str(numAirports))
    print("Número de vértices en el digrafo: " + str(numDiVertices))
    print('Numero de rutas en el digrafo: ' + str(numDiRoutes))
    #print("Número de vértices en el grafo no dirigido: " + str(numNoVertices))
    #print("Número de rutas en el grafo no dirigido: " + str(numNoRoutes))
    print("Número de ciudades: " + str(numCities))
    controller.printFirstAirport(analyzer)
    controller.printLastCity(analyzer)
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    stop_time = time.process_time()
    elapsed_time_ms = (stop_time-start_time)*1000
    print("\nLa operación tardó ", elapsed_time_ms, " ms.")

"""
Menu principal
"""


def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs[0]) == 1:
            print("\nInicializando....")
            # cont es el controlador que se usará de acá en adelante
            analyzer = controller.init()

        elif int(inputs[0]) == 2:
            optionTwo(analyzer)

        elif int(inputs[0]) == 3:
            #optionThree(analyzer)
            pass

        elif int(inputs[0]) == 4:
            #optionFour(analyzer)
            pass

        elif int(inputs[0]) == 5:
            #optionFive(analyzer)
            pass

        elif int(inputs[0]) == 6:
            #optionSix(analyzer)
            pass

        elif int(inputs[0]) == 7:
            #optionSeven(analyzer)
            pass

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()

