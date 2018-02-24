# 2015.01.14 22:24:27 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortificationsViewMeta(DAAPIModule):

    def onFortCreateClick(self):
        self._printOverrideError('onFortCreateClick')



    def onDirectionCreateClick(self):
        self._printOverrideError('onDirectionCreateClick')



    def onEscapePress(self):
        self._printOverrideError('onEscapePress')



    def as_loadViewS(self, flashAlias, pyAlias):
        if self._isDAAPIInited():
            return self.flashObject.as_loadView(flashAlias, pyAlias)



    def as_setCommonDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setCommonData(data)



    def as_waitingDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_waitingData(data)




+++ okay decompyling fortificationsviewmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:27 CET
