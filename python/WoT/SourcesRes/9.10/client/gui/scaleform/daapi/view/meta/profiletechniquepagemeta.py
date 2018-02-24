# 2015.01.14 22:24:30 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ProfileTechniquePageMeta(DAAPIModule):

    def setIsInHangarSelected(self, value):
        self._printOverrideError('setIsInHangarSelected')



    def as_setSelectedVehicleIntCDS(self, index):
        if self._isDAAPIInited():
            return self.flashObject.as_setSelectedVehicleIntCD(index)




+++ okay decompyling profiletechniquepagemeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:30 CET
