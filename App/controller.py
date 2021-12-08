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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de rutas.
def init():
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos
def loadData(analyzer, airportsFileName, routesFileName, citiesFileName):
    airports = cf.data_dir + airportsFileName
    airportsFile = csv.DictReader(open(airports, encoding="utf-8"),
                                delimiter=",")
    routes = cf.data_dir + routesFileName
    routesFile = csv.DictReader(open(routes, encoding="utf-8"),
                                delimiter=",")
    cities = cf.data_dir + citiesFileName
    citiesFile = csv.DictReader(open(cities, encoding="utf-8"),
                                delimiter=",")  

    firstAirport = None
    lastAirport = None
    firstCity = None
    lastCity = None 

    #Añadir aeropuertos al mapa
    for airport in airportsFile:
        model.addAirportRoute(analyzer["routes"], airport["IATA"])
        model.addAirportRoute(analyzer["roundTrip"], airport["IATA"])
        model.addAirport(analyzer, airport)

    #Añadir rutas al grafo dirigido
    for route in routesFile:
        if firstAirport == None:
            firstAirport = route["Departure"]
        lastAirport = route["Destination"]
        model.addRoute(analyzer, route)

    #Añadir rutas al grafo no dirigido
    model.createNonDirGraph(analyzer)

    #Añadir ciudades al mapa
    for city in citiesFile:
        if firstCity == None:
            firstCity = city["city_ascii"]
        lastCity = city["city_ascii"]
        model.addCity(analyzer, city)  

    analyzer["firstAirport"] = model.getAirportByIATA(firstAirport, analyzer)
    analyzer["lastAirport"] = model.getAirportByIATA(lastAirport, analyzer)
    analyzer["firstCity"] = model.getCity(firstCity, analyzer)
    analyzer["lastCity"] = model.getCity(lastCity, analyzer)

    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def mapSize(map):

    return model.mapSize(map)

def totalConnections(graph):

    return model.totalConnections(graph)

def numVertices(graph):

    return model.numVertices(graph)

def minRoute(analyzer):

    return model.minRoute(analyzer)

def findInterconection(analyzer):

    return model.findInterconection(analyzer)

def findClusters(analyzer):

    return model.findClusters(analyzer)

def closedAirport(analyzer):
    
    return model.closedAirport(analyzer) 

def ordMapSize(map):
    
    return model.ordMapSize(map)

def printFirstLastAirports(analyzer):

    model.printFirstLastAirports(analyzer)

def printFirstLastCities(analyzer):

    model.printFirstLastCities(analyzer)

#Funciones auxiliares
def selectSample(sample):
    airportStr = "airports-utf8-"
    routeStr = "routes-utf8-"

    if sample == 1:
        airportStr += "small.csv"
        routeStr += "small.csv"
    
    elif sample == 2:
        airportStr += "5pct.csv"
        routeStr += "5pct.csv"

    elif sample == 3:
        airportStr += "10pct.csv"
        routeStr += "10pct.csv"

    elif sample == 4:
        airportStr += "20pct.csv"
        routeStr += "20pct.csv"
    
    elif sample == 5:
        airportStr += "30pct.csv"
        routeStr += "30pct.csv"

    elif sample == 6:
        airportStr += "50pct.csv"
        routeStr += "50pct.csv"

    elif sample == 7:
        airportStr += "80pct.csv"
        routeStr += "80pct.csv"

    elif sample == 8:
        airportStr += "large.csv"
        routeStr += "large.csv"

    return airportStr,routeStr

