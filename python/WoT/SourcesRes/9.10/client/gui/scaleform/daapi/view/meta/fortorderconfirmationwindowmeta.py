# 2015.01.14 22:24:27 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortOrderConfirmationWindowMeta(DAAPIModule):

    def submit(self, count):
        self._printOverrideError('submit')



    def getTimeStr(self, time):
        self._printOverrideError('getTimeStr')



    def as_setDataS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(value)



    def as_setSettingsS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setSettings(value)




+++ okay decompyling fortorderconfirmationwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:27 CET
