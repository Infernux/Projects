# 2015.01.14 22:24:32 CET
from gui.Scaleform.daapi.view.lobby.rally.BaseRallyRoomView import BaseRallyRoomView

class SquadViewMeta(BaseRallyRoomView):

    def leaveSquad(self):
        self._printOverrideError('leaveSquad')



    def as_updateBattleTypeS(self, battleTypeName):
        if self._isDAAPIInited():
            return self.flashObject.as_updateBattleType(battleTypeName)



    def as_updateInviteBtnStateS(self, isEnabled):
        if self._isDAAPIInited():
            return self.flashObject.as_updateInviteBtnState(isEnabled)



    def as_setCoolDownForReadyButtonS(self, timer):
        if self._isDAAPIInited():
            return self.flashObject.as_setCoolDownForReadyButton(timer)




+++ okay decompyling squadviewmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:32 CET
