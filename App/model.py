"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Utils import error as error
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    try:
        analyzer = {
                    'airports': None,
                    'routes': None,
                    'countries': None,
                    'roundTrip': None
                    }

        analyzer['airports'] = mp.newMap(numelements=10000,
                                     maptype='PROBING',
                                     comparefunction=compareAirportIds)

        analyzer['routes'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareAirportIds)

        analyzer["cities"] = mp.newMap(numelements=37500, maptype="PROBING", comparefunction=cmpStrings)

        analyzer["roundTrip"] = gr.newGraph(datastructure="ADJ_LIST", directed=False, size=14000, comparefunction=compareAirportIds)
        
        return analyzer
    
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo
def addRoute(analyzer, route):
    try:
        origin = createOriginID(route)
        destination = createDestinationID(route)
        verifyDistance(route)
        addAirportRoute(analyzer, origin)
        addAirportRoute(analyzer, destination)
        addConnection(analyzer, origin, destination, route["distance_km"])
        return analyzer

    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

def addAirportRoute(analyzer, airportID):
    """
    Adiciona un aeropuerto como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['routes'], airportID):
            gr.insertVertex(analyzer['routes'], airportID)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos aeropuertos
    """
    edge = gr.getEdge(analyzer['routes'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['routes'], origin, destination, distance)

def addAirport(analyzer, airport):
    mp.put(analyzer["airports"], airport["IATA"], airport)

def addCity(analyzer, city):
    mp.put(analyzer["cities"], city["city_ascii"], city)    

# Funciones para creacion de datos
def createOriginID(route):
    departure = route["Departure"] + "-"
    name = departure + route["Airline"]

    return name

def createDestinationID(route):
    departure = route["Destination"] + "-"
    name = departure + route["Airline"]

    return name

def createNonDirGraph(analyzer):
    dirGraph = analyzer["routes"]
    nonDirGraph = analyzer["roundTrip"]

    vertices = gr.vertices(dirGraph)

    for vertex in lt.iterator(vertices):
        adjacent = gr.adjacents(dirGraph, vertex)
        for adjVertex in lt.iterator(adjacent):
            adjacentB = gr.adjacents(dirGraph, adjVertex)
            if lt.isPresent(adjacentB, vertex) != 0:
                weight = gr.getEdge(dirGraph, vertex, adjVertex)["weight"]

                if not gr.containsVertex(nonDirGraph, vertex):
                    gr.insertVertex(nonDirGraph, vertex)
                if not gr.containsVertex(nonDirGraph, adjVertex):
                    gr.insertVertex(nonDirGraph, adjVertex)
                if gr.getEdge(nonDirGraph, vertex, adjVertex) == None:
                    gr.addEdge(nonDirGraph, vertex, adjVertex, weight)              

# Funciones de consulta
def mapSize(map):
    size = mp.size(map)

    return size

def totalConnections(graph):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(graph)

def printFirstAirport(analyzer):
    airportsMap = analyzer["airports"]
    airports = mp.keySet(airportsMap)
    key = lt.getElement(airports, 1)
    dic = mp.get(airportsMap, key)["value"]

    print("\nPRIMER AEROPUERTO CARGADO")
    print("Nombre: " + dic["Name"])
    print("País: " + dic["Country"])
    print("IATA: " + dic["IATA"])
    print("Latitud: " + dic["Latitude"])
    print("Longitud: " + dic["Longitude"])

def printLastCity(analyzer):
    citiesMap = analyzer["cities"]
    cities = mp.keySet(citiesMap)
    key = lt.getElement(cities, lt.size(cities))
    dic = mp.get(citiesMap, key)["value"]

    print("\nÚLTIMA CIUDAD CARGADA")
    print("Nombre: " + dic["city_ascii"])
    print("Población: " + dic["population"])
    print("Latitud: " + dic["lat"])
    print("Longitud: " + dic["lng"])

def numVertices(graph):
    return gr.numVertices(graph)

# Funciones utilizadas para comparar elementos dentro de una lista
def compareAirportIds(airport, keyValueAirport):
    """
    Compara dos estaciones
    """
    airportCode = keyValueAirport['key']
    if (airport == airportCode):
        return 0
    elif (airport > airportCode):
        return 1
    else:
        return -1

def cmpStrings(string, key):
    """
    Compara dos estaciones
    """
    keyString = key['key']
    if (string == keyString):
        return 0
    elif (string > keyString):
        return 1
    else:
        return -1

# Funciones de ordenamiento

# Funciones de verificación
def verifyDistance(route):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if route['distance_km'] == '':
        route['distance_km'] = 0
