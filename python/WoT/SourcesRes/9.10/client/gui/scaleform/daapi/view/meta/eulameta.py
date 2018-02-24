# 2015.01.14 22:24:26 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class EULAMeta(DAAPIModule):

    def requestEULAText(self):
        self._printOverrideError('requestEULAText')



    def onLinkClick(self, url):
        self._printOverrideError('onLinkClick')



    def onApply(self):
        self._printOverrideError('onApply')



    def as_setEULATextS(self, text):
        if self._isDAAPIInited():
            return self.flashObject.as_setEULAText(text)




+++ okay decompyling eulameta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:26 CET
