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
- sales_calculator
- match_orders
- combine_workorders

workorder_object class essentially turns a list of attributes into an object, therefore not having a test.
fetch_conf_data essentially returns the content of a file, therefore not having a test.
attribute_list function is a sepatated function for testability isolate a call to another module from the name space
"""

import unittest
from unittest.mock import patch
from src import workorders


class Workorder_tests(unittest.TestCase):


    # Testing for combining workorders, but there is only one order to be combined
    @patch('src.workorders.match_orders')
    @patch('src.workorders.sales_calculator')
    def test_combine_single_workorder(self, mock_sales, mock_orders):

        # Create a test object for comparison
        attr_dict = {'id': 0, 'owner': 2, 'destination': -1, 'sell': True, 'product': 'grain', 'method': '', 'worker': -1, 'reserved': -1, 'price': 12.0, 'amount': 5, 'capacityperitem': 1, 'distance': 0, 'angle': -1, 'processed': 'free'}
        
        class Obj(object): pass
        obj1 = Obj()
        for key, value in attr_dict.items():
            setattr(obj1, key, value)

        # Mock return values for other functions
        mock_sales.return_value = False
        mock_orders.return_value = obj1, [], []

        # Returns a list of of combined work orders and resulting bying orders
        ord_objects = [obj1]
        result_orders, result_unfinished = workorders.combine_workorders(ord_objects)
        self.assertEqual(result_orders, [])
        self.assertEqual(result_unfinished, [obj1])


    # Testing for combining workorders, sales and buy, where there is no sale
    @patch('src.workorders.match_orders')
    @patch('src.workorders.sales_calculator')
    def test_combine_2_workorders(self, mock_sales, mock_orders):

        # Create a test object for comparison
        attr_dict1 = {'id': 0, 'owner': 2, 'destination': -1, 'sell': True, 'product': 'grain', 'method': '', 'worker': -1, 'reserved': -1, 'price': 12.0, 'amount': 5, 'capacityperitem': 1, 'distance': 0, 'angle': -1, 'processed': 'free'}
        attr_dict2 = {"id": 1,"owner": 1,"destination": -1,"sell": False,"product": "grain","method": "","worker": -1,"reserved": -1,"price": 11.5,"amount": 5,"capacityperitem": 1,"distance": 0,"angle": -1,"processed": "free"}
        
        class Obj(object): pass
        obj1 = Obj()
        for key, value in attr_dict1.items():
            setattr(obj1, key, value)

        obj2 = Obj()
        for key, value in attr_dict2.items():
            setattr(obj2, key, value)
        # Mock return values for other functions
        mock_sales.return_value = False
        mock_orders.return_value = obj1, [], []

        # Returns a list of of combined work orders and resulting bying orders
        ord_objects = [obj1, obj2]
        result_orders, result_unfinished = workorders.combine_workorders(ord_objects)
        self.assertEqual(result_orders, [])
        self.assertEqual(result_unfinished, [obj2,obj1])


    # Testing for combining workorders, sales and buy with successful purchase
    # Testing hasn't been patched due to it being a complex case that requires functions that return varying values
    def test_combine_4_workorders(self):

        # Create a test object for comparison
        attr_dict1 = {'id': 0, 'owner': 2, 'destination': -1, 'sell': True, 'product': 'grain', 'method': '', 'worker': -1, 'reserved': -1, 'price': 12.0, 'amount': 5, 'capacityperitem': 1, 'distance': 0, 'angle': -1, 'processed': 'free'}
        attr_dict2 = {"id": 1,"owner": 1,"destination": -1,"sell": False,"product": "grain","method": "","worker": -1,"reserved": -1,"price": 11.5,"amount": 5,"capacityperitem": 1,"distance": 0,"angle": -1,"processed": "free"}
        attr_dict3 = {'id': 2, 'owner': 2, 'destination': -1, 'sell': True, 'product': 'peas', 'method': '', 'worker': -1, 'reserved': -1, 'price': 12.0, 'amount': 5, 'capacityperitem': 1, 'distance': 0, 'angle': -1, 'processed': 'free'}
        attr_dict4 = {"id": 3,"owner": 1,"destination": -1,"sell": False,"product": "peas","method": "","worker": -1,"reserved": -1,"price": 11.5,"amount": 5,"capacityperitem": 1,"distance": 0,"angle": -1,"processed": "free"}
        
        class Obj(object): pass
        obj1 = Obj()
        for key, value in attr_dict1.items():
            setattr(obj1, key, value)

        obj2 = Obj()
        for key, value in attr_dict2.items():
            setattr(obj2, key, value)
        
        obj3 = Obj()
        for key, value in attr_dict3.items():
            setattr(obj3, key, value)

        obj4 = Obj()
        for key, value in attr_dict4.items():
            setattr(obj4, key, value)

        obj_r1 = Obj()
        for key, value in attr_dict1.items():
            setattr(obj_r1, key, value)
        obj_r1.destination = obj2.owner
        obj_r1.id = obj_r1.id + 100

        obj_r2 = Obj()
        for key, value in attr_dict3.items():
            setattr(obj_r2, key, value)
        obj_r2.destination = obj4.owner
        obj_r2.id = obj3.id + 100

        # Returns a list of of combined work orders and resulting bying orders
        ord_objects = [obj1, obj2, obj3, obj4]
        result_orders, result_unfinished = workorders.combine_workorders(ord_objects)
        self.assertEqual(result_orders[0].__dict__, obj_r1.__dict__,)
        self.assertEqual(result_orders[1].__dict__, obj_r2.__dict__)
        self.assertEqual(result_unfinished, [])


    # Testing for combining workorders, sales and buy with successful purchase
    # Testing hasn't been patched due to it being a complex case that requires functions that return varying values
    def test_combine_4_workorders_with_1_left_out(self):

        # Create a test object for comparison
        attr_dict1 = {'id': 0, 'owner': 2, 'destination': -1, 'sell': True, 'product': 'grain', 'method': '', 'worker': -1, 'reserved': -1, 'price': 12.0, 'amount': 5, 'capacityperitem': 1, 'distance': 0, 'angle': -1, 'processed': 'free'}
        attr_dict2 = {"id": 1,"owner": 1,"destination": -1,"sell": False,"product": "grain","method": "","worker": -1,"reserved": -1,"price": 11.5,"amount": 5,"capacityperitem": 1,"distance": 0,"angle": -1,"processed": "free"}
        attr_dict3 = {'id': 2, 'owner': 2, 'destination': -1, 'sell': True, 'product': 'peas', 'method': '', 'worker': -1, 'reserved': -1, 'price': 12.0, 'amount': 5, 'capacityperitem': 1, 'distance': 0, 'angle': -1, 'processed': 'free'}
        attr_dict4 = {"id": 3,"owner": 1,"destination": -1,"sell": False,"product": "peas","method": "","worker": -1,"reserved": -1,"price": 11.5,"amount": 5,"capacityperitem": 1,"distance": 0,"angle": -1,"processed": "free"}
        attr_dict5 = {"id": 4,"owner": 2,"destination": -1,"sell": False,"product": "bread","method": "","worker": -1,"reserved": -1,"price": 10.5,"amount": 5,"capacityperitem": 1,"distance": 0,"angle": -1,"processed": "free"}
       
        class Obj(object): pass
        obj1 = Obj()
        for key, value in attr_dict1.items():
            setattr(obj1, key, value)

        obj2 = Obj()
        for key, value in attr_dict2.items():
            setattr(obj2, key, value)
        
        obj3 = Obj()
        for key, value in attr_dict3.items():
            setattr(obj3, key, value)

        obj4 = Obj()
        for key, value in attr_dict4.items():
            setattr(obj4, key, value)

        obj5 = Obj()
        for key, value in attr_dict5.items():
            setattr(obj5, key, value)

        obj_r1 = Obj()
        for key, value in attr_dict1.items():
            setattr(obj_r1, key, value)
        obj_r1.destination = obj2.owner
        obj_r1.id = obj_r1.id + 100

        obj_r2 = Obj()
        for key, value in attr_dict3.items():
            setattr(obj_r2, key, value)
        obj_r2.destination = obj4.owner
        obj_r2.id = obj_r2.id + 100

        # Returns a list of of combined work orders and resulting bying orders
        ord_objects = [obj1, obj2, obj3, obj4, obj5]
        result_orders, result_unfinished = workorders.combine_workorders(ord_objects)
        self.assertEqual(result_orders[0].__dict__, obj_r1.__dict__,)
        self.assertEqual(result_orders[1].__dict__, obj_r2.__dict__)
        self.assertEqual(result_unfinished[0].__dict__, obj5.__dict__)


    # Testing for combining workorders, sales and buy with successful purchase
    # Testing hasn't been patched due to it being a complex case that requires functions that return varying values
    def test_combine_4_workorders_with_1_left_out_and_some_is_left_over(self):

        # Create a test object for comparison
        attr_dict1 = {'id': 0, 'owner': 2, 'destination': -1, 'sell': True, 'product': 'grain', 'price': 12.0, 'amount': 7, 'capacityperitem': 1, 'distance': 0, 'angle': -1, 'processed': 'free'}
        attr_dict2 = {"id": 1,"owner": 1,"destination": -1,"sell": False,"product": "grain", "price": 11.5,"amount": 5,"capacityperitem": 1,"distance": 0,"angle": -1,"processed": "free"}
        attr_dict3 = {'id': 2, 'owner': 2, 'destination': -1, 'sell': True, 'product': 'peas', 'price': 12.0, 'amount': 5, 'capacityperitem': 1, 'distance': 0, 'angle': -1, 'processed': 'free'}
        attr_dict4 = {"id": 3,"owner": 1,"destination": -1,"sell": False,"product": "peas", "price": 11.5,"amount": 5,"capacityperitem": 1,"distance": 0,"angle": -1,"processed": "free"}
        attr_dict5 = {"id": 4,"owner": 2,"destination": -1,"sell": False,"product": "bread","price": 10.5,"amount": 5,"capacityperitem": 1,"distance": 0,"angle": -1,"processed": "free"}
       
        class Obj(object): pass
        obj1 = Obj()
        for key, value in attr_dict1.items():
            setattr(obj1, key, value)

        obj2 = Obj()
        for key, value in attr_dict2.items():
            setattr(obj2, key, value)
        
        obj3 = Obj()
        for key, value in attr_dict3.items():
            setattr(obj3, key, value)

        obj4 = Obj()
        for key, value in attr_dict4.items():
            setattr(obj4, key, value)

        obj5 = Obj()
        for key, value in attr_dict5.items():
            setattr(obj5, key, value)

        obj_r1 = Obj()
        for key, value in attr_dict1.items():
            setattr(obj_r1, key, value)
        obj_r1.destination = obj2.owner
        obj_r1.amount = 5

        obj_r2 = Obj()
        for key, value in attr_dict3.items():
            setattr(obj_r2, key, value)
        obj_r2.destination = obj4.owner
        obj_r2.id = obj_r2.id + 100

        obj_r3 = Obj()
        for key, value in attr_dict1.items():
            setattr(obj_r3, key, value)
        obj_r3.amount = 2
        obj_r3.id = obj_r3.id + 100

        # Returns a list of of combined work orders and resulting bying orders
        ord_objects = [obj1, obj2, obj3, obj4, obj5]
        result_orders, result_unfinished = workorders.combine_workorders(ord_objects)
        self.assertEqual(result_orders[0].__dict__, obj_r1.__dict__,)
        self.assertEqual(result_orders[1].__dict__, obj_r2.__dict__)
        self.assertEqual(result_unfinished[0].__dict__, obj5.__dict__)
        self.assertEqual(result_unfinished[1].__dict__, obj_r3.__dict__)


    # Testing for combining workorders, sales and buy with successful purchase
    # Testing hasn't been patched due to it being a complex case that requires functions that return varying values
    def test_combine_4_workorders_with_1_left_out_with_left_over_sold(self):

        # Create a test object for comparison
        attr_dict1 = {'id': 0, 'owner': 2, 'destination': -1, 'sell': True, 'product': 'grain', 'price': 12.0, 'amount': 7, 'capacityperitem': 1, 'distance': 0, 'angle': -1, 'processed': 'free'}
        attr_dict2 = {"id": 1,"owner": 1,"destination": -1,"sell": False,"product": "grain", "price": 11.5,"amount": 5,"capacityperitem": 1,"distance": 0,"angle": -1,"processed": "free"}
        attr_dict3 = {'id': 2, 'owner': 2, 'destination': -1, 'sell': True, 'product': 'peas', 'price': 12.0, 'amount': 5, 'capacityperitem': 1, 'distance': 0, 'angle': -1, 'processed': 'free'}
        attr_dict4 = {"id": 3,"owner": 1,"destination": -1,"sell": False,"product": "peas", "price": 11.5,"amount": 5,"capacityperitem": 1,"distance": 0,"angle": -1,"processed": "free"}
        attr_dict5 = {"id": 4,"owner": 2,"destination": -1,"sell": False,"product": "bread","price": 10.5,"amount": 5,"capacityperitem": 1,"distance": 0,"angle": -1,"processed": "free"}
        attr_dict6 = {"id": 5,"owner": 3,"destination": -1,"sell": False,"product": "grain","price": 12.0,"amount": 3,"capacityperitem": 1,"distance": 0,"angle": -1,"processed": "free"}
       
        class Obj(object): pass
        obj1 = Obj()
        for key, value in attr_dict1.items():
            setattr(obj1, key, value)

        obj2 = Obj()
        for key, value in attr_dict2.items():
            setattr(obj2, key, value)
        
        obj3 = Obj()
        for key, value in attr_dict3.items():
            setattr(obj3, key, value)

        obj4 = Obj()
        for key, value in attr_dict4.items():
            setattr(obj4, key, value)

        obj5 = Obj()
        for key, value in attr_dict5.items():
            setattr(obj5, key, value)

        obj6 = Obj()
        for key, value in attr_dict6.items():
            setattr(obj6, key, value)

        obj_r1 = Obj()
        for key, value in attr_dict1.items():
            setattr(obj_r1, key, value)
        obj_r1.destination = obj2.owner
        obj_r1.amount = 5

        obj_r2 = Obj()
        for key, value in attr_dict3.items():
            setattr(obj_r2, key, value)
        obj_r2.destination = obj4.owner
        obj_r2.id += 100

        obj_r3 = Obj()
        for key, value in attr_dict6.items():
            setattr(obj_r3, key, value)
        obj_r3.amount = 1
        obj_r3.id += 100

        obj_r4 = Obj()
        for key, value in attr_dict1.items():
            setattr(obj_r4, key, value)
        obj_r4.amount = 2
        obj_r4.destination = obj6.owner
        obj_r4.id += 100

        # Returns a list of of combined work orders and resulting bying orders
        ord_objects = [obj1, obj2, obj3, obj4, obj5, obj6]
        result_orders, result_unfinished = workorders.combine_workorders(ord_objects)
        self.assertEqual(result_orders[0].__dict__, obj_r1.__dict__,)
        self.assertEqual(result_orders[1].__dict__, obj_r2.__dict__)
        self.assertEqual(result_orders[2].__dict__, obj_r4.__dict__)
        self.assertEqual(result_unfinished[0].__dict__, obj5.__dict__)
        self.assertEqual(result_unfinished[1].__dict__, obj_r3.__dict__)


if __name__ == '__main__':
    unittest.main()