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

Le jeu de données normalisé est ensuite réparti en 4 classes correspondant à l'état de l'iPhone. Cela permet de mieux identifier les tendances pour chacune des classes et d'éviter les effets de bords entre elles.

## Visualisation des données
### Courbe de tendance
Nous allons étudier l'évolution du prix moyen des iPhone catégorisé en "Used" par eBay. Cette classe est la plus représentée dans le jeu de données qui a été constitué et est donc plus pertinente.

![](https://github.com/QuarkyUp/eBay-price-Analysis/blob/master/Used%20Evolution.png)

Ce graphique nous apporte plusieurs informations concernant l'évolution du prix du produit au cours des derniers mois.

Dans un premier temps, la courbe trace l'évolution du prix moyen en fonction du jour de la vente.
Une régression linéaire paramétrant une fonction d'ordre 3 permet de mettre en évidance que le prix de vente moyen reste constante avec une légère hausse.

Un pic du prix moyen est enregistré durant la deuxième semaine de Juillet 2018. La date du pic correspond à celle du renouvellement de la gamme des MacBook Pro par Apple le 12 Juillet 2018.
Cet évènement pourrait éventuellement justifier la légère hausse du prix moyen qui s'en est suivi.

La courbe est aussi encadrée par un intervalle de confiance à 95% calculé à l'aide d'une moyenne glissante sur 5 valeurs.
L'intervalle est assez large, signe que la marge d'incertitude autour du prix moyen est important. Cela montre d'une part que le taille du jeu de données pour la classe "used" n'est pas assez important et d'autre part que le prix est très volatile sur la période observée. 


















