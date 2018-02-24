# 2015.01.14 22:24:27 CET
from gui.Scaleform.daapi.view.lobby.rally.BaseRallyIntroView import BaseRallyIntroView

class FortIntroMeta(BaseRallyIntroView):

    def as_setIntroDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setIntroData(data)




+++ okay decompyling fortintrometa.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:27 CET
