from .device import Device
import os


class Driver:
    def __init__(self):
        pass

    @staticmethod
    def Detect(device: Device):
        driver_path = os.path.join(device.path, "driver")
        if os.path.islink(driver_path):
            device.driver_name = os.path.basename(os.readlink(driver_path))
            device.driver_set = True
        else:
            device.driver_name = ""
            device.driver_set = False

