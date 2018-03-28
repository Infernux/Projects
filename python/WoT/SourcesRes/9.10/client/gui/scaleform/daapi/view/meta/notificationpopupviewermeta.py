# 2015.01.14 22:24:29 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class NotificationPopUpViewerMeta(DAAPIModule):

    def setListClear(self):
        self._printOverrideError('setListClear')



    def onMessageHided(self, byTimeout, wasNotified):
        self._printOverrideError('onMessageHided')



    def onClickAction(self, typeID, entityID, action):
        self._printOverrideError('onClickAction')



    def onSecuritySettingsLinkClick(self):
        self._printOverrideError('onSecuritySettingsLinkClick')



    def getMessageActualTime(self, msTime):
        self._printOverrideError('getMessageActualTime')



    def as_getPopUpIndexS(self, typeID, entityID):
        if self._isDAAPIInited():
            return self.flashObject.as_getPopUpIndex(typeID, entityID)



    def as_appendMessageS(self, messageData):
        if self._isDAAPIInited():
            return self.flashObject.as_appendMessage(messageData)



    def as_updateMessageS(self, messageData):
        if self._isDAAPIInited():
            return self.flashObject.as_updateMessage(messageData)



    def as_removeMessageS(self, typeID, entityID):
        if self._isDAAPIInited():
            return self.flashObject.as_removeMessage(typeID, entityID)



    def as_removeAllMessagesS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_removeAllMessages()



    def as_layoutInfoS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_layoutInfo(data)



    def as_initInfoS(self, maxMessagessCount, padding):
        if self._isDAAPIInited():
            return self.flashObject.as_initInfo(maxMessagessCount, padding)




+++ okay decompyling notificationpopupviewermeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:29 CET
