import subprocess as sb
import json

import os


device_template = {
    "name": "",
    "portID": "",
    "children": [],
    "isUSB3": False,
}

child_template = {
    "name": "",
    "mountPoint": "",
    "portID": "",
    "devPath": "",
    "size": {
        "total": 0,
        "used": 0,
        "usedPerc": 0,
    },
}


def usb_devices_connected():
    response = sb.getoutput("lsblk -J -e7 ")
    response = json.loads(response)["blockdevices"]

    device_data_for_UI = {}
    for device in response:
        if device["rm"]:
            device_data = structure_device_data(device)
            device_data_for_UI[device_data["portID"]] = (device_data)
    save_data_for_UI(device_data_for_UI)
    print(device_data_for_UI)


def structure_device_data(device):
    if "children" in device:
        device_data = handle_device_with_children(device)
    else:
        device_data = handle_device_without_children(device)
    return device_data


def handle_device_with_children(device):
    children = device["children"]
    device_name = device["name"]
    device_path = get_device_dev_path(device)
    device_children_count = len(children)
    is_usb_3 = check_if_usb_3(device)
    device_identifier = get_device_identifier_from_path(device_path)
    device_template = {
        "name": device_name,
        "portID": device_identifier,
        "isUSB3": is_usb_3,
        "children_count": device_children_count,
        "children": structure_children(children),
    }

    return device_template


def structure_children(children):
    child_template = {
        "name": "",
        "mountPoint": "",
        "portID": "",
        "devPath": "",
        "size": {
            "total": 0,
            "used": 0,
            "usedPerc": 0,
        },
    }

    child_list = []
    for child in children:
        name = child["name"]
        # mountPoint = child["mountpoint"]
        child_template = {
            "name": child["name"],
            "mountPoint": child["mountpoints"][0],
            "size": {
                "total": 0,
                "used": 0,
                "usedPerc": 0,
            },
        }
        child_list.append(child_template)
    return child_list


def handle_device_without_children(device):
    return


def check_if_usb_3(device):
    return "usb2" in get_device_dev_path(device)


def get_device_dev_path(device):
    device_dev_path = sb.getoutput(
        f"udevadm info --query=property --export --name={device['name']} | grep 'DEVPATH'"
    )
    device_dev_path = device_dev_path.replace("DEVPATH=", "").replace("'", "")
    return device_dev_path


def get_device_identifier_from_path(dev_path):
    dev_path = dev_path.split("/")
    for section in dev_path:
        if "1.0" in section:
            return section


def mount_device_if_not_mounted(partition):
    if partition["mountpoints"][0] == None:
        os.system(
            f"udisksctl mount -b /dev/{partition['name']} --no-user-interaction > /dev/null"
        )
        return True
    else:
        return False


def save_data_for_UI(usb_data_for_ui):
    with open(
        get_app_path("data/usb_data/formated_UI_usb_data.json"), "w"
    ) as per_usb_info:
        return per_usb_info.write(json.dumps(usb_data_for_ui))


def save_per_usb_info(usb_info):
    with open(get_app_path("data/per_usb_info.json"), "w") as per_usb_info:
        return per_usb_info.write(json.dumps(usb_info))


def get_app_path(relative_path):
    app_root = os.path.dirname(os.path.abspath("web_server2.py"))
    return os.path.join(app_root, relative_path)


# print(response["blockdevices"])

# udevadm info --query=property --export --name=sdb1 |grep "DEVPATH"
# /devices/pci0000:00/0000:00:14.0/usb2/2-1/2-1.2/2-1.2:1.0/host2/target2:0:0/2:0:0:0/block/sdb/sdb1
# DEVPATH='/devices/pci0000:00/0000:00:14.0/usb1/1-1/1-1.4/1-1.4:1.0/host3/target3:0:0/3:0:0:0/block/sdc/sdc1'

# echo "2-x" | sudo /sys/bus/usb/drivers/usb/unbind (apaga dispositivo)


# tree -d -JL 3 --charset utf-8 --du $HOME/share
