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
            
        obj3 = Obj()
        for key, value in attr_dict1.items():
            setattr(obj3, key, value)
        obj3.destination = obj2.owner

        # Mock return values for other functions
        mock_sales.return_value = True
        obj3.destination = obj2.owner
        mock_orders.return_value = obj3, [], []

        # Returns a list of of combined work orders and resulting bying orders
        ord_objects = [obj1, obj2]
        result_orders, result_unfinished = workorders.combine_workorders(ord_objects)
        self.assertEqual(result_orders, [obj3])
        self.assertEqual(result_unfinished, [])


    # This tests simple sales calculator
    def test_sales_calculator(self):

        # Equal sums
        sale = workorders.sales_calculator(10, 10)
        self.assertEqual(sale, True)

        # Large gap
        sale = workorders.sales_calculator(100, 10)
        self.assertEqual(sale, False)
        
        # 2% larger asking
        sale = workorders.sales_calculator(104, 100)
        self.assertEqual(sale, True)


    # This tests match orders
    def test_match_orders(self):

        # Create a test object for comparison
        attr_dict1 = {'owner': 2, 'destination': -1, 'amount': 5}
        attr_dict2 = {"owner": 1, "destination": -1, "amount": 5}
        attr_dict3 = {'owner': 2, 'destination': 1, 'amount': 5}
        attr_dict4 = {'owner': 2, 'destination': -1, 'amount': 1}
        
        class Obj(object): pass
        seller = Obj()
        for key, value in attr_dict1.items():
            setattr(seller, key, value)

        buyer = Obj()
        for key, value in attr_dict2.items():
            setattr(buyer, key, value)

        new_seller = Obj()
        for key, value in attr_dict3.items():
            setattr(new_seller, key, value)

        new_order = Obj()
        for key, value in attr_dict4.items():
            setattr(new_order, key, value)

        # If workorders match each other, the seller order is updated and buy-order is removed
        complete_order, newsale, newbuy = workorders.match_orders(seller, buyer)
        self.assertEqual(complete_order.__dict__, new_seller.__dict__)
        self.assertEqual(newsale, [])
        self.assertEqual(newbuy, [])

        # If seller has more than buyer is willing to buy, a new order will be created for the surplus
        seller.amount = 6
        seller.destination = -1
        complete_order, newsale, newbuy = workorders.match_orders(seller, buyer)
        self.assertEqual(complete_order.__dict__, new_seller.__dict__)
        self.assertEqual(newsale[0].__dict__, new_order.__dict__)
        self.assertEqual(newbuy, [])

        # If buyer wants to buy more than seller has to sell, a new order will be created for the lacking amount
        buyer.amount = 6
        seller.destination = -1
        new_order.owner = 1
        complete_order, newsale, newbuy = workorders.match_orders(seller, buyer)
        self.assertEqual(complete_order.__dict__, new_seller.__dict__)
        self.assertEqual(newsale, [])
        self.assertEqual(newbuy[0].__dict__, new_order.__dict__)


if __name__ == '__main__':
    unittest.main()