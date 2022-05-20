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


class attach_resource_to_production_tests(unittest.TestCase):


    # testing producer creation with multiple lines
    def test_attach_resource_1(self):
        print("test_attach_resource_1")
        
        class Obj: pass

        prod_obj = Obj()
        prod_obj.__dict__ = {'id': 0, 'name': 'Bridge Crossings Bakery', 'product': 'bread', 'requirements': {'peas': 1, 'grain': 2}, 'settlementid': 0, 'storedresources': {"grain": 3, 'peas': 10}, 'storedproduct': {'butter': 10}, 'cyclesprunit': 5, 'goodsgroup': 5, 'maxresources': 20, 'maxgoods': 10}

        sett_obj = Obj()
        sett_obj.__dict__ = {'id': 0, 'name': 'Bridge Crossings', 'coordx': 320, 'coordy': 100, 'population': 30, 'goods': {'bread': 20}, 'resourcegoods': {'peas': 10}, 'basewealth': 100.0, 'liquidwealth': 100.0, 'marketsell': {'bread': 25.0}, 'marketbuy': {'grain': 11.7, 'peas': 11.7}}

        # Attach resources to production places
        result = producers.attach_resource_to_production([sett_obj], [prod_obj])
        print(result)
        print()


    # testing producer creation with multiple lines
    def test_attach_resource_2(self):
        print("test_attach_resource_2")
        
        class Obj: pass

        prod_obj = Obj()
        prod_obj.__dict__ = {'id': 0, 'name': 'Bridge Crossings Bakery', 'product': 'bread', 'requirements': {}, 'settlementid': 0, 'storedresources': {"grain": 3}, 'storedproduct': {"grain": 3}, 'cyclesprunit': 5, 'goodsgroup': 5, 'maxresources': 20, 'maxgoods': 10}

        sett_obj = Obj()
        sett_obj.__dict__ = {'id': 2, 'name': 'Bridge Crossings', 'coordx': 320, 'coordy': 100, 'population': 30, 'goods': {'bread': 20}, 'resourcegoods': {'grain': 10}, 'basewealth': 100.0, 'liquidwealth': 100.0, 'marketsell': {'bread': 25.0}, 'marketbuy': {'grain': 11.7, 'peas': 11.7}}

        # Attach resources to production places
        result = producers.attach_resource_to_production([sett_obj], [prod_obj])
        print(result)
        print()


    # testing producer attachment to settlement where production site create something from nothing
    def test_attach_resource_3(self):
        print("test_attach_resource_3")
        
        class Obj: pass

        prod_obj = Obj()
        prod_obj.__dict__ = {'id': 0, 'name': 'Bridge Crossings Bakery', 'product': 'bread', 'requirements': {}, 'settlementid': 1, 'storedresources': {}, 'storedproduct': {"grain": 3}, 'cyclesprunit': 5, 'goodsgroup': 5, 'maxresources': 20, 'maxgoods': 10}

        sett_obj = Obj()
        sett_obj.__dict__ = {'id': 1, 'name': 'Bridge Crossings', 'coordx': 320, 'coordy': 100, 'population': 30, 'goods': {'bread': 20}, 'resourcegoods': {'grain': 10}, 'basewealth': 100.0, 'liquidwealth': 100.0, 'marketsell': {'bread': 25.0}, 'marketbuy': {'grain': 11.7, 'peas': 11.7}}

        # Attach resources to production places
        result = producers.attach_resource_to_production([sett_obj], [prod_obj])
        print(result)
        print()


    # testing producer creation with multiple lines
    def test_attach_resource_4(self):
        print("test_attach_resource_4")
        class Obj: pass

        prod_obj = Obj()
        prod_obj.__dict__ = {'id': 0, 'name': 'Bridge Crossings Bakery', 'product': 'bread', 'requirements': {'peas': 1, 'grain': 2}, 'settlementid': 0, 'storedresources': {"grain": 11, 'peas': 10}, 'storedproduct': {'butter': 10}, 'cyclesprunit': 5, 'goodsgroup': 5, 'maxresources': 20, 'maxgoods': 10}

        sett_obj = Obj()
        sett_obj.__dict__ = {'id': 0, 'name': 'Bridge Crossings', 'coordx': 320, 'coordy': 100, 'population': 30, 'goods': {'bread': 20}, 'resourcegoods': {'peas': 10}, 'basewealth': 100.0, 'liquidwealth': 100.0, 'marketsell': {'bread': 25.0}, 'marketbuy': {'grain': 11.7, 'peas': 11.7}}


        # Attach resources to production places
        result = producers.attach_resource_to_production([sett_obj], [prod_obj])
        print(result)
        print()



if __name__ == '__main__':
    unittest.main()