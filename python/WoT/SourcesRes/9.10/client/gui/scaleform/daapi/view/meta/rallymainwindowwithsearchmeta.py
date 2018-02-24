# 2015.01.14 22:24:30 CET
from gui.Scaleform.daapi.view.lobby.rally.BaseRallyMainWindow import BaseRallyMainWindow

class RallyMainWindowWithSearchMeta(BaseRallyMainWindow):

    def onAutoMatch(self, value, values):
        self._printOverrideError('onAutoMatch')



    def autoSearchApply(self, value):
        self._printOverrideError('autoSearchApply')



    def autoSearchCancel(self, value):
        self._printOverrideError('autoSearchCancel')



    def as_autoSearchEnableBtnS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_autoSearchEnableBtn(value)



    def as_changeAutoSearchStateS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_changeAutoSearchState(value)



    def as_changeAutoSearchBtnsStateS(self, waitingPlayers, searchEnemy):
        if self._isDAAPIInited():
            return self.flashObject.as_changeAutoSearchBtnsState(waitingPlayers, searchEnemy)



    def as_hideAutoSearchS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideAutoSearch()




+++ okay decompyling rallymainwindowwithsearchmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:31 CET
