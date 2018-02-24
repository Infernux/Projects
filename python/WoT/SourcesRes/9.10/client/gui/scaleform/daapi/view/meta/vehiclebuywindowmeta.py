# 2015.01.14 22:24:32 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class VehicleBuyWindowMeta(DAAPIModule):

    def submit(self, data):
        self._printOverrideError('submit')



    def storeSettings(self, expanded):
        self._printOverrideError('storeSettings')



    def as_setGoldS(self, gold):
        if self._isDAAPIInited():
            return self.flashObject.as_setGold(gold)



    def as_setCreditsS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setCredits(value)



    def as_setInitDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)



    def as_setEnabledSubmitBtnS(self, enabled):
        if self._isDAAPIInited():
            return self.flashObject.as_setEnabledSubmitBtn(enabled)




+++ okay decompyling vehiclebuywindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:32 CET
