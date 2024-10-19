class Device:
    """
        Represents a PCI device.
    """
    def __init__(self, path, vendor_id, device_id, subsystem_vendor_id, subsystem_device_id, class_id, bus):
        self.path = path
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
        self.driver_name = ""
        self.processed = False
        self.driver_set = False

    def GetDeviceID(self):
        return f"{self.bus} {self.vendor_id} {self.device_id} {self.subsystem_vendor_id} {self.subsystem_device_id} {self.class_id}"

