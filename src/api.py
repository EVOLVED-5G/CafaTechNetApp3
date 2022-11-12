from flask import Flask, request, render_template
from flask_cors import CORS
import requests
import qos_awareness
import connection_monitor
import json
from os import path
import netapp_capif_connector

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


def get_capif_and_nef_credentials_json():
    dirname = path.dirname(path.abspath(__file__))
    filename = path.join(dirname, "capif_and_nef_credentials.json")
    with open(filename, "r") as f:
        capif_and_nef_credentials_json = json.load(f)
    return capif_and_nef_credentials_json


def add_capifhost_to_hosts(capif_ip, capif_host):
    hosts_file = "/etc/hosts"
    capifhost_found = False
    with open(hosts_file, "r") as h:
        lines = h.readlines()
        for index, line in enumerate(lines):
            if capif_host in line:
                row_no = index
                lines[row_no] = f"{capif_ip}    {capif_host}"
                capifhost_found = True
    if capifhost_found:
        with open(hosts_file, "w") as h:
            h.writelines(lines)
    else:
        with open(hosts_file, "a") as h:
            h.write(f"{capif_ip}    {capif_host}")


@app.route('/')
def index():
    return render_template('index.html', data=get_capif_and_nef_credentials_json())


@app.route('/', methods=['GET', 'POST'])
def index_post():
    if request.form.get("button") == "SAVE NEF AND CAPIF CREDENTIALS":
        capif_nef_credentials = {
            "nef_user": request.form["nef_user"],
            "nef_pwd": request.form["nef_pwd"],
            "nef_host": request.form["nef_host"],
            "capif_cert_path": request.form["capif_cert_path"],
            "capif_host": request.form["capif_host"],
            "capifcore_ip": request.form["capifcore_ip"],
            "capif_port": request.form["capif_port"]
        }
        dirname = path.dirname(path.abspath(__file__))
        filename = path.join(dirname, "capif_and_nef_credentials.json")
        with open(filename, "w") as f:
            json.dump(capif_nef_credentials, f)
        capif_host = request.form["capif_host"]
        capif_ip = request.form["capifcore_ip"]
        add_capifhost_to_hosts(capif_ip, capif_host)
    if request.form.get("button") == "REGISTER NETAPP TO CAPIF":
        netapp_user = request.form["netapp_user"]
        netapp_pass = request.form["netapp_pass"]
        netapp_capif_connector.capif_connector(netapp_user, netapp_pass)
    return render_template('index.html', data=get_capif_and_nef_credentials_json())


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
        return conn_state


@app.route('/capifcallbacks', methods=['POST'])
def capif_reporter():
    print(request.get_json())
    return "capif"


if __name__ == '__main__':
    print("initiating")
    app.run(host='0.0.0.0', port=5555)

