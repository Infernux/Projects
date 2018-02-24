# 2015.01.14 22:24:29 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class NotificationsListMeta(DAAPIModule):

    def onClickAction(self, typeID, entityID, action):
        self._printOverrideError('onClickAction')



    def onSecuritySettingsLinkClick(self):
        self._printOverrideError('onSecuritySettingsLinkClick')



    def getMessageActualTime(self, msTime):
        self._printOverrideError('getMessageActualTime')



    def as_setInitDataS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(value)



    def as_setMessagesListS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setMessagesList(value)



    def as_appendMessageS(self, messageData):
        if self._isDAAPIInited():
            return self.flashObject.as_appendMessage(messageData)



    def as_updateMessageS(self, messageData):
        if self._isDAAPIInited():
            return self.flashObject.as_updateMessage(messageData)




+++ okay decompyling notificationslistmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:29 CET
