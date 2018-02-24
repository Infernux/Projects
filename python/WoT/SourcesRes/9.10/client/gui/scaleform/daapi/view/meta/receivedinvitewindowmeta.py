# 2015.01.14 22:24:31 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ReceivedInviteWindowMeta(DAAPIModule):

    def acceptInvite(self):
        self._printOverrideError('acceptInvite')



    def declineInvite(self):
        self._printOverrideError('declineInvite')



    def cancelInvite(self):
        self._printOverrideError('cancelInvite')



    def as_setTitleS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setTitle(value)



    def as_setReceivedInviteInfoS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setReceivedInviteInfo(value)




+++ okay decompyling receivedinvitewindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:31 CET
