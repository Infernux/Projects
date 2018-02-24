# 2015.01.14 22:24:26 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortBuildingCardPopoverMeta(DAAPIModule):

    def openUpgradeWindow(self, value):
        self._printOverrideError('openUpgradeWindow')



    def openAssignedPlayersWindow(self, value):
        self._printOverrideError('openAssignedPlayersWindow')



    def openDemountBuildingWindow(self, value):
        self._printOverrideError('openDemountBuildingWindow')



    def openDirectionControlWindow(self):
        self._printOverrideError('openDirectionControlWindow')



    def openBuyOrderWindow(self):
        self._printOverrideError('openBuyOrderWindow')



    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)



    def as_setModernizationDestructionEnablingS(self, modernizationButtonEnabled, destroyButtonEnabled, modernizationButtonTooltip, destroyButtonTooltip):
        if self._isDAAPIInited():
            return self.flashObject.as_setModernizationDestructionEnabling(modernizationButtonEnabled, destroyButtonEnabled, modernizationButtonTooltip, destroyButtonTooltip)




+++ okay decompyling fortbuildingcardpopovermeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:26 CET
