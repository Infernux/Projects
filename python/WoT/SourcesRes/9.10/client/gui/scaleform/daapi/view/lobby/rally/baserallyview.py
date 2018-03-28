# 2015.01.14 22:27:18 CET
from debug_utils import LOG_DEBUG
from gui.Scaleform.daapi.view.meta.BaseRallyViewMeta import BaseRallyViewMeta
from gui.Scaleform.daapi.view.meta.WindowViewMeta import WindowViewMeta
from gui.prb_control.prb_cooldown import getPrbRequestCoolDown
from gui.shared import events
from gui.shared.event_bus import EVENT_BUS_SCOPE

class BaseRallyView(BaseRallyViewMeta, WindowViewMeta):

    def __init__(self):
        super(BaseRallyView, self).__init__()



    def canBeClosed(self, callback):
        callback(True)



    def setData(self, initialData):
        LOG_DEBUG('BaseRallyView.setItemId stub implementation. Passed id is:', initialData)



    def getCoolDownRequests(self):
        return []



    def _populate(self):
        super(BaseRallyView, self)._populate()
        self.addListener(events.CoolDownEvent.PREBATTLE, self._handleSetPrebattleCoolDown, scope=EVENT_BUS_SCOPE.LOBBY)
        self._checkCoolDowns()



    def _dispose(self):
        super(BaseRallyView, self)._dispose()
        self.removeListener(events.CoolDownEvent.PREBATTLE, self._handleSetPrebattleCoolDown, scope=EVENT_BUS_SCOPE.LOBBY)



    def _handleSetPrebattleCoolDown(self, event):
        if event.requestID in self.getCoolDownRequests():
            self.as_setCoolDownS(event.coolDown, event.requestID)



    def _checkCoolDowns(self):
        for requestID in self.getCoolDownRequests():
            coolDown = getPrbRequestCoolDown(requestID)
            if coolDown > 0:
                self.as_setCoolDownS(coolDown, requestID)





+++ okay decompyling baserallyview.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:27:18 CET
