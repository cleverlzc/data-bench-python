'''
'''

import unittest
import sys

from .. data_model.schemas import Schemas

class SchemasTestCase(unittest.TestCase):

    def testSchemasClassmethodCatalogKeysAreStrings(self):
        '''
        '''

        keys = Schemas.catalogKeys()
        self.assertIsInstance(keys, list,
                              msg=f'got {type(keys)} expected list ')
        
        for key in Schemas.catalogKeys():
            self.assertIsInstance(key, str, msg=f'{key} is not a string')


    def testScheamsClassmethodCreateRowFactory(self):
        '''
        '''
        for key in Schemas.catalogKeys():
            factory = Schemas.createRowFactory(key)
            self.assertIsInstance(factory, type, msg=f'{factory} is not a type')

        for key in ['fake','garbage','madeup']:
            with self.assertRaises(KeyError):
                factory = Schemas.createRowFactory(key)


    def testScheamsClassmethodRowFactoryCreation(self, testValue='a'):
        '''
        '''
        for key in Schemas.catalogKeys():
            factory = Schemas.createRowFactory(key)

            self.assertIsInstance(factory._fields, tuple,
                                  msg=f'factory {key} _fields is not a tuple')
            
            args = [testValue for _ in range(len(factory._fields))]
            
            o = factory(*args)
            
            self.assertEqual(o.__class__.__name__, key,
                             msg=f'expected {key} got {o.__class__.__name__}')
            
            for v in [getattr(o,f) for f in o._fields]:
                self.assertEqual(v, testValue,
                                 msg="expected {testValue} got {v}")

            with self.assertRaises(TypeError,
                                   msg=f'{key} accepted too few arguments'):
                o = factory(*args[1:])

            with self.assertRaises(TypeError,
                                   msg=f'{key} accepted too many arguments'):
                o = factory(*(args+args))
            
