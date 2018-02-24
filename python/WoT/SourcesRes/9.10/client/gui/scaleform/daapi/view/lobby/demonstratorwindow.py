# 2015.01.14 22:14:35 CET
import ArenaType
from gui.Scaleform.daapi.view.meta.DemonstratorWindowMeta import DemonstratorWindowMeta
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView
from gui.Scaleform.framework.entities.View import View
from gui.prb_control.context import PrebattleAction
from gui.prb_control.dispatcher import g_prbLoader

class DemonstratorWindow(View, AbstractWindowView, DemonstratorWindowMeta):

    def _populate(self):
        super(DemonstratorWindow, self)._populate()
        maps = dict(ctf=[], assault=[], domination=[], nations=[])
        for (arenaTypeID, arenaType,) in ArenaType.g_cache.iteritems():
            if arenaType.explicitRequestOnly:
                continue
            if arenaType.gameplayName in maps:
                maps[arenaType.gameplayName].append({'id': arenaTypeID,
                 'name': arenaType.name,
                 'type': arenaType.gameplayName})

        sorting = lambda item: item['name']
        self.as_setDataS({'standard': sorted(maps['ctf'], key=sorting),
         'assault': sorted(maps['assault'], key=sorting),
         'encounter': sorted(maps['domination'], key=sorting),
         'nations': sorted(maps['nations'], key=sorting)})



    def onMapSelected(self, mapID):
        dispatcher = g_prbLoader.getDispatcher()
        if dispatcher is not None:
            dispatcher.doAction(PrebattleAction(None, mapID=mapID))
            self.onWindowClose()



    def onWindowClose(self):
        self.destroy()




+++ okay decompyling demonstratorwindow.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:14:35 CET
