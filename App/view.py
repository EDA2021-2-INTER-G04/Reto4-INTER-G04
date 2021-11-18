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




# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Cargar archivos")
    print("2- Crear catálogo")
    print("3- Encontrar puntos de interconexión aérea")
    print("4- Encontrar clústeres de tráfico aéreo")
    print("5- Encontrar la ruta más corta entre ciudades")
    print("6- Utilizar las millas de viajero ")
    print("7- Cuantificar el efecto de un aeropuerto cerrado ")
    print("8- Comparar con servicio WEB externo")
    print("9- Visualizar gráficamente los requerimientos")
    print("0- Salir")
    print("*******************************************")


def optionOne(cont):
    print("\nCargando información de transporte de singapur ....")
    start_time = time.process_time()
    print("\nLa operación tardó ", elapsed_time_ms, " ms.")

"""
Menu principal
"""


def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs[0]) == 1:
            optionOne(cont)

        elif int(inputs[0]) == 2:
            optionTwo(cont)

        elif int(inputs[0]) == 3:
            optionThree(cont)

        elif int(inputs[0]) == 4:
            optionFour(cont)

        elif int(inputs[0]) == 5:
            optionFive(cont)

        elif int(inputs[0]) == 6:
            optionSix(cont)

        elif int(inputs[0]) == 7:
            optionSeven(cont)

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()

