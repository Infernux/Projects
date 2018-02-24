# 2015.01.14 22:24:31 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ReportBugPanelMeta(DAAPIModule):

    def reportBug(self):
        self._printOverrideError('reportBug')



    def as_setHyperLinkS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setHyperLink(value)




+++ okay decompyling reportbugpanelmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:31 CET
