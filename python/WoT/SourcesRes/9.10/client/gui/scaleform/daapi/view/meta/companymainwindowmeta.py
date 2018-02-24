# 2015.01.14 22:24:25 CET
from gui.Scaleform.daapi.view.lobby.rally.AbstractRallyWindow import AbstractRallyWindow

class CompanyMainWindowMeta(AbstractRallyWindow):

    def getCompanyName(self):
        self._printOverrideError('getCompanyName')



    def showFAQWindow(self):
        self._printOverrideError('showFAQWindow')



    def as_setWindowTitleS(self, title, icon):
        if self._isDAAPIInited():
            return self.flashObject.as_setWindowTitle(title, icon)




+++ okay decompyling companymainwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:25 CET
