# 2015.01.14 22:24:31 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class RecruitParametersMeta(DAAPIModule):

    def onNationChanged(self, nationID):
        self._printOverrideError('onNationChanged')



    def onVehicleClassChanged(self, vehClass):
        self._printOverrideError('onVehicleClassChanged')



    def onVehicleChanged(self, vehID):
        self._printOverrideError('onVehicleChanged')



    def onTankmanRoleChanged(self, roleID):
        self._printOverrideError('onTankmanRoleChanged')



    def as_setVehicleClassDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setVehicleClassData(data)



    def as_setVehicleDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setVehicleData(data)



    def as_setTankmanRoleDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setTankmanRoleData(data)



    def as_setNationsDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setNationsData(data)




+++ okay decompyling recruitparametersmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:31 CET
