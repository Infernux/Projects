# 2015.01.14 22:24:28 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortSettingsWindowMeta(DAAPIModule):

    def activateDefencePeriod(self):
        self._printOverrideError('activateDefencePeriod')



    def disableDefencePeriod(self):
        self._printOverrideError('disableDefencePeriod')



    def cancelDisableDefencePeriod(self):
        self._printOverrideError('cancelDisableDefencePeriod')



    def as_setFortClanInfoS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setFortClanInfo(data)



    def as_setMainStatusS(self, title, msg, toolTip):
        if self._isDAAPIInited():
            return self.flashObject.as_setMainStatus(title, msg, toolTip)



    def as_setViewS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setView(value)



    def as_setDataForActivatedS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setDataForActivated(data)



    def as_setCanDisableDefencePeriodS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setCanDisableDefencePeriod(value)



    def as_setDataForNotActivatedS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setDataForNotActivated(data)




+++ okay decompyling fortsettingswindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:28 CET
