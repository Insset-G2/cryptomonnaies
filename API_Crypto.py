from flask import Flask, jsonify, render_template
from blockcypher import get_transaction_details
import requests
import json
import matplotlib
import matplotlib.pyplot as plt
import io
from datetime import datetime, timedelta
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64

app = Flask(__name__)
matplotlib.use('Agg')
plt.interactive(False)

cryptocurrency_dict     = {'litecoin': 0, 'bitcoin': 0, 'ethereum': 0}
cryptocurrency_prices   = {'litecoin': 0, 'bitcoin': 0, 'ethereum': 0}

@app.route('/cryptodata', methods=['GET'])
def get_crypto_data():
    
    for symbol, value in cryptocurrency_prices.items():
        if value == 0:
            cryptocurrency_prices.update({symbol: get_crypto_info(symbol)})
    
    # Enregistrez les données dans un fichier JSON
    with open('crypto_data.json', 'w') as json_file:
        json.dump(cryptocurrency_prices, json_file)
    
    return jsonify(cryptocurrency_prices)

# 5f45de1eb5f769505d94ded907784f203987c950531122c142d7f846e57ed571
@app.route('/transaction/<crypto>/<transactionId>', methods=['GET'])
def get_transaction_data(crypto, transactionId):
    
    crypto = crypto.upper()
    
    if crypto == 'BTC':
        # Clé API pour accéder à l'API Blockchain
        api_key = 'f1e6b3e0-5f9d-4d6d-8a9e-9b6d1b5f4c9e'
        transaction_details = get_btc_transaction_detail(transactionId)
    elif crypto == 'ETH':
        api_key = 'F9XGBIM5K3U64R42S2D5ZDZ4E92DH9WZYS'
        transaction_details = get_eth_transaction_detail(api_key, transactionId)
    elif crypto == 'LTC':
        api_key = '4b5f636623e2478b87e9caa2dce700c7'
        transaction_details = get_ltc_transaction_detail(api_key, transactionId)
    
    # Retourner les détails de la transaction
    return jsonify(transaction_details)

@app.route('/graph/<symbol>', methods=['GET'])
def graphic(symbol):
    charts = []

    if symbol in cryptocurrency_dict:
        if cryptocurrency_dict[symbol] == 0:
            prices = get_price_data(symbol)
            cryptocurrency_dict.update({symbol: prices})
        else:
            prices = cryptocurrency_dict[symbol]
    else:
        prices = get_price_data(symbol)
        cryptocurrency_dict.update({symbol: prices})
    fig = plot_price_chart(symbol, prices)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    encoded_image = base64.b64encode(output.getvalue()).decode('utf-8')
    charts.append(encoded_image)
    plt.close(fig)

    return render_template('index.html', charts=charts)

@app.route('/graphs', methods=['GET'])
def index():
    charts = []

    for symbol, value in cryptocurrency_dict.items():
        if value == 0:
            prices = get_price_data(symbol)
            cryptocurrency_dict.update({symbol: prices})
        else:
            prices = value
        fig = plot_price_chart(symbol, prices)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        encoded_image = base64.b64encode(output.getvalue()).decode('utf-8')
        charts.append(encoded_image)
        plt.close(fig)

    return render_template('index.html', charts=charts)

def get_price_data(crypto_symbol, days=1):
    api_url = f'https://api.coingecko.com/api/v3/coins/{crypto_symbol.lower()}/market_chart'
    params = {
        'vs_currency': 'eur',
        'days': days
    }

    response = requests.get(api_url, params=params)
    data = response.json()

    return data['prices']

def plot_price_chart(symbol, prices):
    timestamps, values = zip(*prices)
    timestamps = [datetime.utcfromtimestamp(timestamp / 1000) for timestamp in timestamps]

    fig, ax = plt.subplots()

    # Personnalisation du graphique
    ax.plot(timestamps, values, label=symbol, color='grey', linestyle='solid', linewidth=1, marker='o', markersize=3)
    
    # Modification de la taille de la police pour les étiquettes de l'axe des x
    for label in ax.get_xticklabels():
        label.set_fontsize(8)

    # Personnalisation des axes
    ax.set_xlabel('Heure (UTC)', fontsize=10)
    ax.set_ylabel('Prix (EUR)', fontsize=10)

    # Personnalisation du titre
    ax.set_title(f'Évolution du prix de {symbol} sur les dernières 24 heures', fontsize=14)

    # Personnalisation de la légende
    ax.legend(loc='upper left', fontsize=10)

    # Ajout de la grille
    ax.grid(True, linestyle='--', alpha=0.7)

    return fig

def get_crypto_info(symbol):
    # Faites une requête à l'API de cryptomonnaie pour obtenir les informations spécifiques à la cryptomonnaie
    api_url = f'https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=eur'
    response = requests.get(api_url)
    data = response.json()
    if data['status']['error_code'] != 0:
        return data['status']['error_message']
    return data[symbol.lower()]['eur']

def get_eth_transaction_detail(api_key, transaction_id):
    # Endpoint de l'API Etherscan pour obtenir les détails d'une transaction
    api_url = f'https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={transaction_id}&apikey={api_key}'

    try:
        # Faire la requête à l'API
        response = requests.get(api_url)
        data = response.json()

        # Vérifier si la requête a réussi
        if data['status'] == '1':
            # Retourner les détails de la transaction
            return data['result']
        else:
            return f"Erreur: {data['message']}"

    except Exception as e:
        return f"Erreur lors de la requête à l'API : {str(e)}"
    
def get_ltc_transaction_detail(api_token, transaction_hash):
    base_url = "https://api.blockcypher.com/v1/ltc/main"
    endpoint = f"/txs/{transaction_hash}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {api_token}'
    }

    try:
        response = requests.get(base_url + endpoint, headers=headers)
        data = response.json()

        if 'error' in data:
            return f"Erreur de l'API BlockCypher : {data['error']}"

        return data

    except Exception as e:
        return f"Erreur lors de la requête à l'API : {str(e)}"

def get_btc_transaction_detail(transaction_hash):
    api_url = f'https://api.blockchair.com/bitcoin/dashboards/transaction/{transaction_hash}'

    try:
        response = requests.get(api_url)
        data = response.json()

        if 'data' in data :
            return data['data']
        else:
            return f"La transaction {transaction_hash} n'est pas confirmée ou n'existe pas."

    except Exception as e:
        return f"Erreur lors de la requête à l'API : {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, threaded=True)