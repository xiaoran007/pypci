import subprocess
import json
from re import split

file_path = "./src/pypci/data/pci.ids"
device_id_path = "./src/pypci/data/pci.data"
class_id_path = "./src/pypci/data/pci.class"
device_id_json_path = "./src/pypci/data/pci.data.json"
class_id_json_path = "./src/pypci/data/pci.class.json"



def fetch_pci_ids():
    # use subprocess to call bash - wget to get new pci.ids file
    print("Fetching new PCI IDs...")
    subprocess.run(["bash", "-c", "wget -q -O ./src/pypci/data/pci.ids.gz https://pci-ids.ucw.cz/v2.2/pci.ids.gz"])
    subprocess.run(["bash", "-c", "rm ./src/pypci/data/pci.ids"])
    print("Updating local copy of PCI IDs... ")
    subprocess.run(["bash", "-c", "gunzip ./src/pypci/data/pci.ids.gz"])
    print("Finished fetching new PCI IDs.  ")


def split_pci_ids():
    with open(file_path, 'r') as f:
        lines = f.readlines()
    if "# List of known device classes, subclasses and programming interfaces\n" in lines:
        split_index = lines.index("# List of known device classes, subclasses and programming interfaces\n")
        data = lines[0:split_index]
        class_data = lines[split_index:]
        with open(device_id_path, 'w') as d:
            d.writelines(data)
        with open(class_id_path, 'w') as c:
            c.writelines(class_data)
    else:
        print("no")


def parse_pci_ids():
    pci_data = {}
    current_vendor = None

    with open(device_id_path, 'r') as f:
        for line in f:
            if not line or line.startswith("#"):
                continue

            if line[0] != '\t' and line[0] != 'C' and line[0] != '\n':
                # vendor line
                current_vendor = line[:4]
                vendor_name = line[4:].strip()
                pci_data[current_vendor] = {'name': vendor_name}
                print("Processing vendor: ", current_vendor, " - ", vendor_name, "  ...")
            elif line[0] == '\t' and line[1] != '\t':
                # device line
                device_id = line[1:5]
                device_name = line[5:].strip()
                pci_data[current_vendor][device_id] = {'name': device_name}
                print("    Processing device: ", device_id, " - ", device_name, "  ...")
            elif line[0] == '\t' and line[1] == '\t':
                # subsystem line
                subsystem_vendor = line[2:6]
                subsystem_device = line[7:11]
                subsystem_name = line[12:].strip()
                pci_data[current_vendor][device_id][subsystem_vendor] = {}
                pci_data[current_vendor][device_id][subsystem_vendor][subsystem_device] = subsystem_name
            elif line[0] == 'C':
                # class line, implement later
                break

    return pci_data


def parse_pci_classes():
    pci_class_data = {}
    current_class = None

    with open(class_id_path, 'r') as f:
        for line in f:
            if not line or line.startswith("#"):
                continue

            if line[0] != '\t' and line[0] == 'C' and line[0] != '\n':
                # class line
                current_class = line[2:4]
                class_name = line[4:].strip()
                pci_class_data[current_class] = {'name': class_name}
                print("Processing class: ", current_class, " - ", class_name, "  ...")
            elif line[0] == '\t' and line[1] != '\t':
                # subclass line
                subclass_id = line[1:3]
                subclass_name = line[3:].strip()
                pci_class_data[current_class][subclass_id] = {'name': subclass_name}
                print("    Processing subclass: ", subclass_id, " - ", subclass_name, "  ...")
            elif line[0] == '\t' and line[1] == '\t':
                # prog-if line
                prog_if_id = line[2:4]
                prog_if_name = line[4:].strip()
                pci_class_data[current_class][subclass_id][prog_if_id] = {'name': prog_if_name}
                print("        Processing prog-if: ", prog_if_id, " - ", prog_if_name, "  ...")


    return pci_class_data


def json_creator():
    device_dict = parse_pci_ids()
    class_dict = parse_pci_classes()
    with open(device_id_json_path, 'w') as f:
        json.dump(device_dict, f, indent=4)
    with open(class_id_json_path, 'w') as f:
        json.dump(class_dict, f, indent=4)


if __name__ == "__main__":
    fetch_pci_ids()
    split_pci_ids()
    json_creator()
