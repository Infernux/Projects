# 2015.01.14 22:24:23 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class AccountPopoverMeta(DAAPIModule):

    def openProfile(self):
        self._printOverrideError('openProfile')



    def openClanStatistic(self):
        self._printOverrideError('openClanStatistic')



    def openCrewStatistic(self):
        self._printOverrideError('openCrewStatistic')



    def openReferralManagement(self):
        self._printOverrideError('openReferralManagement')



    def as_setDataS(self, userData, isTeamKiller, mainAchievements, infoBtnEnabled, clanData, crewData):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(userData, isTeamKiller, mainAchievements, infoBtnEnabled, clanData, crewData)



    def as_setClanEmblemS(self, emblemId):
        if self._isDAAPIInited():
            return self.flashObject.as_setClanEmblem(emblemId)



    def as_setCrewEmblemS(self, emblemId):
        if self._isDAAPIInited():
            return self.flashObject.as_setCrewEmblem(emblemId)



    def as_setReferralDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setReferralData(data)




+++ okay decompyling accountpopovermeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:23 CET
