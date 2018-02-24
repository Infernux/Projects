# 2015.01.14 13:32:38 CET
import BigWorld

class OfflineEntity(BigWorld.Entity):

    def __init__(self):
        pass



    def prerequisites(self):
        return []



    def onEnterWorld(self, prereqs):
        pass



    def onLeaveWorld(self):
        pass




class PlayerOfflineEntity(BigWorld.Entity):

    def __init__(self):
        pass



    def prerequisites(self):
        return []



    def onEnterWorld(self, prereqs):
        pass



    def onLeaveWorld(self):
        pass



    def newFakeModel(self):
        return BigWorld.Model('objects/fake_model.model')



    def handleKeyEvent(self, event):
        return False




+++ okay decompyling offlineentity.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:32:38 CET
