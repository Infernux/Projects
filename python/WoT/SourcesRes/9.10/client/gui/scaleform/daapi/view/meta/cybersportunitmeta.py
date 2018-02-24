# 2015.01.14 22:24:25 CET
from gui.Scaleform.daapi.view.lobby.rally.BaseRallyRoomView import BaseRallyRoomView

class CyberSportUnitMeta(BaseRallyRoomView):

    def toggleFreezeRequest(self):
        self._printOverrideError('toggleFreezeRequest')



    def toggleStatusRequest(self):
        self._printOverrideError('toggleStatusRequest')



    def showSettingsRoster(self, vaue):
        self._printOverrideError('showSettingsRoster')



    def resultRosterSlotsSettings(self, value):
        self._printOverrideError('resultRosterSlotsSettings')



    def cancelRosterSlotsSettings(self):
        self._printOverrideError('cancelRosterSlotsSettings')



    def lockSlotRequest(self, slotIndex):
        self._printOverrideError('lockSlotRequest')



    def as_updateSlotSettingsS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_updateSlotSettings(value)



    def as_closeSlotS(self, slotIdx, cost, slotsLabel):
        if self._isDAAPIInited():
            return self.flashObject.as_closeSlot(slotIdx, cost, slotsLabel)



    def as_openSlotS(self, slotIdx, canBeTaken, slotsLabel, compatibleVehiclesCount):
        if self._isDAAPIInited():
            return self.flashObject.as_openSlot(slotIdx, canBeTaken, slotsLabel, compatibleVehiclesCount)



    def as_lockUnitS(self, isLocked, slotsLabel):
        if self._isDAAPIInited():
            return self.flashObject.as_lockUnit(isLocked, slotsLabel)



    def as_setOpenedS(self, isOpened, statusLabel):
        if self._isDAAPIInited():
            return self.flashObject.as_setOpened(isOpened, statusLabel)



    def as_setTotalLabelS(self, hasTotalLevelError, totalLevelLabel, totalLevel):
        if self._isDAAPIInited():
            return self.flashObject.as_setTotalLabel(hasTotalLevelError, totalLevelLabel, totalLevel)




+++ okay decompyling cybersportunitmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:25 CET
