# 2015.01.14 22:14:46 CET
from debug_utils import LOG_DEBUG
from gui.Scaleform.daapi.view.meta.CyberSportBaseViewMeta import CyberSportBaseViewMeta
__author__ = 'd_dichkovsky'

class CyberSportBaseView(CyberSportBaseViewMeta):

    def __init__(self):
        super(CyberSportBaseView, self).__init__()



    def canBeClosed(self, callback):
        callback(True)



    def setData(self, initialData):
        LOG_DEBUG('CyberSportBaseView.setItemId stub implementation. Passed id is:', initialData)




+++ okay decompyling cybersportbaseview.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:14:46 CET
