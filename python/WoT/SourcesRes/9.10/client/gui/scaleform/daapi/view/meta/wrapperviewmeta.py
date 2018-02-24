# 2015.01.14 22:24:33 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class WrapperViewMeta(DAAPIModule):

    def onWindowClose(self):
        self._printOverrideError('onWindowClose')




+++ okay decompyling wrapperviewmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:33 CET
