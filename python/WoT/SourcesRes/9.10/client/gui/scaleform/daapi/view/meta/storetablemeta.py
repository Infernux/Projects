# 2015.01.14 22:24:32 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class StoreTableMeta(DAAPIModule):

    def refreshStoreTableDataProvider(self):
        self._printOverrideError('refreshStoreTableDataProvider')



    def as_getTableDataProviderS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getTableDataProvider()



    def as_setTableTypeS(self, type):
        if self._isDAAPIInited():
            return self.flashObject.as_setTableType(type)



    def as_scrollToFirstS(self, level, disabled, currency):
        if self._isDAAPIInited():
            return self.flashObject.as_scrollToFirst(level, disabled, currency)



    def as_setGoldS(self, gold):
        if self._isDAAPIInited():
            return self.flashObject.as_setGold(gold)



    def as_setCreditsS(self, credits):
        if self._isDAAPIInited():
            return self.flashObject.as_setCredits(credits)




+++ okay decompyling storetablemeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:32 CET
