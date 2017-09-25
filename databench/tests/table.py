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

from pathlib import Path
import unittest
import sys
from .. data_model import Table, Schemas
from .data import *


class TableTestCase(unittest.TestCase):

    @property
    def validKey(self):
        try:
            return self._validKey
        except AttributeError:
            pass
        self._validKey = Schemas.catalogKeys()[0]
        return self._validKey


    @property
    def validPath(self):
        try:
            return self._validPath
        except AttributeError:
            pass
        self._validPath = filePath(self.validKey)
        return self._validPath

    
    @property
    def bogusPath(self):
        return 'bogus_path'

    @property
    def bogusFactoryName(self):
        return 'bogus_factory_name'

    def validTable(self, seed=0):
        '''
        '''
        return Table.withRowFactory(self.validPath, self.validKey, seed=seed)

    
    def testTableClassmethodWithRowFactoryEmptyArguments(self):

        with self.assertRaises(TypeError):
            Table.withRowFactory()

                        
    def testTableClassmethodWithRowFactoryOneArgument(self):
        
        with self.assertRaises(TypeError):
            Table.withRowFactory(self.bogusPath)


    def testTableClassmethodWithRowFactoryWithBogusFactoryName(self):

        with self.assertRaises(KeyError):
            Table.withRowFactory(self.bogusPath,self.bogusFactoryName)

        
    def testTableClassmethodWithRowFactoryWithSchemaKeys(self):
        
        for key in Schemas.catalogKeys():
            factory = Schemas.createRowFactory(key)
            path = filePath(key)
            if not path.exists():
                # XXX need to emit some kind of diagnostic here
                continue
            
            rows = [x for x in path.read_text().split('\n') if len(x)>0]
            
            t = Table.withRowFactory(str(path), key)
            self.assertIsInstance(t, Table, msg=f'{t} is not a Table')
            self.assertEqual(len(t.rows), len(rows))
            self.assertEqual(t.rowFactory.__class__.__name__,
                             factory.__class__.__name__,
                             msg=f'got {t.rowFactory} expected {factory}')

            
    def testTable__init__(self):

        
        with self.assertRaises(TypeError,
                               msg='Table() succeeded when it should not'):
            Table()

        with self.assertRaises(FileNotFoundError):
            Table(self.bogusPath).rows

        with self.assertRaises(ValueError):
            Table(self.validPath, seed='not_a_seed')


    def testTable_magic_funcs(self):

        t = Table.withRowFactory(self.validPath, self.validKey)
        self.assertIsInstance(str(t), str)
        self.assertIsInstance(iter(t), type(iter([])))

        
    def testTableRandomProperty(self,seed=11):

        q = self.validTable(seed=seed)
        s = self.validTable(seed=seed)
        t = self.validTable(seed=seed+1)

        self.assertFalse(q == s)
        self.assertFalse(q == t)
        self.assertFalse(s == t)

        q.shuffle()
        s.shuffle()
        t.shuffle()

        self.assertListEqual(q.rows, s.rows)
        
        # XXX workaround for missing assertListNotEqual
        with self.assertRaises(AssertionError):
            self.assertListEqual(q.rows, t.rows)

        self.assertListEqual(q.pick(), s.pick())

        # XXX workaround for missing assertListNotEqual
        with self.assertRaises(AssertionError):
            # XXX it is possible that q and t could pick the same
            #     sample from the same population with different seeds
            #     but relatively unlikely
            self.assertListEqual(q.pick(), t.pick())
            
    def testTable_rowsProperty(self):

        t = self.validTable()
        self.assertIsInstance(t.rows, list)

        args = ['a' for _ in range(len(t.rowFactory._fields))]

        rowType = type(t.rowFactory(*args))

        for row in t:
            self.assertIsInstance(row, rowType)


    def testTable_pickMethod(self):

        t = self.validTable()
        nRows = len(t.rows)

        results = t.pick()
        self.assertEqual(len(results), 1)

        for brokenValue in [ 0, -1, -100]:
            results = t.pick(brokenValue)
            self.assertEqual(len(results), 0,msg=f'{brokenValue} worked')

        self.assertEqual(len(t.pick(nRows)), nRows)

        with self.assertRaises(ValueError):
            t.pick(nRows+1)

    def testTable_shuffleMethod(self):

        q = self.validTable(seed=11)
        r = self.validTable(seed=22)

        self.assertNotEqual(q, r)
        self.assertListEqual(q.rows, r.rows)

        self.assertEqual(q, q.shuffle())
        with self.assertRaises(AssertionError):
            self.assertListEqual(q.rows, r.rows)

        r.shuffle()
        with self.assertRaises(AssertionError):
            self.assertListEqual(q.rows, r.rows)

            
    def testTable_unshuffleMethod(self):

        q = self.validTable()
        r = self.validTable()

        self.assertNotEqual(q, r)
        self.assertListEqual(q.rows, r.rows)

        q.shuffle()
        with self.assertRaises(AssertionError):
            self.assertListEqual(q.rows, r.rows)

        self.assertEqual(q, q.unshuffle())            
        self.assertListEqual(q.rows, r.rows)
