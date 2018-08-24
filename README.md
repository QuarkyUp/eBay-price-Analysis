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
Une régression linéaire paramétrant une équation linéaire d'ordre 3 permet de mettre en évidance que le prix de vente moyen reste constante avec une légère hausse.

Un pic du prix moyen est enregistré durant la deuxième semaine de Juillet 2018. La date du pic correspond à celle du renouvellement de la gamme des MacBook Pro par Apple le 12 Juillet 2018.
Cet évènement pourrait éventuellement justifier la légère hausse du prix moyen qui s'en est suivi.

La courbe est aussi encadrée par un intervalle de confiance à 95% calculé à l'aide d'une moyenne glissante sur 5 valeurs.
L'intervalle est assez large, signe que la marge d'incertitude autour du prix moyen est important. Cela montre d'une part que le taille du jeu de données pour la classe "used" n'est pas assez importante et d'autre part que le prix est très volatile sur la période observée.

Liens vers les courbes de tendances des deux autres classes les plus représentées : 
* [Seller refurbished](https://github.com/QuarkyUp/eBay-price-Analysis/blob/master/Refurb%20Seller%20Evolution.png)
* [Manufacturer refurbished](https://github.com/QuarkyUp/eBay-price-Analysis/blob/master/Refurb%20Manufacturer.png)

### Statistiques
![](https://github.com/QuarkyUp/eBay-price-Analysis/blob/master/Price%20Description.png)

Ce tableau regroupe des informations statistiques des trois classes les plus représentées à savoir "used", "seller refurbished", "manufacturer refurbished".

La classe la plus représentée est "used", ce qui correspond à un peu plus de 90% de la taille du jeu de données. Le prix de vente moyen de cette classe sur l'ensemble de la période observée est également le plus bas. On peut donc en déduire que les iPhones labellisés comme "used", c'est à dire qui ne sont pas passé par un contrôle technique et vendu directement par le particulier, ont un prix de vente moyen est moins important dû à leur état.

Cela aurait pu être intéressent afin de corréler le prix moyen et le type d'usure d'un iPhone. Malheureusement eBay ne fournit pas plus de détail concernant les types d'usures d'un produit (vitre abîmée, coque rayée, ...) et se contente seulement de garantir le bon fonctionnement de l'iPhone.

Le prix maximum de vente pour la classe "used" est supérieur à 12 fois le prix moyen de vente, d'où la nécessité de filtrer les données récoltées.

### Matrice de corrélation
![](https://github.com/QuarkyUp/eBay-price-Analysis/blob/master/Correlation%20Matrix.png)

Ce graphique est une matrice de corrélation. Le coefficient de corrélation entre deux variables mesure la dépendance et la direction de leur relation linéaire.

C'est une matrice symétrique carré dont les valeurs sont comprises entre -1.0 et +1.0. Une valeur nulle indique qu'il n'y a aucune relation de dépendance, une valeur proche de +1.0 indique une forte relation linéaire positive (tendance croissante) et une valeur élevée proche de -1.0 indique une forte relation linéaire négative (tendance décroissante).

On peut ainsi voir qu'il existe une faible dépendance entre le pourcentage d'évaluations positives et la note d'évaluation d'un vendeur. Cette relation n'est pas très pertinente pour notre cas.
En revanche, on peut voir qu'il existe une très faible dépendance négative entre le prix et la note d'évaluation d'un vendeur ainsi qu'entre le prix et le pourcentage d'évaluation positive d'un vendeur.

### Répartition du prix en fonction du pourcentage d'évaluations positives
![](https://github.com/QuarkyUp/eBay-price-Analysis/blob/master/Distribution.png)

Les résultats de la matrice de corrélation ont permis de mettre en évidence la faible dépendance entre le prix et le pourcentage d'évaluations positives du vendeur. Ce graphique met donc en évidence la corrélation entre ces deux variables.

On remarque que les prix les plus élevés sont ceux des annonces ajoutée par des utilisateurs ayant un pourcentage assez élevé dont la majorité est centré entre 140€ et 160€, tandis que les utilisateurs ayant un pourcentage plus faible entre 65% et 85% listent des annonces d'iPhone dont le prix entre 60€ et 200€.

En émettant l'hypothèse que les vendeurs ayant un pourcentage élevé mettent en vente des iPhones en meilleur condition que les vendeurs ayant un pourcentage plus faible, on conclu que le prix moyen d'un iPhone 6s 16GB est compris entre 140€ et 160€.

### Histogramme du prix de vente
![](https://github.com/QuarkyUp/eBay-price-Analysis/blob/master/Histogram%20Evolution.png)

Cet histogramme conforte l'hypothèse émise à l'aide du graphique précédent. On peut voir que la majorité des iPhone ont un prix de vente moyen autour de 150€.





















