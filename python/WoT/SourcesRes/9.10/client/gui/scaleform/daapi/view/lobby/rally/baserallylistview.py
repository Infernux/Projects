# 2015.01.14 22:27:17 CET
from abc import abstractmethod
from gui import makeHtmlString
from gui.Scaleform.daapi.view.meta.BaseRallyListViewMeta import BaseRallyListViewMeta
from messenger.proto.events import g_messengerEvents

class BaseRallyListView(BaseRallyListViewMeta):

    def __init__(self):
        super(BaseRallyListView, self).__init__()
        self._searchDP = None



    @abstractmethod
    def getPyDataProvider(self):
        return None



    def setData(self, initialData):
        pass



    def canBeClosed(self, callback):
        callback(True)



    def _populate(self):
        super(BaseRallyListView, self)._populate()
        g_messengerEvents.users.onUserRosterChanged += self._onUserRosterChanged
        self._searchDP = self.getPyDataProvider()
        self._searchDP.setFlashObject(self.as_getSearchDPS())



    def _dispose(self):
        if self._searchDP is not None:
            self._searchDP.fini()
            self._searchDP = None
        g_messengerEvents.users.onUserRosterChanged -= self._onUserRosterChanged
        super(BaseRallyListView, self)._dispose()



    def getRallyDetails(self, index):
        (cfdUnitID, vo,) = self._searchDP.getRally(index)
        return vo



    def _updateVehiclesLabel(self, minVal, maxVal):
        self.as_setVehiclesTitleS(makeHtmlString('html_templates:lobby/rally/', 'vehiclesLabel', {'minValue': minVal,
         'maxValue': maxVal}))



    def _onUserRosterChanged(self, _, user):
        pass




+++ okay decompyling baserallylistview.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:27:17 CET
