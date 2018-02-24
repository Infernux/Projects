# 2015.01.14 22:24:28 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortSettingsDayoffPopoverMeta(DAAPIModule):

    def onApply(self, dayOff):
        self._printOverrideError('onApply')



    def as_setDescriptionsTextS(self, descriptionText, dayOffText):
        if self._isDAAPIInited():
            return self.flashObject.as_setDescriptionsText(descriptionText, dayOffText)



    def as_setButtonsTextS(self, applyButtonText, cancelButtonText):
        if self._isDAAPIInited():
            return self.flashObject.as_setButtonsText(applyButtonText, cancelButtonText)



    def as_setButtonsTooltipsS(self, enabledApplyButtonTooltip, disabledApplyButtonTooltip):
        if self._isDAAPIInited():
            return self.flashObject.as_setButtonsTooltips(enabledApplyButtonTooltip, disabledApplyButtonTooltip)



    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)




+++ okay decompyling fortsettingsdayoffpopovermeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:28 CET
