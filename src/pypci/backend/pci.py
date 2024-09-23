from dataclasses import dataclass
from ..pypciException import BackendException
from pathlib import Path
import os
import json


class Device:
    def __init__(self, vendor_id, device_id, subsystem_vendor_id, subsystem_device_id, class_id, bus):
        self.vendor_id = vendor_id
        self.device_id = device_id
        self.subsystem_vendor_id = subsystem_vendor_id
        self.subsystem_device_id = subsystem_device_id
        self.class_id = class_id
        self.bus = bus
        self.vendor_name = ""
        self.device_name = ""
        self.subsystem_vendor_name = ""
        self.subsystem_device_name = ""
        self.class_name = ""
        self.processed = False

    def GetDeviceID(self):
        return f"{self.bus} {self.vendor_id} {self.device_id} {self.subsystem_vendor_id} {self.subsystem_device_id} {self.class_id}"


class Helper:
    DEVICE_PATH = "/sys/bus/pci/devices"

    def __init__(self):
        self.devices_path = []

    def ScanDevices(self) -> list[Device]:
        devices = []
        for folder in Path(self.DEVICE_PATH).rglob('*'):
            if folder.is_dir():
                self.devices_path.append(folder)
        for device_path in self.devices_path:
            device = self.__LoadDeviceID(device_path)
            devices.append(device)
        return devices

    @staticmethod
    def __LoadDeviceID(path) -> Device:
        vendor_path = f"{path}/vendor"
        device_path = f"{path}/device"
        subsystem_vendor_path = f"{path}/subsystem_vendor"
        subsystem_device_path = f"{path}/subsystem_device"
        class_path = f"{path}/class"
        bus = path.stem.split("/")[-1]
        try:
            with open(vendor_path, "r") as file:
                vendor_id = file.read().strip()[2:]
            with open(device_path, "r") as file:
                device_id = file.read().strip()[2:]
            with open(subsystem_vendor_path, "r") as file:
                subsystem_vendor_id = file.read().strip()[2:]
            with open(subsystem_device_path, "r") as file:
                subsystem_device_id = file.read().strip()[2:]
            with open(class_path, "r") as file:
                class_id = file.read().strip()[2:]
            return Device(vendor_id, device_id, subsystem_vendor_id, subsystem_device_id, class_id, bus)
        except Exception:
            raise BackendException


class PCI:
    def __init__(self):
        self.devices = Helper().ScanDevices()
        self.pci_data = {}
        self.pci_class = {}
        self.__LoadPciData()
        self.__LoadPciClass()

    def __LoadPciData(self):
        file_path = os.path.join(Path(__file__).parent.parent, f"data/pci.data.json")
        with open(file_path, "r") as f:
            self.pci_data = json.load(f)

    def __LoadPciClass(self):
        file_path = os.path.join(Path(__file__).parent.parent, f"data/pci.class.json")
        with open(file_path, "r") as f:
            self.pci_class = json.load(f)

    def ListAll(self):
        for device in self.devices:
            self.GetDeviceInfo(device)
            self.Printer(device)

    def GetDeviceInfo(self, device: Device) -> Device:
        if device.processed:
            return device
        if device.vendor_id in self.pci_data.keys():
            device.vendor_name = self.pci_data[device.vendor_id]["name"]
            if device.device_id in self.pci_data[device.vendor_id].keys():
                device.device_name = self.pci_data[device.vendor_id][device.device_id]["name"]
                if device.subsystem_vendor_id in self.pci_data[device.vendor_id][device.device_id].keys():
                    if device.subsystem_device_id in self.pci_data[device.vendor_id][device.device_id][device.subsystem_vendor_id].keys():
                        device.subsystem_device_name = self.pci_data[device.vendor_id][device.device_id][device.subsystem_vendor_id][device.subsystem_device_id]
        pci_class_id = device.class_id[0:2]
        pci_subclass_id = device.class_id[2:4]
        pci_interface_id = device.class_id[4:6]
        pci_class = self.pci_class.get(pci_class_id)
        if pci_class is not None:
            pci_subclass = pci_class.get(pci_subclass_id)
            if pci_subclass is not None:
                pci_interface = pci_subclass.get(pci_interface_id)
                if pci_interface is not None:
                    device.class_name = pci_interface.get("name")
                else:
                    device.class_name = pci_subclass.get("name")
            else:
                device.class_name = pci_class.get("name")
        else:
            device.class_name = ""

        device.processed = True
        return device

    @staticmethod
    def Printer(device: Device):
        if device.subsystem_device_name != "":
            print(f"{device.bus} {device.class_name}: {device.vendor_name} {device.subsystem_device_name}")
        else:
            print(f"{device.bus} {device.class_name}: {device.vendor_name} {device.device_name}")



