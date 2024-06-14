import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Credenciales de Autodesk
CLIENT_ID = 'DPNBtAv52zM6MAHso6VoiZfjDTK1NKWW'
CLIENT_SECRET = 'pgttXmSskdiyYG7V'
BASE_URL = 'https://developer.api.autodesk.com'
AUTH_URL = f'{BASE_URL}/authentication/v1/authenticate'

# Función para obtener el token de acceso
def get_access_token():
    auth_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials',
        'scope': 'data:read data:write'
    }
    try:
        response = requests.post(AUTH_URL, data=auth_data)
        response.raise_for_status()
        token = response.json().get('access_token')
        return token
    except requests.exceptions.RequestException as e:
        print("Error al obtener el token de acceso:", e)
        return None

# Endpoint para listar los hubs (proyectos)
@app.route('/hubs', methods=['GET'])
def get_hubs():
    token = get_access_token()
    if not token:
        return jsonify({"error": "No se pudo obtener el token de acceso"}), 500
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(f'{BASE_URL}/project/v1/hubs', headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print("Error al obtener los hubs:", e)
        return jsonify({"error": "No se pudo obtener los hubs"}), 500

# Endpoint para listar los proyectos dentro de un hub
@app.route('/hubs/<hub_id>/projects', methods=['GET'])
def get_projects(hub_id):
    token = get_access_token()
    if not token:
        return jsonify({"error": "No se pudo obtener el token de acceso"}), 500
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(f'{BASE_URL}/project/v1/hubs/{hub_id}/projects', headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print("Error al obtener los proyectos:", e)
        return jsonify({"error": "No se pudo obtener los proyectos"}), 500

# Endpoint para listar las carpetas dentro de un proyecto
@app.route('/projects/<project_id>/folders', methods=['GET'])
def get_folders(project_id):
    token = get_access_token()
    if not token:
        return jsonify({"error": "No se pudo obtener el token de acceso"}), 500
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(f'{BASE_URL}/data/v1/projects/{project_id}/folders', headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print("Error al obtener las carpetas:", e)
        return jsonify({"error": "No se pudo obtener las carpetas"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
