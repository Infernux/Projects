# 2015.01.14 22:24:31 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class SimpleDialogMeta(DAAPIModule):

    def onButtonClick(self, buttonId):
        self._printOverrideError('onButtonClick')



    def as_setTextS(self, text):
        if self._isDAAPIInited():
            return self.flashObject.as_setText(text)



    def as_setTitleS(self, title):
        if self._isDAAPIInited():
            return self.flashObject.as_setTitle(title)



    def as_setButtonsS(self, buttonNames):
        if self._isDAAPIInited():
            return self.flashObject.as_setButtons(buttonNames)



    def as_setButtonEnablingS(self, id, isEnabled):
        if self._isDAAPIInited():
            return self.flashObject.as_setButtonEnabling(id, isEnabled)



    def as_setButtonFocusS(self, id):
        if self._isDAAPIInited():
            return self.flashObject.as_setButtonFocus(id)




+++ okay decompyling simpledialogmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:31 CET
