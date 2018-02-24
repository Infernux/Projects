# 2015.01.14 22:24:31 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ReferralReferrerIntroWindowMeta(DAAPIModule):

    def onClickApplyButton(self):
        self._printOverrideError('onClickApplyButton')



    def onClickHrefLink(self):
        self._printOverrideError('onClickHrefLink')



    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)




+++ okay decompyling referralreferrerintrowindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:31 CET
