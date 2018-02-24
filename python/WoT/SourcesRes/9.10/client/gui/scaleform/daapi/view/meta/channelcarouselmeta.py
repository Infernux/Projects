# 2015.01.14 22:24:25 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ChannelCarouselMeta(DAAPIModule):

    def channelOpenClick(self, itemID):
        self._printOverrideError('channelOpenClick')



    def closeAll(self):
        self._printOverrideError('closeAll')



    def channelCloseClick(self, itemID):
        self._printOverrideError('channelCloseClick')



    def as_getDataProviderS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getDataProvider()



    def as_getBattlesDataProviderS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getBattlesDataProvider()




+++ okay decompyling channelcarouselmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:25 CET
