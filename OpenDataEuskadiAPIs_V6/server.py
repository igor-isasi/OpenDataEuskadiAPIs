from flask import Flask, render_template, request
from mapa import Mapa
import json

app = Flask(__name__)
myMapa = Mapa()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
         return render_template('index.html')
    if request.method == 'POST':
        data = request.form
        filtros = json.loads(data['filtros'])
        print(filtros, flush=True)
        añosInd = json.loads(data['añosInd'])
        print(añosInd, flush=True)
        fechaIncidencia = data['fechaIncidencia']
        print(fechaIncidencia, flush=True)
        myMapa.generarMapa(filtros, añosInd, fechaIncidencia)
        return 'mapa cargado'

@app.route('/mapa.html/')
def mapa_html():
    return render_template('mapa.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
