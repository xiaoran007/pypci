from dataclasses import dataclass
from .pypciException import BackendException
from pathlib import Path


class PCI:
    def __init__(self):
        self.devices = Helper().ScanDevices()

    def GetDeviceInfo(self):
        pass





class Device:
    def __init__(self, vendor_id, device_id, subsystem_vendor_id, subsystem_device_id, class_id):
        self.vendor_id = vendor_id
        self.device_id = device_id
        self.subsystem_vendor_id = subsystem_vendor_id
        self.subsystem_device_id = subsystem_device_id
        self.class_id = class_id
        self.vendor_name = ""
        self.device_name = ""
        self.subsystem_vendor_name = ""
        self.subsystem_device_name = ""
        self.class_name = ""
        self.processed = False

    def GetDeviceID(self):
        return f"{self.vendor_id} {self.device_id} {self.subsystem_vendor_id} {self.subsystem_device_id} {self.class_id}"


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
            return Device(vendor_id, device_id, subsystem_vendor_id, subsystem_device_id, class_id)
        except Exception:
            raise BackendException
