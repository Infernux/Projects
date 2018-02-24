# 2015.01.14 22:24:30 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class PrequeueWindowMeta(DAAPIModule):

    def requestToEnqueue(self):
        self._printOverrideError('requestToEnqueue')



    def requestToLeave(self):
        self._printOverrideError('requestToLeave')



    def showFAQWindow(self):
        self._printOverrideError('showFAQWindow')



    def isEnqueueBtnEnabled(self):
        self._printOverrideError('isEnqueueBtnEnabled')



    def isLeaveBtnEnabled(self):
        self._printOverrideError('isLeaveBtnEnabled')



    def as_enableLeaveBtnS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_enableLeaveBtn(value)



    def as_enableEnqueueBtnS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_enableEnqueueBtn(value)




+++ okay decompyling prequeuewindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:30 CET
