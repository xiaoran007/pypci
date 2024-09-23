from .backend.pci import PCI


def main():
    pci = PCI()
    pci.ListAll()


if __name__ == "__main__":
    main()
