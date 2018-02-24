# 2015.01.14 22:24:28 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class LegalInfoWindowMeta(DAAPIModule):

    def getLegalInfo(self):
        self._printOverrideError('getLegalInfo')



    def onCancelClick(self):
        self._printOverrideError('onCancelClick')



    def as_setLegalInfoS(self, legalInfo):
        if self._isDAAPIInited():
            return self.flashObject.as_setLegalInfo(legalInfo)




+++ okay decompyling legalinfowindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:28 CET
