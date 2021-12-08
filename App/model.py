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
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Utils import error as error
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from haversine import haversine, Unit
import webbrowser
import folium
from prettytable import PrettyTable
from DISClib.Algorithms.Graphs import scc as scc
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs.dijsktra import Dijkstra
from DISClib.Algorithms.Graphs.bellmanford import BellmanFord
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    try:
        analyzer = {
                    'airportsByLat': None,
                    'airpotsByIATA' : None,
                    'routes': None,
                    'cities': None,
                    'roundTrip': None
                    }

        analyzer['airportsByLat'] = om.newMap(omaptype='RBT',
                                     comparefunction=cmpFloats)

        analyzer['airportsByIATA'] = mp.newMap(maptype='CHAINING',
                                     comparefunction=cmpStrings)

        analyzer['routes'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=4000,
                                              comparefunction=compareAirportIds)

        analyzer["cities"] = mp.newMap(numelements=37500, maptype="PROBING", comparefunction=cmpStrings)

        analyzer["roundTrip"] = gr.newGraph(datastructure="ADJ_LIST", directed=False, size=3500, comparefunction=compareAirportIds)
        
        return analyzer
    
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo
def addRoute(analyzer, route):
    try:
        origin = route["Departure"]
        destination = route["Destination"] 
        verifyDistance(route)
        #addAirportRoute(analyzer, origin)
        #addAirportRoute(analyzer, destination)
        addConnection(analyzer, origin, destination, route["distance_km"])
        return analyzer

    except Exception as exp:
        error.reraise(exp, 'model:addRoute')

def addAirportRoute(graph, airportID):
    """
    Adiciona un aeropuerto como un vertice del grafo
    """
    try:
        if not gr.containsVertex(graph, airportID):
            gr.insertVertex(graph, airportID)
        return graph
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
    lat = str(round(float(airport["Latitude"]),2))
    lon = str(round(float(airport["Longitude"]),2))
    isPresent = om.contains(analyzer["airportsByLat"], lat)
    if isPresent == True:
        mapLon = om.get(analyzer["airportsByLat"], lat)["value"]
        if om.contains(mapLon, lon) == True:
            listLon = om.get(mapLon, lon)["value"]
            lt.addLast(listLon, airport)
            om.put(mapLon, lon, listLon)
        else:
            listLon = lt.newList('ARRAY_LIST')
            lt.addLast(listLon, airport)
            om.put(mapLon, lon, listLon)
        om.put(analyzer["airportsByLat"], lat, mapLon)
    
    else:
        mapLon = om.newMap("RBT",cmpFloats)
        listLon = lt.newList('ARRAY_LIST')
        lt.addLast(listLon, airport)
        om.put(mapLon, lon, listLon)
        om.put(analyzer["airportsByLat"], lat, mapLon)
    
    IATA = airport["IATA"]
    isPresent = mp.contains(analyzer["airportsByIATA"], IATA)
    if isPresent == True:
            listIATA = mp.get(analyzer["airportsByIATA"], IATA)["value"]
            lt.addLast(listIATA, airport)
            mp.put(analyzer["airportsByIATA"], IATA, listIATA)
    else:
            listIATA = lt.newList('ARRAY_LIST')
            lt.addLast(listIATA, airport)
            mp.put(analyzer["airportsByIATA"], IATA, listIATA)


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
    size = 0

    keys = mp.keySet(map)

    for key in lt.iterator(keys):
        actualSize = lt.size(mp.get(map, key)["value"])
        size += actualSize

    return size

def ordMapSize(map):
    size = 0

    keys = om.keySet(map)

    for key in lt.iterator(keys):
        actualSize = lt.size(om.get(map, key)["value"])
        size += actualSize

    return size

def totalConnections(graph):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(graph)

def numVertices(graph):
    return gr.numVertices(graph)

