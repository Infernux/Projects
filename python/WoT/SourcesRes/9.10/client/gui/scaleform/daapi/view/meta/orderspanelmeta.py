# 2015.01.14 22:24:29 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class OrdersPanelMeta(DAAPIModule):

    def getOrderTooltipBody(self, orderID):
        self._printOverrideError('getOrderTooltipBody')



    def as_setOrdersS(self, orders):
        if self._isDAAPIInited():
            return self.flashObject.as_setOrders(orders)



    def as_updateOrderS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_updateOrder(data)




+++ okay decompyling orderspanelmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:29 CET
