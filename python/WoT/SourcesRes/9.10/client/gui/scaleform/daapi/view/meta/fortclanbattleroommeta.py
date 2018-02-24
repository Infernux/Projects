# 2015.01.14 22:24:26 CET
from gui.Scaleform.daapi.view.lobby.rally.BaseRallyRoomView import BaseRallyRoomView

class FortClanBattleRoomMeta(BaseRallyRoomView):

    def onTimerAlert(self):
        self._printOverrideError('onTimerAlert')



    def as_updateTeamHeaderTextS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_updateTeamHeaderText(value)



    def as_setBattleRoomDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setBattleRoomData(data)



    def as_updateReadyStatusS(self, mineValue, enemyValue):
        if self._isDAAPIInited():
            return self.flashObject.as_updateReadyStatus(mineValue, enemyValue)



    def as_setTimerDeltaS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setTimerDelta(data)



    def as_updateDirectionsS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_updateDirections(data)



    def as_setMineClanIconS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setMineClanIcon(value)



    def as_setEnemyClanIconS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setEnemyClanIcon(value)




+++ okay decompyling fortclanbattleroommeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:26 CET
