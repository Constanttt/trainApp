# Application web permettant de récupérer des voyages grave a l'API SNCF

Application Web développée en Python avec 3 formulaires. 
Fonctionne avec https://github.com/Constanttt/TrainRESTAPIC et https://github.com/Constanttt/train-soap.

## API REST

L'API REST est développée en C#. Elle possède 2 actions. La première permet de récupérer la liste des devises prises en compte par l'API et la deuxième permet de calculer un prix en fonction d'une distance et d'une devise.

## API SOAP

L'API SOAP est développée en Java. Elle possède 1 action. Elle permet de calculer une distance en fonction des latitudes et longitudes du point de départ et d'arrivé.

## Déploiement

L'application Web est déployée sous Heroku. Elle est accessible via https://train-app-constant.herokuapp.com/.

L'API REST est déployée sous Heroku. Elle est accessible via https://rest-apic-train-app-constant.herokuapp.com/.
On peut récupérer les devises disponible via https://rest-apic-train-app-constant.herokuapp.com/devises.
On peut calculer un prix en fonction d'une devise et d'une distance via https://rest-apic-train-app-constant.herokuapp.com/train?distance=XXX&monnaie=XXX. La distance doit être un chiffre et la devise doit être une chaine de caractère.

L'API SOAP est déployée sous Heroku. Elle est accessible via https://soap-api-train-app-constant.herokuapp.com/.
Le wsdl associé est accessible via https://soap-api-train-app-constant.herokuapp.com/services/TchouTchou?wsdl.
