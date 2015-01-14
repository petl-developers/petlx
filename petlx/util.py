"""
Common stuff.

"""


class UnsatisfiedDependency(Exception):
    
    def __init__(self, nested, message):
        self.nested = nested
        self.message = message
        
    def __str__(self):
        return '%r\n%s' % (self.nested, self.message)