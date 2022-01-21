# Comentar o descomentar para descargar el fichero si es necesario
# !wget 'https://covid.ourworldindata.org/data/ecdc/full_data.csv'

# Importación de librerías
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
import time
import datetime

# Ingreso del pais
def IngresarPais():
    condicion = 0
    pais = " "
    pais = input("Ingrese país: ")
    # Se valida pais existente o "?" para ver el listado de paises / Se sale solo ingresando un pais válido
    while condicion == 0:
        if pais.upper() in lista_paises:
            condicion = 1
        elif pais.upper() == "?":
            print(str(lista_paises)[1:-1])  # Lista todos los paises
            pais = input("Ingrese pais: ")
        else:
            pais = input(
                "País ingresado inexistente\nIngrese un país existente o ingrese '?' para ver el listado disponible: ")
    return pais


# Seleccion de las fechas Desde y Hasta
def ValidarFechas():
    fecD = 0
    fecH = 0
    while fecD >= fecH:  # No debe permitir ingresar una fecha D > H. # Si se ingresa misma fecha D y H, no se veran resultados, necesitamos al menos dos puntos en el grafico
        fecD = IngresarFechas("DESDE")
        fecH = IngresarFechas("HASTA")
        if fecD == fecH:
            print("No se veran resultados si se ingresa un unico dia")
        elif fecD > fecH:
            print("La fecha Desde no puede ser superior a Hasta")
    return fecD, fecH


# Se valida el ingreso de fechas en formato YYYY-MM-DD
def IngresarFechas(AoH):
    Valida = False
    hoy = datetime.datetime.now()  # Obtengo la fecha actual
    fecha = ""
    while fecha == "":
        while Valida == False:
            try:
                print("Ingresa la fecha", AoH, "en el formato YYYY-MM-DD: ")
                fecha = input()
                datetime.datetime.strptime(fecha, '%Y-%m-%d')
                Valida = True
            except ValueError:
                print("Fecha inválida")
                Valida = False
        if fecha < "2019-12-31":
            print("No existen datos previos al 2020-12-31 para ningun pais")
            fecha = ""
            Valida = False
        elif fecha > str(hoy.date()):
            print("La fecha ingresada es superior a la actual")
            fecha = ""
            Valida = False
    return fecha


def IngresarN():
    while True:
        n = input("Seleccione la cantidad de paises a ingresar para su graficado: ")
        try:
            n = int(n)
            return n
        except ValueError:
            print("Debe ingresar un numero entero")


def CalcularIntersecciones(ejex, ejey):
    crucex = []
    crucey = []
    for i in range(len(pais) - 1):
        for p in range(1, len(ejey[0]) - 1):
            if (ejey[i][p] == ejey[i + 1][p]) or (
                    ejey[i][p] > ejey[i + 1][p] and ejey[i][p - 1] < ejey[i + 1][p - 1]) or (
                    ejey[i][p] < ejey[i + 1][p] and ejey[i][p - 1] > ejey[i + 1][p - 1]):
                crucey.append(ejey[i][p])
                crucex.append(ejex[i][p])
    return crucex, crucey


def MostraryGrabar(titulo):
    imprime = "X"
    while imprime not in ("S", "s", "N", "n"):
        imprime = input("Desea guardar el grafico de "+titulo+" a generar? (s/n) : ")
    if imprime.upper() == "S":
        nombre = input("Ingrese nombre de grabado para el grafico : ")
        plt.savefig(nombre+'.png')
    plt.show()

def GenerarGraficoUnico(pais):
    x = []
    y_casos = []
    y_muertes = []
    maximo_c = 0
    maximo_m = 0
    for i in range(0, len(archivo["date"])):
        if archivo["location"][i] == pais:
            y_casos.append(archivo["total_cases"][i])
            y_muertes.append(archivo["total_deaths"][i])
            x.append(archivo["date"][i])
            maximo_c = archivo["total_cases"][i]
            maximo_m = archivo["total_deaths"][i]
    plt.figure(figsize=(30, 10))
    plt.xlabel("CALENDARIO COMPLETO")
    plt.title(pais)
    plt.plot(x, y_muertes, 'r', label='Total Muertes')
    plt.plot(x, y_casos, 'g', label='Total Casos')
    # Inserto el valor final de cada grafico
    if maximo_c > 0:
        plt.annotate('%d' % maximo_c, xy=(1, maximo_c), xytext=(8, 0), xycoords=('axes fraction', 'data'),
                 textcoords='offset points')
    if maximo_m > 0:
        plt.annotate('%d' % maximo_m, xy=(1, maximo_m), xytext=(8, 0), xycoords=('axes fraction', 'data'),
                 textcoords='offset points')
    plt.xticks(x[::5], rotation=90)
    plt.grid()
    plt.legend()
    MostraryGrabar("Casos y Muertes")


