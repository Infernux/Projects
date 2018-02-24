# 2015.01.14 22:24:27 CET
from gui.Scaleform.daapi.view.lobby.rally.BaseRallyListView import BaseRallyListView

class FortListMeta(BaseRallyListView):

    def changeDivisionIndex(self, index):
        self._printOverrideError('changeDivisionIndex')



    def as_getDivisionsDPS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getDivisionsDP()



    def as_setSelectedDivisionS(self, index):
        if self._isDAAPIInited():
            return self.flashObject.as_setSelectedDivision(index)



    def as_setCreationEnabledS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setCreationEnabled(value)




+++ okay decompyling fortlistmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:27 CET
