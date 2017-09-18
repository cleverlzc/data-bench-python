'''
'''

from argparse import ArgumentParser
from configparser import ConfigParser

class CLIGenerator(object):
    '''
    '''

    @classmethod
    def parseArgumentsFor(cls, arguments, configFilePath=None):
        '''
        '''
        cli = cls(arguments, configFilePath)
        return cli.parser.parse_args()
    

    def __init__(self, args, configFilePath=None):
        '''
        '''
        self.configFile = configFilePath
        for k,v in args.items():
            self.parser.add_argument(k, **v)
            
        
    @property
    def config(self):
        '''
        '''
        try:
            return self._config
        except AttributeError:
            pass
        self._config = ConfigParser()
        if self.configFile:
            self._config.read(self.configFile)
        return self._config

    @property
    def parser(self):
        '''
        '''
        try:
            return self._parser
        except AttributeError:
            pass
        self._parser = ArgumentParser()
        return self._parser

    def parse_args(self):
        '''
        '''
        return self.parser.parse_args()
    
