# 2015.01.14 22:24:24 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class BattleSessionWindowMeta(DAAPIModule):

    def requestToAssignMember(self, accId):
        self._printOverrideError('requestToAssignMember')



    def requestToUnassignMember(self, accId):
        self._printOverrideError('requestToUnassignMember')



    def canMoveToAssigned(self):
        self._printOverrideError('canMoveToAssigned')



    def canMoveToUnassigned(self):
        self._printOverrideError('canMoveToUnassigned')



    def as_setStartTimeS(self, startTime):
        if self._isDAAPIInited():
            return self.flashObject.as_setStartTime(startTime)



    def as_setInfoS(self, wins, map, firstTeam, secondTeam, count, description, comment):
        if self._isDAAPIInited():
            return self.flashObject.as_setInfo(wins, map, firstTeam, secondTeam, count, description, comment)



    def as_setNationsLimitsS(self, nations):
        if self._isDAAPIInited():
            return self.flashObject.as_setNationsLimits(nations)



    def as_setClassesLimitsS(self, vehicleLevels, classesLimitsAreIdentical):
        if self._isDAAPIInited():
            return self.flashObject.as_setClassesLimits(vehicleLevels, classesLimitsAreIdentical)



    def as_setCommonLimitsS(self, teamLevel, minTotalLevel, maxTotalLevel, maxPlayers):
        if self._isDAAPIInited():
            return self.flashObject.as_setCommonLimits(teamLevel, minTotalLevel, maxTotalLevel, maxPlayers)



    def as_setPlayersCountTextS(self, playersCountText):
        if self._isDAAPIInited():
            return self.flashObject.as_setPlayersCountText(playersCountText)




+++ okay decompyling battlesessionwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:24 CET
