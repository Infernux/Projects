# 2015.01.14 22:24:31 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class RosterSlotSettingsWindowMeta(DAAPIModule):

    def onFiltersUpdate(self, nation, vehicleType, isMain, level, compatibleOnly):
        self._printOverrideError('onFiltersUpdate')



    def getFilterData(self):
        self._printOverrideError('getFilterData')



    def submitButtonHandler(self, value):
        self._printOverrideError('submitButtonHandler')



    def cancelButtonHandler(self):
        self._printOverrideError('cancelButtonHandler')



    def as_setDefaultDataS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setDefaultData(value)



    def as_setListDataS(self, listData):
        if self._isDAAPIInited():
            return self.flashObject.as_setListData(listData)




+++ okay decompyling rosterslotsettingswindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:31 CET
