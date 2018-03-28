# 2015.01.14 22:24:24 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class BrowserMeta(DAAPIModule):

    def browserAction(self, action):
        self._printOverrideError('browserAction')



    def browserMove(self, x, y, z):
        self._printOverrideError('browserMove')



    def browserDown(self, x, y, z):
        self._printOverrideError('browserDown')



    def browserUp(self, x, y, z):
        self._printOverrideError('browserUp')



    def browserFocusOut(self):
        self._printOverrideError('browserFocusOut')



    def onBrowserShow(self, needRefresh):
        self._printOverrideError('onBrowserShow')



    def onBrowserHide(self):
        self._printOverrideError('onBrowserHide')



    def as_loadingStartS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_loadingStart()



    def as_loadingStopS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_loadingStop()



    def as_configureS(self, isDefaultBrowser, title, showActionBtn):
        if self._isDAAPIInited():
            return self.flashObject.as_configure(isDefaultBrowser, title, showActionBtn)



    def as_setBrowserSizeS(self, width, height):
        if self._isDAAPIInited():
            return self.flashObject.as_setBrowserSize(width, height)



    def as_showServiceViewS(self, header, description):
        if self._isDAAPIInited():
            return self.flashObject.as_showServiceView(header, description)



    def as_hideServiceViewS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideServiceView()




+++ okay decompyling browsermeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:25 CET
