# 2015.01.14 22:24:26 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ExchangeVcoinWindowMeta(DAAPIModule):

    def buyVcoin(self):
        self._printOverrideError('buyVcoin')



    def as_setTargetCurrencyDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setTargetCurrencyData(data)



    def as_setSecondaryCurrencyS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setSecondaryCurrency(value)




+++ okay decompyling exchangevcoinwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:26 CET
