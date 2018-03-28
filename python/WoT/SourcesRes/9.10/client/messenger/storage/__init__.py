# 2015.01.14 21:23:08 CET
from messenger import error
from messenger.ext.ROPropertyMeta import ROPropertyMeta
from messenger.storage.ChannelsStorage import ChannelsStorage
from messenger.storage.PlayerCtxStorage import PlayerCtxStorage
from messenger.storage.UsersStorage import UsersStorage
_STORAGE = {'channels': ChannelsStorage(),
 'users': UsersStorage(),
 'playerCtx': PlayerCtxStorage()}
_DYN_STORAGE = {}

class storage_getter(object):

    def __init__(self, name):
        super(storage_getter, self).__init__()
        if name not in _STORAGE:
            raise error, 'Storage "{0:>s}" not found'.format(name)
        self.__name = name



    def __call__(self, *args):
        return _STORAGE[self.__name]




class dyn_storage_getter(object):

    def __init__(self, name):
        super(dyn_storage_getter, self).__init__()
        self.__name = name



    def __call__(self, *args):

        def _getStorage(_self):
            global _DYN_STORAGE
            if self.__name not in _DYN_STORAGE:
                raise error, 'Dyn storage "{0:>s}" not found'.format(self.__name)
            return _DYN_STORAGE[self.__name]


        return property(_getStorage)




def addDynStorage(name, storage):
    if name not in _DYN_STORAGE:
        _DYN_STORAGE[name] = storage
    else:
        raise error, 'Storage "{0:>s}" is exists'.format(name)



def clearDynStorage(name):
    if name in _DYN_STORAGE:
        storage = _DYN_STORAGE.pop(name, None)
        if storage:
            storage.clear()



class StorageDecorator(object):
    __metaclass__ = ROPropertyMeta
    __readonly__ = _STORAGE

    def __repr__(self):
        return 'StorageDecorator(id=0x{0:08X}, ro={1!r:s})'.format(id(self), self.__readonly__.keys())



    def clear(self):
        for storage in self.__readonly__.itervalues():
            storage.clear()





+++ okay decompyling __init__.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 21:23:08 CET
