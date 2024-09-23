from .backend.pci import PCI
from .pypciUtil import getOS


def main():
    if getOS() != "linux":
        print(f"Only Linux is supported for now. Current OS: {getOS()}")
        return
    pci = PCI()
    pci.ListAll()


if __name__ == "__main__":
    main()
