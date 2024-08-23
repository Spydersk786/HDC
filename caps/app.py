from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

alerts = []

@app.route('/')
def index():
    return render_template('index.html', alerts=alerts)

@app.route('/api/alert', methods=['POST'])
def receive_alert():
    alert_message = request.json.get('message', '')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    alerts.append(f"[{timestamp}] {alert_message}")
    return 'Alert received', 200

if __name__ == '__main__':
    app.run(debug=True)
