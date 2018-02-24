# 2015.01.14 22:24:29 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class MinimapEntityMeta(DAAPIModule):

    def as_updatePointsS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_updatePoints()




+++ okay decompyling minimapentitymeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:29 CET
