# 2015.01.14 22:24:30 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ProfileSectionMeta(DAAPIModule):

    def setActive(self, value):
        self._printOverrideError('setActive')



    def requestData(self, data):
        self._printOverrideError('requestData')



    def requestDossier(self, type):
        self._printOverrideError('requestDossier')



    def as_updateS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_update(data)



    def as_setInitDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)



    def as_responseDossierS(self, type, data):
        if self._isDAAPIInited():
            return self.flashObject.as_responseDossier(type, data)




+++ okay decompyling profilesectionmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:30 CET
