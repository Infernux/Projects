# 2015.01.14 22:24:29 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class MessengerBarMeta(DAAPIModule):

    def channelButtonClick(self):
        self._printOverrideError('channelButtonClick')



    def contactsButtonClick(self):
        self._printOverrideError('contactsButtonClick')



    def as_setInitDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)




+++ okay decompyling messengerbarmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:29 CET
