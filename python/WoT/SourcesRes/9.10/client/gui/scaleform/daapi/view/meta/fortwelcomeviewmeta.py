# 2015.01.14 22:24:28 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortWelcomeViewMeta(DAAPIModule):

    def onViewReady(self):
        self._printOverrideError('onViewReady')



    def onCreateBtnClick(self):
        self._printOverrideError('onCreateBtnClick')



    def onNavigate(self, code):
        self._printOverrideError('onNavigate')



    def as_setWarningTextS(self, text, disabledBtnTooltipHeader, disabledBtnTooltipBody):
        if self._isDAAPIInited():
            return self.flashObject.as_setWarningText(text, disabledBtnTooltipHeader, disabledBtnTooltipBody)



    def as_setHyperLinksS(self, searchClanLink, createClanLink, detailLink):
        if self._isDAAPIInited():
            return self.flashObject.as_setHyperLinks(searchClanLink, createClanLink, detailLink)



    def as_setCommonDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setCommonData(data)



    def as_setRequirementTextS(self, text):
        if self._isDAAPIInited():
            return self.flashObject.as_setRequirementText(text)




+++ okay decompyling fortwelcomeviewmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:28 CET
