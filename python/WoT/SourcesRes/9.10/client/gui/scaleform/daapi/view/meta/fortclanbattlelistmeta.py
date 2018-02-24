# 2015.01.14 22:24:26 CET
from gui.Scaleform.daapi.view.lobby.rally.BaseRallyListView import BaseRallyListView

class FortClanBattleListMeta(BaseRallyListView):

    def as_setClanBattleDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setClanBattleData(data)



    def as_upateClanBattlesCountS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_upateClanBattlesCount(value)




+++ okay decompyling fortclanbattlelistmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:26 CET
