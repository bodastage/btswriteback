class CMObject(object):
	
	mo = None 
	
	def __init__(managed_object):
		
		while managed_object.parent is not None:
			print("{1}".format(managed_object.name)),
			
			for p in managed_object.parameters:
				print("".format())
			
	def set_mo():
		self.mo = object
		

class Range(object):
	"""
	Validates parameter ranges 
	"""
	def __init__(self):
		self.name
		self.range
		
	def check(self,value):
		return True; # Passed check 

class Parameter(object):
	
	def __init__(self,name,value=None, range=None, is_mandatory=False, 
			is_vendor_specific=False, is_attr=False, ns_prefix=None, 
			is_multivalued=False):
		self.name = name 
		self.value = value
		self.range = range 
		self.is_mandatory = is_mandatory
		self.is_vendor_specific=is_vendor_specific
		self.is_attr=is_attr # This handles XML attributes
		self.ns_prefix=ns_prefix # for bulkcm format
		self.is_multivalued=is_multivalued
	
	def set_value(self,value):
	    
		# @TODO: Check format and range 
		self.value = value
		
	def __str__(self):
		return "Name:{}, value:{}".format(self.name, self.value)
	

class ManagedObject(object):
	
	def __init__(self,name,**kwargs):
		self.name = name
		self.parameters = {}
		self.parent = None
		self.children_types = [] # What managed_object types can be children. This is used for validation
		self.children = []
		
		for key, value in kwargs.items():
			self.parameters[key]=value
		
	def add_parameter(self, parameter):
	    if parameter.name not in self.parameters:
			self.parameters[parameter.name]=parameter
	
	def set_parameter_value(self,name,value):
		self.parameters[name].set_value(value)
		
	def set_parent(self,parent):
		self.parent = parent
		self.parent.add_child(self)
		print "Parent set"
		
	def get_parent(self):
		return self.parent
		
	def __str__(self):
		mo_str = "{}".format(self.name)
		
		for p in self.parameters:
			mo_str += "\n    {}".format(self.parameters[p].name)
			if self.parameters[p].value is not None:
				mo_str += " : " + str(self.parameters[p].value)
			
		return mo_str
		
	def add_child(self, child):
		print "child_key:" + child.name
		if child.name not in self.children_types:
			print "child not in types"
			return  
			# @TODO: Throw exception 
		self.children.append(child)

			
			
	def get_children(self):
		return self.children
		
	def get_name():
		return self.name

	

class UtranCell(ManagedObject):
	def __init__(self):
		ManagedObject.__init__(self, 'UtranCell',
			id=Parameter(name='id',is_attr=True),
			userLabel= Parameter(name='userLabel'),
			lac= Parameter(name='lac'),
			rac= Parameter(name='rac',ns_prefix='es')
		)
	
class SubNetwork(ManagedObject):
	def __init__(self):
		ManagedObject.__init__(self, 'SubNetwork',
			id=Parameter(name='id',is_attr=True),
			dnPrefix=Parameter(name='dnPrefix',is_attr=True),
		)
		
		self.children_types = ['SubNetwork']

class SubNetwork2(ManagedObject):
	def __init__(self):
		ManagedObject.__init__(self, 'SubNetwork',
			id=Parameter(name='id',is_attr=True),
			dnPrefix=Parameter(name='userDefinedNetworkType'),
			userLabel=Parameter(name='userLabel'),
		)
		
		self.children_types = ['UtranCell']
		
		
subNetwork=SubNetwork()

subNetwork2=SubNetwork2()
subNetwork2.set_parent(subNetwork)

utranCell=UtranCell()
utranCell.set_parent(subNetwork2)


utranCell.set_parameter_value('id',1)
utranCell.set_parameter_value('lac',1004)
utranCell.set_parameter_value('rac',124)


def amos(mo):
	amos_str = "{}:".format(mo.name,)
	p_values = []
	for p in mo.parameters:
		param=mo.parameters[p]
		if param.value is not None:
			p_values.append("{}={}".format(param.name,param.value))
			
	amos_str += ",".join(p_values) + ";"
	return amos_str

def bulkcm(mo,vendor_prefix='es'):
	amos_str = "{}:".format(mo.name,)
	vs_params = []
	params = ""
	for p in mo.parameters:
		param=mo.parameters[p]
		if param.value is not None:
			if param.is_vendor_specific == True:
				vs_params += '<{0}:{1}>{2}</{1}><'.format(vendor_prefix, param.name,param.value)
			else:
				params += '<{0}:{1}>{2}</{0}:{1}>'.format(vendor_prefix,param.name,param.value)
			
	amos_str += params
	return amos_str

print utranCell.get_parent().name
print utranCell

print subNetwork2


print amos(utranCell)
print bulkcm(utranCell)

print "Here\n\n"
	
print "Children"
print "----------------------"

utranCell.set_parameter_value("lac",1114)

for c in subNetwork.get_children():
	print c.name
	print [pm for pm in c.parameters]
	for p in c.get_children():
		print "    {}".format(p.name)
		#print [pm for pm in p.parameters]
		for pm in p.parameters:
			param = p.parameters[pm]
			print "{}:{}".format(param.name, param.value)
	
	
