# 2015.01.14 13:32:40 CET
import sys
import cPickle
import StringIO

class SafeUnpickler(object):
    PICKLE_SAFE = {'__builtin__': set(['object',
                     'set',
                     'frozenset',
                     'list',
                     'tuple']),
     'datetime': set(['datetime']),
     '_BWp': set(['Array', 'FixedDict'])}

    @classmethod
    def find_class(cls, module, name):
        if module not in cls.PICKLE_SAFE:
            raise cPickle.UnpicklingError('Attempting to unpickle unsafe module %s' % module)
        __import__(module)
        mod = sys.modules[module]
        classesSet = cls.PICKLE_SAFE[module]
        if name not in classesSet or classesSet is None:
            raise cPickle.UnpicklingError('Attempting to unpickle unsafe class %s' % name)
        klass = getattr(mod, name)
        return klass



    @classmethod
    def loads(cls, pickle_string):
        pickle_obj = cPickle.Unpickler(StringIO.StringIO(pickle_string))
        pickle_obj.find_global = cls.find_class
        return pickle_obj.load()




+++ okay decompyling safeunpickler.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:32:40 CET
