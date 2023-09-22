from flask import Flask, request, render_template
from flask_cors import CORS
import requests
import qos_awareness
import connection_monitor

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/subscribe_ue', methods=['POST'])
def subscribe_ue():
    vapp_notif_dest = request.get_json()['vapp_notif_dest']
    with open("vapp_notif_dest.txt", "w") as f:
        f.write(vapp_notif_dest)
    ue_id = request.get_json()['ue_id']
    ext_id = request.get_json()['ext_id']
    qos_awareness.create_quaranteed_bit_rate_subscription_for_discrete_automation(ue_id)
    connection_monitor.create_connection_monitor_subscription(ext_id)
    return "Subscribed"


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    qos_awareness.read_and_delete_all_existing_subscriptions()
    connection_monitor.read_and_delete_all_existing_subscriptions()
    return "Unsubscribed from NEF Emulator"


@app.route('/nefcallbacks', methods=['POST'])
def qos_reporter():
    with open("vapp_notif_dest.txt", "r") as f:
        vapp_notif_dest = f.read()
    callback_json = request.get_json()
    if "eventReports" in callback_json:
        qos_state = callback_json['eventReports'][0]['event']
        print(f"QoS state: {qos_state}")
        requests.post(f"{vapp_notif_dest}/qos_state", json=qos_state)
        return qos_state
    if "monitoringType" in callback_json:
        conn_state = callback_json['monitoringType']
        print(f"Connection state: {conn_state}")
        requests.post(f"{vapp_notif_dest}/conn_state", json=conn_state)
        return {"ack": "TRUE"}


@app.route('/capifcallbacks', methods=['POST'])
def capif_reporter():
    print(request.get_json())
    return "capif"


if __name__ == '__main__':
    print("initiating")
    app.run(host='0.0.0.0', port=5555)
