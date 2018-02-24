# 2015.01.14 22:24:26 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortCreateDirectionWindowMeta(DAAPIModule):

    def openNewDirection(self):
        self._printOverrideError('openNewDirection')



    def closeDirection(self, id):
        self._printOverrideError('closeDirection')



    def as_setDescriptionS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setDescription(value)



    def as_setupButtonS(self, enabled, visible, ttHeader, ttDescr):
        if self._isDAAPIInited():
            return self.flashObject.as_setupButton(enabled, visible, ttHeader, ttDescr)



    def as_setDirectionsS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setDirections(data)




+++ okay decompyling fortcreatedirectionwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:26 CET
