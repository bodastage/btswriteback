#
from btswriteback.cm_object import ManagedObject, Parameter, BulkCMExtras


class SubNetwork(ManagedObject, BulkCMExtras):
    """
    SubNetwork
    """
    def __init__(self, **kwargs):
        ManagedObject.__init__(self, 'SubNetwork',
                               id=Parameter(name='id', is_attr=True),
                               )

        BulkCMExtras.__init__(self)

        # Set the values
        for k, v in kwargs.items():
            self.set_parameter_value(k, v)

        self.children_types = ['SubNetwork']
        self.ns_prefix = 'xn'


class SubNetwork2(ManagedObject, BulkCMExtras):
    def __init__(self, **kwargs):
        ManagedObject.__init__(self, 'SubNetwork',
                               id=Parameter(name='id', is_attr=True),
                               userDefinedNetworkType=Parameter(
                                   name='userDefinedNetworkType'),
                               userLabel=Parameter(name='userLabel'),
                               )

        BulkCMExtras.__init__(self)

        # Set the values
        for k, v in kwargs.items():
            self.set_parameter_value(k, v)

        self.children_types = ['RncFunction']
        self.ns_prefix = 'xn'


class RncFunction(ManagedObject, BulkCMExtras):
    """
    RncFunction
    """
    def __init__(self, **kwargs):
        ManagedObject.__init__(self, 'RncFunction',
                               id=Parameter(name='id', is_attr=True),
                               userLabel=Parameter(name='userLabel',
                                                   ns_prefix='un'),
                               mcc=Parameter(name='mcc', ns_prefix='un'),
                               mnc=Parameter(name='mnc', ns_prefix='un'),
                               rncId=Parameter(name='rncId', ns_prefix='un')
                               )

        # Set the values
        for k, v in kwargs.items():
            self.set_parameter_value(k, v)

        self.children_types = ['UtranCell']
        self.ns_prefix = 'un'


class UtranCell(ManagedObject, BulkCMExtras):
    def __init__(self, **kwargs):
        ManagedObject.__init__(self, 'UtranCell',
                               id=Parameter(name='id', is_attr=True),
                               localCellId=Parameter(name='localCellId'),
                               userLabel=Parameter(name='userLabel',
                                                   ns_prefix='un'),
                               lac=Parameter(name='lac', ns_prefix='un'),
                               rac=Parameter(name='rac', ns_prefix='un'),

                               # Vendor specific
                               lbUtranCellOffloadCapacity=Parameter(
                                   name='lbUtranCellOffloadCapacity',
                                   ns_prefix='es',
                                   is_vendor_specific=True)
                               )

        BulkCMExtras.__init__(self)

        # Set the values
        for k, v in kwargs.items():
            self.set_parameter_value(k, v)

        self.ns_prefix = 'un'
