# 2015.01.17 21:49:49 CET
import Keys
from gui import InputHandler
from gui.Scaleform.framework.entities.View import View
from gui.Scaleform.daapi.view.meta.WaitingViewMeta import WaitingViewMeta

class WaitingView(WaitingViewMeta, View):

    def __init__(self):
        super(WaitingView, self).__init__()
        InputHandler.g_instance.onKeyUp += self.handleKeyUpEvent
        self.__callback = None



    def handleKeyUpEvent(self, event):
        if event.key == Keys.KEY_ESCAPE:
            if self.__callback:
                self.__callback()



    def close(self):
        self.__callback = None
        self.hideS(None)



    def destroy(self):
        self.__callback = None
        InputHandler.g_instance.onKeyUp -= self.handleKeyUpEvent
        super(WaitingView, self).destroy()



    def setCallback(self, value):
        self.__callback = value



    def cancelCallback(self):
        self.__callback = None




+++ okay decompyling waitingview.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.17 21:49:49 CET
