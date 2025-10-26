## Welcome to pypci-ng!

`pypci-ng` is a pciutils-like library for fetching system PCI/PCI-E device information, but written mostly in Python.

### Architecture

- **Core Logic**: The `src/pypci/backend/` directory contains the core logic.
    - `pci.py` is the main entry point. It contains the `PCI` class (the main class for interacting with the library) and the `Helper` class (which handles OS-specific device scanning logic, supporting Linux, Windows, and FreeBSD).
    - `device.py` and `driver.py` handle device-specific and driver-specific logic.
- **Data**: The `src/pypci/data/` directory contains PCI device data. `pci.ids` is the raw data downloaded from `pci-ids.ucw.cz`, which is then parsed into JSON files by the `fetch_ids.py` script.
- **Command-Line Interface**: `src/pypci/__main__.py` provides the command-line interface.

### Development Workflow

- **Build**: To build the package, run `make build` or `python -m build`.
- **Install**: To install from source, run `make install`.
- **Update PCI IDs**: The `fetch_ids.py` script is used to download and parse the latest `pci.ids` file from `pci-ids.ucw.cz`. Run this script if you need to update the device data.

### Conventions

- The project uses `setuptools` for packaging. The `pyproject.toml` file defines the project metadata and dependencies.
- The `Makefile` provides shortcuts for common development tasks.

### External Dependencies

- The project relies on `wget` and `gunzip` to fetch and decompress the `pci.ids` file. Ensure these commands are available on your system.
