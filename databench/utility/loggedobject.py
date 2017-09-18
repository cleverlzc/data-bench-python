import logging

class LoggedObject(object):
    '''
    LoggedObject provides a logger property initialized with the
    class' name. Descended objects can then log events accessing
    this property. 

    EXAMPLE

      class LoggedFoo(LoggedObject):

        def fooTheBar(self):
          self.logger.info('informative message about Foo'ing the Bar')

        def bazTheAck(self, arg):
          if not arg:
            self.logger.debug('debugging message')

    '''

    @property
    def logger(self):
        '''
        Returns a logging.Logger whose name is the class name.
        '''
        try:
            return self._logger
        except AttributeError:
            pass
        self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
