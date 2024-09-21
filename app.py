from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Variables globales pour stocker les PV, phases et attaques
game_data = {
    'pv_joueur': 50,
    'phases_ennemi': [
        {'nom': 'Phase 1', 'pv': 30, 'atk': 5, 'def': 2}
    ],
    'phase_actuelle': 0  # Indice de la phase actuelle
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        try:
            game_data['pv_joueur'] = int(request.form['pv_joueur'])
            game_data['phases_ennemi'] = []
            for i in range(int(request.form['nb_phases'])):
                game_data['phases_ennemi'].append({
                    'nom': request.form[f'nom_phase_{i}'],
                    'pv': int(request.form[f'pv_phase_{i}']),
                    'atk': int(request.form[f'atk_phase_{i}']),
                    'def': int(request.form[f'def_phase_{i}'])
                })
            return render_template('game.html', data=game_data)
        except ValueError:
            error = "Veuillez entrer des valeurs numériques valides."
            return render_template('config.html', error=error)
    return render_template('config.html')

@app.route('/enlever', methods=['POST'])
def enlever():
    data = request.get_json()
    cible = data.get('cible')
    kii = int(data.get('kii'))

    if cible == 'boss':
        attaque = int(data.get('atk')) if not data.get('ultime') else 1  # Multiplier par 1 pour l'attaque ultime
        defense = game_data['phases_ennemi'][game_data['phase_actuelle']]['def']
        degats = max((kii * attaque) // defense, 0)
        game_data['phases_ennemi'][game_data['phase_actuelle']]['pv'] = max(
            game_data['phases_ennemi'][game_data['phase_actuelle']]['pv'] - degats, 0)
        # Si le boss atteint 0 PV, passer à la phase suivante
        if game_data['phases_ennemi'][game_data['phase_actuelle']]['pv'] <= 0:
            if game_data['phase_actuelle'] < len(game_data['phases_ennemi']) - 1:
                game_data['phase_actuelle'] += 1
    elif cible == 'joueur':
        attaque = game_data['phases_ennemi'][game_data['phase_actuelle']]['atk']
        defense = int(data.get('def'))
        degats = max((kii * attaque) // defense, 0)
        game_data['pv_joueur'] = max(game_data['pv_joueur'] - degats, 0)

    return jsonify(game_data)

@app.route('/reset', methods=['POST'])
def reset():
    game_data['pv_joueur'] = 50
    for phase in game_data['phases_ennemi']:
        phase['pv'] = 30  # Réinitialiser les PV des phases (par exemple)
    game_data['phase_actuelle'] = 0
    return jsonify(game_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
