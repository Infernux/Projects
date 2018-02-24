# 2015.01.14 22:24:26 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortBuildingComponentMeta(DAAPIModule):

    def onTransportingRequest(self, exportFrom, importTo):
        self._printOverrideError('onTransportingRequest')



    def requestBuildingProcess(self, direction, position):
        self._printOverrideError('requestBuildingProcess')



    def upgradeVisitedBuilding(self, uid):
        self._printOverrideError('upgradeVisitedBuilding')



    def getBuildingTooltipData(self, uid):
        self._printOverrideError('getBuildingTooltipData')



    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)



    def as_setBuildingDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setBuildingData(data)



    def as_refreshTransportingS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_refreshTransporting()




+++ okay decompyling fortbuildingcomponentmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:26 CET
