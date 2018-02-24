# 2015.01.14 22:24:26 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ExchangeWindowMeta(DAAPIModule):

    def as_setSecondaryCurrencyS(self, credits):
        if self._isDAAPIInited():
            return self.flashObject.as_setSecondaryCurrency(credits)



    def as_setWalletStatusS(self, walletStatus):
        if self._isDAAPIInited():
            return self.flashObject.as_setWalletStatus(walletStatus)




+++ okay decompyling exchangewindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:26 CET
