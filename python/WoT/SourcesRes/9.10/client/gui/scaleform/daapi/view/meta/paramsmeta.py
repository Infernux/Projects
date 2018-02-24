# 2015.01.14 22:24:29 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ParamsMeta(DAAPIModule):

    def as_setValuesS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setValues(data)



    def as_highlightParamsS(self, type):
        if self._isDAAPIInited():
            return self.flashObject.as_highlightParams(type)




+++ okay decompyling paramsmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:29 CET