def findInterconection(analyzer):

    airportsbyDegree = lt.newList(datastructure="ARRAY_LIST")
    mostInteractions = lt.newList(datastructure="ARRAY_LIST")
    routes = analyzer["routes"]
    vertices = gr.vertices(routes)
    totalEdges = gr.edges(routes)

    for vertex in lt.iterator(vertices):
        inDegree = gr.indegree(routes, vertex)
        outDegree = gr.outdegree(routes, vertex)
        actualDegree = inDegree + outDegree
        element = {"key": vertex, "value": actualDegree}
        lt.addLast(airportsbyDegree, element)
    
    ms.sort(airportsbyDegree, cmpDegree)
    size = lt.size(airportsbyDegree)
    
    for i in range(1, 6):
        index = (lt.size(airportsbyDegree)+1)-i
        iata = lt.getElement(airportsbyDegree, index)
        lt.addLast(mostInteractions, iata["key"])
    
    printFindInterconections(analyzer, mostInteractions, size)

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
            print("No se encontró la ciudad.")
    

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
            print("No se encontró la ciudad.")

        airport1 = closestAirport(analyzer, dictCity1)
        distance1 = haversine((float(dictCity1["lat"]), float(dictCity1["lng"])), (float(airport1["Latitude"]), float(airport1["Longitude"]))) #Km
        print("\nCIUDAD Y AEROPUERTO DE SALIDA")
        printAirportAndCity(airport1, dictCity1, distance1)
        airport2 = closestAirport(analyzer, dictCity2)
        distance2 = haversine((float(dictCity2["lat"]), float(dictCity2["lng"])), (float(airport2["Latitude"]), float(airport2["Longitude"]))) #Km
        print("\nCIUDAD Y AEROPUERTO DE LLEGADA")
        printAirportAndCity(airport2, dictCity2,distance2)

    except Exception as exp:
        error.reraise(exp, 'model:minRoute')

def findClusters(analyzer):
    iata0 = input("Ingrese el código IATA del primer aeropuerto: ")
    iata1 = input("Ingrese el código IATA del segundo aeropuerto: ")
    stronglyConnected = scc.KosarajuSCC(analyzer["routes"])

    totalSCC = stronglyConnected["components"]
    idSCC = stronglyConnected["idscc"]

    sameSCC = "no"
    if mp.get(idSCC, iata0)["value"] == mp.get(idSCC, iata1)["value"]:
        sameSCC = "sí" 

    print("\nEl total de clústeres es de " + str(totalSCC) + ".")
    print("\nLos dos aeropuertos " + sameSCC + " pertenecen al mismo clúster.")

def closedAirport(analyzer):
    iata = input("Ingrese el código IATA del aeropuerto: ")

    routes = analyzer["routes"]
    totalEdges = gr.edges(routes) 
    result = lt.newList(datastructure="ARRAY_LIST")
    
    for actualedge in lt.iterator(totalEdges):
        if actualedge["vertexB"] == iata:
            if not lt.isPresent(result, actualedge["vertexA"]):
                lt.addLast(result,  actualedge["vertexA"])
    
        if actualedge["vertexA"] == iata:
            if not lt.isPresent(result, actualedge["vertexB"]):
                lt.addLast(result,  actualedge["vertexB"])

    printclosedAirport(analyzer, result, iata)

def getAirportByIATA(IATA, analyzer):
    airports = analyzer["airportsByIATA"]
    airport = lt.getElement(mp.get(airports, IATA)["value"], 1)

    return airport

def getCity(city, analyzer):
    cities = analyzer["cities"]
    city = lt.getElement(mp.get(cities, city)["value"], 1)

    return city

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

def cmpStrings2(string, key):
    """
    Compara dos strings
    """
    keyString = key
    if (string == keyString):
        return 0
    elif (string > keyString):
        return 1
    else:
        return -1

def cmpFloats(float1, float2):
        float1 = float(float1)
        float2 = float(float2)
        if (float1 == float2):
                return 0
        elif (float1 > float2):
                return 1
        else:
                return -1

def cmpDegree(degree1, degree2):

    degree1 = degree1["value"]
    degree2 = degree2["value"]
    try:
        int(degree1)
        int(degree2)
        its_int = True
    except ValueError:
        its_int = False
        return False

    if its_int == True:
        return degree1 < degree2

def cmpIATA(iata1, iata2):

        return iata1 < iata2

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

def printFindInterconections(analyzer, mostInteractions, size):

    airports = analyzer["airportsByIATA"]
    keyset = mostInteractions["elements"]
    table = PrettyTable()
    table.field_names = ["IATA", "Nombre", "Ciudad", "País"]
    print("\nHay " + str(size) + " aereopuertos interconectados en la red")
    print("\nEl TOP 5 de los aereopuertos más interconectados son: ")
    for iata in keyset:
        actualIATA = mp.get(airports, iata)["value"]
        actualIATA = actualIATA["elements"][0]
        table.add_row([actualIATA["IATA"], actualIATA["Name"], actualIATA["City"], actualIATA["Country"]])
    print(table)

