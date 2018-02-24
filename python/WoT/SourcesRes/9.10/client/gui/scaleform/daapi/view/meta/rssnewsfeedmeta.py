# 2015.01.14 22:24:31 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class RssNewsFeedMeta(DAAPIModule):

    def openBrowser(self, linkToOpen):
        self._printOverrideError('openBrowser')



    def as_updateFeedS(self, feed):
        if self._isDAAPIInited():
            return self.flashObject.as_updateFeed(feed)




+++ okay decompyling rssnewsfeedmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:31 CET
