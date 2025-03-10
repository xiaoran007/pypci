from .device import Device


class Printer:
    """
    Helper class to print PCI/PCI-E device information.
    """
    def __init__(self):
        pass

    @staticmethod
    def DefaultPrint(device: Device):
        """
        Print the device information. Default.
        :param device: device object
        :return: None
        """
        if device.subsystem_device_name != "":
            print(f"{device.bus} {device.class_name}: {device.vendor_name} {device.device_name} ({device.subsystem_device_name})")
        else:
            print(f"{device.bus} {device.class_name}: {device.vendor_name} {device.device_name}")

    @staticmethod
    def DriverPrint(device: Device):
        """
        Print the device information with driver information.
        :param device: device object
        :return: None
        """
        if device.subsystem_device_name != "":
            print(f"{device.bus} {device.class_name}: {device.vendor_name} {device.device_name} ({device.subsystem_device_name})")
            if device.driver_set:
                print(f"        Driver: {device.driver_name}")
        else:
            print(f"{device.bus} {device.class_name}: {device.vendor_name} {device.device_name}")
            if device.driver_set:
                print(f"        Driver: {device.driver_name}")

