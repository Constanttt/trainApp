from zeep import Client
import requests
from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse
from datetime import datetime

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

    return render_template('resultatCalculDistance.html', result=r)

@app.route('/formulaireCalculPrix')
def formulaireCalculPrix():
    return render_template('calculPrix.html')

@app.route('/calculPrix', methods=['GET','POST'])
def calculPrix():
    if request.method == 'POST':
        result = request.form

        adress = RESTAPI
        response = requests.get(adress, params = {'distance':result['distance'], 'monnaie':result['monnaie']})
        resu = response.json()
        prix = resu['prix']

    return render_template('resultatCalculPrix.html', result=prix)

@app.route('/villes')
def horairesVille():
    return render_template('villes.html')

@app.route('/trouverCoordonnees', methods=['GET','POST'])
def trouverCoordonnees():
    if request.method == 'POST':
        adresse = 'http://data.sncf.com/api/records/1.0/search/'
        result = request.form
        erreur = False;
        messageErreur = ""

        r=0
        devise=""
        prix=0

        #Requete pour les codes et la localisation des gares (on ne prends que les premiers numéros)
        if(not erreur):
            try:
                r1 = requests.get(adresse, params = {'dataset' : 'referentiel-gares-voyageurs', 'q':result['ville1']}).json()
                coordonnees1 = r1['records'][0]['fields']['wgs_84']
                cp1 = r1['records'][0]['fields']['pltf_uic_code']
                r2 = requests.get(adresse, params = {'dataset' : 'referentiel-gares-voyageurs', 'q':result['ville2']}).json()
                coordonnees2 = r2['records'][0]['fields']['wgs_84']
                cp2 = r2['records'][0]['fields']['pltf_uic_code']
            except:
                erreur = True
                messageErreur = "Ville non trouvée"

        #Utilisation de l'API SOAP pour avoir la distance
        if(not erreur):
            try:
                adresse = SOAPAPI
                client = Client(adresse)
                result = request.form

                r = client.service.calculDistance(coordonnees1[0], coordonnees2[0], coordonnees1[1], coordonnees2[1])
            except:
                erreur = True
                messageErreur = "Erreur dans le calcul de la distance"


        #Requete pour avoir les trajets disponible entre les 2 villes données
        if(not erreur):
            try:
                adresse2 = 'https://api.sncf.com/v1/coverage/sncf/journeys?'
                response = requests.get(adresse2, params = {'from':'stop_area:OCE:SA:'+str(cp1), 'to':'stop_area:OCE:SA:'+str(cp2), 'min_nb_journeys': 5}, auth=(TOKEN, ''))

                iti = response.json()
                devise = result['monnaie']
            except:
                erreur = True
                messageErreur = "Erreur lors de la recherche de trajet"

        #print(result)

        #Utilisation de l'API REST pour avoir le prix en fonction de la distance et de la devise
        if(not erreur):
            try:
                adress = RESTAPI
                response = requests.get(adress, params = {'distance':r, 'monnaie':devise})
                resu = response.json()
                prix = resu['prix']
            except:
                erreur = True
                messageErreur = "Erreur lors du calcul du prix"

        tabresultat = []

        try:
            iti['journeys']
        except:
            erreur = True
            messageErreur = "Aucun trajet disponible"

        #Création du tableau des résultats
        if(not erreur):
            if(len(iti['journeys']) < 5):
                for i in range(0,len(iti['journeys'])):
                    tabresultat.append(str(datetime.strptime(iti['journeys'][i]['departure_date_time'].replace('T',''),'%Y%m%d%H%M%S')))
            else:
                for i in range(0,5):
                    tabresultat.append(str(datetime.strptime(iti['journeys'][i]['departure_date_time'].replace('T',''),'%Y%m%d%H%M%S')))
        else:
            tabresultat.append(messageErreur)

        #res = {'depart':result['ville1'], 'arrive':result['ville2'], 'distance':r, 'prix':prix, 'iti':tabresultat}

    return render_template('resultatCalculHoraires.html', depart=result['ville1'], arrive=result['ville2'], distance="%.2f" % r, prix="%.2f" % prix, devise=devise, iti=tabresultat)

def jsonToArray_iti(json):
    print(json)

#app.run(debug=True)
