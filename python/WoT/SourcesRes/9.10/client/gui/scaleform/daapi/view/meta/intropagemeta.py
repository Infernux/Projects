# 2015.01.14 22:24:28 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class IntroPageMeta(DAAPIModule):

    def stopVideo(self):
        self._printOverrideError('stopVideo')



    def handleError(self, data):
        self._printOverrideError('handleError')



    def as_playVideoS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_playVideo(data)




+++ okay decompyling intropagemeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:28 CET
