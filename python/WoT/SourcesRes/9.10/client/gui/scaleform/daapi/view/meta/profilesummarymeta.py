# 2015.01.14 22:24:30 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ProfileSummaryMeta(DAAPIModule):

    def getPersonalScoreWarningText(self, data):
        self._printOverrideError('getPersonalScoreWarningText')



    def getGlobalRating(self, userName):
        self._printOverrideError('getGlobalRating')



    def as_setUserDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setUserData(data)




+++ okay decompyling profilesummarymeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:30 CET
