# 2015.01.14 22:24:25 CET
from gui.Scaleform.daapi.view.lobby.rally.BaseRallyIntroView import BaseRallyIntroView

class CyberSportIntroMeta(BaseRallyIntroView):

    def requestVehicleSelection(self):
        self._printOverrideError('requestVehicleSelection')



    def startAutoMatching(self):
        self._printOverrideError('startAutoMatching')



    def showSelectorPopup(self):
        self._printOverrideError('showSelectorPopup')



    def as_setSelectedVehiclesS(self, vehiclesData, infoText, hasReadyVehicles):
        if self._isDAAPIInited():
            return self.flashObject.as_setSelectedVehicles(vehiclesData, infoText, hasReadyVehicles)




+++ okay decompyling cybersportintrometa.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:25 CET
