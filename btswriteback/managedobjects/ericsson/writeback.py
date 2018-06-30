
def amos(mo):
    amos_str = "{}:".format(mo.name,)
    p_values = []
    for p in mo.parameters:
        param=mo.parameters[p]
        if param.value is not None:
            p_values.append("{}={}".format(param.name,param.value))

    amos_str += ",".join(p_values) + ";"
    return amos_str


def bulkcm(mo, vendor_prefix='es'):
    amos_str = "{}:".format(mo.name)
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