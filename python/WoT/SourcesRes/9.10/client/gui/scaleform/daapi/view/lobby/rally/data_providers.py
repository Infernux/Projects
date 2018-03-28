# 2015.01.14 22:27:18 CET
from abc import abstractmethod
from debug_utils import LOG_ERROR
from gui.Scaleform.framework.entities.DAAPIDataProvider import DAAPIDataProvider, SortableDAAPIDataProvider
from gui.shared.utils import sortByFields

class BaseRallyListDataProvider(SortableDAAPIDataProvider):

    def __init__(self):
        super(BaseRallyListDataProvider, self).__init__()
        self.clear()
        self._selectedIdx = -1
        self.__selectedRallyIndex = -1



    @property
    def selectedRallyIndex(self):
        return self.__selectedRallyIndex



    @abstractmethod
    def getVO(self, unitIndex = None):
        return None



    @abstractmethod
    def updateList(self, selectedID, result):
        return self._selectedIdx



    def fini(self):
        self.clear()
        self._dispose()



    def clear(self):
        self.__list = []
        self.__mapping = {}



    def updateItems(self, diff):
        self.flashObject.update(diff)



    @property
    def collection(self):
        return self.__list



    @property
    def mapping(self):
        return self.__mapping



    def requestUpdatedItemsHandler(self, indexes):
        return filter(lambda item: item[0] in indexes, enumerate(self.__list))



    def emptyItem(self):
        return None



    def getRally(self, index):
        cfdUnitID = 0
        if index >= 0:
            try:
                cfdUnitID = self.__list[index]['cfdUnitID']
                self.__selectedRallyIndex = index
            except IndexError:
                self.__selectedRallyIndex = -1
                LOG_ERROR('Item not found', index)
        if cfdUnitID:
            vo = self.getVO(cfdUnitID)
        else:
            vo = None
        return (cfdUnitID, vo)



    def rebuildList(self, selectedID, result):
        self._selectedIdx = self.buildList(selectedID, result)
        self.refresh()
        return self._selectedIdx



    def rebuildIndexes(self):
        self.__mapping = dict(map(lambda item: (item[1]['cfdUnitID'], item[0]), enumerate(self.__list)))




+++ okay decompyling data_providers.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:27:18 CET
