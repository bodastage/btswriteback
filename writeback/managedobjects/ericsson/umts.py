#

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

class UtranCell(ManagedObject):
	def __init__(self):
		ManagedObject.__init__(self, 'UtranCell',
			id=Parameter(name='id',is_attr=True),
			userLabel= Parameter(name='userLabel'),
			lac= Parameter(name='lac'),
			rac= Parameter(name='rac',ns_prefix='es')
		)
	
