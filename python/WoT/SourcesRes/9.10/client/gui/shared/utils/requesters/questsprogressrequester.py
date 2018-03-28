# 2015.01.14 23:24:42 CET
from collections import namedtuple
import BigWorld
import potapov_quests
from adisp import async
from abstract import AbstractRequester

class QuestsProgressRequester(AbstractRequester):
    PotapovQuestProgress = namedtuple('PotapovQuestProgress', ['state',
     'selected',
     'rewards',
     'unlocked'])

    def __init__(self):
        super(QuestsProgressRequester, self).__init__()
        self.__pqStorage = None



    def getQuestProgress(self, qID):
        return self.__getQuestsData().get(qID, {}).get('progress')



    def getPotapovQuestProgress(self, pqType, potapovQuestID):
        potapovQuestsProgress = self.__getPotapovQuestsData()
        return self.PotapovQuestProgress(self.__pqStorage.get(potapovQuestID, (0, potapov_quests.PQ_STATE.NONE))[1], potapovQuestID in potapovQuestsProgress['selected'], potapovQuestsProgress['rewards'].get(potapovQuestID, {}), pqType.maySelectQuest(self.__pqStorage.keys()))



    def getPotapovQuestsStorage(self):
        return self.__pqStorage



    def getPotapovQuestsFreeSlots(self):
        pqProgress = self.__getPotapovQuestsData()
        return pqProgress['slots'] - len(pqProgress['selected'])



    def getSelectedPotapovQuestsIDs(self):
        return self.__getPotapovQuestsData()['selected']



    def getTankmanLastIDs(self, nationID):
        return self.__getPotapovQuestsData()['lastIDs'].get(nationID, (-1, -1, -1))



    def getTokenCount(self, tokenID):
        tokenData = self.__getTokensData().get(tokenID, {})
        return tokenData.get('count', 0)



    @async
    def _requestCache(self, callback = None):
        BigWorld.player().questProgress.getCache(lambda resID, value: self._response(resID, value, callback))



    def _response(self, resID, value, callback):
        self.__pqStorage = potapov_quests.PQStorage(value['potapovQuests']['compDescr'])
        super(QuestsProgressRequester, self)._response(resID, value, callback)



    def __getQuestsData(self):
        return self.getCacheValue('quests', {})



    def __getTokensData(self):
        return self.getCacheValue('tokens', {})



    def __getPotapovQuestsData(self):
        return self.getCacheValue('potapovQuests', {})




+++ okay decompyling questsprogressrequester.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 23:24:42 CET
