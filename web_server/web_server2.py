from flask import Flask, render_template, request

import usb_management.initialize_usb_hub as initialize_usb_hub

import usb_management.usb_checker as usb_checker

import usb_management.usb_info as usb_info

import os

from threading import Thread

import random

import json

from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

main_usb_thread = False


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/hub_config")
def initialize_hub():
    req_id = "." + str(random.randint(1111, 999999999)) + "."

    return render_template("hub_config.html", req_id=req_id)


@app.route("/hub_config_backend")
def hub_config_backend():
    messages = []
    req_id = request.args.get("req_id")
    start_usb_logic(req_id)
    return {"messages": messages}


@app.route("/hub_session_logs")
def log_responses():
    with open(get_app_path("data/logs/usb/current_session.log"), "r") as current_session_log:
        session_log = current_session_log.read()
    with open(get_app_path("data/logs/usb/identifiers.log"), "r") as current_session_identifiers_log:
        identifiers_log = current_session_identifiers_log.read()
    return {"session": session_log, "identifiers": json.loads(identifiers_log)}


@app.route("/clear_logs")
def clear_logs():
    with open(get_app_path("data/logs/usb/current_session.log"), "w") as current_session_log:
        current_session_log.write("")
    return "cleared"


@app.route("/save_current_hub_config")
def save_usb_identifiers():
    with open(get_app_path("data/logs/usb/identifiers.log"), "r+") as identifiers_list:
        json_identifiers_list = json.loads(identifiers_list.read())

    with open(get_app_path("data/hub_maps.json"), "r") as hub_map:
        json_hub_map = json.loads(hub_map.read())

    json_hub_map.append(json_identifiers_list)

    with open(get_app_path("data/hub_maps.json"), "w") as hub_map:
        hub_map.write(json.dumps(json_hub_map))
    return "test"


@app.route("/get_hubs")
@cross_origin()
def get_hubs():
    with open(get_app_path("data/hub_maps.json"), "r") as hub_map:
        json_hub_map = json.loads(hub_map.read())
        usb_info.usb_devices_connected()
    return json_hub_map


@app.route("/get_per_usb_data")
@cross_origin()
def get_per_usb_data():
    with open(get_app_path("data/usb_data/formated_UI_usb_data.json"), "r") as per_usb_data:
        json_per_usb_data = json.loads(per_usb_data.read())
    return json_per_usb_data


def start_usb_logic(request_id):
    global main_usb_thread
    usb_thread = Thread(target=initialize_usb_hub.configure_hub, args=(request_id,))
    if not main_usb_thread:
        main_usb_thread = usb_thread
    if not main_usb_thread.is_alive():
        usb_thread.start()
    print(usb_thread.is_alive())


def get_app_path(relative_path):
    app_root = os.path.dirname(os.path.abspath("web_server2.py"))
    return os.path.join(app_root, relative_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=config.CONTROLLERS[whoami]["port"],debug=True)
