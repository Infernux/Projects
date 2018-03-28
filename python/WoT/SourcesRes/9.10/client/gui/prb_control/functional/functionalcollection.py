# 2015.01.14 22:10:03 CET
import types
from debug_utils import LOG_ERROR
from gui.prb_control.items import FunctionalState, PlayerDecorator
from gui.prb_control.restrictions.interfaces import IGUIPermissions
from gui.prb_control.settings import FUNCTIONAL_ORDER

class FunctionalCollection(object):

    def __init__(self):
        super(FunctionalCollection, self).__init__()
        self.__items = {}



    def clear(self, woEvents = False):
        for item in self.__items.itervalues():
            if item is not None:
                item.fini(woEvents=woEvents)

        self.__items.clear()



    def reset(self):
        for item in self.__items.itervalues():
            if hasattr(item, 'reset'):
                item.reset()




    def getItem(self, ctrlType):
        result = None
        if ctrlType in self.__items:
            result = self.__items[ctrlType]
        return result



    def setItem(self, ctrlType, item, initParams = None):
        if ctrlType in self.__items:
            self.__items[ctrlType].fini()
        self.__items[ctrlType] = item
        if initParams is None or type(initParams) is not types.DictType:
            initParams = {}
        return item.init(**initParams)



    def addListener(self, listener):
        for item in self.__items.itervalues():
            item.addListener(listener)




    def removeListener(self, listener):
        for item in self.__items.itervalues():
            item.removeListener(listener)




    def hasModalEntity(self):
        for item in self.__items.itervalues():
            if item.hasEntity():
                return True

        return False



    def getState(self, factories):
        result = None
        for (ctrlType, item,) in self.__items.iteritems():
            if item and item.hasEntity():
                factory = factories.get(ctrlType)
                if factory:
                    result = factory.createStateEntity(item)
                    break

        if result is None:
            result = FunctionalState()
        return result



    def getPlayerInfo(self, factories):
        result = None
        for (ctrlType, item,) in self.__items.iteritems():
            if item and item.hasEntity():
                factory = factories.get(ctrlType)
                if factory:
                    result = factory.createPlayerInfo(item)
                    break

        if result is None:
            result = PlayerDecorator()
        return result



    def getGUIPermissions(self):
        permissions = IGUIPermissions()
        for item in self.__items.itervalues():
            if item and item.hasEntity() and hasattr(item, 'getPermissions'):
                permissions = item.getPermissions()
                break

        return permissions



    def canPlayerDoAction(self, afterGeneralChecking = False):
        if afterGeneralChecking:
            order = FUNCTIONAL_ORDER.AFTER_GENERAL_CHECKING
        else:
            order = FUNCTIONAL_ORDER.BEFORE_GENERAL_CHECKING
        for ctrlType in order:
            item = self.getItem(ctrlType)
            if not item:
                continue
            (canDo, restriction,) = item.canPlayerDoAction()
            if not canDo:
                return (canDo, restriction)

        return (True, '')



    def exitFromQueue(self):
        for ctrlType in FUNCTIONAL_ORDER.EXIT_FROM_QUEUE:
            item = self.getItem(ctrlType)
            if item and item.exitFromQueue():
                return 




    def doAction(self, dispatcher, action, factories):
        result = False
        state = self.getState(factories)
        if state.hasModalEntity:
            order = [state.ctrlTypeID]
        else:
            order = FUNCTIONAL_ORDER.ACTION
        for ctrlType in order:
            item = self.getItem(ctrlType)
            if item and item.doAction(action=action, dispatcher=dispatcher):
                result = True
                break

        return result



    def doSelectAction(self, action):
        result = False
        for item in self.__items.itervalues():
            if item and item.hasEntity():
                result = item.doSelectAction(action)
                break

        return result



    def getIterator(self):
        for ctrlType in FUNCTIONAL_ORDER.ENTRY:
            item = self.getItem(ctrlType)
            if item:
                yield item




    def getIteratorToLeave(self, factories):
        for ctrlType in FUNCTIONAL_ORDER.ENTRY:
            item = self.getItem(ctrlType)
            factory = factories.get(ctrlType)
            if factory:
                ctx = factory.createLeaveCtx()
            else:
                LOG_ERROR('Factory is not found', ctrlType)
                continue
            if item and ctx:
                yield (item, ctx)




    def canSendInvite(self, playerDBID):
        for func in self.getIterator():
            if func.getPermissions().canSendInvite():
                return True

        return False




+++ okay decompyling functionalcollection.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:10:03 CET
