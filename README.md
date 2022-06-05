# Projet 11 Améliorez une application Web Python par des tests et du débogage

Application web Python de réservation de places à des compétitions pour l'entreprise Güdlft.

L'objectif du projet est de corriger les erreurs et les bugs du projet Python_Testing (https://github.com/OpenClassrooms-Student-Center/Python_Testing) et d'implémenter de nouvelles fonctionnalités, pour chacun des bugs ou amélioration, il faut créer une nouvelle branche dans github.


## Initialisation du projet 

Création d'un environnement virtuel ENV  

### Windows :
```
git clone https://github.com/Cisco1964/OC_Python_Testing.git

cd oc_python_testing
python -m venv ENV
ENV\Scripts\activate


```

### MacOS et Linux :
```
git clone https://github.com/Cisco1964/OC_Python_Testing.git

cd oc_python_testing
python -m venv ENV 
source ENV/bin/activate

pip install -r requirements.txt
```


## Lancement du projet

1. Lancer le serveur Flask :

```
$ export FLASK_APP=server.py
flask run
```

2. Accéder au site à l'adresse http://127.0.0.1:5000/



## Tests

- **Note : Tous les packages nécessaires à l'exécution de ces tests sont inclus dans 'requirements.txt'.**


### Tests unitaires et d'intégration

Les tests unitaires sont exécutés avec pytest.
```
pytest -v
```

### Test de couverture 

Le tests de couverture est éxécuté avec pytest. Suite à son éxécution, un dossier nommé htmlcov est créer, il faut ouvrir le fichier index.html avec n'importe quel navigateur pour consulter les résultats
```
py.test --cov=tests --cov-report=html tests/tests_*/*.py
```

### Test de performances

Le test de performance est éxécuté avec locust
```
locust -f tests/performance/locustfile.py --host=http://localhost:5000
```
Accéder au site de performance à l'adresse http://localhost:8089
