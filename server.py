from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        generarMapa(data.get('filtro1'), data.get('filtro2'))
    return render_template('index.html')

@app.route('/mapa.html/')
def mapa_html():
    return render_template('mapa.html')

def generarMapa(filtro1, filtro2):
    import folium

    m = folium.Map(location=[43.276803, -2.950852], tiles="cartodb positron")
    if filtro1 == "checked":
        folium.Marker(location=[43.276803, -2.950852], popup = 'Sakarya').add_to(m)
    if filtro2 == "checked":
        folium.CircleMarker(location=(43.276803, -2.950852),radius=100, fill_color='blue').add_to(m)

    m.save("templates/mapa.html")

if __name__ == '__main__':
    generarMapa("unchecked", "unchecked")
    app.run(host='0.0.0.0', debug=True)
