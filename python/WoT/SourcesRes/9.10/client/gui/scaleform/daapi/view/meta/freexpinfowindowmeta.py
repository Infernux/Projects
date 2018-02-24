# 2015.01.14 22:24:28 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FreeXPInfoWindowMeta(DAAPIModule):

    def onSubmitButton(self):
        self._printOverrideError('onSubmitButton')



    def onCancelButton(self):
        self._printOverrideError('onCancelButton')



    def as_setSubmitLabelS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setSubmitLabel(value)



    def as_setTitleS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setTitle(value)



    def as_setTextS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setText(value)




+++ okay decompyling freexpinfowindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:28 CET
