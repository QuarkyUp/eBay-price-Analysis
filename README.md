# Analyse des prix de l'iPhone sur eBay

Ce script permet de récupérer l'historique de vente de l'iPhone 6S 16GB sur eBay entre le 25-05-2018 et le 22-08-2018. Seules les ventes terminées et réussies ont été prises en considération.

Il génère différents graphiques mettant en perspective l'évolution du prix moyen de vente.

## Installation

Dépendances : 
* Python 3.4
* git

Modules Python :
*  numpy
*  scipy
*  pandas
*  matplotlib
*  seaborn

## Run

Après avoir récupérer les dépendances et les modules, il faut maintenant récupérer le script : 
```shell
git clone https://github.com/QuarkyUp/eBay-price-Analysis.git
cd eBay-price-Analysis
```

Il y a deux façon d'utiliser le script, en important les données locales de l'historique des ventes ou récupérer ces données depuis eBay.

* Dans le premier cas, il faut décompresser le fichier [```ebayDump.json.gz```](https://github.com/QuarkyUp/eBay-price-Analysis/blob/master/ebayDump.json.gz) et passer la variable ```IMPORT``` à ```True``` définie en haut du script : 
```shell
gunzip -k ebayDump.json.gz
```

* Dans le deuxième cas, il faut récupérer une clé d'API auprès du [portail développeur d'eBay](https://developer.ebay.com/) et passer la variable ```IMPORT``` à ```False```.

Après avoir choisi l'une des deux options, pour lancer le script :
```shell
python main.py
```

## Scraping & Normalisation
Le jeu de données est constitué de 41,936 éléments décrivant les détails de la vente d'un produit.

Il a fallu récupérer l'historique de vente en prenant en compte différents paramètres:
* Type d'état : used, seller refurbished, manufacturer refurbished, acceptable
* Type de vente : vente terminé et produit vendu
* Information concernant le vendeur
* Information concernant la vente : date de début, date de fin

Il a ensuite fallu nettoyer et normaliser les données pour ne prendre que les champs pertinents en s'appuyant sur la structure suivante :
```python
item = {
            'title' : e['title'][0],
            'price' : float(e['sellingStatus'][0]['currentPrice'][0]['__value__']),
            'endTime' : e['listingInfo'][0]['endTime'][0].replace('T', ' ')[:-14],
            'condition': e['condition'][0]['conditionDisplayName'][0],
            'sellerUserName': e['sellerInfo'][0]['sellerUserName'][0],
            'feedbackScore': float(e['sellerInfo'][0]['feedbackScore'][0]),
            'positiveFeedbackPercent': float(e['sellerInfo'][0]['positiveFeedbackPercent'][0]),
            'feedbackRatingStar': e['sellerInfo'][0]['feedbackRatingStar'][0]
        }
```

Le jeu de données normalisé est ensuite réparti en quatre classes correspondant à l'état de l'iPhone. Cela permet de mieux identifier les tendances pour chacune des classes et d'éviter les effets de bords entre elles.

## Visualisation des données
### Courbe de tendance
![alt-text-1](https://github.com/QuarkyUp/eBay-price-Analysis/blob/master/Used%20Evolution.png "used")
![alt-text-1](https://github.com/QuarkyUp/eBay-price-Analysis/blob/master/Refurb%20Seller%20Evolution.png "seller refurbished") ![alt-text-2](https://github.com/QuarkyUp/eBay-price-Analysis/blob/master/Refurb%20Manufacturer.png "manufacturer refurbished")
















