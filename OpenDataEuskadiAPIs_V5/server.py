from flask import Flask, render_template, request
from apis import Apis
import json

app = Flask(__name__)

indicators = {10: 'Tasa de ocupación de la población de 16 y mas años (%)',
              8: 'Tasa de actividad (%)',
              44: 'Índice de sobreenvejecimiento: Población de 75 y más años (%)',
              160: 'Consumo eléctrico anual no industrial (Kwh./habitante)'}
my_apis = Apis(indicators)

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
        my_apis.generarMapa(filtros, añosInd)
        return 'mapa cargado'

@app.route('/mapa.html/')
def mapa_html():
    return render_template('mapa.html')

@app.route('/prueba.html/')
def prueba_html():
    return render_template('prueba.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
