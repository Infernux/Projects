# 2015.01.14 22:24:28 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class InputCheckerMeta(DAAPIModule):

    def sendUserInput(self, value, isValidSyntax):
        self._printOverrideError('sendUserInput')



    def as_setTitleS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setTitle(value)



    def as_setBodyS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setBody(value)



    def as_setErrorMsgS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setErrorMsg(value)



    def as_setFormattedControlNumberS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setFormattedControlNumber(value)



    def as_setOriginalControlNumberS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setOriginalControlNumber(value)



    def as_invalidUserTextS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_invalidUserText(value)




+++ okay decompyling inputcheckermeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:28 CET
