import folium
from DB import DB
import json

class Mapa:
    def __init__(self):
        self.myDB = DB()
        self.indicators = self.myDB.getIndicators()
        geojson_f = open('geodata/municipios.geojson')
        self.geojson = json.load(geojson_f)
        self.cargarGeoJson()

    def cargarGeoJson(self):
        for municipio in self.geojson['features']:
            for ind in self.indicators:
                cursorInd = self.myDB.getCursorIndMunicipio(ind, municipio)
                for i in cursorInd:
                    municipio['properties']['indicator_' + str(ind) + '_2021'] = i['data']['2021']
                    municipio['properties']['indicator_' + str(ind) + '_2020'] = i['data']['2020']
                    municipio['properties']['indicator_' + str(ind) + '_2019'] = i['data']['2019']

    def generarMapa(self, filtros, añosInd, fechaIncidencia):
        m = folium.Map(location=[43.276803, -2.950852], tiles="cartodb positron")
        geojson_fields = ['iz_ofizial']
        geojson_aliases = ['Municipio:']
        myIFrame = None
        myIcon = None
        myPopup = None

        # Indicadores
        indIn = 1
        for indicator in self.indicators:
            if filtros['filtroInd' + str(indIn)]:
                año = añosInd['filtroInd' + str(indIn)]
                geojson_fields.append('indicator_' + str(indicator) + '_' + año)
                geojson_aliases.append(self.indicators[indicator] + ' (' + año + ')')
            indIn = indIn + 1
        # Trafico
        if filtros['filtroTraf1']:
            cursorCamaras = self.myDB.getCamaras()
            for camara in cursorCamaras:
                #myIFrame = folium.IFrame('<strong>Latitud:</strong> ' + camara['latitud'] + '<br><br>' + '<strong>Longitud:</strong> ' + camara['longitud'])
                #myPopup = folium.Popup(myIFrame, min_width=300, max_width=500)
                myIcon = folium.Icon(color='red', icon='video-camera', prefix='fa')
                folium.Marker(location=[camara['latitud'], camara['longitud']], icon = myIcon).add_to(m)
        if filtros['filtroTraf2']:
            cursorIncidencias = self.myDB.getIncidenciasDia(fechaIncidencia)
            for inc in cursorIncidencias:
                myIFrame = folium.IFrame('<strong>Día:</strong> ' + inc['dia'] + '<br><br><strong>Hora:</strong> ' + inc['hora'] + '<br><br><strong>Tipo:</strong> ' + inc['tipo'] + '<br><br><strong>Causa:</strong> ' + inc['causa'])
                myPopup = folium.Popup(myIFrame, min_width=300, max_width=500)
                myIcon = folium.Icon(color='red', icon='car', prefix='fa')
                folium.Marker(location=[inc['latitud'], inc['longitud']],popup = myPopup, icon = myIcon).add_to(m)
        # Eventos
        cursoresEventos = []
        if filtros['filtroEv1']:
            cursoresEventos.append(self.myDB.getEventosTodos())
        else:
            if filtros['filtroEv2']:
                cursoresEventos.append(self.myDB.getEventosConciertos())
            if filtros['filtroEv3']:
                cursoresEventos.append(self.myDB.getEventosTeatro())
            if filtros['filtroEv4']:
                cursoresEventos.append(self.myDB.getEventosDanza())
            if filtros['filtroEv5']:
                cursoresEventos.append(self.myDB.getEventosConferencia())
            if filtros['filtroEv6']:
                cursoresEventos.append(self.myDB.getEventosBertsolaritza())
            if filtros['filtroEv7']:
                cursoresEventos.append(self.myDB.getEventosFeria())
            if filtros['filtroEv8']:
                cursoresEventos.append(self.myDB.getEventosExposicion())
            if filtros['filtroEv9']:
                cursoresEventos.append(self.myDB.getEventosProyeccion())
            if filtros['filtroEv10']:
                cursoresEventos.append(self.myDB.getEventosFormacion())
            if filtros['filtroEv11']:
                cursoresEventos.append(self.myDB.getEventosConcurso())
            if filtros['filtroEv12']:
                cursoresEventos.append(self.myDB.getEventosFestival())
            if filtros['filtroEv13']:
                cursoresEventos.append(self.myDB.getEventosInfantil())
            if filtros['filtroEv14']:
                cursoresEventos.append(self.myDB.getEventosFiestas())
            if filtros['filtroEv15']:
                cursoresEventos.append(self.myDB.getEventosOtro())
        for cursorEventos in cursoresEventos:
            for evento in cursorEventos:
                myIFrame = folium.IFrame('<strong>Nombre:</strong> ' + evento['nombre'] + '<br><br><strong>Tipo de evento:</strong> ' + evento['tipo'] + '<br><br><strong>Día:</strong> ' + evento['dia'] + '<br><br><strong>Hora:</strong> ' + evento['hora'] + '<br><br><strong>Precio:</strong> ' + evento['precio'])
                myPopup = folium.Popup(myIFrame, min_width=300, max_width=500)
                myIcon = self.getIconoEvento(evento)
                folium.Marker(location=[evento['latitud'], evento['longitud']], popup = myPopup, icon = myIcon).add_to(m)

        folium.GeoJson(self.geojson, tooltip=folium.features.GeoJsonTooltip(fields=geojson_fields, aliases=geojson_aliases)).add_to(m)
        m.fit_bounds(m.get_bounds())
        m.save("templates/mapa.html")

    def getIconoEvento(self, evento):
        myIcon = folium.Icon(color='green', icon='question', prefix='fa')
        if evento['tipoCod'] == 1: #concierto
            myIcon = folium.Icon(color='green', icon='music', prefix='fa')
        if evento['tipoCod'] == 2: #teatro
            myIcon = folium.Icon(color='green', icon='film', prefix='fa')
        if evento['tipoCod'] == 4: #danza
            myIcon = folium.Icon(color='green', icon='female', prefix='fa')
        if evento['tipoCod'] == 6: #conferencia
            myIcon = folium.Icon(color='green', icon='bar-chart', prefix='fa')
        if evento['tipoCod'] == 7: #bertsolaritza
            myIcon = folium.Icon(color='green', icon='microphone', prefix='fa')
        if evento['tipoCod'] == 8: #feria
            myIcon = folium.Icon(color='green', icon='balance-scale', prefix='fa')
        if evento['tipoCod'] == 9 or evento['tipoCod'] == 3: #exposicion o proyeccion audiovisual
            myIcon = folium.Icon(color='green', icon='play', prefix='fa')
        if evento['tipoCod'] == 11: #formacion
            myIcon = folium.Icon(color='green', icon='graduation-cap', prefix='fa')
        if evento['tipoCod'] == 12: #concurso
            myIcon = folium.Icon(color='green', icon='video-camera', prefix='fa')
        if evento['tipoCod'] == 13: #festival
            myIcon = folium.Icon(color='green', icon='users', prefix='fa')
        if evento['tipoCod'] == 14: #actividad infantil
            myIcon = folium.Icon(color='green', icon='child', prefix='fa')
        if evento['tipoCod'] == 15: #otro
            myIcon = folium.Icon(color='green', icon='question', prefix='fa')
        if evento['tipoCod'] == 16: #fiestas
            myIcon = folium.Icon(color='green', icon='flag', prefix='fa')
        return myIcon

