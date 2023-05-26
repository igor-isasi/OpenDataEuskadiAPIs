import requests

def getIndicator(indicator):
    qUrl = "https://api.euskadi.eus/udalmap/indicators/" + str(indicator) + "/municipalities"
    myHeaders = {'accept': 'application/json'}
    myParams = {'lang': 'SPANISH'}
    response = requests.get(url=qUrl, headers=myHeaders, params=myParams)
    myJson = response.json()
    return myJson

def getEventosMes(año, mes):
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/byMonth/" + str(año) + "/" + str(mes)
    qParams = {'_elements': 5000}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    myJson = response.json()
    return myJson

def getCamaras():
    qUrl = "https://api.euskadi.eus/traffic/v1.0/cameras"
    qParams = {'_page': 1}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    myJson = response.json()
    nPaginas = myJson['totalPages']
    myJsonList = []
    # se solicitan todas las paginas hasta conseguir todas las camaras
    for pagActual in range(1, nPaginas + 1):
        qParams = {'_page': pagActual}
        response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
        myJsonList.append(response.json())
    return myJsonList

def getIncidenciasMes(año, mes):
    qUrl = "https://api.euskadi.eus/traffic/v1.0/incidences/byMonth/" + str(año) + "/" + str(mes)
    qParams = {'_page': 1}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    myJson = response.json()
    nPaginas = myJson['totalPages']
    myJsonList = []
    # se solicitan todas las paginas hasta conseguir todas las camaras
    for pagActual in range(1, nPaginas + 1):
        qParams = {'_page': pagActual}
        response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
        myJsonList.append(response.json())
    return myJsonList