# Para puntos 2 y 3;Params= lista_paises, F desde, F hasta, flag de solicitudes True = punto 2 / False = punto 3
def GenerarGraficos(pais, fecha_desde, fecha_hasta, flag):
    # Para permitir imprimir hasta 21 graficos cambiando de colores/tipos de linea
    colores = ["b", "g", "r", "c", "m", "y", "k", "b-.", "g-.", "r-.", "c-.", "m-.", "y-.", "k-.", "b--", "g--", "r--",
               "c--", "m--", "y--", "k--"]
    x = []
    y_casos = []
    y_muertes = []
    max_casos = []
    max_muertes = []
    crucex = []
    crucey = []

    for p in range(len(pais)):
        x.append([])
        y_muertes.append([])
        y_casos.append([])
        max_casos.append([])
        max_muertes.append([])
        for i in range(0, len(archivo["date"])):
            max_casos[p] = 0
            max_muertes[p] = 0
            if archivo["location"][i] == pais[p] and archivo["date"][i] >= fecha_desde and archivo["date"][i] <= fecha_hasta:
                x[p].append(archivo["date"][i])
                y_casos[p].append(archivo["total_cases"][i])
                y_muertes[p].append(archivo["total_deaths"][i])
                max_casos[p] = archivo["total_cases"][i]
                max_muertes[p] = archivo["total_deaths"][i]

    start = datetime.datetime.strptime(fecha_desde, "%Y-%m-%d")
    end = datetime.datetime.strptime(fecha_hasta, "%Y-%m-%d")
    calendario = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]

    dias = []
    for date in calendario:
        dias.append(date.strftime("%Y-%m-%d"))

    if len(dias) >= 50:
        cant_eje = int(len(dias) / 50)  # Cada cuantos dias ver eje Y
    else:
        cant_eje = 1

        # Completo los dias que no hayan reportado casos (aun no tenian casos / fallecidos)
    for t in dias:
        for p in range(len(pais)):
            if t not in x[p]:
                x[p].append(t)
                y_casos[p].append(0)
                y_muertes[p].append(0)

    # Ordeno, aprovechando que los datos son acumulativos, no podria haber decrecimiento de casos o muertes
    for p in range(len(pais)):
        x[p].sort()
        y_casos[p].sort()
        y_muertes[p].sort()

    # Grafico de Casos
    plt.figure(figsize=(30, 10))
    plt.xlabel("CASOS ENTRE EL " + fecha_desde + " Y EL " + fecha_hasta)
    plt.title("CASOS")
    for p in range(len(pais)):
        plt.plot(x[p], y_casos[p], colores[p], label=pais[p])
        plt.annotate('%d' % max_casos[p], xy=(1, max_casos[p]), xytext=(8, 0), xycoords=('axes fraction', 'data'),
                     textcoords='offset points')  # Muestra el valor final de casos

    # Si flag = False es punto 3 y no requiere graficar cruces
    if flag:
        crucex, crucey = CalcularIntersecciones(x, y_casos)
        plt.plot(crucex, crucey, 'k.')

    plt.xticks(dias[::cant_eje], rotation=90)
    plt.grid()
    plt.legend()
    MostraryGrabar("Casos")

    # Si flag = False es punto 3 y no requiere graficar las muertes
    if flag:
        # Grafico de Muertes
        plt.figure(figsize=(30, 10))
        plt.xlabel("FALLECIMIENTOS ENTRE EL " + fecha_desde + " Y EL " + fecha_hasta)
        plt.title("FALLECIMIENTOS")
        for p in range(len(pais)):
            plt.plot(x[p], y_muertes[p], colores[p], label=pais[p])
            plt.annotate('%d' % max_muertes[p], xy=(1, max_muertes[p]), xytext=(8, 0),
                         xycoords=('axes fraction', 'data'),
                         textcoords='offset points')  # Muestra el valor final de muertes
        crucex, crucey = CalcularIntersecciones(x, y_muertes)
        plt.plot(crucex, crucey, 'k.')
        plt.xticks(dias[::cant_eje], rotation=90)
        plt.grid()
        plt.legend()
        MostraryGrabar("Muertes")


def MostrarMenu():
    print("Ingrese Opción Deseada: ")
    print("1. Graficar Casos y Fallecimientos de país a Ingresar ")
    print("2. Graficar Casos y Fallecimientos de 2 paises a Ingresar con Periodo Seleccionable ")
    print("3. Graficar Casos Totales de n paises con Periodo Seleccionable ")
    print("0. Salir ")

# Lectura de archivo
archivo = pd.read_csv("full_data.csv")
# No tomo en cuenta la ubicacion "World"
archivo = archivo[archivo["location"] != "World"]
# Cambio nulos por ceros
archivo['total_deaths'] = archivo['total_deaths'].fillna(0)
archivo['total_cases'] = archivo['total_cases'].fillna(0)
# Paso todos los paises a mayusculas
archivo["location"] = [element.upper() for element in archivo["location"]]
# Genero una lista de paises incluidos en el archivo/ Para chequear que exista lo ingresado y para listar las opciones
lista_paises = []
for i in archivo["location"]:
    if i not in lista_paises:
        lista_paises.append(i)
archivo = archivo.to_dict('list')

# Ingreso de opcion de menu
opcion_menu = "X"
pais = []
while opcion_menu != "0":
    MostrarMenu()
    opcion_menu = input()
    if opcion_menu == "0":
        print("Programa finalizado")
    elif opcion_menu == "1":
        pais_ingresado = IngresarPais()
        pais_ingresado = pais_ingresado.upper()
        GenerarGraficoUnico(pais_ingresado)
    elif opcion_menu == "2":
        FechaD, FechaH = ValidarFechas()
        for i in range(2):
            print("Ingreso del " + str(i + 1) + "° país")
            pais.append(IngresarPais())
            pais[i] = pais[i].upper()
        GenerarGraficos(pais, FechaD, FechaH, True)
    elif opcion_menu == "3":
        FechaD, FechaH = ValidarFechas()
        n_paises = 0
        while n_paises == 0:
            n_paises = IngresarN()
            if n_paises < 2 or n_paises > 20:
                print("Solo se permiten valores entre 2 y 20")
                n_paises = 0
        for i in range(n_paises):
            print("Ingreso del " + str(i + 1) + "° país")
            pais.append(IngresarPais())
            pais[i] = pais[i].upper()
        GenerarGraficos(pais, FechaD, FechaH, False)
    else:
        print("OPCION INEXISTENTE")