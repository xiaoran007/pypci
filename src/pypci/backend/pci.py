from ..pypciException import BackendException
from ..pypciUtil import getOS
from .device import Device
from .driver import Driver
from .util import Printer
from pathlib import Path
import os
import json
import subprocess
import re


class Helper:
    DEVICE_PATH = "/sys/bus/pci/devices"

    def __init__(self):
        self.devices_path = []
        self.__os = getOS()

    def ScanDevices(self) -> list[Device]:
        if getOS() == "linux":
            return self.__ScanDevicesLinux()
        elif getOS() == "windows":
            return self.__ScanDevicesWindows()

    def __ScanDevicesLinux(self) -> list[Device]:
        devices = []
        for folder in Path(self.DEVICE_PATH).rglob('*'):
            if folder.is_dir():
                self.devices_path.append(folder)
        self.devices_path.sort()
        for device_path in self.devices_path:
            device = self.__LoadDeviceID(device_path)
            devices.append(device)
        return devices

    def __ScanDevicesWindows(self) -> list[Device]:
        devices = []
        COMMAND = 'Get-CimInstance -ClassName Win32_PnPEntity | Where-Object { $_.DeviceID -like "PCI*" } | Select-Object HardwareID | ConvertTo-JSON'
        try:
            result = subprocess.run(["powershell", "-Command", COMMAND], capture_output=True, text=True)
        except subprocess.SubprocessError:
            raise BackendException

        hardware_ids = json.loads(result.stdout)

        count = 0

        for hardware_id in hardware_ids:
            device_ser = hardware_id["HardwareID"][0]
            class_ser = hardware_id["HardwareID"][-2]
            # example device_ser = PCI\\VEN_8086&DEV_2F28&SUBSYS_00000000&REV_02
            pattern_device = r"VEN_([0-9A-Za-z]{4})&DEV_([0-9A-Za-z]{4})&SUBSYS_([0-9A-Za-z]{4})([0-9A-Za-z]{4})"
            match_device = re.search(pattern_device, device_ser)
            try:
                vendor_id = match_device.group(1).lower()
                device_id = match_device.group(2).lower()
                subsystem_vendor_id = match_device.group(4).lower()
                subsystem_device_id = match_device.group(3).lower()
            except:
                continue

            # example class_ser = PCI\\VEN_8086&DEV_9D03&CC_010601
            pattern_class = r"CC_([0-9A-Za-z]{6})"
            match_class = re.search(pattern_class, class_ser)
            try:
                class_id = match_class.group(1).lower()
            except:
                continue
            if count < 10:
                bus = f"PCI 0{count}"
            else:
                bus = f"PCI {count}"
            devices.append(Device("", vendor_id, device_id, subsystem_vendor_id, subsystem_device_id, class_id, bus))
            count += 1

        return devices



    @staticmethod
    def __LoadDeviceID(path) -> Device:
        vendor_path = f"{path}/vendor"
        device_path = f"{path}/device"
        subsystem_vendor_path = f"{path}/subsystem_vendor"
        subsystem_device_path = f"{path}/subsystem_device"
        class_path = f"{path}/class"
        bus = str(path).split("/")[-1][5:]
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
            return Device(path, vendor_id, device_id, subsystem_vendor_id, subsystem_device_id, class_id, bus)
        except Exception:
            raise BackendException


class PCI:
    def __init__(self):
        self.devices = Helper().ScanDevices()
        self.pci_data = {}
        self.pci_class = {}
        self.__LoadPciData()
        self.__LoadPciClass()
        self.__FetchAll()

    def __LoadPciData(self):
        file_path = os.path.join(Path(__file__).parent.parent, f"data/pci.data.json")
        with open(file_path, "r") as f:
            self.pci_data = json.load(f)

    def __LoadPciClass(self):
        file_path = os.path.join(Path(__file__).parent.parent, f"data/pci.class.json")
        with open(file_path, "r") as f:
            self.pci_class = json.load(f)

    def __FetchAll(self):
        for device in self.devices:
            self.GetDeviceInfo(device)

    def FindAllVGA(self) -> list[Device]:
        """
        Find all Display controller in the system.
        :return: list of Device.
        """
        vga_devices = []
        for device in self.devices:
            if device.class_id[0:2] == "03" or device.class_id[0:4] == "0001" or device.class_id[0:4] == "0005":
                vga_devices.append(device)
        return vga_devices

    def FindAllNIC(self) -> list[Device]:
        """
        Find all Network controller in the system.
        :return: list of Device.
        """
        nic_devices = []
        for device in self.devices:
            if device.class_id[0:2] == "02" or device.class_id[0:2] == "0d":
                nic_devices.append(device)
        return nic_devices

    def FindAllNPU(self) -> list[Device]:
        """
        Find all Neural Processing Unit (NPU) in the system.
        :return: list of Device.
        """
        npu_devices = []
        for device in self.devices:
            if device.class_id[0:4] == "1200":
                npu_devices.append(device)
        return npu_devices

    def FindAllDevice(self) -> list[Device]:
        """
        Find all PCI/PCI-E devices in the system.
        :return: list of Device.
        """
        return self.devices

    def ListAll(self):
        """
        Print all PCI/PCI-E devices in the system. Similar to lspci.
        """
        for device in self.devices:
            self.GetDeviceInfo(device)
            Printer.DefaultPrint(device)

    def ListAllDrivers(self):
        """
        Print all loaded drivers for PCI/PCIE devices in the system.
        """
        for device in self.devices:
            self.GetDeviceInfo(device)
            Driver.Detect(device)
            Printer.DriverPrint(device)

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
                    # device.class_name = pci_interface.get("name")
                    device.class_name = f"{pci_subclass.get('name')} ({pci_interface.get('name')})"
                else:
                    device.class_name = pci_subclass.get("name")
            else:
                device.class_name = pci_class.get("name")
        else:
            device.class_name = ""

        device.processed = True
        return device

