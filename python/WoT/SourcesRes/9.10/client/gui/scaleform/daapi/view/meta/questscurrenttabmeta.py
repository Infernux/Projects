# 2015.01.14 22:24:30 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class QuestsCurrentTabMeta(DAAPIModule):

    def sort(self, type, hideDone):
        self._printOverrideError('sort')



    def getQuestInfo(self, questID):
        self._printOverrideError('getQuestInfo')



    def getSortedTableData(self, tableData):
        self._printOverrideError('getSortedTableData')



    def as_setQuestsDataS(self, data, totalTasks):
        if self._isDAAPIInited():
            return self.flashObject.as_setQuestsData(data, totalTasks)



    def as_setSelectedQuestS(self, questID):
        if self._isDAAPIInited():
            return self.flashObject.as_setSelectedQuest(questID)




+++ okay decompyling questscurrenttabmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:30 CET
