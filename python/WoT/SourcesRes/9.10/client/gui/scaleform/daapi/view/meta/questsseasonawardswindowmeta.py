# 2015.01.14 22:24:30 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class QuestsSeasonAwardsWindowMeta(DAAPIModule):

    def showVehicleInfo(self, vehicleId):
        self._printOverrideError('showVehicleInfo')



    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)




+++ okay decompyling questsseasonawardswindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:30 CET
