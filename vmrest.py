import requests
from pathlib import Path

def vwconnect(param1, param2):
    global baseurl
    baseurl = param1
    global session
    session = param2

def help():
    print('''vwconnect : Connect to vmrest API Server\n\t* Required an url, ids (e.g vwconnect("http://127.0.0.1:8697", ("admin","Password1!")))')
vmlist : Returns a list of VM IDs and paths for all VMs
vmid : Returns a VM IDs for specific VMs\n\t* Required a name
vmpath : Returns a VM path for specific VMs\n\t* Required a name
vminfo : Returns the VM setting information\n\t* Required a name
vminfop : Returns more VM setting information of a VM\n\t* Required a name
vmset : Updates the VM settings\n\t* Required a name, cpu, memory
vmreg : Register VM to VM Library\n\t* Required a name, path
vmcopy : Creates a copy of the VM\n\t* Required a name, existing vm name
vmdel : Deletes a VM\n\t* Required a name
vmstate : Returns the power state of the VM\n\t* Required a name
vmstate : Changes the VM power state\n\t* Required a name
vslist : Returns all virtual networks
niclist : Returns all network adapters in the VM\n\t* Required a name
nicset : Updates a network adapter in the VM\n\t* Required a name, index
nicadd : Creates a network adapter in the VM\n\t* Required a name
nicdel : Deletes a VM network adapter\n\t* Required a name, index\n''')

def vmlist():
    url = f'{baseurl}/api/vms'
    r = requests.get(url, auth = session)
    for vm in r.json():
        vm['name'] = Path(vm['path']).stem
        print(vm)

def vmid(vmname):
    url = f'{baseurl}/api/vms'
    r = requests.get(url, auth = session)
    for vm in r.json():
        if vmname+'.vmx' in vm['path'] or vmname == vm['id']:
            return vm['id']

def vmpath(vmname):
    url = f'{baseurl}/api/vms'
    r = requests.get(url, auth = session)
    for vm in r.json():
        if vmid(vmname) == vm['id'] or vmname == vm['id']:
            return vm['path']

def vminfo(vmname):
    url = f'{baseurl}/api/vms/{vmid(vmname)}'
    r = requests.get(url, auth = session)
    print(r.json())

def vminfop(vmname):
    url = f'{baseurl}/api/vms/{vmid(vmname)}/restrictions'
    r = requests.get(url, auth = session)
    print(r.json())

def vmset(vmname, cpu, ram):
    url = f'{baseurl}/api/vms/{vmid(vmname)}'
    headers = {'Content-Type': 'application/vnd.vmware.vmw.rest-v1+json'}
    data = '{"processors": '+str(cpu)+', "memory": '+str(ram)+'}'
    r = requests.put(url, auth = session, headers = headers, data = data)
    print(r.json())

def vmreg(name, path):
    url = f'{baseurl}/api/vms/registration'
    headers = {'Content-Type': 'application/vnd.vmware.vmw.rest-v1+json'}
    data = '{"name":"'+str(name)+'", "path":"'+str(repr(path)[1:-1])+'"}'
    r = requests.post(url, auth = session, headers = headers, data = data)
    print(r.json())

def vmcopy(name, vmname):
    url = f'{baseurl}/api/vms'
    headers = {'Content-Type': 'application/vnd.vmware.vmw.rest-v1+json'}
    data = '{"name": "'+str(name)+'", "parentId": "'+str(vmid(vmname))+'"}'
    print("Virtual machine copy started..")
    r = requests.post(url, auth = session, headers = headers, data = data)
    vmreg(name, vmpath(name))

def vmdel(vmname):
    url = f'{baseurl}/api/vms/{vmid(vmname)}'
    r = requests.delete(url, auth = session)
    print(r.json())

def vmstate(vmname):
    url = f'{baseurl}/api/vms/{vmid(vmname)}/power'
    r = requests.get(url, auth = session)
    print(r.json())

def vmpower(vmname):
    url = f'{baseurl}/api/vms/{vmid(vmname)}/power'
    headers = {'Content-Type': 'application/vnd.vmware.vmw.rest-v1+json'}
    data = input('Action [on, off, shutdown, suspend, pause, unpause] : ')
    r = requests.put(url, auth = session, headers = headers, data = data)
    print(r.json())

def vslist():
    url = f'{baseurl}/api/vmnet'
    r = requests.get(url, auth = session)
    for vs in r.json()['vmnets']:
        print(vs)

def niclist(vmname):
    url = f'{baseurl}/api/vms/{vmid(vmname)}/nic'
    r = requests.get(url, auth = session)
    for nic in r.json()['nics']:
        print(nic)

def nicset(vmname, index):
    url = f'{baseurl}/api/vms/{vmid(vmname)}/nic/{index}'
    headers = {'Content-Type': 'application/vnd.vmware.vmw.rest-v1+json'}
    nictype = input('Type  [custom, bridged, nat, hostonly] : ')
    if nictype == 'custom':
        nicname = input('Name : ')
    else:
        nicname = ''
    data = '{"type" : "'+str(nictype)+'", "vmnet" : "'+str(nicname)+'"}'
    r = requests.put(url, auth = session, headers = headers, data = data)
    print(r.json())

def nicadd(vmname):
    url = f'{baseurl}/api/vms/{vmid(vmname)}/nic'
    headers = {'Content-Type': 'application/vnd.vmware.vmw.rest-v1+json'}
    nictype = input('Type  [custom, bridged, nat, hostonly] : ')
    if nictype == 'custom':
        nicname = input('Name : ')
    else:
        nicname = ''
    data = '{"type" : "'+str(nictype)+'", "vmnet" : "'+str(nicname)+'"}'
    r = requests.post(url, auth = session, headers = headers, data = data)
    print(r.json())

def nicdel(vmname, index):
    url = f'{baseurl}/api/vms/{vmid(vmname)}/nic/{index}'
    r = requests.delete(url, auth = session)
    if r.status_code == 204:
        print('Network adapter deleted')
    else:
        print(r)