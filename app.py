from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to UDP Flood Control API!"

@app.route('/start', methods=['GET'])
def start_attack():
    ip = request.args.get('ip')
    port = request.args.get('port')
    time = request.args.get('time')
    threads = request.args.get('threads')
    api_key = request.args.get('apikey')

    if api_key != 'valid-api-key':
        return jsonify({'error': 'Invalid API Key'}), 403

    attack_id = subprocess.run(['python', 'start_attack.py', ip, port, time, threads], capture_output=True, text=True).stdout.strip()
    return jsonify({'attack_id': attack_id})

@app.route('/stop', methods=['GET'])
def stop_attack():
    attack_id = request.args.get('attack_id')
    # Logic to stop the attack goes here.
    return jsonify({'status': f'Stopped attack with ID {attack_id}'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
