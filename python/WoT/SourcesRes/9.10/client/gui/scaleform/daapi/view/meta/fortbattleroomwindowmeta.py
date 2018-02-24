# 2015.01.14 22:24:26 CET
from gui.Scaleform.daapi.view.lobby.rally.RallyMainWindowWithSearch import RallyMainWindowWithSearch

class FortBattleRoomWindowMeta(RallyMainWindowWithSearch):

    def onBrowseClanBattles(self):
        self._printOverrideError('onBrowseClanBattles')



    def onJoinClanBattle(self, rallyId, slotIndex, peripheryId):
        self._printOverrideError('onJoinClanBattle')



    def onCreatedBattleRoom(self, battleID, peripheryId):
        self._printOverrideError('onCreatedBattleRoom')




+++ okay decompyling fortbattleroomwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:26 CET
