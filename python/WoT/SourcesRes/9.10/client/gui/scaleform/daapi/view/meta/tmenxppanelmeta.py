# 2015.01.14 22:24:32 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class TmenXpPanelMeta(DAAPIModule):

    def accelerateTmenXp(self, selected):
        self._printOverrideError('accelerateTmenXp')



    def as_setTankmenXpPanelS(self, visible, selected):
        if self._isDAAPIInited():
            return self.flashObject.as_setTankmenXpPanel(visible, selected)




+++ okay decompyling tmenxppanelmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:32 CET
