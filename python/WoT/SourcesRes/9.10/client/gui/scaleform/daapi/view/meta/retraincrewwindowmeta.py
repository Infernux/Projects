# 2015.01.14 22:24:31 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class RetrainCrewWindowMeta(DAAPIModule):

    def submit(self, data):
        self._printOverrideError('submit')



    def changeRetrainType(self, retrainTypeIndex):
        self._printOverrideError('changeRetrainType')



    def as_setCommonDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setCommonData(data)



    def as_updateDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_updateData(data)




+++ okay decompyling retraincrewwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:31 CET
