# 2015.01.14 22:24:24 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class BasePrebattleViewMeta(DAAPIModule):

    def as_setPyAliasS(self, alias):
        if self._isDAAPIInited():
            return self.flashObject.as_setPyAlias(alias)



    def as_getPyAliasS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getPyAlias()




+++ okay decompyling baseprebattleviewmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:24 CET
