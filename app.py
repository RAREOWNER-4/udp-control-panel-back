from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os
import signal

app = Flask(__name__, static_folder='static')
CORS(app)
active_attacks = {}

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

@app.route('/start', methods=['GET'])
def start_attack():
    try:
        ip = request.args.get('ip')
        port = request.args.get('port')
        time = request.args.get('time')
        threads = request.args.get('threads')
        apikey = request.args.get('apikey')

        if not all([ip, port, time, threads, apikey]):
            raise ValueError("Missing parameters")

        command = ['./rare', ip, port, time, threads, apikey]
        process = subprocess.Popen(command)
        attack_id = str(process.pid)
        active_attacks[attack_id] = process

        return jsonify({'status': 'started', 'attack_id': attack_id})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stop', methods=['GET'])
def stop_attack():
    try:
        attack_id = request.args.get('attack_id')
        if attack_id not in active_attacks:
            raise ValueError("Invalid attack ID")

        os.kill(active_attacks[attack_id].pid, signal.SIGTERM)
        del active_attacks[attack_id]

        return jsonify({'status': f'Stopped attack {attack_id}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
