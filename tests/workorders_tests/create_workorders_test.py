#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

"""
SUT: src/workorder.py

workorder.py module contains work order related functions and classes. They are the following:
- workorder_object class
- fetch_conf_data function
- attribute_list function
- create_workorder_from_configures function

workorder_object class essentially turns a list of attributes into an object, therefore not having a test.
fetch_conf_data essentially returns the content of a file, therefore not having a test.
attribute_list function is a sepatated function for testability isolate a call to another module from the name space
"""

import unittest
from unittest.mock import patch
from src import workorders


class Workorder_tests(unittest.TestCase):

    # Testing work prder creation
    @patch('src.workorders.fetch_conf_data')
    def test_create_workorder(self, mock_fetch):

        ## Creating a test case that tests for different data types
        # int, float, list, dict, bool, and string
        mock_fetch.return_value = ['id=0,destination=-1,sell=True,product=grain,method=,price=12.0,marketbuy={\'peas\': 12.1}']
        
        # Create a test object for comparison
        class Obj(object): pass
        obj = Obj()
        obj.id = 0
        obj.destination = -1
        obj.product = "grain"
        obj.sell = True
        obj.method = ""
        obj.price = 12.0
        obj.marketbuy = {'peas': 12.1}

        # Returns a list of objects
        result = workorders.create_workorders_from_configures()
        self.assertEqual(result[0].__dict__, obj.__dict__)


    # testing work order creation with multiple lines
    @patch('src.workorders.fetch_conf_data')
    def test_create_multiple_workorders(self, mock_fetch):

        ## Creating a test case that tests for different data types
        # int, float, list, dict, bool, and string
        mock_fetch.return_value = ['id=0,destination=-1,sell=True,product=grain,method=,price=12.0,goods={\'peas\': 12.1}', \
                                    'id=1,destination=0,sell=True,product=peas,method=walk,price=12.1,goods={\'peas\': 12.2}']
        
        # Create a test object for comparison
        class Obj(object): pass
        obj1 = Obj()
        obj1.id = 0
        obj1.destination = -1
        obj1.product = "grain"
        obj1.sell = True
        obj1.method = ""
        obj1.price = 12.0
        obj1.goods = {'peas': 12.1}

        class Obj(object): pass
        obj2 = Obj()
        obj2.id = 1
        obj2.destination = 0
        obj2.product = "peas"
        obj2.sell = True
        obj2.method = "walk"
        obj2.price = 12.1
        obj2.goods = {'peas': 12.2}

        # Returns a list of objects
        result = workorders.create_workorders_from_configures()
        self.assertEqual(result[0].__dict__, obj1.__dict__)
        self.assertEqual(result[1].__dict__, obj2.__dict__)



if __name__ == '__main__':
    unittest.main()