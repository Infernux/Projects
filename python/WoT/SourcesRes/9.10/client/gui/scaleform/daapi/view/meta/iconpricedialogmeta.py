# 2015.01.14 22:24:28 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class IconPriceDialogMeta(DAAPIModule):

    def as_setMessagePriceS(self, price, currency, actionPriceData):
        if self._isDAAPIInited():
            return self.flashObject.as_setMessagePrice(price, currency, actionPriceData)



    def as_setPriceLabelS(self, label):
        if self._isDAAPIInited():
            return self.flashObject.as_setPriceLabel(label)



    def as_setOperationAllowedS(self, isAllowed):
        if self._isDAAPIInited():
            return self.flashObject.as_setOperationAllowed(isAllowed)




+++ okay decompyling iconpricedialogmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:28 CET
