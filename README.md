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
git clone ...
cd ...
```

Il y a deux façon d'utiliser le script, en important les données locales de l'historique des ventes ou récupérer ces données depuis eBay.

* Dans le premier cas, il faut décompresser le fichier [```ebayDump.json.gz```](https://github.com/...) et passer la variable ```IMPORT``` à ```True``` définie en haut du script : 
```shell
gunzip -k ebayDump.json.gz
```

* Dans le deuxième cas, il faut récupérer une clé d'API auprès du [portail développeur d'eBay](https://developer.ebay.com/) et passer la variable ```IMPORT``` à ```False```.

Après avoir choisi l'une des deux options, pour lancer le script :
```shell
python main.py
```













