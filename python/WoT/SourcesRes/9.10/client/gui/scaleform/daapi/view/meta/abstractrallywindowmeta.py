# 2015.01.14 22:24:23 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class AbstractRallyWindowMeta(DAAPIModule):

    def canGoBack(self):
        self._printOverrideError('canGoBack')



    def onBrowseRallies(self):
        self._printOverrideError('onBrowseRallies')



    def onCreateRally(self):
        self._printOverrideError('onCreateRally')



    def onJoinRally(self, rallyId, slotIndex, peripheryId):
        self._printOverrideError('onJoinRally')



    def as_loadViewS(self, flashAlias, pyAlias):
        if self._isDAAPIInited():
            return self.flashObject.as_loadView(flashAlias, pyAlias)



    def as_enableWndCloseBtnS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_enableWndCloseBtn(value)




+++ okay decompyling abstractrallywindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:23 CET
