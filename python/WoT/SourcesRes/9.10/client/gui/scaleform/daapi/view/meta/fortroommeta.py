# 2015.01.14 22:24:27 CET
from gui.Scaleform.daapi.view.lobby.rally.BaseRallyRoomView import BaseRallyRoomView

class FortRoomMeta(BaseRallyRoomView):

    def showChangeDivisionWindow(self):
        self._printOverrideError('showChangeDivisionWindow')



    def as_showLegionariesCountS(self, isShow, msg):
        if self._isDAAPIInited():
            return self.flashObject.as_showLegionariesCount(isShow, msg)



    def as_showLegionariesToolTipS(self, isShow):
        if self._isDAAPIInited():
            return self.flashObject.as_showLegionariesToolTip(isShow)




+++ okay decompyling fortroommeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:28 CET
