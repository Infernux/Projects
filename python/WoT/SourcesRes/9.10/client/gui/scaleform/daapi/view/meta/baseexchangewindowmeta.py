# 2015.01.14 22:24:24 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class BaseExchangeWindowMeta(DAAPIModule):

    def exchange(self, data):
        self._printOverrideError('exchange')



    def as_setPrimaryCurrencyS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setPrimaryCurrency(value)



    def as_exchangeRateS(self, value, actionValue):
        if self._isDAAPIInited():
            return self.flashObject.as_exchangeRate(value, actionValue)




+++ okay decompyling baseexchangewindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:24 CET
