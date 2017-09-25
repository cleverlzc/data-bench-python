#
#   Copyright 2017 Intel Corporation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#    
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
            
