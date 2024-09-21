from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

# Stocker les profils de boss sauvegardés
boss_profiles = {}

# Variables globales pour stocker l'état du jeu
game_data = {
    'pv_joueur': 50,
    'phases_ennemi': [],
    'phase_actuelle': 0,
    'pv_boss': 0
}

# Charger les profils depuis un fichier (si souhaité)
def load_boss_profiles():
    try:
        with open('boss_profiles.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Sauvegarder les profils dans un fichier
def save_boss_profiles():
    with open('boss_profiles.json', 'w') as f:
        json.dump(boss_profiles, f)

# Charger les profils au démarrage
boss_profiles = load_boss_profiles()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        try:
            pv_joueur = int(request.form['pv_joueur'])
            game_data['pv_joueur'] = pv_joueur

            # Récupérer les phases de l'ennemi
            phases = []
            for i in range(1, int(request.form['nbr_phases']) + 1):
                phases.append({
                    'pv': int(request.form[f'pv_phase_{i}']),
                    'atk': int(request.form[f'atk_phase_{i}']),
                    'def': int(request.form[f'def_phase_{i}']),
                    'nom': request.form[f'nom_phase_{i}']
                })
            
            game_data['phases_ennemi'] = phases
            game_data['phase_actuelle'] = 0
            game_data['pv_boss'] = phases[0]['pv']

            return render_template('game.html', game_data=game_data)
        except ValueError:
            error = "Veuillez entrer des valeurs valides."
            return render_template('config.html', error=error)

    return render_template('config.html')

@app.route('/enlever', methods=['POST'])
def enlever():
    data = request.get_json()
    cible = data.get('cible')
    kii = int(data.get('kii'))
    atk = int(data.get('atk')) if 'atk' in data else 0
    def_cible = int(data.get('def')) if 'def' in data else 0
    ultime = data.get('ultime', False)

    if cible == 'boss':
        if not ultime:
            dmg = (kii * atk) // game_data['phases_ennemi'][game_data['phase_actuelle']]['def']
        else:
            dmg = kii // game_data['phases_ennemi'][game_data['phase_actuelle']]['def']

        game_data['pv_boss'] = max(game_data['pv_boss'] - dmg, 0)

        # Passer à la phase suivante si PV du boss à 0
        if game_data['pv_boss'] <= 0 and game_data['phase_actuelle'] < len(game_data['phases_ennemi']) - 1:
            game_data['phase_actuelle'] += 1
            game_data['pv_boss'] = game_data['phases_ennemi'][game_data['phase_actuelle']]['pv']
        elif game_data['pv_boss'] <= 0:
            return jsonify({'gagne': True, 'message': 'Vous avez vaincu le boss !'})

    elif cible == 'joueur':
        if not ultime:
            dmg = (kii * atk) // def_cible
        else:
            dmg = kii // def_cible

        game_data['pv_joueur'] = max(game_data['pv_joueur'] - dmg, 0)

        if game_data['pv_joueur'] <= 0:
            return jsonify({'gagne': False, 'message': 'Le joueur a été vaincu.'})

    return jsonify(game_data)

@app.route('/reset', methods=['POST'])
def reset():
    game_data['pv_joueur'] = 50
    game_data['phase_actuelle'] = 0
    game_data['pv_boss'] = game_data['phases_ennemi'][0]['pv']
    return jsonify(game_data)

@app.route('/save_boss_profile', methods=['POST'])
def save_boss_profile():
    profile_name = request.form['profile_name']
    nbr_phases = int(request.form['nbr_phases'])

    phases = []
    for i in range(1, nbr_phases + 1):
        phases.append({
            'pv': int(request.form[f'pv_phase_{i}']),
            'atk': int(request.form[f'atk_phase_{i}']),
            'def': int(request.form[f'def_phase_{i}']),
            'nom': request.form[f'nom_phase_{i}']
        })

    boss_profiles[profile_name] = phases
    save_boss_profiles()

    return jsonify(success=True)

@app.route('/load_boss_profile/<profile_name>', methods=['GET'])
def load_boss_profile(profile_name):
    if profile_name in boss_profiles:
        return jsonify(boss_profiles[profile_name])
    else:
        return jsonify(error="Profil introuvable"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
