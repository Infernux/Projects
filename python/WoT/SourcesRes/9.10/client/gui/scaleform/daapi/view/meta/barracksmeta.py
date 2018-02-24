# 2015.01.14 22:24:24 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class BarracksMeta(DAAPIModule):

    def invalidateTanksList(self):
        self._printOverrideError('invalidateTanksList')



    def setFilter(self, nation, role, tankType, location, nationID):
        self._printOverrideError('setFilter')



    def onShowRecruitWindowClick(self, rendererData, menuEnabled):
        self._printOverrideError('onShowRecruitWindowClick')



    def unloadTankman(self, dataCompact):
        self._printOverrideError('unloadTankman')



    def dismissTankman(self, dataCompact):
        self._printOverrideError('dismissTankman')



    def buyBerths(self):
        self._printOverrideError('buyBerths')



    def closeBarracks(self):
        self._printOverrideError('closeBarracks')



    def setTankmenFilter(self):
        self._printOverrideError('setTankmenFilter')



    def openPersonalCase(self, value, tabNumber):
        self._printOverrideError('openPersonalCase')



    def as_setTankmenS(self, tankmenCount, placesCount, tankmenInBarracks, berthPrice, actionPriceData, berthBuyCount, tankmanArr):
        if self._isDAAPIInited():
            return self.flashObject.as_setTankmen(tankmenCount, placesCount, tankmenInBarracks, berthPrice, actionPriceData, berthBuyCount, tankmanArr)



    def as_updateTanksListS(self, provider):
        if self._isDAAPIInited():
            return self.flashObject.as_updateTanksList(provider)



    def as_setTankmenFilterS(self, nation, role, tankType, location, nationID):
        if self._isDAAPIInited():
            return self.flashObject.as_setTankmenFilter(nation, role, tankType, location, nationID)




+++ okay decompyling barracksmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:24 CET
