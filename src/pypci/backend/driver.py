from .device import Device
import os


class Driver:
    """
    Helper Class to detect the driver of a PCI/PCI-E device.
    """
    def __init__(self):
        pass

    @staticmethod
    def Detect(device: Device):
        """
        Detect the driver of a PCI/PCI-E device.
        :param device: device object
        :return: None, directly set attributes of the device object.
        """
        driver_path = os.path.join(device.path, "driver")
        if os.path.islink(driver_path):
            device.driver_name = os.path.basename(os.readlink(driver_path))
            device.driver_set = True
        else:
            device.driver_name = ""
            device.driver_set = False

