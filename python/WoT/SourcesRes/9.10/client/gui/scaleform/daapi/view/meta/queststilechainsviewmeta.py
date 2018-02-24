# 2015.01.14 22:24:30 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class QuestsTileChainsViewMeta(DAAPIModule):

    def getTileData(self, vehicleType, taskFilterType, hideCompleted):
        self._printOverrideError('getTileData')



    def getChainProgress(self):
        self._printOverrideError('getChainProgress')



    def getTaskDetails(self, taskId):
        self._printOverrideError('getTaskDetails')



    def selectTask(self, taskId):
        self._printOverrideError('selectTask')



    def refuseTask(self, taskId):
        self._printOverrideError('refuseTask')



    def gotoBack(self):
        self._printOverrideError('gotoBack')



    def showAwardVehicleInfo(self, awardVehicleID):
        self._printOverrideError('showAwardVehicleInfo')



    def showAwardVehicleInHangar(self, awardVehicleID):
        self._printOverrideError('showAwardVehicleInHangar')



    def as_setHeaderDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setHeaderData(data)



    def as_updateTileDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_updateTileData(data)



    def as_updateChainProgressS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_updateChainProgress(data)



    def as_updateTaskDetailsS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_updateTaskDetails(data)



    def as_setSelectedTaskS(self, taskId):
        if self._isDAAPIInited():
            return self.flashObject.as_setSelectedTask(taskId)




+++ okay decompyling queststilechainsviewmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:30 CET
