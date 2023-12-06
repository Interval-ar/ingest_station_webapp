import time

from usb_management.usb_checker import usb_devices_connected as usb_check
import json
import os

import datetime


stop_string = "XXXX Programa detenido - XXXX"


def configure_hub(request_id):
    local_request_id = False
    now = datetime.datetime.now()
    date_time = now.strftime("%d/%m %H:%M:%S")
    if not local_request_id:
        local_request_id = request_id

    if local_request_id == request_id:
        append_to_log(
            f"\n{'#'*20}\n-- {date_time} --\nNueva instancia de configuracion iniciada\n{'#'*20}\n"
        )
        append_to_log_identifiers([""])
        iterations = 1
        max_iterations = 120 * 2
        usb_devices_connected = usb_check()
        print(usb_devices_connected)
        # print(type(usb_devices_connected))

        temp_devices = usb_devices_connected
        ports_identifiers = []
        run = True
        while run:
            if temp_devices == usb_devices_connected and len(usb_devices_connected) > 0:
                iterations += 1
                # print(usb_devices_connected)
                # print(temp_devices == usb_devices_connected)
                usb_devices_connected = usb_check()
                time.sleep(0.5)
            else:
                iterations = 0
                usb_devices_connected = usb_check()
                temp_devices = usb_devices_connected
                if len(usb_devices_connected) == 1:
                    for device in usb_devices_connected.items():
                        device = device[1]
                        print(device)
                        device_path_list = device["children"][0]["dev_path"].split("/")
                        port_identifier = 00000
                        for section in device_path_list:
                            if "1.0" in section:
                                port_identifier = section
                        if (
                            len(ports_identifiers)
                            and port_identifier == ports_identifiers[0]
                        ):
                            line_log = (
                                date_time
                                + " | "
                                + "Insertaste el lector en el primer puerto. Saliendo del programa"
                            )
                            append_to_log(line_log)
                            append_to_log(stop_string)
                            run = False
                            break

                        if port_identifier not in ports_identifiers:
                            ports_identifiers.append(port_identifier)
                            append_to_log_identifiers(ports_identifiers)
                            line_log = (
                                date_time
                                + " | "
                                + "Desconecta el lector y colocalo siguiente puerto hacia la derecha"
                            )
                            append_to_log(line_log)

                            temp_devices = usb_devices_connected

                time.sleep(1)
            if (max_iterations - iterations + 1) % 10 == 0:
                append_to_log(
                    f"Escaneando... tienes {max_iterations - iterations + 1} segundos para pasar al siguiente puerto."
                )

            if iterations > max_iterations:
                line_log = date_time + " | " + "Tiempo terminado. Saliendo del programa"
                append_to_log(line_log)
                append_to_log(stop_string)
                exit()

        return ports_identifiers


def append_to_log(line):
    print("appended")
    with open(
        get_app_path("data/logs/usb/current_session.log"), "a"
    ) as current_session_log:
        current_session_log.write(line + "\n")


def append_to_log_identifiers(identifiers_list):
    with open(
        get_app_path("data/logs/usb/identifiers.log"), "w"
    ) as current_session_log:
        current_session_log.write(json.dumps(identifiers_list))


def get_app_path(relative_path):
    app_root = os.path.dirname(os.path.abspath("web_server2.py"))
    return os.path.join(app_root, relative_path)


# configure_hub()
