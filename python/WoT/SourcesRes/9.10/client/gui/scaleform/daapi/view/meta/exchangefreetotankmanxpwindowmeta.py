# 2015.01.14 22:24:26 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ExchangeFreeToTankmanXpWindowMeta(DAAPIModule):

    def apply(self):
        self._printOverrideError('apply')



    def onValueChanged(self, data):
        self._printOverrideError('onValueChanged')



    def calcValueRequest(self, value):
        self._printOverrideError('calcValueRequest')



    def as_setInitDataS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(value)



    def as_setCalcValueResponseS(self, price, actionPriceData):
        if self._isDAAPIInited():
            return self.flashObject.as_setCalcValueResponse(price, actionPriceData)



    def as_setWalletStatusS(self, walletStatus):
        if self._isDAAPIInited():
            return self.flashObject.as_setWalletStatus(walletStatus)




+++ okay decompyling exchangefreetotankmanxpwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:26 CET
