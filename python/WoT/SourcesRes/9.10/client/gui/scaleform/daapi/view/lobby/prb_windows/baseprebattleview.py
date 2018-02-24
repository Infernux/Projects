# 2015.01.17 21:34:00 CET
from gui.Scaleform.daapi.view.meta.BasePrebattleViewMeta import BasePrebattleViewMeta
__author__ = 'a_ushyutsau'

class BasePrebattleView(BasePrebattleViewMeta):

    def __init__(self):
        super(BasePrebattleView, self).__init__()



    def canBeClosed(self, callback):
        callback(True)



    def _populate(self):
        super(BasePrebattleView, self)._populate()



    def _dispose(self):
        super(BasePrebattleView, self)._dispose()




+++ okay decompyling baseprebattleview.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.17 21:34:00 CET
