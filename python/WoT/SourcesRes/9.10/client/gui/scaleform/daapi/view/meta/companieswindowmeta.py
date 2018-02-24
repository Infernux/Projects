# 2015.01.14 22:24:25 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class CompaniesWindowMeta(DAAPIModule):

    def createCompany(self):
        self._printOverrideError('createCompany')



    def joinCompany(self, prbID):
        self._printOverrideError('joinCompany')



    def getDivisionsList(self):
        self._printOverrideError('getDivisionsList')



    def refreshCompaniesList(self, creatorMask, isNotInBattle, division):
        self._printOverrideError('refreshCompaniesList')



    def requestPlayersList(self, prbID):
        self._printOverrideError('requestPlayersList')



    def showFAQWindow(self):
        self._printOverrideError('showFAQWindow')



    def getClientID(self):
        self._printOverrideError('getClientID')



    def as_getCompaniesListDPS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getCompaniesListDP()



    def as_showPlayersListS(self, index):
        if self._isDAAPIInited():
            return self.flashObject.as_showPlayersList(index)



    def as_setDefaultFilterS(self, creatorMask, isNotInBattle, division):
        if self._isDAAPIInited():
            return self.flashObject.as_setDefaultFilter(creatorMask, isNotInBattle, division)



    def as_setRefreshCoolDownS(self, time):
        if self._isDAAPIInited():
            return self.flashObject.as_setRefreshCoolDown(time)



    def as_disableCreateButtonS(self, isDisable):
        if self._isDAAPIInited():
            return self.flashObject.as_disableCreateButton(isDisable)




+++ okay decompyling companieswindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:25 CET
