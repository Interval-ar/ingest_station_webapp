import subprocess as sb
import json

import os


# class Device:
#     def __init__(self, device):
#         self.device = device
#         self.name = device["name"]
#         self.port_identifier = ""
#         self.children = []
#         self.structure_children_data()
#         print(self.__dict__)

#     def structure_children_data(self):
#         children = self.device["children"]
#         for child in children:
#             new_child = Child(child)
#             self.children.append(new_child.__dict__)


# class Child:
#     def __init__(self, device):
#         self.device = device
#         self.name = device["name"]
#         self.mount_point = device["mountpoints"]
#         self.size = device["size"]
#         self.port_identifier = ""
#         self.dev_path = ""
#         self.usb_v_3 = False
#         self.get_dev_path()
#         self.get_port_identifier()
#         self.check_if_usb_3()

#     def get_dev_path(self):
#         device_dev_path = sb.getoutput(
#             f"udevadm info --query=property --export --name={self.name} | grep 'DEVPATH'"
#         )
#         device_dev_path = device_dev_path.replace("DEVPATH=", "").replace("'", "")
#         self.dev_path = device_dev_path

#     def check_if_usb_3(self):
#         self.usb_v_3 = "usb2" in get_device_dev_path(self.device)

#     def get_port_identifier(self):
#         device_path_list = self.dev_path.split("/")
#         child_port_identifier = 00000
#         for section in device_path_list:
#             if "1.0" in section:
#                 child_port_identifier = section
#         self.port_identifier = child_port_identifier

device_template = {
    "name": "",
    "portID": "",
    "children": [],
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
    devices_list = {}
    per_usb_info = {}
    for device in response:
        if device["rm"]:
            devices_list[device["name"]] = {"children_count": 0, "children": []}

            if "children" in device:
                children = device["children"]
                devices_list[device["name"]]["children_count"] = len(children)
                # print("children: ", len(children))
                # detects usb 2.0 or 3.x based on the usb
                device_dev_path = get_device_dev_path(device)
                is_usb_3 = check_if_usb_3(device)
                for child in children:
                    device_path_list = device_dev_path.split("/")
                    port_identifier = 00000
                    for section in device_path_list:
                        if "1.0" in section:
                            port_identifier = section
                    child_values = {
                        "name": device["name"],
                        "mount_points": [],
                        "size": [],
                        "children": {},
                        "usb_version_3": is_usb_3,
                        "dev_path": device_dev_path + "/" + child["name"],
                        "port_identifier": port_identifier,
                    }
                    if not child_values["port_identifier"] in per_usb_info:
                        per_usb_info[child_values["port_identifier"]] = child_values
                    per_usb_info[child_values["port_identifier"]]["children"][
                        child["name"]
                    ] = []
                    if child["mountpoints"][0] == None:
                        os.system(
                            f"udisksctl mount -b /dev/{child['name']} --no-user-interaction > /dev/null"
                        )
                    else:
                        df_data = os.system(f"df /dev/{child['name']} -h > /dev/null")
                        per_usb_children_info = per_usb_info[
                            child_values["port_identifier"]
                        ]["children"][child["name"]]

                        per_usb_children_info.append(child["name"])
                        per_usb_children_info.append(child["mountpoints"][0])
                        per_usb_children_info.append(child["size"])
                        # print(child["mountpoints"])
                        children_file_count = os.system(
                            f"find {child['mountpoints'][0]} -type f | wc -l > /dev/null"
                        )
                        per_usb_children_info.append(children_file_count)

                    devices_list[device["name"]]["children"].append(child_values)

            else:
                print(device)
                # per_usb_info[device["name"]] = "no_child"
                print("no_sd")
    with open(get_app_path("data/hubs_data.json"), "w") as hub_data_file:
        hub_data_file.write(json.dumps(devices_list))
    save_per_usb_info(per_usb_info)
    return devices_list


def structure_device_data(device):
    if "children" in device:
        handle_device_with_children(device)
    else:
        handle_device_without_children(device)
    return


def handle_device_with_children(device):
    children = device["children"]
    device_path = get_device_dev_path(device)
    device_children_count = len(children)
    is_usb_3 = check_if_usb_3(device)
    device_identifier = get_device_identifier_from_path(device_path)
    return


def handle_device_without_children():
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
