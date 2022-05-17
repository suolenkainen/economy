#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

# This tests the creation of a worker object


import unittest
from unittest.mock import patch
from src import workers


class Worker_tests(unittest.TestCase):

    # Testing worker creation
    @patch('src.workers.fetch_conf_data')
    def test_create_worker(self, mock_fetch):

        ## Creating a test case that tests for different data types
        # int, float, list, dict, bool, and string
        mock_fetch.return_value = ['id=1,name=Markus,marketbuy={\'peas\': 12.0},workers=[1],sell=True']
        

        class Obj(object): pass
        obj = Obj()
        obj.id = 1
        obj.name = "Markus"
        obj.marketbuy = {'peas': 12.0}
        obj.workers = [1]
        obj.sell = True

        ret = workers.create_worker_from_configures()

        self.assertEqual(ret[0].__dict__, obj.__dict__)


    # testing worker creation with multiple lines
    @patch('src.workers.fetch_conf_data')
    def test_create_worker(self, mock_fetch):

        ## Creating a test case that tests for different data types
        # int, float, list, dict, bool, and string
        mock_fetch.return_value = ['id=0,name=Markus,marketbuy={\'peas\': 12.1},workers=[0],sell=False', \
                                    'id=1,name=Paul,marketbuy={\'peas\': 12.0},workers=[1],sell=True']
        
        class Obj(object): pass
        obj1 = Obj()
        obj1.id = 0
        obj1.name = "Markus"
        obj1.marketbuy = {'peas': 12.1}
        obj1.workers = [0]
        obj1.sell = False
        
        class Obj(object): pass
        obj2 = Obj()
        obj2.id = 1
        obj2.name = "Paul"
        obj2.marketbuy = {'peas': 12.0}
        obj2.workers = [1]
        obj2.sell = True

        ret = workers.create_worker_from_configures()

        self.assertEqual(ret[0].__dict__, obj1.__dict__)
        self.assertEqual(ret[1].__dict__, obj2.__dict__)



if __name__ == '__main__':
    unittest.main()