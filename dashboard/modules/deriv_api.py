# ~/NikolaWeb/dashboard/modules/deriv_api.py
from flask import Blueprint, jsonify
import sys
import os

# Gör så att vi kan importera från projektroten
sys.path.append(os.path.expanduser("~/NikolaWeb"))
from executors.deriv_executor import connect_deriv

deriv_api = Blueprint('deriv_api', __name__)

@deriv_api.route('/api/deriv/status', methods=['GET'])
def deriv_status():
    try:
        status = connect_deriv()
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
