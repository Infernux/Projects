# 2015.01.14 22:24:25 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class CrewOperationsPopOverMeta(DAAPIModule):

    def invokeOperation(self, operationName):
        self._printOverrideError('invokeOperation')



    def as_updateS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_update(data)




+++ okay decompyling crewoperationspopovermeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:25 CET
