# import pytest
#
# Copyright 2017 - 2018 Bodastage Solutions
#
# Licensed under the Apache License, Version 2.0 ;
# you may not use this work except in compliance with the License.
# You may obtain a copy of the License in the LICENSE file, or at:
#
# https://www.apache.org/licenses/LICENSE-2.0

from xml.etree import ElementTree

from btswriteback.managedobjects.ericsson.umts import SubNetwork2, \
    SubNetwork, RncFunction, UtranCell
from btswriteback.managedobjects.ericsson.writeback import BulkCM


def test_utrancell():
    """
    Test UtranCell
    """

    subNetwork = SubNetwork(id='ONRM_ROOT_MO_R')

    subNetwork2 = SubNetwork2(id='BSC', userDefinedNetworkType='IPRAN',
                              userLabel='BSC')
    subNetwork.add_child(subNetwork2)

    subnetwork2_switch = SubNetwork2(id='Switch',
                                     userDefinedNetworkType='Switch',
                                     userLabel='Switch')
    subNetwork.add_child(subnetwork2_switch)

    subnetwork2_sasn = SubNetwork2(id='SASN',
                                   userDefinedNetworkType='SASN',
                                   userLabel='SASN')
    subNetwork.add_child(subnetwork2_sasn)

    rncFunction = RncFunction(userLabel='SOMERNC1',
                              mcc=635,
                              mnc=10,
                              rncId=3)
    rncFunction.modifier = 'update'
    subNetwork2.add_child(rncFunction)

    utrancell = UtranCell(id="10001C1",
                          userLabel='Cell_1',
                          rac=2000,
                          lac=1002,
                          lbUtranCellOffloadCapacity=1000)
    rncFunction.add_child(utrancell)

    print ""
    print utrancell

    is_bulkcm_xml_valid = False
    bulkcm = BulkCM()
    print bulkcm.build_script(subNetwork)

    try:
        ElementTree.fromstring(bulkcm.build_script(subNetwork))
        is_bulkcm_xml_valid = True
    except Exception, e:
        print(e)
        is_bulkcm_xml_valid = False

    assert is_bulkcm_xml_valid is True
