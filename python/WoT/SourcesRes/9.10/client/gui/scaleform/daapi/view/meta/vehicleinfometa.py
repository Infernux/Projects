# 2015.01.14 22:24:32 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class VehicleInfoMeta(DAAPIModule):

    def getVehicleInfo(self):
        self._printOverrideError('getVehicleInfo')



    def onCancelClick(self):
        self._printOverrideError('onCancelClick')



    def as_setVehicleInfoS(self, vehicleInfo):
        if self._isDAAPIInited():
            return self.flashObject.as_setVehicleInfo(vehicleInfo)




+++ okay decompyling vehicleinfometa.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:32 CET
