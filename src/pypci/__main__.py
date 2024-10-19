from .backend.pci import PCI
from .pypciUtil import getOS
from . import __version__
import sys


def main():
    if getOS() != "linux":
        print(f"Only Linux is supported for now. Current OS: {getOS()}")
        return
    if len(sys.argv) == 2:
        if sys.argv[1] == "-d" or sys.argv[1] == "--list-drivers":
            pci = PCI()
            pci.ListAllDrivers()
        elif sys.argv[1] == "-v" or sys.argv[1] == "--version":
            print(f"pypci version: {__version__}")
        elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print_help()
        else:
            print("Wrong argument.")
            print_help()
    else:
        pci = PCI()
        pci.ListAll()


def print_help():
    print("Usage: pypci [options]")
    print("Options:")
    print("  [Empty]             List all PCI/PCI-E devices in the system.")
    print("  -d, --list-drivers  List all loaded drivers for PCI/PCI-E devices.")
    print("  -v, --version       Print the version of pypci.")
    print("  -h, --help          Print this help message.")


if __name__ == "__main__":
    main()
