# 2015.01.14 22:24:30 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class PromoPremiumIgrWindowMeta(DAAPIModule):

    def as_setTitleS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setTitle(value)



    def as_setTextS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setText(value)



    def as_setWindowTitleS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setWindowTitle(value)



    def as_setApplyButtonLabelS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setApplyButtonLabel(value)




+++ okay decompyling promopremiumigrwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:30 CET
