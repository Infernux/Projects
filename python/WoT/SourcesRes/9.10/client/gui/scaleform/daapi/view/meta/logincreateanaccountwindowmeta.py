# 2015.01.14 22:24:29 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class LoginCreateAnAccountWindowMeta(DAAPIModule):

    def onRegister(self, nickname):
        self._printOverrideError('onRegister')



    def as_updateTextsS(self, defValue, titleText, messageText, submitText):
        if self._isDAAPIInited():
            return self.flashObject.as_updateTexts(defValue, titleText, messageText, submitText)



    def as_registerResponseS(self, success, message):
        if self._isDAAPIInited():
            return self.flashObject.as_registerResponse(success, message)




+++ okay decompyling logincreateanaccountwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:29 CET
