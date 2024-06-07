# Microservice de Cryptomonnaie

Ce projet est un microservice de cryptomonnaie développé en Python utilisant le framework Flask. Il fournit une API pour récupérer les informations sur les cryptomonnaies et effectuer diverses opérations.

## Fonctionnalités

- Récupérer les prix actuels des principales cryptomonnaies.
- Récupérer les données actuels des principales cryptomonnaies et afficher leurs graphique des dernières 24 heures.
- Récupèrer le détail d'une transaction sur la blockchain selon une cryptomonnaie spécifié.

## Prérequis

- Python 3.8 ou supérieur
- Flask 2.0 ou supérieur

## Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/Insset-G2/cryptomonnaies
    cd cryptomonnaies
    ```

2. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

1. Démarrez le serveur Flask :
    ```bash
    flask run
    ```

2. L'API sera disponible à l'adresse `http://127.0.0.1:5000`.

## Points de terminaison de l'API

- `GET /api/` : Page d'index, affiche un 'Hello World !'
- `GET /api/graphs` : Récupère la liste des principales cryptomonnaies et affiche leur graphique sur 24 heures.
- `GET /api/graph/<crypto>` : Récupère les détails d'une cryptomonnaie spécifié et affiche son graphique sur 24 heures.
- `GET /api/cryptodata` : Récupère les détails de toutes cryptomonnaies spécifiés.
- `GET /api/transaction/<crypto>/<transactionId>` : Récupère le détail d'une transaction sur la blockchain selon la cryptomonnaie spécifié.

## Tests

Pour exécuter les tests unitaires, utilisez :
```bash
pytest
