#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

"""
SUT: src/producers.py

producers.py module contains producer related functions and classes. They are the following:
- producer_object class
- fetch_conf_data function
- attribute_list function
- create_producer_from_configures function

producer_object class essentially turns a list of attributes into an object, therefore not having a test.
fetch_conf_data essentially returns the content of a file, therefore not having a test.
attribute_list function is a sepatated function for testability isolate a call to another module from the name space
"""

import unittest
from unittest.mock import patch
from src import producers


class request_production_resources(unittest.TestCase):


    ## Testing how much resources is required from settlement
    def test_attach_resource_1(self):
        
        class Obj: pass

        prod_obj = Obj()
        prod_obj.__dict__ = {'id': 0, 'name': 'Bridge Crossings Bakery', 'product': 'bread', 'requirements': {'peas': 1, 'grain': 2}, 'settlementid': 0, 'storedresources': {'peas': 4, "grain": 3}, 'storedproduct': {'butter': 10}, 'cyclesprunit': 5, 'goodsgroup': 5, 'maxresources': 20, 'maxgoods': 10}

        sett_obj = Obj()
        sett_obj.__dict__ = {'id': 0, 'goods': {'bread': 20}, 'resourcegoods': {'peas': 10}}

        # Attach resources to production places
        result = producers.request_production_resources([sett_obj], [prod_obj])

        self.assertEqual(result, [(0, 0, {'peas': 3, 'grain': 9})])


    ## Testing how much resources is required from settlement
    ## when there's two production facilities in one settlement
    def test_attach_resource_2(self):
        
        class Obj: pass

        prod_obj1 = Obj()
        prod_obj1.__dict__ = {'id': 0, 'name': 'Bridge Crossings Bakery', 'product': 'bread', 'requirements': {}, 'settlementid': 0, 'storedresources': {"grain": 3}, 'storedproduct': {"grain": 3}, 'cyclesprunit': 5, 'goodsgroup': 5, 'maxresources': 20, 'maxgoods': 10}
        
        prod_obj2 = Obj()
        prod_obj2.__dict__ = {'id': 1, 'name': 'Road Crossings Smeltery', 'product': 'iron ingots', 'requirements': {"iron ore": 5, "coal": 10}, 'settlementid': 0, 'storedresources': {"coal": 10}, 'storedproduct': {}, 'cyclesprunit': 20, 'goodsgroup': 1, 'maxresources': 120, 'maxgoods': 10}

        sett_obj = Obj()
        sett_obj.__dict__ = {'id': 0, 'population': 30, 'goods': {'bread': 20}, 'resourcegoods': {'grain': 10}}

        # Test that 
        result = producers.request_production_resources([sett_obj], [prod_obj1, prod_obj2])

        self.assertEqual(result, [(1, 0, {'iron ore': 40, 'coal': 70})])


    ## Testing how much resources is required from settlement
    ## When settlement
    def test_attach_resource_3(self):
        
        class Obj: pass

        prod_obj1 = Obj()
        prod_obj1.__dict__ = {'id': 0, 'name': 'Bridge Crossings Bakery', 'product': 'bread', 'requirements': {"peas": 5}, 'settlementid': 0, 'storedresources': {"peas": 5}, 'storedproduct': {"grain": 3}, 'cyclesprunit': 5, 'goodsgroup': 5, 'maxresources': 40, 'maxgoods': 10}
        
        prod_obj2 = Obj()
        prod_obj2.__dict__ = {'id': 1, 'name': ' Smeltery', 'product': 'iron ingots', 'requirements': {"iron ore": 5, "coal": 10}, 'settlementid': 1, 'storedresources': {"coal": 10}, 'storedproduct': {}, 'cyclesprunit': 20, 'goodsgroup': 1, 'maxresources': 120, 'maxgoods': 10}

        sett_obj1 = Obj()
        sett_obj1.__dict__ = {'id': 0, 'population': 30, 'goods': {'bread': 20}, 'resourcegoods': {'grain': 10}}
        
        sett_obj2 = Obj()
        sett_obj2.__dict__ = {'id': 1, 'population': 30, 'goods': {'bread': 20}, 'resourcegoods': {'grain': 10}}

        # Test that 
        result = producers.request_production_resources([sett_obj1, sett_obj2], [prod_obj1, prod_obj2])

        self.assertEqual(result, [(0, 0, {'peas': 35}), (1, 1, {'iron ore': 40, 'coal': 70})])


if __name__ == '__main__':
    unittest.main()