# 2015.01.14 22:24:30 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class PunishmentDialogMeta(DAAPIModule):

    def as_setMsgTitleS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setMsgTitle(value)




+++ okay decompyling punishmentdialogmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:30 CET
