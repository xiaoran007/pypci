# pypci-ng
pypci-ng, a pciutils-like library for fetching system PCI/PCI-E devices but written mostly in python.


![demo0](https://files.catbox.moe/mku1dg.png)


![demo1](https://files.catbox.moe/scnd3j.png)

## Install
There are already a lot of similar tools so you can choose any of them; they're all essentially no different. If you want to try this tool, just install it directly by pip.
```shell
pip install pypci-ng
```
To upgrade pypci:
```shell
pip install pypci-ng --upgrade
```
You can then use this tool directly from the command line with the following command, just like neofetch.
```shell
pypci
```
Please note that the command line entry for __pypci__ is created by pip, and depending on the user, this entry may not in the __system PATH__. If you encounter this problem, pip will give you a prompt, follow the prompts to add entry to the __system PATH__.

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
