# 2015.01.14 22:24:26 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortBuildingProcessWindowMeta(DAAPIModule):

    def requestBuildingInfo(self, uid):
        self._printOverrideError('requestBuildingInfo')



    def applyBuildingProcess(self, uid):
        self._printOverrideError('applyBuildingProcess')



    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)



    def as_responseBuildingInfoS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_responseBuildingInfo(data)




+++ okay decompyling fortbuildingprocesswindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:26 CET
