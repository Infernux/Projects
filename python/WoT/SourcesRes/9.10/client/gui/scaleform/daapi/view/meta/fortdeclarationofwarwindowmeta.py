# 2015.01.14 22:24:27 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortDeclarationOfWarWindowMeta(DAAPIModule):

    def onDirectonChosen(self, directionUID):
        self._printOverrideError('onDirectonChosen')



    def onDirectionSelected(self):
        self._printOverrideError('onDirectionSelected')



    def as_setupHeaderS(self, title, description):
        if self._isDAAPIInited():
            return self.flashObject.as_setupHeader(title, description)



    def as_setupClansS(self, myClan, enemyClan):
        if self._isDAAPIInited():
            return self.flashObject.as_setupClans(myClan, enemyClan)



    def as_setDirectionsS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setDirections(data)



    def as_selectDirectionS(self, uid):
        if self._isDAAPIInited():
            return self.flashObject.as_selectDirection(uid)




+++ okay decompyling fortdeclarationofwarwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:27 CET
