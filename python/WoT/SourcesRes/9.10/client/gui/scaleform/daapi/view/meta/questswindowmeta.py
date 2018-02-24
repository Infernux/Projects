# 2015.01.14 22:24:30 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class QuestsWindowMeta(DAAPIModule):

    def onTabSelected(self, tabID):
        self._printOverrideError('onTabSelected')



    def as_loadViewS(self, flashAlias, pyAlias):
        if self._isDAAPIInited():
            return self.flashObject.as_loadView(flashAlias, pyAlias)



    def as_selectTabS(self, tabID):
        if self._isDAAPIInited():
            return self.flashObject.as_selectTab(tabID)




+++ okay decompyling questswindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:30 CET
