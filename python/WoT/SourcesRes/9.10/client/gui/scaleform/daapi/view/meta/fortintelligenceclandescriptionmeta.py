# 2015.01.14 22:24:27 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortIntelligenceClanDescriptionMeta(DAAPIModule):

    def onOpenCalendar(self):
        self._printOverrideError('onOpenCalendar')



    def onOpenClanList(self):
        self._printOverrideError('onOpenClanList')



    def onOpenClanStatistics(self):
        self._printOverrideError('onOpenClanStatistics')



    def onOpenClanCard(self):
        self._printOverrideError('onOpenClanCard')



    def onAddRemoveFavorite(self, isAdd):
        self._printOverrideError('onAddRemoveFavorite')



    def onAttackDirection(self, uid):
        self._printOverrideError('onAttackDirection')



    def onHoverDirection(self):
        self._printOverrideError('onHoverDirection')



    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)



    def as_updateBookMarkS(self, isAdd):
        if self._isDAAPIInited():
            return self.flashObject.as_updateBookMark(isAdd)




+++ okay decompyling fortintelligenceclandescriptionmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:27 CET
