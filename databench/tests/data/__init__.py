
from pathlib import Path

def filePath(filename):
    '''
    '''
    return Path(__file__).parent.joinpath(f'{filename}.txt')
    
    
