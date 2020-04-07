from zeep import Client
import requests
from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse

TOKEN = 'cb48489b-567a-4458-8525-517390fb1220'
SOAPAPI = 'http://soap-api-train-app-constant.herokuapp.com/services/TchouTchou?wsdl'
RESTAPI ='http://rest-apic-train-app-constant.herokuapp.com/train'

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulaireCalculDistance')
def formulaireCalculDistance():
    return render_template('formulaireCalculDistance.html')

@app.route('/calculDistance', methods=['GET','POST'])
def calculDistance():
    if request.method == 'POST':
        adresse = SOAPAPI
        client = Client(adresse)
        result = request.form

        r = client.service.calculDistance(result["longitudeA"], result["longitudeB"], result["latitudeA"], result["latitudeB"])

    return render_template('resultatCalcul.html', result=r)

@app.route('/formulaireCalculPrix')
def formulaireCalculPrix():
    return render_template('calculPrix.html')

@app.route('/calculPrix', methods=['GET','POST'])
def calculPrix():
    if request.method == 'POST':
        adresse = ''
        client = Client(adresse)
        result = request.form

        r = client.service.calculDistance(result["longitudeA"], result["longitudeB"], result["latitudeA"], result["latitudeB"])

    return render_template('resultatCalcul.html', result=r)

@app.route('/villes')
def horairesVille():
    return render_template('villes.html')

@app.route('/trouverCoordonnees', methods=['GET','POST'])
def trouverCoordonnees():
    if request.method == 'POST':
        adresse = 'http://data.sncf.com/api/records/1.0/search/'
        result = request.form
        
        r1 = requests.get(adresse, params = {'dataset' : 'referentiel-gares-voyageurs', 'q':result['ville1']}).json()
        coordonnees1 = r1['records'][0]['fields']['wgs_84']
        cp1 = r1['records'][0]['fields']['pltf_uic_code']
        r2 = requests.get(adresse, params = {'dataset' : 'referentiel-gares-voyageurs', 'q':result['ville2']}).json()
        coordonnees2 = r2['records'][0]['fields']['wgs_84']
        cp2 = r2['records'][0]['fields']['pltf_uic_code']


        adresse = SOAPAPI
        client = Client(adresse)
        result = request.form

        r = client.service.calculDistance(coordonnees1[0], coordonnees2[0], coordonnees1[1], coordonnees2[1])

        adresse2 = 'https://api.sncf.com/v1/coverage/sncf/journeys'
        response = requests.get(adresse2, params = {'from':'stop_area:OCE:SA:'+str(cp1), 'to':'stop_area:OCE:SA:'+str(cp1)}, auth=(TOKEN, ''))

        iti = response.json()

        adress = RESTAPI
        response = requests.get(adress, params = {'distance':r, 'monnaie':result['monnaie']})
        prix = response.json()

        for i in range(0, 5):
            r1['records'][0]

        res = {'depart':result['ville1'], 'arrive':result['ville2'], 'distance':r, 'prix':prix}

    return render_template('resultatCalcul.html', depart=result['ville1'], arrive=result['ville2'], distance=r, prix=prix['prix'])

def jsonToArray_iti(json):
    print(json)

#app.run(debug=True)
