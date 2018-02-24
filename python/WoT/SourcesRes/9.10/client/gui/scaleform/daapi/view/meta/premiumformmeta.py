# 2015.01.14 22:24:29 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class PremiumFormMeta(DAAPIModule):

    def onPremiumBuy(self, days, price):
        self._printOverrideError('onPremiumBuy')



    def onPremiumDataRequest(self):
        self._printOverrideError('onPremiumDataRequest')



    def as_setCostsS(self, costs):
        if self._isDAAPIInited():
            return self.flashObject.as_setCosts(costs)



    def as_setGoldS(self, gold):
        if self._isDAAPIInited():
            return self.flashObject.as_setGold(gold)



    def as_setPremiumS(self, isPremium):
        if self._isDAAPIInited():
            return self.flashObject.as_setPremium(isPremium)




+++ okay decompyling premiumformmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:29 CET