def printclosedAirport(analyzer, result, iata):

    airports = analyzer["airportsByIATA"]
    size = lt.size(result)
    ms.sort(result, cmpIATA)
    result = result["elements"]
    table = PrettyTable()
    table.field_names = ["IATA", "Nombre", "Ciudad", "País"]
    print("\nHay " + str(size) + " aereopuertos afectados por el cierre de " + iata + ".")
    print("\nLos primeros y últimos 3 afectados son: ")
    if size >= 6:
        for m in range(1, 4):
            iata = result[m]
            actualIATA = mp.get(airports, iata)["value"]
            actualIATA = actualIATA["elements"][0]
            table.add_row([actualIATA["IATA"], actualIATA["Name"], actualIATA["City"], actualIATA["Country"]])
        for n in range(1, 4):
            index = (size)-n
            iata = result[index]
            actualIATA = mp.get(airports, iata)["value"]
            actualIATA = actualIATA["elements"][0]
            table.add_row([actualIATA["IATA"], actualIATA["Name"], actualIATA["City"], actualIATA["Country"]])
    else:
        for element in result:
            actualIATA = mp.get(airports, element)["value"]
            actualIATA = actualIATA["elements"][0]
            table.add_row([actualIATA["IATA"], actualIATA["Name"], actualIATA["City"], actualIATA["Country"]])
    
    print(table)

def printFirstLastAirports(analyzer):
    table = PrettyTable()
    table.field_names = ["Nombre", "Ciudad", "País", "Latitud", "Longitud"]
    airport0 = analyzer["firstAirport"]
    airport1 = analyzer["lastAirport"]
    table.add_row([airport0["Name"], airport0["City"], airport0["Country"], airport0["Latitude"], airport0["Longitude"]])
    table.add_row([airport1["Name"], airport1["City"], airport1["Country"], airport1["Latitude"], airport1["Longitude"]])
    print("\nPRIMER Y ÚLTIMO AEROPUERTO CARGADO")
    print(table)

def printFirstLastCities(analyzer):
    table = PrettyTable()
    table.field_names = ["Ciudad", "Población", "Latitud", "Longitud"]
    city0 = analyzer["firstCity"]
    city1 = analyzer["lastCity"]
    table.add_row([city0["city_ascii"], city0["population"], city0["lat"], city0["lng"]])
    table.add_row([city1["city_ascii"], city1["population"], city1["lat"], city1["lng"]])
    print("\nPRIMERA Y ÚLTIMA CIUDAD CARGADA")
    print(table)

def closestAirport(analyzer, city):
    lon = city["lng"]
    lat = city["lat"]

    airportsTree = analyzer["airportsByLat"]
    north = float(lat)+(float(lat)*0.005)
    south = float(lat)-(float(lat)*0.005)
    east = float(lon)-(float(lon)*0.005)
    west = float(lon)+(float(lon)*0.005)

    closeAirports = findAirports(airportsTree, north, south, east, west) 

    if lt.size(closeAirports) > 1:
        minDistance = 1000000000000
        closestAirport = None

        for airport in lt.iterator(closeAirports):
            distance = haversine((float(lat), float(lon)), (float(airport["Latitude"]), float(airport["Longitude"]))) #Km
            if minDistance > distance:
                minDistance = distance
                closestAirport = airport
    else:
        closestAirport = lt.getElement(closeAirports, 1)

    return closestAirport

def findAirports(tree, north, south, east, west):
    filteredByLat = om.values(tree, south, north) #Lista de mapas
    filteredAirports = lt.newList("ARRAY_LIST")

    if lt.size(filteredByLat) != 0:
        for map in lt.iterator(filteredByLat):
            filteredLon = om.values(map, east, west) #Lista de listas
            if lt.size(filteredLon) != 0:
                for lonList in lt.iterator(filteredLon):
                    if lt.size(lonList) != 0:
                        for airport in lt.iterator(lonList):
                            lt.addLast(filteredAirports, airport)

    if lt.size(filteredAirports) == 0:
        filteredAirports = findAirports(tree, north+(north*0.005), south-(south*0.005), west+(west*0.005), east-(east*0.005))

    return filteredAirports 

def printAirportAndCity(airport, city, distance):
    table0 = PrettyTable()
    table0.field_names = ["Ciudad", "Estado", "País", "Latitud", "Longitud"]
    table0.add_row([city["city_ascii"], city["admin_name"],city["country"], city["lat"], city["lng"]])
    
    table1 = PrettyTable()
    table1.field_names = ["Nombre", "Ciudad", "País", "IATA", "Latitud", "Longitud"]
    table1.add_row([airport["Name"], airport["City"], airport["Country"], airport["IATA"], airport["Latitude"], airport["Longitude"]])
    
    print(table0)
    print(table1)
    print("La distancia entre la ciudad y el aeropuerto es de ", distance, " km.")

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