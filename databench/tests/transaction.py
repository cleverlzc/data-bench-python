'''
'''

import time
import unittest
import sys

from ..  data_model import Transaction, Schemas, Table
from .data import *

class TransactionTestCase(unittest.TestCase):

    @property
    def validPayload(self):
        try:
            return self._validPayload
        except AttributeError:
            pass
        key = Schemas.catalogKeys()[0]
        path = filePath(key)
        table = Table.withRowFactory(path, key)
        self._validPayload = table.rows[0]
        return self._validPayload

    @property
    def bogusContent(self):
        return 'bogus|data|foo|bar|baz'

    def testTransactionClassmethodParse(self):

        with self.assertRaises(TypeError):
            Transaction.parse()

        with self.assertRaises(NotImplementedError):
            Transaction.parse(self.bogusContent)
            
    
    def testTransaction__init__(self):

        with self.assertRaises(TypeError):
            Transaction()

        t = Transaction(self.validPayload, sep='?')
        self.assertEqual(t.payload, self.validPayload)
        self.assertEqual(t.sep, '?')

    def testTransaction_magic_funcs(self):

        t = Transaction(self.validPayload)

        self.assertIsInstance(str(t), str)
        self.assertIsInstance(repr(t), str)

    def testTransaction_uuidProperty(self):
        
        q = Transaction(self.validPayload)
        r = Transaction(self.validPayload)

        self.assertNotEqual(q, r)
        self.assertEqual(q.payload, r.payload)
        self.assertNotEqual(q.uuid, r.uuid)

    def testTransaction_timestampProperty(self):

        q = Transaction(self.validPayload)

        self.assertIsInstance(q.timestamp, int)

        # The following proves that the timestamp is sampled
        # everytime the property is accessed. 
        a = q.timestamp
        time.sleep(0.001)
        b = q.timestamp

        self.assertNotEqual(a, b)


    def testTransaction_sequenceProperty(self):

        q = Transaction(self.validPayload)
        r = Transaction(self.validPayload)

        self.assertGreater(q.sequence, 0)

        self.assertNotEqual(q, r)
        self.assertNotEqual(q.sequence, r.sequence)
        self.assertLess(q.sequence, r.sequence)
        self.assertEqual(q.sequence+1, r.sequence) # Monotonically increasing

        self.assertIsInstance(q.sequence, int)
