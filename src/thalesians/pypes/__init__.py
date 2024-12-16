import pkgutil
__path__ = pkgutil.extend_path(__path__, __name__)  # @ReservedAssignment

import abc
import enum
import random
import string

import thalesians.adiutor.checks as checks
from thalesians.adiutor.strings import ToStringHelper 

class Direction(enum.Enum):
    INCOMING = 1
    OUTGOING = 2

class Pype(metaclass=abc.ABCMeta):
    def __init__(self, direction, name=None):
        if name is None: name = random.choice(string.ascii_uppercase) + \
                ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
        checks.check_string(name, allow_none=False)
        checks.check(lambda: name.isalnum(), 'Pype\'s name is not alphanumeric')
        checks.check(lambda: len(name) > 0, 'Pype\'s name is an empty string')        
        self._name = name
        self._direction = direction
        self._closed = True
        self._to_string_helper_Pype = None
        self._str_Pype = None

    @abc.abstractmethod        
    def close(self):
        pass
        
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):  # @UnusedVariable @ReservedAssignment
        self.close()
    
    @abc.abstractmethod
    def send(self, obj):
        pass

    @abc.abstractclassmethod
    def receive(self, notify_of_eof=False):
        pass
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._closed: raise StopIteration
        o, eof = self.receive(notify_of_eof=True)
        if eof: raise StopIteration
        return o
        
    @property
    def name(self):
        return self._name
    
    @property
    def direction(self):
        return self._direction

    @property
    def closed(self):
        return self._closed
    
    def to_string_helper(self):
        if self._to_string_helper_Pype is None:
            self._to_string_helper_Pype = ToStringHelper(self) \
                    .add('name', self._name) \
                    .add('direction', self._direction)
        return self._to_string_helper_Pype
    
    def __str__(self):
        if self._str_Pype is None: self._str_Pype = self.to_string_helper().to_string()
        return self._str_Pype 

    def __repr__(self):
        return str(self)

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()
