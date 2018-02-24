# 2015.01.14 22:24:29 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class NotificationListButtonMeta(DAAPIModule):

    def handleClick(self):
        self._printOverrideError('handleClick')



    def as_setStateS(self, isBlinking):
        if self._isDAAPIInited():
            return self.flashObject.as_setState(isBlinking)




+++ okay decompyling notificationlistbuttonmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:29 CET
