# 2015.01.14 22:24:27 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortModernizationWindowMeta(DAAPIModule):

    def applyAction(self):
        self._printOverrideError('applyAction')



    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)



    def as_applyButtonLblS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_applyButtonLbl(value)



    def as_cancelButtonS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_cancelButton(value)



    def as_windowTitleS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_windowTitle(value)




+++ okay decompyling fortmodernizationwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:27 CET
