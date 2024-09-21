from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Variables globales pour stocker les PV
game_data = {
    'pv_boss': 20,
    'pv_joueur': 50
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        try:
            game_data['pv_boss'] = int(request.form['pv_boss'])
            game_data['pv_joueur'] = int(request.form['pv_joueur'])
            return render_template('game.html', pv_boss=game_data['pv_boss'], pv_joueur=game_data['pv_joueur'])
        except ValueError:
            error = "Veuillez entrer des valeurs numériques valides."
            return render_template('config.html', error=error)
    return render_template('config.html')

@app.route('/enlever', methods=['POST'])
def enlever():
    data = request.get_json()
    cible = data.get('cible')
    pv_enleve = int(data.get('pv_enleve'))

    if cible == 'boss':
        game_data['pv_boss'] = max(game_data['pv_boss'] - pv_enleve, 0)  # Empêche PV négatifs
    elif cible == 'joueur':
        game_data['pv_joueur'] = max(game_data['pv_joueur'] - pv_enleve, 0)  # Empêche PV négatifs

    return jsonify(game_data)

@app.route('/reset', methods=['POST'])
def reset():
    game_data['pv_boss'] = 20
    game_data['pv_joueur'] = 50
    return jsonify(game_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
