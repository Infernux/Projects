# 2015.01.14 22:24:28 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortSettingsPeripheryPopoverMeta(DAAPIModule):

    def onApply(self, server):
        self._printOverrideError('onApply')



    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)



    def as_setTextsS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setTexts(data)




+++ okay decompyling fortsettingsperipherypopovermeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:28 CET
