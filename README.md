# vmrest

Manage your hypervisor VMware Workstation from command line with minimum effort

## Prerequisites
1) Follow the instructions in documentation :
https://docs.vmware.com/en/VMware-Workstation-Pro/16.0/com.vmware.ws.using.doc/GUID-C3361DF5-A4C1-432E-850C-8F60D83E5E2B.html

## Installation
```
git clone https://github.com/CobblePot59/vmrest.git
python3 -m pip install -r requirements.txt
```

## Execution

### List VMs
```
from vmrest import *

vwconnect('http://127.0.0.1:8697', ('admin','Password1!'))

vmlist()
```

### More ? Get Help
```
from vmrest import *

help()
```
![alt vmrest_help](https://raw.githubusercontent.com/CobblePot59/vmrest/main/vmrest_help.png)
