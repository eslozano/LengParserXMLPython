import re
class Capability:
	def __init__(self, name=None, value=None):
		self.name = name
		self.value = value

def leerCapDeString(str):
	c=re.search("<capability\s", str)
	if c:
		cap = Capability()
		m=re.search("name=\".*?\"", str)
		if m:
			m2=re.split("\"+",m.group(0))
			cap.name=m2[1]
		m=re.search("value=\".*?\"", str)
		if m:
			m2=re.split("\"+",m.group(0))
			cap.value=m2[1]
		return cap


class Group:
	def __init__(self, id=None, capabilities=None):
		self.id = id
		if capabilities is None:
			self.capabilities = []
		else:
			self.capabilities = capabilities

class Device:
	def __init__(self, id=None, user_agent=None, actual_device_root=None, fall_back=None, groups=None, fbDevice=None):
		self.id=id
		self.user_agent=user_agent
		self.actual_device_root=actual_device_root
		self.fall_back=fall_back
		self.fbDevice=fbDevice
		if groups is None:
			self.groups = []
		else:
			self.groups = groups
			
def leerDevDeString(str):
	c=re.search("<device\s", str)
	if c:
		dev = Device()
		m=re.search("id=\".*?\"", str)
		if m:
			m2=re.split("\"+",m.group(0))
			dev.id=m2[1]
		m=re.search("user_agent=\".*?\"", str)
		if m:
			m2=re.split("\"+",m.group(0))
			dev.user_agent=m2[1]
		m=re.search("actual_device_root=\".*?\"", str)
		if m:
			m2=re.split("\"+",m.group(0))
			dev.actual_device_root=m2[1]
		m=re.search("fall_back=\".*?\"", str)
		if m:
			m2=re.split("\"+",m.group(0))
			dev.fall_back=m2[1]
		return dev

def leerGroupDeString(str):
	c=re.search("<group\s", str)
	if c:
		grp = Group()
		m=re.search("id=\".*?\"", str)
		if m:
			m2=re.split("\"+",m.group(0))
			grp.id=m2[1]		
		return grp
		
def listarDevices(file):
	devlist=[]
	lst=list(file)
	i=iter(lst)
	a=next(i)
	while not re.search("<devices>", a) :
		a=next(i)
	while not re.search("</devices>", a) :
		m=re.search("<device\s", a)
		if m:
			dev=leerDevDeString(a)
			if not re.search("/>", a) :
				while not re.search("</device>", a) :
					gm=re.search("<group\s",a)
					if gm:
						tempgroup=leerGroupDeString(a)
						while not re.search("</group>",a) :
							cap=leerCapDeString(a)
							if cap:
								tempgroup.capabilities.append(cap)
							a=next(i)
						dev.groups.append(tempgroup)
					a=next(i)
			devlist.append(dev)
		a=next(i)
	
	templist=sorted(devlist, key=lambda device: device.id)
	for de in devlist:
		de.fbDevice=busqueda(templist, de.fall_back)
	return devlist

def busqueda (devices, deviceId):
    if (devices != None) and (devices != []):
        return busquedaBinaria (devices, 0, len (devices) - 1, deviceId)

def busquedaBinaria (devices, inicio, fin, deviceId):
    if (inicio == fin ):
    	if devices[inicio].id == deviceId:
    		return devices[inicio]
    	else:
    		return None
    centro = (inicio + fin) // 2 
    if (deviceId < devices [centro].id):
        return busquedaBinaria (devices, inicio, centro, deviceId) 
    elif (deviceId > devices [centro].id):
        return busquedaBinaria (devices, centro + 1, fin, deviceId) 
    else: 
    	return devices[centro]


