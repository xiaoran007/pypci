# pypci-ng
[![Downloads](https://static.pepy.tech/badge/pypci-ng)](https://pepy.tech/project/pypci-ng)
![PyPI - Version](https://img.shields.io/pypi/v/pypci-ng?label=version)

![Static Badge](https://img.shields.io/badge/Linux-blue)


pypci-ng, a pciutils-like library for fetching system PCI/PCI-E devices but written mostly in python.


![demo0](https://files.catbox.moe/mku1dg.png)


![demo1](https://files.catbox.moe/scnd3j.png)

## Install
Just install it directly by pip.
```shell
pip install pypci-ng
```
To upgrade pypci:
```shell
pip install pypci-ng --upgrade
```

## Usage
### Use as a command line tool
You can use this tool directly from the command line with the following command, just like lspci.
```shell
pypci
```
Or use -d flag to print driver information.
```shell
pypci -d
```
For more command line flags, see:
```shell
pypci -h
```
Please note that the command line entry for __pypci__ is created by pip, and depending on the user, this entry may not in the __system PATH__. If you encounter this problem, pip will give you a prompt, follow the prompts to add entry to the __system PATH__.

### Use as a Python Package
You can also use this package in Python, here is the demo:
```python
import pypci
pci = pypci.PCI()
vga_devices = pci.FindAllVGA()
nic_devices = pci.FindAllNIC()
```
More functionalities are under development.

## Supported (Tested) OS
* Linux


## Build from source
### Build tools
Make sure the following Python build tools are already installed.
* setuptools
* build
* twine

### Build package
clone the project, and run:
```shell
python -m build
```
After the build process, the source package and the binary whl package can be found in the dist folder.
