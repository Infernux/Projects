# 2015.01.14 22:24:27 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortMainViewMeta(DAAPIModule):

    def onStatsClick(self):
        self._printOverrideError('onStatsClick')



    def onClanClick(self):
        self._printOverrideError('onClanClick')



    def onCalendarClick(self):
        self._printOverrideError('onCalendarClick')



    def onSettingClick(self):
        self._printOverrideError('onSettingClick')



    def onCreateDirectionClick(self, dirId):
        self._printOverrideError('onCreateDirectionClick')



    def onEnterBuildDirectionClick(self):
        self._printOverrideError('onEnterBuildDirectionClick')



    def onLeaveBuildDirectionClick(self):
        self._printOverrideError('onLeaveBuildDirectionClick')



    def onEnterTransportingClick(self):
        self._printOverrideError('onEnterTransportingClick')



    def onLeaveTransportingClick(self):
        self._printOverrideError('onLeaveTransportingClick')



    def onIntelligenceClick(self):
        self._printOverrideError('onIntelligenceClick')



    def onSortieClick(self):
        self._printOverrideError('onSortieClick')



    def onFirstTransportingStep(self):
        self._printOverrideError('onFirstTransportingStep')



    def onNextTransportingStep(self):
        self._printOverrideError('onNextTransportingStep')



    def onViewReady(self):
        self._printOverrideError('onViewReady')



    def as_switchModeS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_switchMode(data)



    def as_toggleCommanderHelpS(self, show):
        if self._isDAAPIInited():
            return self.flashObject.as_toggleCommanderHelp(show)



    def as_setMainDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setMainData(data)



    def as_setClanIconIdS(self, clanIconId):
        if self._isDAAPIInited():
            return self.flashObject.as_setClanIconId(clanIconId)



    def as_setHeaderMessageS(self, message, isWrongLocalTime):
        if self._isDAAPIInited():
            return self.flashObject.as_setHeaderMessage(message, isWrongLocalTime)



    def as_setBattlesDirectionDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setBattlesDirectionData(data)




+++ okay decompyling fortmainviewmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:27 CET
