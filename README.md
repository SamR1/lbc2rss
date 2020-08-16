# lbc2rss

[![Python Version](https://img.shields.io/badge/python-3.7|3.8-brightgreen.svg)](https://python.org)
[![Flask Version](https://img.shields.io/badge/flask-1.1.2-brightgreen.svg)](http://flask.pocoo.org/)
[![code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)  
[![pipeline status](https://gitlab.com/SamR1/lbc2rss/badges/master/pipeline.svg)](https://gitlab.com/SamR1/lbc2rss/-/commits/master)
[![coverage report](https://gitlab.com/SamR1/lbc2rss/badges/master/coverage.svg)](https://gitlab.com/SamR1/lbc2rss/-/commits/master) 

Génère un flux RSS à partir d'une recherche immobilière sur LeBonCoin

---

## Dépendances

* [Flask](http://flask.pocoo.org/)
* [feedgenerator](https://github.com/getpelican/feedgenerator)
* [pylbc](https://github.com/razaborg/pylbc) (version forkée)


## Installation

- cloner le projet

```shell script
$ git clone https://github.com/SamR1/lbc2rss
```

- installer `lbc2rss` et lancer l'application

    - directement (après avoir créé un environnement virtuel si nécessaire)
    ```shell script
    $ pip install -e .
    $ lbc2rss
    ```

    - via le Makefile (qui génère un environnement virtuel)
    ```shell script
    $ make install
    $ make run
    ```


## Utilisation

Les flux sont accessibles en indiquant le type d'offre (**immobilier**, **ventes**, **locations** ou **colocations**) et 
les filtres souhaités (au moins un filtre doit être renseigné):

`http://0.0.0.0:5000/locations?lat=48.866667&lon=2.333333&radius=10&price_max=2000&rooms_min=2&rooms_max=3&square_min=40&keywords=balcon&order_by=time_desc`

Filtres disponibles :

- **Type de logement**
    
| filtre      | description                                                                                     |
| ----------- | ----------------------------------------------------------------------------------------------- |
| `types`     | liste des types de logement recherchés (`maison`, `appartement`, `terrain`, `parking`, `autre`) |

exemple:  
`types=maison`  
`types=maison|appartement|autre`  

Si non défini, la valeur par défaut est `maison|appartement`

- **Localisation**  
3 types de localisation peuvent être utilisées.

    ○ Coordonnées géographiques
     
    | filtre   | description                              |
    | -------- | ---------------------------------------- |
    | `lat`    | latitude                                 |
    | `lon`    | longitude                                |
    | `radius` | distance maximale en km (non obligatoire)|

    exemple:   
    `lat=48.866667&lon=2.333333&radius=10`  
    `lat=45.75&lon=4.85`

    ○ Liste de villes
     
    | filtre   | description                                                              |
    | -------- | ------------------------------------------------------------------------ |
    | `cities` | liste des villes (nom avec la 1ère lettre en capitale et le code postal) |

    exemple:   
    `cities=Paris,75000`  
    `cities=Lyon,69003|Villeurbanne,69100`
    
    ○ Liste de départements
     
    | filtre        | description                                           |
    | ------------- | ----------------------------------------------------- |
    | `departments` | liste de départements                                 |
    
    exemple:  
    `departments=75`  
    `departments=69|01|38`
    
- **Prix**
    
| filtre      | description                                 |
| ----------- | ------------------------------------------- |
| `price_min` | prix minimum                                |
| `price_max` | prix maximum                                |

- **Nombre de pièces**
    
| filtre      | description                                 |
| ----------- | ------------------------------------------- |
| `rooms_min` | nombre de pièces minimum                    |
| `rooms_max` | nombre de pièces maximum                    |

- **Surface**
    
| filtre       | description                                |
| ------------ | ------------------------------------------ |
| `square_min` | surface minimum                            |
| `square_max` | surface maximum                            |

- **Mots clés**
    
| filtre      | description                                  |
| ----------- | -------------------------------------------- |
| `keywords`  | mots-clés recherchés                         |
| `titleonly` | restreindre la recherche au titre uniquement |

- **Tri**
    
| filtre      | description                                   |
| ----------- | --------------------------------------------- |
| `order_by`  | tri par date ou prix, ascendant ou descendant |

choix possibles: `time_desc`, `time_asc`, `price_desc`, `price_asc`

Le flux renvoie pour chaque offre : le titre, la ville, la date de publication,
le prix, si les charges sont comprises ou non, le type, la surface, la description
et les photos.


## Non géré actuellement

- limiter le nombre d'offres renvoyées par le flux  
(les requêtes avec des filtres peu restrictifs sont lentes)
