# 2015.01.14 22:24:32 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class TrainingFormMeta(DAAPIModule):

    def joinTrainingRequest(self, id):
        self._printOverrideError('joinTrainingRequest')



    def createTrainingRequest(self):
        self._printOverrideError('createTrainingRequest')



    def onEscape(self):
        self._printOverrideError('onEscape')



    def onLeave(self):
        self._printOverrideError('onLeave')



    def as_setListS(self, provider, totalPlayers):
        if self._isDAAPIInited():
            return self.flashObject.as_setList(provider, totalPlayers)




+++ okay decompyling trainingformmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:32 CET
