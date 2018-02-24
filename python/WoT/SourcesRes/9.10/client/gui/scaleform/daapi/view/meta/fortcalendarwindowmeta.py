# 2015.01.14 22:24:26 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortCalendarWindowMeta(DAAPIModule):

    def as_updatePreviewDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_updatePreviewData(data)




+++ okay decompyling fortcalendarwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:26 CET
