#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

"""
SUT: src/settlements.py

settlements.py module contains settlement related functions and classes. They are the following:
- settlement_object class
- fetch_conf_data function
- attribute_list function
- create_settlement_from_configures function

settlement_object class essentially turns a list of attributes into an object, therefore not having a test.
fetch_conf_data essentially returns the content of a file, therefore not having a test.
attribute_list function is a sepatated function for testability isolate a call to another module from the name space
"""

import unittest
from unittest.mock import patch
from src import settlements


class settlement_tests(unittest.TestCase):

    # Testing settlement creation
    @patch('src.settlements.fetch_conf_data')
    def test_create_settlement(self, mock_fetch):

        ## Creating a test case that tests for different data types
        # int, float, list, dict, bool, and string
        mock_fetch.return_value = ['id=1,name=Markus,marketbuy={\'peas\': 12.0},goods=[1],sell=True']
        
        # Create a test object for comparison
        class Obj(object): pass
        obj = Obj()
        obj.id = 1
        obj.name = "Markus"
        obj.marketbuy = {'peas': 12.0}
        obj.goods = [1]
        obj.sell = True

        # Returns a list of objects
        result = settlements.create_settlements_from_configures()
        self.assertEqual(result[0].__dict__, obj.__dict__)



    # testing settlement creation with multiple lines
    @patch('src.settlements.fetch_conf_data')
    def test_create_multiple_settlement(self, mock_fetch):

        ## Creating a test case that tests for different data types
        # int, float, list, dict, bool, and string
        mock_fetch.return_value = ['id=0,name=Markus,marketbuy={\'peas\': 12.1},goods=[0],sell=False', \
                                    'id=1,name=Paul,marketbuy={\'peas\': 12.0},goods=[1],sell=True']
        
        # Create test objects for comparison
        class Obj(object): pass
        obj1 = Obj()
        obj1.id = 0
        obj1.name = "Markus"
        obj1.marketbuy = {'peas': 12.1}
        obj1.goods = [0]
        obj1.sell = False
        
        class Obj(object): pass
        obj2 = Obj()
        obj2.id = 1
        obj2.name = "Paul"
        obj2.marketbuy = {'peas': 12.0}
        obj2.goods = [1]
        obj2.sell = True

        # Returns a list of objects
        result = settlements.create_settlements_from_configures()
        self.assertEqual(result[0].__dict__, obj1.__dict__)
        self.assertEqual(result[1].__dict__, obj2.__dict__)



if __name__ == '__main__':
    unittest.main()