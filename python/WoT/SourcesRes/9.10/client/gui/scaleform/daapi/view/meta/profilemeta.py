# 2015.01.14 22:24:30 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ProfileMeta(DAAPIModule):

    def onCloseProfile(self):
        self._printOverrideError('onCloseProfile')



    def as_updateS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_update(data)




+++ okay decompyling profilemeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:30 CET
