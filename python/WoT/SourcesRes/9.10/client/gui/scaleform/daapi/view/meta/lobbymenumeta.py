# 2015.01.14 22:24:28 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class LobbyMenuMeta(DAAPIModule):

    def settingsClick(self):
        self._printOverrideError('settingsClick')



    def cancelClick(self):
        self._printOverrideError('cancelClick')



    def refuseTraining(self):
        self._printOverrideError('refuseTraining')



    def logoffClick(self):
        self._printOverrideError('logoffClick')



    def quitClick(self):
        self._printOverrideError('quitClick')



    def versionInfoClick(self):
        self._printOverrideError('versionInfoClick')



    def as_setVersionMessageS(self, message, showLinkButton):
        if self._isDAAPIInited():
            return self.flashObject.as_setVersionMessage(message, showLinkButton)




+++ okay decompyling lobbymenumeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:29 CET
