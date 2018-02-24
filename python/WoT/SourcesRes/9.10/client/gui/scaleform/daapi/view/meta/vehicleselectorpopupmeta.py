# 2015.01.14 22:24:32 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class VehicleSelectorPopupMeta(DAAPIModule):

    def onFiltersUpdate(self, nation, vehicleType, isMain, level, compatibleOnly):
        self._printOverrideError('onFiltersUpdate')



    def onSelectVehicles(self, items):
        self._printOverrideError('onSelectVehicles')



    def as_setFiltersDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setFiltersData(data)



    def as_setListDataS(self, listData, selectedItems):
        if self._isDAAPIInited():
            return self.flashObject.as_setListData(listData, selectedItems)



    def as_setListModeS(self, isMultipleSelect):
        if self._isDAAPIInited():
            return self.flashObject.as_setListMode(isMultipleSelect)



    def as_setInfoTextS(self, text):
        if self._isDAAPIInited():
            return self.flashObject.as_setInfoText(text)




+++ okay decompyling vehicleselectorpopupmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:32 CET
