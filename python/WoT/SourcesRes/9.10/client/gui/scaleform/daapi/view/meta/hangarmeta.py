# 2015.01.14 22:24:28 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class HangarMeta(DAAPIModule):

    def onEscape(self):
        self._printOverrideError('onEscape')



    def checkMoney(self):
        self._printOverrideError('checkMoney')



    def showHelpLayout(self):
        self._printOverrideError('showHelpLayout')



    def closeHelpLayout(self):
        self._printOverrideError('closeHelpLayout')



    def toggleGUIEditor(self):
        self._printOverrideError('toggleGUIEditor')



    def as_setCrewEnabledS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setCrewEnabled(value)



    def as_setCarouselEnabledS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setCarouselEnabled(value)



    def as_setupAmmunitionPanelS(self, maintenanceEnabled, customizationEnabled):
        if self._isDAAPIInited():
            return self.flashObject.as_setupAmmunitionPanel(maintenanceEnabled, customizationEnabled)



    def as_setControlsVisibleS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setControlsVisible(value)



    def as_showHelpLayoutS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_showHelpLayout()



    def as_closeHelpLayoutS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_closeHelpLayout()



    def as_setIsIGRS(self, value, text):
        if self._isDAAPIInited():
            return self.flashObject.as_setIsIGR(value, text)



    def as_setServerStatsS(self, stats, tooltipType):
        if self._isDAAPIInited():
            return self.flashObject.as_setServerStats(stats, tooltipType)



    def as_setServerStatsInfoS(self, tooltipFullData):
        if self._isDAAPIInited():
            return self.flashObject.as_setServerStatsInfo(tooltipFullData)



    def as_setVehicleIGRS(self, actionIgrDaysLeft):
        if self._isDAAPIInited():
            return self.flashObject.as_setVehicleIGR(actionIgrDaysLeft)




+++ okay decompyling hangarmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:28 CET
