# 2015.01.14 22:24:28 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortTransportConfirmationWindowMeta(DAAPIModule):

    def onCancel(self):
        self._printOverrideError('onCancel')



    def onTransporting(self, size):
        self._printOverrideError('onTransporting')



    def onTransportingLimit(self):
        self._printOverrideError('onTransportingLimit')



    def as_setMaxTransportingSizeS(self, maxSizeStr):
        if self._isDAAPIInited():
            return self.flashObject.as_setMaxTransportingSize(maxSizeStr)



    def as_setFooterTextS(self, text):
        if self._isDAAPIInited():
            return self.flashObject.as_setFooterText(text)



    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)



    def as_enableForFirstTransportingS(self, isFirstTransporting):
        if self._isDAAPIInited():
            return self.flashObject.as_enableForFirstTransporting(isFirstTransporting)




+++ okay decompyling forttransportconfirmationwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:28 CET
