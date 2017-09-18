'''
'''

from uuid import uuid4
from datetime import datetime
from .schemas import Schemas


class Transaction(object):
    '''
    '''
    _sequence = 0

    @classmethod
    def parse(self, content, sep='|'):
        '''
        '''
        raise NotImplementedError()
        
    
    def __init__(self, payload, sep='|'):
        '''
        payload - instance of a class created from namedtuple
        sep     - optional string value 

        '''
        self.payload = payload
        self.sep = sep


    def __repr__(self):
        '''
        '''
        payload_class = self.payload.__class__.__name__
        return '{}(payload={}, sep={!r})'.format(self.__class__.__name__,
                                                 payload_class,
                                                 self.sep)

    def __str__(self):
        '''
        '''
        fields = [self.payload.__class__.__name__,
                  str(self.uuid),
                  str(self.timestamp),
                  str(self.sequence)]
        for field in self.payload._fields:
            fields.append(str(getattr(self.payload, field)))
        return self.sep.join(fields)


    @property
    def uuid(self):
        '''
        Returns a uuid.uuid4().
        '''
        try:
            return self._uuid
        except AttributeError:
            pass
        self._uuid = uuid4()
        return self._uuid

    @property
    def timestamp(self):
        '''
        Millisecond epoch timestamp.
        '''
        return int(datetime.now().timestamp() * 1000)

    
    @property
    def sequence(self):
        '''
        An integer assigned to each Transaction instance which
        is monotonic and increasing.
        '''
        Transaction._sequence += 1
        return Transaction._sequence




