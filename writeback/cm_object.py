class CMObject(object):

    def __init__(self, mo):
        self.mo = mo

        while mo.parent is not None:
            print("{1}".format(mo.name)),

            for p in mo.parameters:
                print("".format())

    def set_mo(self):
        self.mo = object


class Range(object):
    """
    Validates parameter ranges
    """
    def __init__(self):
        self.name
        self.range

    def check(self, value):
        return True


class Parameter(object):

    def __init__(self, name, value=None, range=None, is_mandatory=False,
                 is_vendor_specific=False, is_attr=False, ns_prefix=None,
                 is_multivalued=False):
        self.name = name
        self.value = value
        self.range = range
        self.is_mandatory = is_mandatory
        self.is_vendor_specific = is_vendor_specific

        # This handles XML attributes
        self.is_attr = is_attr

        # for bulkcm format
        self.ns_prefix = ns_prefix
        self.is_multivalued = is_multivalued

    def set_value(self, value):

        # @TODO: Check format and range
        self.value = value

    def __str__(self):
        return "Name:{}, value:{}".format(self.name, self.value)


class ManagedObject(object):

    def __init__(self, name, **kwargs):
        self.name = name
        self.parameters = {}
        self.parent = None

        # What managed_object types can be children. This is used for
        # validation
        self.children_types = []
        self.children = []

        for key, value in kwargs.items():
            self.parameters[key] = value

    def add_parameter(self, parameter):
        if parameter.name not in self.parameters:
            self.parameters[parameter.name] = parameter

    def set_parameter_value(self, name, value):
        self.parameters[name].set_value(value)

    def set_parent(self, parent):
        self.parent = parent
        self.parent.add_child(self)

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

            # @TODO: Throw exception
            return

        self.children.append(child)

    def get_children(self):
        return self.children

    def get_name(self):
        return self.name
