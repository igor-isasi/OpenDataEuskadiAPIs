import requests
import json
import folium
from arango import ArangoClient
from geopy.geocoders import Nominatim

import traceback
import sys

class Apis:
    def __init__(self, indicators):
        self.indicators = indicators

        client = ArangoClient(hosts='http://127.0.0.1:8529')
        sys_db = client.db(name='_system', username='root', password='root_passwd')
        if sys_db.has_database('ODE'):
            sys_db.delete_database('ODE')
        sys_db.create_database('ODE')
        self.db = client.db('ODE', username='root', password='root_passwd')
        self.cargarDB()

        geojson_f = open('geodata/municipios.geojson')
        self.geojson = json.load(geojson_f)
        self.cargarGeoJson()

    def getEventosTodos(self):
        cursorEventos = self.db.aql.execute('FOR doc IN eventos RETURN doc')
        return cursorEventos

    def getEventosConciertos(self):
        cursorEventos = self.db.aql.execute('FOR doc IN eventos FILTER doc.tipoCod == @value RETURN doc', bind_vars={'value': 1})
        return cursorEventos

    def getEventosTeatro(self):
        cursorEventos = self.db.aql.execute('FOR doc IN eventos FILTER doc.tipoCod == @value RETURN doc', bind_vars={'value': 2})
        return cursorEventos

    def getEventosDanza(self):
        cursorEventos = self.db.aql.execute('FOR doc IN eventos FILTER doc.tipoCod == @value RETURN doc', bind_vars={'value': 4})
        return cursorEventos

    def getEventosConferencia(self):
        cursorEventos = self.db.aql.execute('FOR doc IN eventos FILTER doc.tipoCod == @value RETURN doc', bind_vars={'value': 6})
        return cursorEventos

    def getEventosBertsolaritza(self):
        cursorEventos = self.db.aql.execute('FOR doc IN eventos FILTER doc.tipoCod == @value RETURN doc', bind_vars={'value': 7})
        return cursorEventos

    def getEventosFeria(self):
        cursorEventos = self.db.aql.execute('FOR doc IN eventos FILTER doc.tipoCod == @value RETURN doc', bind_vars={'value': 8})
        return cursorEventos

    def getEventosExposicion(self):
        cursorEventos = self.db.aql.execute('FOR doc IN eventos FILTER doc.tipoCod == @value RETURN doc', bind_vars={'value': 9})
        return cursorEventos

    def getEventosProyeccion(self):
        cursorEventos = self.db.aql.execute('FOR doc IN eventos FILTER doc.tipoCod == @value RETURN doc', bind_vars={'value': 3})
        return cursorEventos

    def getEventosFormacion(self):
        cursorEventos = self.db.aql.execute('FOR doc IN eventos FILTER doc.tipoCod == @value RETURN doc', bind_vars={'value': 11})
        return cursorEventos

    def getEventosConcurso(self):
        cursorEventos = self.db.aql.execute('FOR doc IN eventos FILTER doc.tipoCod == @value RETURN doc', bind_vars={'value': 12})
        return cursorEventos

    def getEventosFestival(self):
        cursorEventos = self.db.aql.execute('FOR doc IN eventos FILTER doc.tipoCod == @value RETURN doc', bind_vars={'value': 13})
        return cursorEventos

    def getEventosInfantil(self):
        cursorEventos = self.db.aql.execute('FOR doc IN eventos FILTER doc.tipoCod == @value RETURN doc', bind_vars={'value': 14})
        return cursorEventos

    def getEventosOtro(self):
        cursorEventos = self.db.aql.execute('FOR doc IN eventos FILTER doc.tipoCod == @value RETURN doc', bind_vars={'value': 15})
        return cursorEventos

    def getEventosFiestas(self):
        cursorEventos = self.db.aql.execute('FOR doc IN eventos FILTER doc.tipoCod == @value RETURN doc', bind_vars={'value': 16})
        return cursorEventos

    def generarMapa(self, filtros, añosInd):
        m = folium.Map(location=[43.276803, -2.950852], tiles="cartodb positron")
        geojson_fields = ['iz_ofizial']
        geojson_aliases = ['Municipio:']
        myIFrame = None
        myIcon = None
        myPopup = None

        # Indicadores
        indIn = 1
        print(self.indicators)
        print(filtros)
        for indicator in self.indicators:
            if filtros['filtroInd' + str(indIn)]:
                print(indicator, flush = True)
                año = añosInd['filtroInd' + str(indIn)]
                geojson_fields.append('indicator_' + str(indicator) + '_' + año)
                geojson_aliases.append(self.indicators[indicator] + ' (' + año + ')')
            indIn = indIn + 1
        # Eventos
        cursoresEventos = []
        if filtros['filtroEv1']:
            cursoresEventos.append(self.getEventosTodos())
        else:
            if filtros['filtroEv2']:
                cursoresEventos.append(self.getEventosConciertos())
            if filtros['filtroEv3']:
                cursoresEventos.append(self.getEventosTeatro())
            if filtros['filtroEv4']:
                cursoresEventos.append(self.getEventosDanza())
            if filtros['filtroEv5']:
                cursoresEventos.append(self.getEventosConferencia())
            if filtros['filtroEv6']:
                cursoresEventos.append(self.getEventosBertsolaritza())
            if filtros['filtroEv7']:
                cursoresEventos.append(self.getEventosFeria())
            if filtros['filtroEv8']:
                cursoresEventos.append(self.getEventosExposicion())
            if filtros['filtroEv9']:
                cursoresEventos.append(self.getEventosProyeccion())
            if filtros['filtroEv10']:
                cursoresEventos.append(self.getEventosFormacion())
            if filtros['filtroEv11']:
                cursoresEventos.append(self.getEventosConcurso())
            if filtros['filtroEv12']:
                cursoresEventos.append(self.getEventosFestival())
            if filtros['filtroEv13']:
                cursoresEventos.append(self.getEventosInfantil())
            if filtros['filtroEv14']:
                cursoresEventos.append(self.getEventosFiestas())
            if filtros['filtroEv15']:
                cursoresEventos.append(self.getEventosOtro())
        for cursorEventos in cursoresEventos:    
            for evento in cursorEventos:
                myIFrame = folium.IFrame('<strong>Nombre:</strong> ' + evento['nombre'] + '<br><br>' + '<strong>Tipo de evento:</strong> ' + evento['tipo'] + '<br><br>' + '<strong>Precio:</strong> ' + evento['precio'])
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

    def getIndicatorsIDs(self):
        myHeaders = {'accept': 'application/json'}
        myParams = {'lang': 'SPANISH'}
        response = requests.get('https://api.euskadi.eus/udalmap/indicators/', headers=myHeaders, params=myParams)
        myJson = response.json()
        for i in range(0,len(myJson)):
            print(myJson[i]['name'] + ' -> ' + myJson[i]['id'])

    def getIndicatorMunicipalities(self, indicator):
        cursorInd = self.db.aql.execute('FOR doc IN ' + 'ind_' + str(indicator) + ' RETURN doc') 
        return cursorInd

    def getCoords(self, place):
        geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0")
        location = geolocator.geocode(place + ' Spain')
        return (location.latitude, location.longitude)

    def cargarDB(self):
        for ind in self.indicators:
            indicators_col = self.db.create_collection('indicator_' + str(ind))
            self.cargarIndicatorDB(ind, indicators_col)
        events_col = self.db.create_collection('eventos')
        self.cargarUpcomingEventsDB(events_col)    

    def cargarIndicatorDB(self, indicator, indicators_col):
        myHeaders = {'accept': 'application/json'}
        myParams = {'lang': 'SPANISH'}
        response = requests.get('https://api.euskadi.eus/udalmap/indicators/' + str(indicator) + '/municipalities', headers=myHeaders, params=myParams)
        myJson = response.json()
        for ind in myJson['municipalities']:
            indJson = {'id': ind['id'], 'lugar': ind['name'], 'data': ind['years'][0]}
            indicators_col.insert(indJson)

    def esEuskadi(self, provinciaCod):
        if provinciaCod == '48' or provinciaCod == '20' or provinciaCod == '1':
            return True
        else:
            return False

    def cargarUpcomingEventsDB(self, events_col):
        qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
        qParams = {'_elements': 1000}
        qHeaders = {'accept': 'application/json'}
        response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
        myJson = response.json()
        eventJson = {}
        for event in myJson['items']:
            try:
                if self.esEuskadi(event['provinceNoraCode']):
                    eventJson['id'] = event['id']
                    eventJson['latitud'] = event['municipalityLatitude']
                    eventJson['longitud'] = event['municipalityLongitude']
                    eventJson['tipoCod'] = event['type']
                    eventJson['tipo'] = event['typeEs']
                    eventJson['nombre'] = event['nameEs']
                    eventJson['fecha'] = event['startDate'].split("T")
                    if 'priceEs' in event:
                        eventJson['precio'] = event['priceEs']
                    else:
                        eventJson['precio'] = 'Sin información'
                    events_col.insert(eventJson)
            except:
                print('No se ha guardado el evento ' + str(event['id']) + ' en BD por falta de información clave')

    def cargarGeoJson(self):
        for municipio in self.geojson['features']:
            for ind in self.indicators:
                indicator_db = self.db.collection('indicator_' + str(ind))
                cursorInd = indicator_db.find({'id': municipio['properties']['ud_kodea']})
                for x in cursorInd:
                    municipio['properties']['indicator_' + str(ind) + '_2021'] = x['data']['2021']
                    municipio['properties']['indicator_' + str(ind) + '_2020'] = x['data']['2020']
                    municipio['properties']['indicator_' + str(ind) + '_2019'] = x['data']['2019']
