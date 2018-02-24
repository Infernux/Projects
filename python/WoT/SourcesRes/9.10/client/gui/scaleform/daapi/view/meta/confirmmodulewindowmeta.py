# 2015.01.14 22:24:25 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ConfirmModuleWindowMeta(DAAPIModule):

    def submit(self, count, currency):
        self._printOverrideError('submit')



    def as_setDataS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(value)



    def as_setSettingsS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setSettings(value)




+++ okay decompyling confirmmodulewindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:25 CET
