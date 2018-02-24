# 2015.01.14 22:35:44 CET
import GUI
from debug_utils import LOG_DEBUG
from gui.Scaleform.Flash import Flash
from gui.Scaleform import SCALEFORM_SWF_PATH_V3
from helpers import getFullClientVersion, getClientOverride

class GameLoading(Flash):

    def __init__(self, component = None):
        Flash.__init__(self, 'gameLoading.swf', path=SCALEFORM_SWF_PATH_V3)
        self._displayRoot = self.getMember('root.main')
        if self._displayRoot is not None:
            self._displayRoot.resync()
            self._displayRoot.setLocale(getClientOverride())
            self._displayRoot.setVersion(getFullClientVersion())
            (width, height,) = GUI.screenResolution()
            self._displayRoot.updateStage(width, height)



    def onLoad(self, dataSection):
        self.active(True)



    def onDelete(self):
        if self._displayRoot is not None:
            self._displayRoot.cleanup()
            self._displayRoot = None



    def setProgress(self, value):
        self._displayRoot.setProgress(value)



    def addMessage(self, message):
        LOG_DEBUG(message)



    def reset(self):
        self._displayRoot.setProgress(0)




+++ okay decompyling gameloading.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:35:44 CET
