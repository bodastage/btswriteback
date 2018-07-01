
from datetime import datetime


def amos(mo):
    amos_str = "{}:".format(mo.name,)
    p_values = []
    for p in mo.parameters:
        param = mo.parameters[p]
        if param.value is not None:
            p_values.append("{}={}".format(param.name, param.value))

    amos_str += ",".join(p_values) + ";"
    return amos_str


class BulkCM(object):
    """
    Bulk CM XML Script builder class
    """
    def __init__(self):
        self.attr_version = "00.00"
        self.file_format_version = '00.000 V0.0'
        self.config_dn_prefix = 'Undefined'
        self.ns_prefix = 'xn'
        self.mo_tree = None

    def set_ns_prefix(self, ns_prefix):
        self.ns_prefix = ns_prefix

    def set_attr_version(self, attr_version):
        self.attr_version = attr_version

    def set_file_format_version(self, file_format_version):
        self.file_format_version = file_format_version

    def set_config_dn_prefix(self, config_dn_prefix):
        self.config_dn_prefix = config_dn_prefix

    def header(self):
        return """<?xml version="1.0" encoding="UTF-8"?>
<bulkCmConfigDataFile xmlns:es="EricssonSpecificAttributes.{0}.xsd"
        xmlns:un="utranNrm.xsd" xmlns:xn="genericNrm.xsd"
        xmlns:gn="geranNrm.xsd" xmlns="configData.xsd">
    <fileHeader fileFormatVersion="{1}" vendorName="Ericsson"/>
    <configData dnPrefix="{2}">
            """.format(self.attr_version, self.file_format_version,
                       self.config_dn_prefix)

    def footer(self):
        date_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        return """
    </configData>
    <fileFooter dateTime="{0}"/>
</bulkCmConfigDataFile>
            """.format(date_time)

    def body(self, mo):
        """
        Bulk CM XML
        :param mo:  Managed object instance
        :return: XML string
        """
        writeback_str = ""
        vs_params = ""
        str_params = ""
        str_attr = ""
        vs_section = ""
        modifier_str = ""

        # Set modifier
        if mo.modifier is not None:
            modifier_str = ' modifier="{0}"'.format(mo.modifier)

        for p in mo.parameters:
            param = mo.parameters[p]
            if param.value is not None:

                if param.is_attr is True:
                    str_attr = " {0}=\"{1}\"".format(param.name, param.value)
                    continue

                if param.is_vendor_specific is True:
                    vs_params += '    <es:{0}>{1}</es:{0}>\n'. \
                        format(
                               param.name,
                               param.value)
                else:
                    str_params += '    <{0}:{1}>{2}</{0}:{1}>\n'. \
                        format(self.ns_prefix,
                               param.name,
                               param.value)

        # Handle children
        children_xml = ""
        if len(mo.children) > 0:
            for child in mo.children:
                children_xml += self.body(child)

        # Vendor specific section
        if vs_params != "":
            vs_section += "{0}<xn:VsDataContainer{1}{2}>\n".\
                format(" "*4, str_attr, modifier_str)
            vs_section += "{0}<xn:attributes>\n".format(" "*4)
            vs_section += "    <xn:vsDataType>vsData{0}</xn:vsDataType>\n". \
                format(mo.name)
            vs_section += "    <xn:vsDataFormatVersion>" \
                          "EricssonSpecificAttributes.{0}" \
                          "</xn:vsDataFormatVersion>\n".\
                format(self.attr_version)

            vs_section += "    <es:vsData{0}>\n".format(mo.name)
            vs_section += "        {}".format(vs_params)
            vs_section += "    </es:vsData{0}>\n".format(mo.name)
            vs_section += "    </xn:attributes>\n"
            vs_section += "    </xn:VsDataContainer>\n"

        writeback_str += '<{0}:{1}{2}{3}>\n'.format(mo.ns_prefix, mo.name,
                                                    str_attr,
                                                    modifier_str)
        writeback_str += '    <{0}:attributes>\n'.format(mo.ns_prefix)
        writeback_str += str_params
        writeback_str += '    </{0}:attributes>\n'.format(mo.ns_prefix)
        writeback_str += vs_section

        # XML from children
        writeback_str += children_xml
        writeback_str += '    </{0}:{1}>\n'.format(mo.ns_prefix, mo.name)
        return writeback_str

    def build_script(self, mo_tree):
        return self.header() + self.body(mo_tree) + self.footer()
