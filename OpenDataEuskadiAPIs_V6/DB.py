from arango import ArangoClient
import apis
import json
from datetime import datetime

class DB:
    def __init__(self):
        with open('indicators.txt') as f:
            indicators_raw = f.read()
        self.indicators = json.loads(indicators_raw)

        client = ArangoClient(hosts='http://127.0.0.1:8529')
        sys_db = client.db(name='_system', username='root', password='root_passwd')
        if sys_db.has_database('ODE'):
            sys_db.delete_database('ODE')
        sys_db.create_database('ODE')
        self.db = client.db('ODE', username='root', password='root_passwd')
        self.cargarDB()

    def cargarDB(self):
        # cargar indicadores
        for ind in self.indicators:
            indicators_col = self.db.create_collection('indicator_' + str(ind))
            self.cargarIndicatorDB(ind, indicators_col)
        # cargar camaras
        camaras_col = self.db.create_collection('camaras')
        self.cargarCamarasDB(camaras_col)
        # cargar eventos del mes
        events_col = self.db.create_collection('eventos')
        self.cargarEventosMesDB(events_col)
        # cargar incidencias del mes
        incidencias_col = self.db.create_collection('incidencias')
        self.cargarIncidenciasMesDB(incidencias_col)

    def cargarIndicatorDB(self, indicator, indicators_col):
        myJson = apis.getIndicator(indicator)
        for ind in myJson['municipalities']:
            indJson = {'id': ind['id'], 'lugar': ind['name'], 'data': ind['years'][0]}
            indicators_col.insert(indJson)

    def cargarEventosMesDB(self, events_col):
        myJson = apis.getEventosMes('2023', '05')
        for event in myJson['items']:
            try:
                if self.esEuskadi(event['provinceNoraCode']):
                    eventJson = {}
                    eventJson['id'] = event['id']
                    eventJson['latitud'] = event['municipalityLatitude']
                    eventJson['longitud'] = event['municipalityLongitude']
                    eventJson['tipoCod'] = event['type']
                    eventJson['tipo'] = event['typeEs']
                    eventJson['nombre'] = event['nameEs']
                    eventJson['dia'] = event['startDate'].split("T")[0]
                    if event['startDate'].split("T")[1][:-1] != '00:00:00':
                        eventJson['hora'] = event['startDate'].split("T")[1][:-1]
                    else:
                        eventJson['hora'] = 'Sin información'
                    if 'priceEs' in event:
                        eventJson['precio'] = event['priceEs']
                    else:
                        eventJson['precio'] = 'Sin información'
                    events_col.insert(eventJson)
            except:
                print('No se ha guardado el evento ' + str(event['id']) + ' en BD por falta de información clave')

    def cargarCamarasDB(self, camaras_col):
        myJsonList = apis.getCamaras()
        for myJson in myJsonList:
            for camara in myJson['cameras']:
                if float(camara['latitude']) < 45 and float(camara['longitude']) < 0:
                    camaraJson = {}
                    camaraJson['latitud'] = camara['latitude']
                    camaraJson['longitud'] = camara['longitude']
                    camaras_col.insert(camaraJson)

    def cargarIncidenciasMesDB(self, incidencias_col):
        año = datetime.now().year
        mes = datetime.now().month
        myJsonList = apis.getIncidenciasMes(año, mes)
        for myJson in myJsonList:
            for incidencia in myJson['incidences']:
                try:
                    incidenciaJson = {}
                    incidenciaJson['latitud'] = incidencia['latitude']
                    incidenciaJson['longitud'] = incidencia['longitude']
                    incidenciaJson['dia'] = incidencia['startDate'].split('T')[0]
                    incidenciaJson['hora'] = incidencia['startDate'].split('T')[1]
                    incidenciaJson['tipo'] = incidencia['incidenceType']
                    incidenciaJson['causa'] = incidencia['cause']
                    incidencias_col.insert(incidenciaJson)
                except:
                    print('No se ha guardado la incidencia ' + str(incidencia['incidenceId']) + ' en BD por falta de información')

    def getIndicators(self):
        return self.indicators

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

    def getIndicatorMunicipalities(self, indicator):
        cursorInd = self.db.aql.execute('FOR doc IN ' + 'ind_' + str(indicator) + ' RETURN doc')
        return cursorInd

    def getCamaras(self):
        cursorCamaras = self.db.aql.execute('FOR doc IN camaras RETURN doc')
        return cursorCamaras

    def getIncidenciasDia(self, fechaIncidencia):
        incidencias_db = self.db.collection('incidencias')
        cursorIncidencias = incidencias_db.find({'dia': fechaIncidencia})
        return cursorIncidencias

    def getCursorIndMunicipio(self, ind, municipio):
        indicator_db = self.db.collection('indicator_' + str(ind))
        cursorInd = indicator_db.find({'id': municipio['properties']['ud_kodea']})
        return cursorInd

    def esEuskadi(self, provinciaCod):
        if provinciaCod == '48' or provinciaCod == '20' or provinciaCod == '1':
            return True
        else:
            return False
