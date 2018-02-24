# 2015.01.18 11:53:47 CET
from messenger.proto.interfaces import IProtoSettings

class BWServerSettings(IProtoSettings):
    __slots__ = ('_isEnabled',)

    def __init__(self):
        super(BWServerSettings, self).__init__()
        self._isEnabled = False



    def update(self, data):
        if 'isChat2Enabled' in data:
            self._isEnabled = data['isChat2Enabled']
        else:
            self._isEnabled = False



    def isEnabled(self):
        return self._isEnabled




+++ okay decompyling bwserversettings.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.18 11:53:47 CET
