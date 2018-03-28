# 2015.01.18 23:11:04 CET
from debug_utils import LOG_ERROR
from gui.prb_control.factories.ControlFactory import ControlFactory
from gui.prb_control.factories.PreQueueFactory import PreQueueFactory
from gui.prb_control.factories.PrebattleFactory import PrebattleFactory
from gui.prb_control.factories.UnitFactory import UnitFactory
from gui.prb_control.settings import CTRL_ENTITY_TYPE

class ControlFactoryDecorator(ControlFactory):

    def __init__(self):
        self.__factories = {CTRL_ENTITY_TYPE.PREBATTLE: PrebattleFactory(),
         CTRL_ENTITY_TYPE.UNIT: UnitFactory(),
         CTRL_ENTITY_TYPE.PREQUEUE: PreQueueFactory()}



    def start(self, dispatcher, ctx):
        setItem = dispatcher.getFunctionalCollection().setItem
        result = 0
        for (ctrlType, factory,) in self.__factories.iteritems():
            result |= setItem(ctrlType, factory.createFunctional(dispatcher, ctx))

        return result



    def clear(self):
        self.__factories.clear()



    def get(self, ctrlType):
        factory = None
        if ctrlType in self.__factories:
            factory = self.__factories[ctrlType]
        return factory



    def getIterator(self):
        return self.__factories.itervalues()



    def createEntry(self, ctx):
        item = None
        ctrlType = ctx.getCtrlType()
        if ctrlType in self.__factories:
            item = self.__factories[ctrlType].createEntry(ctx)
        else:
            LOG_ERROR('Entry factory is not found', ctx)
        return item



    def createEntryByAction(self, action):
        return self._search(action, 'createEntryByAction')



    def createFunctional(self, dispatcher, ctx):
        item = None
        ctrlType = ctx.getCtrlType()
        if ctrlType in self.__factories:
            item = self.__factories[ctrlType].createFunctional(dispatcher, ctx)
            dispatcher.getFunctionalCollection().setItem(ctrlType, item, ctx.getInitParams())
        else:
            LOG_ERROR('Functional factory is not found', ctrlType, ctx)
        ctx.clear()
        del ctx
        return item



    def _search(self, action, method):
        for factory in self.__factories.itervalues():
            result = getattr(factory, method)(action)
            if result:
                return result





+++ okay decompyling __init__.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.18 23:11:04 CET
