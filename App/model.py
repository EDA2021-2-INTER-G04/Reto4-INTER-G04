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
from haversine import haversine, Unit
import webbrowser
import folium
from prettytable import PrettyTable
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
                    'cities': None,
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
        error.reraise(exp, 'model:addRoute')

def addAirportRoute(analyzer, airportID):
    """
    Adiciona un aeropuerto como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['routes'], airportID):
            gr.insertVertex(analyzer['routes'], airportID)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addAirportRoute')

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
    key = city["city_ascii"]
    isPresent = mp.contains(analyzer["cities"], key)
    if isPresent == True:
        listCities = mp.get(analyzer["cities"], key)["value"]
        lt.addLast(listCities, city)
        mp.put(analyzer["cities"], key, listCities)
    else:
        listCities = lt.newList('ARRAY_LIST')
        lt.addLast(listCities, city)
        mp.put(analyzer["cities"], key, listCities) 

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
    airport = mp.get(airportsMap, key)["value"]
    print("\nPRIMER AEROPUERTO CARGADO")
    table = PrettyTable()
    table.field_names = ["Nombre", "País", "IATA", "Latitud", "Longitud"]
    table.add_row([airport["Name"], airport["Country"], airport["IATA"], airport["Latitude"], airport["Longitude"]])
    print(table)

def printLastCity(analyzer):
    citiesMap = analyzer["cities"]
    cities = mp.keySet(citiesMap)
    key = lt.getElement(cities, lt.size(cities))
    list = mp.get(citiesMap, key)["value"]
    city = lt.getElement(list, lt.size(list))
    print("\nÚLTIMA CIUDAD CARGADA")
    table = PrettyTable()
    table.field_names = ["Ciudad", "País", "Estado", "Latitud", "Longitud", "Población"]
    table.add_row([city["city_ascii"], city["country"], city["admin_name"], city["lat"], city["lng"], city["population"]])
    print(table)

def numVertices(graph):
    return gr.numVertices(graph)

def minRoute(analyzer):
    try:
        cities = analyzer["cities"]
        inputCity1 = input("Ingrese el nombre de la ciudad de origen: ")
        cityList1 = mp.get(cities, inputCity1)["value"]
        
        if cityList1 != None:
            if lt.size(cityList1) > 1:
                printCityOptions(cityList1)
                pos = input("Ingrese el número de la ciudad que desea seleccionar: ") 
                dictCity1 = lt.getElement(cityList1, int(pos))
            else:
                dictCity1 = lt.getElement(cityList1, 1)
        else:
            print("No se encontró la ciudad")
        #map(dictCity1)
        inputCity2 = input("\nIngrese el nombre de la ciudad de destino: ")
        cityList2 = mp.get(cities, inputCity2)["value"]
        
        if cityList2 != None:
            if lt.size(cityList2) > 1:
                printCityOptions(cityList2)
                pos = input("Ingrese el número de la ciudad que desea seleccionar: ") 
                dictCity2 = lt.getElement(cityList2, int(pos))
            else:
                dictCity2 = lt.getElement(cityList2, 1)
        else:
            print("No se encontró la ciudad")

    except Exception as exp:
        error.reraise(exp, 'model:minRoute')

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
    Compara dos strings
    """
    keyString = key['key']
    if (string == keyString):
        return 0
    elif (string > keyString):
        return 1
    else:
        return -1

# Funciones de ordenamiento

# Funciones auxiliares
def verifyDistance(route):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if route['distance_km'] == '':
        route['distance_km'] = 0

def printCityOptions(cityList):
    table = PrettyTable()
    table.field_names = ["No.", "Ciudad", "Latitud", "Longitud", "País", "Estado", "Población"]
    for position in range(1, lt.size(cityList)+1):
        city = lt.getElement(cityList, position)
        table.add_row([str(position), city["city_ascii"], city["lat"], city["lng"], city["country"], city["admin_name"], city["population"]])
    print(table)

#def map(city):
    """
    lat = float(city["lat"])
    lon = float(city["lng"])
    map = folium.Map(location=[lat,lon], zoom_start=10, control_scale=True)

    #Aumentar north y west = *
    #Aumentar south y east = /
    north = lat*1.001
    south = lat/1.001
    east = lon/1.001
    west = lon*1.001
    folium.Rectangle(
    bounds=[[north,east],[south, west],[north,west],[south,east]],
    color="#3186cc",
    fill=True,
    fill_color="#3186cc",
    ).add_to(map)

    folium.Rectangle(
    bounds=[[north*1.001,east/1.001],[south/1.001, west*1.001],[north*1.001,west*1.001],[south/1.001,east/1.001]],
    color="#ff0000",
    fill=True,
    fill_color="#ff0000",
    ).add_to(map)

    map.save("map.html")
    mapDir = cf.file_dir + "/map.html"
    print(mapDir)
    webbrowser.open(mapDir, new=1)
    """