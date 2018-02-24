# 2015.01.14 22:24:25 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class CursorMeta(DAAPIModule):

    def as_setCursorS(self, cursor):
        if self._isDAAPIInited():
            return self.flashObject.as_setCursor(cursor)




+++ okay decompyling cursormeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:25 CET
