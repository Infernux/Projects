# 2015.01.14 22:24:24 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class BattleQueueMeta(DAAPIModule):

    def startClick(self):
        self._printOverrideError('startClick')



    def exitClick(self):
        self._printOverrideError('exitClick')



    def onEscape(self):
        self._printOverrideError('onEscape')



    def as_setTimerS(self, textLabel, timeLabel):
        if self._isDAAPIInited():
            return self.flashObject.as_setTimer(textLabel, timeLabel)



    def as_setTypeS(self, type):
        if self._isDAAPIInited():
            return self.flashObject.as_setType(type)



    def as_setPlayersS(self, text):
        if self._isDAAPIInited():
            return self.flashObject.as_setPlayers(text)



    def as_setListByTypeS(self, listData):
        if self._isDAAPIInited():
            return self.flashObject.as_setListByType(listData)



    def as_showStartS(self, vis):
        if self._isDAAPIInited():
            return self.flashObject.as_showStart(vis)



    def as_showExitS(self, vis):
        if self._isDAAPIInited():
            return self.flashObject.as_showExit(vis)




+++ okay decompyling battlequeuemeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:24 CET
