# 2015.01.14 22:13:49 CET
import Event

class _PrbCtrlEvents(object):

    def __init__(self):
        super(_PrbCtrlEvents, self).__init__()
        self.__eManager = Event.EventManager()
        self.onPrebattleIntroModeJoined = Event.Event(self.__eManager)
        self.onPrebattleIntroModeLeft = Event.Event(self.__eManager)
        self.onUnitIntroModeLeft = Event.Event(self.__eManager)
        self.onPrebattleInited = Event.Event(self.__eManager)
        self.onUnitIntroModeJoined = Event.Event(self.__eManager)
        self.onUnitIntroModeLeft = Event.Event(self.__eManager)
        self.onPreQueueFunctionalCreated = Event.Event(self.__eManager)
        self.onPreQueueFunctionalDestroyed = Event.Event(self.__eManager)
        self.onPreQueueFunctionalChanged = Event.Event(self.__eManager)



    def clear(self):
        self.__eManager.clear()



g_prbCtrlEvents = _PrbCtrlEvents()

+++ okay decompyling ctrl_events.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:13:49 CET
