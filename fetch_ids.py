import subprocess
import hashlib


def fetch_pci_ids():
    # use subprocess to call bash - wget to get new pci.ids file
    print("Fetching new PCI IDs...")
    subprocess.run(["bash", "-c", "wget -q -O ./src/pypci/data/pci.ids.gz https://pci-ids.ucw.cz/v2.2/pci.ids.gz"])
    subprocess.run(["bash", "-c", "rm ./src/pypci/data/pci.ids"])
    print("Updating local copy of PCI IDs... ")
    subprocess.run(["bash", "-c", "gunzip ./src/pypci/data/pci.ids.gz"])
    print("Finished fetching new PCI IDs.  ")


if __name__ == "__main__":
    fetch_pci_ids()
