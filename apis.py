import json
import requests

# función para imprimir json más entendibles mediante la json.dumps()
def jprint(rJson):
    print(json.dumps(rJson, indent=4))

# definición de los campos de la solicitud a la API REST
qUrl = "https://api.euskadi.eus/udalmap/groups"
qParams = {'lang': 'SPANISH', 'summarized': 'false'}
qHeaders = {'accept': 'application/json'}

# solictud a la API REST
response = requests.get(url=qUrl, params=qParams, headers=qHeaders)


# se comprueba que la respuesta de la API es exitosa
# si el código de respuesta está entre 200 y 400 devuelve true, si no false
if response.ok:
    rJson = response.json()

    """ jPrint(rJson) """
    
    # guardar el json en un fichero
    """ with open("data_file.json", "w") as write_file:
        json.dump(response.json(), write_file) """
    
    """ jprint(rJson[0]['subgroups'][0]['indicators'][0]) """
    jprint(requests.get(url=rJson[0]['subgroups'][0]['indicators'][0]['_links']['self']['href']).json())
else:
    print(str(response.status_code) + " " + str(response.reason))