# 2015.01.14 22:24:26 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class EliteWindowMeta(DAAPIModule):

    def as_setVehicleS(self, vehicle):
        if self._isDAAPIInited():
            return self.flashObject.as_setVehicle(vehicle)




+++ okay decompyling elitewindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:26 CET
