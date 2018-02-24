# 2015.01.14 22:24:33 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class WindowViewMeta(DAAPIModule):

    def onWindowMinimize(self):
        self._printOverrideError('onWindowMinimize')



    def onSourceLoaded(self):
        self._printOverrideError('onSourceLoaded')



    def onTryClosing(self):
        self._printOverrideError('onTryClosing')



    def as_showWaitingS(self, msg, props):
        if self._isDAAPIInited():
            return self.flashObject.as_showWaiting(msg, props)



    def as_hideWaitingS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideWaiting()



    def as_getGeometryS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getGeometry()



    def as_setGeometryS(self, x, y, width, height):
        if self._isDAAPIInited():
            return self.flashObject.as_setGeometry(x, y, width, height)



    def as_isModalS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_isModal()




+++ okay decompyling windowviewmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:33 CET
