import rpa_insee_deaths
from flask import Flask, jsonify, request, send_from_directory
import re
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)

df_deaths = None


@app.route('/home')
def Welcome():
    return "Welcome to the API!!!"


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/deces', methods=['POST'])
def get_death_person():
    """
    Récupère les informations d'une personne donnée
    :return:
    """
    data = request.get_json()
    global df_deaths

    if df_deaths is None:
        df_deaths = rpa_insee_deaths.get_deaths()

    nomprenom = data['nom'].lower() + "*" + data['prenom'].lower() + "/"

    dateNaissance = int(re.sub("-", "", data['dateNaissance']))

    death_person = df_deaths[(df_deaths['nomprenom'].str.lower() == nomprenom) &
                             (df_deaths['datenaiss'] == dateNaissance)]
    if len(death_person) > 0:
        datedeces = death_person['datedeces'].values[0]
        datedeces = str(datedeces)
        dateformat = datedeces[:4] + "-" + datedeces[4:6] + "-" + datedeces[6:]

        return jsonify({'deces': dateformat})
    else:
        return jsonify({'deces': "nondeces"})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
