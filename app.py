# app.py
from flask import Flask, jsonify, request, send_from_directory
from algorithms import compute_pci, compute_disconnect_score
import time

app = Flask(__name__, static_folder='static')

TIMELINE = []

@app.route('/api/pci', methods=['POST'])
def api_pci():
    data = request.get_json() or {}
    hrv_change = float(data.get('hrv_change', 0.0))
    tone_shift = float(data.get('tone_shift', 0.0))
    breath_sync = float(data.get('breath_sync', 0.8))
    micro_pos = float(data.get('micro_pos', 0.05))
    micro_neg = float(data.get('micro_neg', 0.05))
    pci_drop = float(data.get('pci_drop', 0.0))

    pci = compute_pci(hrv_change, tone_shift, breath_sync, micro_pos, micro_neg)
    disconnect = compute_disconnect_score(max(0, -hrv_change), tone_shift, max(0, 1-breath_sync), micro_neg, pci_drop)

    entry = {
        'ts': int(time.time()*1000),
        'pci': pci,
        'disconnect_score': disconnect,
        'components': {
            'hrv_change': hrv_change,
            'tone_shift': tone_shift,
            'breath_sync': breath_sync,
            'micro_pos': micro_pos,
            'micro_neg': micro_neg,
            'pci_drop': pci_drop
        }
    }
    TIMELINE.append(entry)
    if len(TIMELINE) > 500:
        TIMELINE.pop(0)

    return jsonify(entry)

@app.route('/api/timeline', methods=['GET'])
def api_timeline():
    return jsonify(TIMELINE[-200:])

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
