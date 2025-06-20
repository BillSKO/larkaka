from flask import Blueprint, jsonify
import json
import os

data_api = Blueprint('data_api', __name__)

@data_api.route('/api/nikola-data')
def get_nikola_data():
    try:
        with open(os.path.expanduser('~/NikolaDeploy/data/nikola_live_status.json'), 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})
