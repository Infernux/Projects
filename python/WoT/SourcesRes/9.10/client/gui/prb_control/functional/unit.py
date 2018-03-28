# 2015.01.14 22:10:05 CET
import cgi
import time
from CurrentVehicle import g_currentVehicle
from UnitBase import UNIT_SLOT, INV_ID_CLEAR_VEHICLE, UNIT_ROLE, UNIT_ERROR
import account_helpers
from gui.prb_control.restrictions import createUnitActionValidator
from gui.shared.fortifications import getClientFortMgr
from messenger.ext import passCensor
from account_helpers.AccountSettings import AccountSettings
from adisp import process
from constants import PREBATTLE_TYPE, REQUEST_COOLDOWN
from debug_utils import LOG_ERROR, LOG_DEBUG, LOG_CURRENT_EXCEPTION
from gui import prb_control, DialogsInterface
from gui.Scaleform.daapi.view.dialogs import rally_dialog_meta
from gui.prb_control import settings
from gui.prb_control import isParentControlActivated
from gui.prb_control.context import unit_ctx
from gui.prb_control.ctrl_events import g_prbCtrlEvents
from gui.prb_control.functional import interfaces
from gui.prb_control.functional import unit_ext
from gui.prb_control.items import unit_items
from gui.prb_control.prb_cooldown import PrbCooldownManager
from gui.prb_control.restrictions.interfaces import IUnitPermissions
from gui.prb_control.restrictions.permissions import UnitPermissions
from gui.prb_control.settings import FUNCTIONAL_INIT_RESULT, FUNCTIONAL_EXIT, CTRL_ENTITY_TYPE, PREBATTLE_ACTION_NAME
from gui.shared import g_itemsCache, REQ_CRITERIA
from gui.shared.utils.ListenersCollection import ListenersCollection
from helpers import time_utils
from items import vehicles as core_vehicles
from gui.prb_control.events_dispatcher import g_eventDispatcher

class UnitIntro(interfaces.IPrbEntry):

    def __init__(self, prbType):
        super(UnitIntro, self).__init__()
        self._prbType = prbType



    def makeDefCtx(self):
        return unit_ctx.JoinModeCtx(self._prbType)



    def create(self, ctx, callback = None):
        raise Exception, 'UnitIntro is not create entity'



    def join(self, ctx, callback = None):
        if not prb_control.hasModalEntity() or ctx.isForced():
            g_prbCtrlEvents.onUnitIntroModeJoined(ctx.getPrbType(), ctx.getModeFlags())
            if callback:
                callback(True)
        else:
            LOG_ERROR('First, player has to confirm exit from the current prebattle/unit')
            if callback:
                callback(False)



    def select(self, ctx, callback = None):
        self.join(ctx, callback=callback)




class UnitEntry(interfaces.IPrbEntry):

    def __init__(self):
        super(UnitEntry, self).__init__()



    def create(self, ctx, callback = None):
        if not prb_control.hasModalEntity() or ctx.isForced():
            unitMgr = prb_control.getClientUnitMgr()
            if unitMgr:
                ctx.startProcessing(callback=callback)
                unitMgr.create()
            else:
                LOG_ERROR('Unit manager is not defined')
        else:
            LOG_ERROR('First, player has to confirm exit from the current prebattle/unit')
            if callback:
                callback(False)



    def join(self, ctx, callback = None):
        if not prb_control.hasModalEntity() or ctx.isForced():
            unitMgr = prb_control.getClientUnitMgr()
            if unitMgr:
                ctx.startProcessing(callback=callback)
                unitMgr.join(ctx.getID(), slotIdx=ctx.getSlotIdx())
            else:
                LOG_ERROR('Unit manager is not defined')
        else:
            LOG_ERROR('First, player has to confirm exit from the current prebattle/unit')
            if callback:
                callback(False)



    def select(self, ctx, callback = None):
        LOG_ERROR('Routine "select" can not be invoked for UnitEntry')




class FortBattleEntry(interfaces.IPrbEntry):

    def __init__(self):
        super(FortBattleEntry, self).__init__()



    def create(self, ctx, callback = None):
        if not prb_control.hasModalEntity() or ctx.isForced():
            fortMgr = getClientFortMgr()
            if fortMgr:
                ctx.startProcessing(callback=callback)
                fortMgr.createOrJoinFortBattle(ctx.getID(), slotIdx=ctx.getSlotIdx())
            else:
                LOG_ERROR('Fort provider is not defined')
        else:
            LOG_ERROR('First, player has to confirm exit from the current prebattle/unit')
            if callback:
                callback(False)



    def join(self, ctx, callback = None):
        if not prb_control.hasModalEntity() or ctx.isForced():
            fortMgr = getClientFortMgr()
            if fortMgr:
                ctx.startProcessing(callback=callback)
                fortMgr.createOrJoinFortBattle(ctx.getID(), slotIdx=ctx.getSlotIdx())
            else:
                LOG_ERROR('Fort provider is not defined')
        else:
            LOG_ERROR('First, player has to confirm exit from the current prebattle/unit')
            if callback:
                callback(False)



    def select(self, ctx, callback = None):
        LOG_ERROR('Routine "select" can not be invoked for FortBattleEntry')




class NoUnitFunctional(interfaces.IUnitFunctional):
    pass

class _UnitFunctional(ListenersCollection, interfaces.IUnitFunctional):

    def __init__(self, requestHandlers, listenerClass, prbType, rosterSettings):
        super(_UnitFunctional, self).__init__()
        self._exit = settings.FUNCTIONAL_EXIT.NO_FUNC
        self._listReq = None
        self._setListenerClass(listenerClass)
        self._requestHandlers = requestHandlers
        self._rosterSettings = rosterSettings
        self._searchHandler = None
        self._prbType = prbType
        self._hasEntity = False
        self._showLeadershipNotification = False



    def getExit(self):
        return self._exit



    def setExit(self, exit):
        if exit in settings.FUNCTIONAL_EXIT.UNIT_RANGE:
            self._exit = exit



    def showGUI(self):
        g_eventDispatcher.showUnitWindow(self._prbType)



    def setPrbType(self, prbType):
        self._prbType = prbType



    def getPrbType(self):
        return self._prbType



    def hasEntity(self):
        return self._hasEntity



    def getPlayerInfo(self, dbID = None, unitIdx = None):
        if dbID is None:
            dbID = account_helpers.getPlayerDatabaseID()
        (unitIdx, unit,) = self.getUnit(unitIdx=unitIdx)
        if unit:
            pInfo = self._buildPlayerInfo(unitIdx, unit, dbID, unit.getPlayerSlotIdx(dbID), unit.getPlayer(dbID))
        else:
            pInfo = unit_items.PlayerUnitInfo(dbID, unitIdx, unit)
        return pInfo



    def getReadyStates(self, unitIdx = None):
        (_, unit,) = self.getUnit(unitIdx=unitIdx)
        result = []
        if unit:
            isSlotClosed = unit.isSlotClosed
            isPlayerReady = unit.isPlayerReadyInSlot
            for slotIdx in self._rosterSettings.getAllSlotsRange():
                isClosed = isSlotClosed(slotIdx)
                result.append(isPlayerReady(slotIdx) if not isClosed else None)

        return result



    def getPermissions(self, dbID = None, unitIdx = None):
        pDbID = account_helpers.getPlayerDatabaseID()
        if dbID is None:
            dbID = pDbID
        (_, unit,) = self.getUnit(unitIdx=unitIdx, safe=True)
        if unit:
            isPlayerReady = False
            roles = 0
            players = unit.getPlayers()
            if dbID in players:
                roles |= players[dbID].get('role', roles)
                inSlots = unit.getPlayerSlots()
                if dbID in inSlots:
                    isPlayerReady = unit.isPlayerReadyInSlot(inSlots[dbID])
            return UnitPermissions(roles, unit._state, pDbID == dbID, isPlayerReady)
        else:
            return IUnitPermissions()



    def isCreator(self, dbID = None, unitIdx = None):
        if dbID is None:
            dbID = account_helpers.getPlayerDatabaseID()
        (_, unit,) = self.getUnit(unitIdx=unitIdx)
        if unit:
            result = UnitPermissions.isCreator(unit.getPlayers().get(dbID, {}).get('role', 0))
        else:
            result = False
        return result



    def getRosterSettings(self):
        return self._rosterSettings



    def getSlotState(self, slotIdx, unitIdx = None):
        (_, unit,) = self.getUnit(unitIdx=unitIdx)
        if unit:
            slotState = unit_items.SlotState(unit.isSlotClosed(slotIdx), unit.isSlotFree(slotIdx))
        else:
            slotState = unit_items.SlotState()
        return slotState



    def getPlayers(self, unitIdx = None):
        (unitIdx, unit,) = self.getUnit(unitIdx=unitIdx)
        result = {}
        if unit:
            slotGetter = unit.getPlayerSlotIdx
            players = unit.getPlayers()
            for (dbID, data,) in players.iteritems():
                result[dbID] = self._buildPlayerInfo(unitIdx, unit, dbID, slotGetter(dbID), data)

        return result



    def getCandidates(self, unitIdx = None):
        (unitIdx, unit,) = self.getUnit(unitIdx=unitIdx)
        if not unit:
            return {}
        players = unit.getPlayers()
        memberIDs = set((value['playerID'] for value in unit.getMembers().itervalues()))
        dbIDs = set(players.keys()).difference(memberIDs)
        result = {}
        for (dbID, data,) in players.iteritems():
            if dbID not in dbIDs:
                continue
            result[dbID] = unit_items.PlayerUnitInfo(dbID, unitIdx, unit, **data)

        return result



    def getRoster(self, unitIdx = None):
        (unitIdx, unit,) = self.getUnit(unitIdx=unitIdx)
        if unit:
            return unit.getRoster()



    def getVehicleInfo(self, dbID = None, unitIdx = None):
        if dbID is None:
            dbID = account_helpers.getPlayerDatabaseID()
        (_, unit,) = self.getUnit(unitIdx=unitIdx)
        if unit:
            vehicles = unit.getVehicles()
            if dbID in vehicles:
                result = unit_items.VehicleInfo(**vehicles[dbID])
            else:
                result = unit_items.VehicleInfo()
        else:
            result = unit_items.VehicleInfo()
        return result



    def getUnitFullData(self, unitIdx = None):
        (unitIdx, unit,) = self.getUnit(unitIdx=unitIdx)
        if not unit:
            return None
        dbID = account_helpers.getPlayerDatabaseID()
        pInfo = self._buildPlayerInfo(unitIdx, unit, dbID, unit.getPlayerSlotIdx(dbID), unit.getPlayer(dbID))
        unitState = self._buildState(unit)
        unitStats = self._buildStats(unitIdx, unit)
        slotsIter = self._getSlotsIterator(unitIdx, unit)
        return (unit,
         unitState,
         unitStats,
         pInfo,
         slotsIter)



    def getState(self, unitIdx = None):
        (_, unit,) = self.getUnit(unitIdx=unitIdx)
        if unit:
            unitState = self._buildState(unit)
        else:
            unitState = unit_items.UnitState(0)
        return unitState



    def getStats(self, unitIdx = None):
        (_, unit,) = self.getUnit(unitIdx=unitIdx)
        if not unit:
            return unit_items.UnitStats(0, 0, 0, 0, 0, [], 0, 0)
        return self._buildStats(unitIdx, unit)



    def getComment(self, unitIdx = None):
        (_, unit,) = self.getUnit(unitIdx=unitIdx)
        if unit:
            return unit.getComment()
        return ''



    def getCensoredComment(self, unitIdx = None):
        (_, unit,) = self.getUnit(unitIdx=unitIdx)
        if unit:
            pInfo = self.getPlayerInfo(unitIdx=unitIdx)
            if not pInfo.isCreator():
                return passCensor(unit.getComment())
            else:
                return unit.getComment()
        return ''



    def request(self, ctx, callback = None):
        requestType = ctx.getRequestType()
        if requestType in self._requestHandlers:
            LOG_DEBUG('Unit request', ctx)
            self._requestHandlers[requestType](ctx, callback=callback)
        else:
            LOG_ERROR('Handler not found', ctx)
            if callback:
                callback(False)



    @process
    def doLeaveAction(self, dispatcher, ctx = None):
        meta = self.getConfirmDialogMeta()
        if meta is not None:
            isConfirmed = yield DialogsInterface.showDialog(meta)
        else:
            isConfirmed = yield lambda callback: callback(True)
        if isConfirmed:
            if ctx is None:
                ctx = unit_ctx.LeaveUnitCtx(waitingID='prebattle/leave')
            if dispatcher._setRequestCtx(ctx):
                self.leave(ctx)



    def getSelectedVehicles(self, section, useAll = True):
        accSettings = dict(AccountSettings.getSettings('unitWindow'))
        vehicles = accSettings.get(section, [])
        if vehicles or not useAll:
            selectedVehicles = []
            for vehCD in vehicles:
                vehicle = g_itemsCache.items.getItemByCD(int(vehCD))
                if vehicle.isInInventory and not vehicle.rentalIsOver and not vehicle.isDisabledInPremIGR:
                    selectedVehicles.append(int(vehCD))

        else:
            criteria = REQ_CRITERIA.INVENTORY
            criteria |= ~REQ_CRITERIA.VEHICLE.DISABLED_IN_PREM_IGR
            criteria |= ~REQ_CRITERIA.VEHICLE.EXPIRED_RENT
            selectedVehicles = [ k for (k, v,) in g_itemsCache.items.getVehicles(criteria).iteritems() if v.level in self._rosterSettings.getLevelsRange() ]
        return selectedVehicles



    def setSelectedVehicles(self, section, vehicles):
        settings = dict(AccountSettings.getSettings('unitWindow'))
        settings[section] = vehicles
        AccountSettings.setSettings('unitWindow', settings)



    def getShowLeadershipNotification(self):
        return self._showLeadershipNotification



    def doLeadershipNotificationShown(self):
        self._showLeadershipNotification = False



    def _buildPlayerInfo(self, unitIdx, unit, dbID, slotIdx = -1, data = None):
        if data is None:
            data = {}
        if slotIdx != -1:
            isReady = unit.isPlayerReadyInSlot(slotIdx)
            isInSlot = True
        else:
            isReady = False
            isInSlot = False
        return unit_items.PlayerUnitInfo(dbID, unitIdx, unit, isReady=isReady, isInSlot=isInSlot, slotIdx=slotIdx, **data)



    def _buildState(self, unit):
        return unit_items.UnitState(unit.getState(), isReady=unit.arePlayersReady(ignored=[settings.CREATOR_SLOT_INDEX]))



    def _buildStats(self, unitIdx, unit):
        readyCount = 0
        occupiedSlotsCount = 0
        openedSlotsCount = 0
        curTotalLevel = unit.getPointsSum()
        freeSlotsCount = 0
        isReadyInSlot = unit.isPlayerReadyInSlot
        isSlotFree = unit.isSlotFree
        isSlotClosed = unit.isSlotClosed
        isCreator = self.isCreator(unitIdx=unitIdx)
        for slotIdx in self._rosterSettings.getAllSlotsRange():
            if isCreator and slotIdx == settings.CREATOR_SLOT_INDEX:
                readyCount += 1
            elif isReadyInSlot(slotIdx):
                readyCount += 1
            if not isSlotClosed(slotIdx):
                if not isSlotFree(slotIdx):
                    occupiedSlotsCount += 1
                else:
                    freeSlotsCount += 1
                openedSlotsCount += 1
            else:
                curTotalLevel += 1

        levelsSeq = map(lambda vehicle: vehicle.get('vehLevel', 0), unit.getVehicles().itervalues())
        levelsSeq.sort()
        return unit_items.UnitStats(readyCount, occupiedSlotsCount, openedSlotsCount, freeSlotsCount, curTotalLevel, levelsSeq, self._rosterSettings.getMinTotalLevel(), self._rosterSettings.getMaxTotalLevel())



    def _getSlotsIterator(self, unitIdx, unit):
        players = unit.getPlayers()
        members = unit.getMembers()
        vehicles = unit.getVehicles()
        isPlayerReady = unit.isPlayerReadyInSlot
        isSlotClosed = unit.isSlotClosed
        isSlotFree = unit.isSlotFree
        isSlotDisabled = unit.isSlotDisabled
        for slotIdx in self._rosterSettings.getAllSlotsRange():
            if isSlotDisabled(slotIdx):
                continue
            state = unit_items.SlotState(isSlotClosed(slotIdx), isSlotFree(slotIdx))
            player = None
            vehicle = None
            if not state.isFree and slotIdx in members:
                dbID = members[slotIdx].get('playerID', -1L)
                if dbID in players:
                    player = unit_items.PlayerUnitInfo(dbID, unitIdx, unit, isReady=isPlayerReady(slotIdx), isInSlot=True, slotIdx=slotIdx, **players[dbID])
                if dbID in vehicles:
                    vehicle = vehicles.get(dbID)
            yield unit_items.SlotInfo(slotIdx, state, player, vehicle)




    def _isParentControlActivated(self, callback = None):
        result = False
        if isParentControlActivated():
            g_eventDispatcher.showParentControlNotification()
            if callback:
                callback(False)
            result = True
        return result




class IntroFunctional(_UnitFunctional):

    def __init__(self, prbType, modeFlags, rosterSettings):
        RQ_TYPE = settings.REQUEST_TYPE
        handlers = {RQ_TYPE.AUTO_SEARCH: self.doAutoSearch,
         RQ_TYPE.ACCEPT_SEARCH: self.acceptSearch,
         RQ_TYPE.DECLINE_SEARCH: self.declineSearch}
        super(IntroFunctional, self).__init__(handlers, interfaces.IIntroUnitListener, prbType, rosterSettings)
        self._modeFlags = modeFlags



    def init(self):
        self._hasEntity = True
        self._searchHandler = unit_ext.UnitAutoSearchHandler(self)
        self._searchHandler.init()
        g_eventDispatcher.loadUnit(self._prbType, self._modeFlags)
        for listener in self._listeners:
            listener.onIntroUnitFunctionalInited()

        g_eventDispatcher.updateUI()
        return FUNCTIONAL_INIT_RESULT.INITED | FUNCTIONAL_INIT_RESULT.LOAD_WINDOW



    def fini(self, woEvents = False):
        if self._searchHandler is not None:
            self._searchHandler.fini()
            self._searchHandler = None
        self._requestHandlers.clear()
        self._hasEntity = False
        for listener in self._listeners:
            listener.onIntroUnitFunctionalFinished()

        if self._exit != settings.FUNCTIONAL_EXIT.UNIT:
            g_eventDispatcher.unloadUnit(self._prbType)
            g_eventDispatcher.updateUI()
        unit_ext.destroyListReq()



    def canPlayerDoAction(self):
        return (not self._hasEntity, '')



    def getUnit(self, unitIdx = None, safe = False):
        if unitIdx is None and not safe:
            LOG_ERROR('Unit index is not defined')
            return (None, None)
        return unit_ext.getUnitFromStorage(self._prbType, unitIdx)



    def getConfirmDialogMeta(self, funcExit = FUNCTIONAL_EXIT.NO_FUNC):
        return rally_dialog_meta.createUnitIntroLeaveMeta(funcExit, self._prbType)



    def isPlayerJoined(self, ctx):
        result = False
        if isinstance(ctx, unit_ctx.JoinModeCtx):
            result = ctx.getPrbType() == self._prbType
            self._modeFlags = ctx.getModeFlags()
        return result



    def showGUI(self):
        g_eventDispatcher.showUnitWindow(self._prbType, self._modeFlags)



    def initEvents(self, listener):
        if listener in self._listeners:
            if self._searchHandler:
                self._searchHandler.initEvents(listener)
        else:
            LOG_ERROR('Listener not found', listener)



    def reset(self):
        if self._searchHandler and self._searchHandler.isInSearch():
            self._searchHandler.stop()



    def leave(self, ctx, callback = None):
        self._exit = ctx.getFuncExit()
        g_prbCtrlEvents.onUnitIntroModeLeft()
        if callback:
            callback(True)



    def doSelectAction(self, action):
        result = False
        if action.actionName == PREBATTLE_ACTION_NAME.FORT and self._prbType in [PREBATTLE_TYPE.SORTIE, PREBATTLE_TYPE.FORT_BATTLE]:
            g_eventDispatcher.showUnitWindow(self._prbType)
            result = True
        return result



    def doAutoSearch(self, ctx, callback = None):
        if ctx.isRequestToStart():
            if self._isParentControlActivated(callback=callback):
                return 
            result = self._searchHandler.start(ctx.getVehTypes())
        else:
            result = self._searchHandler.stop()
        if callback:
            callback(result)



    def acceptSearch(self, _, callback = None):
        result = self._searchHandler.accept()
        if callback:
            callback(result)



    def declineSearch(self, _, callback = None):
        result = self._searchHandler.decline()
        if callback:
            callback(result)




class UnitFunctional(_UnitFunctional):

    def __init__(self, prbType, rosterSettings):
        RQ_TYPE = settings.REQUEST_TYPE
        handlers = {RQ_TYPE.ASSIGN: self.assign,
         RQ_TYPE.LOCK: self.lock,
         RQ_TYPE.CHANGE_OPENED: self.changeOpened,
         RQ_TYPE.CHANGE_COMMENT: self.changeComment,
         RQ_TYPE.SET_VEHICLE: self.setVehicle,
         RQ_TYPE.SET_PLAYER_STATE: self.setPlayerReady,
         RQ_TYPE.SET_ROSTERS_SLOTS: self.setRostersSlots,
         RQ_TYPE.CLOSE_SLOT: self.closeSlot,
         RQ_TYPE.SEND_INVITE: self.invite,
         RQ_TYPE.KICK: self.kick,
         RQ_TYPE.AUTO_SEARCH: self.doAutoSearch,
         RQ_TYPE.BATTLE_QUEUE: self.doBattleQueue,
         RQ_TYPE.GIVE_LEADERSHIP: self.giveLeadership}
        super(UnitFunctional, self).__init__(handlers, interfaces.IUnitListener, prbType, rosterSettings)
        self._requestsProcessor = None
        self._vehiclesWatcher = None
        self._lastErrorCode = UNIT_ERROR.OK
        self._cooldown = PrbCooldownManager()
        self._actionValidator = createUnitActionValidator(prbType, rosterSettings)
        self._deferredReset = False



    def canPlayerDoAction(self):
        return self._actionValidator.canDoAction(self)



    def init(self):
        self._hasEntity = True
        state = self.getState()
        g_eventDispatcher.loadHangar()
        g_eventDispatcher.loadUnit(self._prbType)
        self._requestsProcessor = unit_ext.UnitRequestProcessor(self)
        self._requestsProcessor.init()
        self._vehiclesWatcher = unit_ext.InventoryVehiclesWatcher(self)
        self._vehiclesWatcher.init()
        self._addClientUnitListeners()
        idle = state.isInIdle()
        if idle:
            timeLeftInIdle = self._getTimeLeftInIdle()
        else:
            timeLeftInIdle = 0
        for listener in self._listeners:
            listener.onUnitFunctionalInited()
            if idle:
                g_eventDispatcher.setUnitProgressInCarousel(self._prbType, True)
                listener.onUnitStateChanged(state, timeLeftInIdle)

        unit_ext.destroyListReq()
        g_eventDispatcher.updateUI()
        return FUNCTIONAL_INIT_RESULT.INITED | FUNCTIONAL_INIT_RESULT.LOAD_WINDOW



    def fini(self, woEvents = False):
        self._requestHandlers.clear()
        self._hasEntity = False
        if not woEvents:
            try:
                for listener in self._listeners:
                    listener.onUnitFunctionalFinished()

            except:
                LOG_CURRENT_EXCEPTION()
        if self._requestsProcessor:
            self._requestsProcessor.fini()
            self._requestsProcessor = None
        if self._vehiclesWatcher:
            self._vehiclesWatcher.fini()
            self._vehiclesWatcher = None
        self._removeClientUnitListeners()
        if self._exit == settings.FUNCTIONAL_EXIT.INTRO_UNIT:
            g_eventDispatcher.requestToDestroyPrbChannel(PREBATTLE_TYPE.UNIT)
            return 
        if not woEvents:
            g_eventDispatcher.unloadUnit(self._prbType)
        else:
            g_eventDispatcher.removeUnitFromCarousel(self._prbType)
            g_eventDispatcher.requestToDestroyPrbChannel(PREBATTLE_TYPE.UNIT)
        g_eventDispatcher.updateUI()
        self._deferredReset = False



    def rejoin(self):
        self._addClientUnitListeners()
        LOG_DEBUG('onUnitRejoin')
        for listener in self._listeners:
            listener.onUnitRejoin()




    def initEvents(self, listener):
        if listener in self._listeners:
            state = self.getState()
            if state.isInIdle():
                g_eventDispatcher.setUnitProgressInCarousel(self._prbType, True)
                listener.onUnitStateChanged(state, self._getTimeLeftInIdle())
        else:
            LOG_ERROR('Listener not found', listener)



    def isPlayerJoined(self, ctx):
        result = ctx.getCtrlType() is settings.CTRL_ENTITY_TYPE.UNIT and ctx.getID() == self.getID()
        if result and hasattr(ctx, 'getPrbType'):
            result = ctx.getPrbType() == self._prbType
        return result



    def setLastError(self, errorCode):
        self._lastErrorCode = errorCode



    def isKicked(self):
        return self._lastErrorCode in [UNIT_ERROR.KICKED_CANDIDATE, UNIT_ERROR.KICKED_PLAYER, UNIT_ERROR.CLAN_CHANGED]



    def getConfirmDialogMeta(self, funcExit = FUNCTIONAL_EXIT.NO_FUNC):
        if self.hasLockedState():
            meta = rally_dialog_meta.RallyLeaveDisabledDialogMeta(CTRL_ENTITY_TYPE.UNIT, self._prbType)
        else:
            meta = rally_dialog_meta.createUnitLeaveMeta(funcExit, self._prbType)
        return meta



    def getID(self):
        return prb_control.getUnitMgrID()



    def getUnitIdx(self):
        return prb_control.getUnitIdx()



    def setExit(self, exit):
        allowToStoreExit = True
        if self.getState().isSortie():
            pInfo = self.getPlayerInfo()
            if pInfo.isLegionary():
                allowToStoreExit = False
        if allowToStoreExit:
            super(UnitFunctional, self).setExit(exit)



    def getUnit(self, unitIdx = None, safe = False):
        if unitIdx is None:
            unitIdx = self.getUnitIdx()
        return (unitIdx, prb_control.getUnit(unitIdx, safe=True))



    def hasLockedState(self):
        return self.getState().isInIdle() and self.getPlayerInfo().isInSlot



    def isVehicleReadyToBattle(self):
        vInfo = self.getVehicleInfo()
        return not vInfo.isEmpty() and vInfo.isReadyToBattle()



    def validateLevels(self, stats = None, state = None, vInfo = None):
        stats = stats or self.getStats()
        state = state or self.getState()
        vInfo = vInfo or self.getVehicleInfo()
        return (self._actionValidator.canCreatorDoAction(stats, state, vInfo)[0], self._actionValidator.getRestrictionByLevel(stats, state))



    def getUnitInvalidLevels(self, stats = None):
        return self._actionValidator.getUnitInvalidLevels(stats or self.getStats())



    def leave(self, ctx, callback = None):
        ctx.startProcessing(callback)
        self.setExit(ctx.getFuncExit())
        unitMgr = prb_control.getClientUnitMgr()
        unitMgr.leave()



    def assign(self, ctx, callback = None):
        slotIdx = ctx.getSlotIdx()
        dbID = ctx.getPlayerID()
        pInfo = self.getPlayerInfo(dbID=dbID)
        if pInfo.dbID == -1:
            LOG_ERROR('Player is not in unit', ctx)
            if callback:
                callback(False)
            return 
        if pInfo.isCreator() and slotIdx != settings.CREATOR_SLOT_INDEX:
            LOG_ERROR('Creator can be in given slot only', ctx, settings.CREATOR_SLOT_INDEX)
            if callback:
                callback(False)
            return 
        if slotIdx == UNIT_SLOT.REMOVE:
            self._unassign(ctx, callback=callback)
        elif slotIdx == UNIT_SLOT.ANY:
            if pInfo.isInSlot:
                LOG_DEBUG('Player already assigned to slot', ctx)
                if callback:
                    callback(True)
                return 
            self._assign(ctx, callback=callback)
        elif slotIdx not in self._rosterSettings.getAllSlotsRange():
            LOG_ERROR('Index of slot is invalid', ctx)
            if callback:
                callback(False)
            return 
        if not pInfo.isCreator() and slotIdx == settings.CREATOR_SLOT_INDEX:
            LOG_ERROR('In slot can be creator only', ctx)
            if callback:
                callback(False)
            return 
        if pInfo.isInSlot or not self.getSlotState(slotIdx).isFree:
            if pInfo.slotIdx == slotIdx:
                LOG_DEBUG('Player already assigned to slot', ctx)
                if callback:
                    callback(True)
                return 
            self._reassign(ctx, callback=callback)
        else:
            self._assign(ctx, callback=callback)



    def invite(self, ctx, callback = None):
        pPermissions = self.getPermissions()
        if not pPermissions.canSendInvite():
            LOG_ERROR('Player can not send invites', pPermissions)
            if callback:
                callback(False)
            return 
        self._requestsProcessor.doRequest(ctx, 'invite', ctx.getDatabaseIDs(), ctx.getComment())
        self._cooldown.process(settings.REQUEST_TYPE.SEND_INVITE, coolDown=REQUEST_COOLDOWN.PREBATTLE_INVITES)



    def kick(self, ctx, callback = None):
        pPermissions = self.getPermissions()
        if not pPermissions.canKick():
            LOG_ERROR('Player can not can another players', pPermissions)
            if callback:
                callback(False)
            return 
        self._requestsProcessor.doRequest(ctx, 'kick', ctx.getPlayerID())



    def setVehicle(self, ctx, callback = None):
        pPermissions = self.getPermissions()
        if not pPermissions.canSetVehicle():
            LOG_ERROR('Player can not set vehicle', pPermissions)
            if callback:
                callback(False)
            return 
        if ctx.getVehTypeCD() or ctx.getVehInvID():
            self._setVehicle(ctx, callback=callback)
        else:
            self._clearVehicle(ctx, callback=callback)



    def setPlayerReady(self, ctx, callback = None):
        isReady = ctx.isReady()
        pInfo = self.getPlayerInfo()
        if isReady and self._isParentControlActivated(callback=callback):
            return 
        if not pInfo.isInSlot:
            LOG_ERROR('Player is not in slot', ctx)
            if callback:
                callback(False)
            return 
        if pInfo.isReady is isReady:
            LOG_DEBUG('Player already ready', ctx)
            if callback:
                callback(True)
            return 
        if not self.isVehicleReadyToBattle():
            LOG_DEBUG('Vehicle is not ready to battle', ctx)
            if callback:
                callback(False)
            return 
        if isReady:
            vehInfo = self.getVehicleInfo()
            g_currentVehicle.selectVehicle(vehInfo.vehInvID)
        if self._isInCoolDown(settings.REQUEST_TYPE.SET_PLAYER_STATE):
            return 
        pPermissions = self.getPermissions()
        if not pPermissions.canSetReady():
            LOG_ERROR('Player can not set ready state', pPermissions)
            if callback:
                callback(False)
            return 
        self._requestsProcessor.doRequest(ctx, 'setReady', isReady)
        self._cooldown.process(settings.REQUEST_TYPE.SET_PLAYER_STATE)



    def closeSlot(self, ctx, callback = None):
        if self._isInCoolDown(settings.REQUEST_TYPE.CLOSE_SLOT):
            return 
        slotIdx = ctx.getSlotIdx()
        rosterSettings = self.getRosterSettings()
        if slotIdx not in rosterSettings.getPlayersSlotsRange():
            LOG_ERROR('Index of slot is invalid', ctx)
            if callback:
                callback(False)
            return 
        if not 1 << slotIdx & settings.UNIT_CLOSED_SLOTS_MASK:
            LOG_ERROR('Player can close given slot', ctx)
            if callback:
                callback(False)
            return 
        isClosed = ctx.isClosed()
        slotState = self.getSlotState(slotIdx)
        if isClosed:
            if slotState.isClosed:
                LOG_DEBUG('Slot already is closed', ctx)
                if callback:
                    callback(True)
                return 
            if not slotState.isFree:
                LOG_ERROR('Player can close a free slot', ctx)
                if callback:
                    callback(False)
                return 
        elif not slotState.isClosed:
            LOG_DEBUG('Slot already is opened', ctx)
            if callback:
                callback(True)
            return 
        pPermissions = self.getPermissions()
        if not pPermissions.canChangeClosedSlots():
            LOG_ERROR('Player can not change closed slots', pPermissions)
            if callback:
                callback(False)
            return 
        self._requestsProcessor.doRequest(ctx, 'closeSlot', slotIdx, isClosed, unitIdx=ctx.getUnitIdx())
        self._cooldown.process(settings.REQUEST_TYPE.CLOSE_SLOT)



    def changeOpened(self, ctx, callback = None):
        isOpened = self.getState().isOpened()
        if isOpened is ctx.isOpened():
            LOG_DEBUG('Unit already is opened/closed', ctx)
            if callback:
                callback(True)
            return 
        if self._isInCoolDown(settings.REQUEST_TYPE.CHANGE_UNIT_STATE):
            return 
        pPermissions = self.getPermissions()
        if not pPermissions.canChangeUnitState():
            LOG_ERROR('Player can not change unit state', pPermissions)
            if callback:
                callback(False)
            return 
        self._requestsProcessor.doRequest(ctx, 'openUnit', isOpen=ctx.isOpened(), unitIdx=ctx.getUnitIdx())
        self._cooldown.process(settings.REQUEST_TYPE.CHANGE_UNIT_STATE)



    def changeComment(self, ctx, callback = None):
        (_, unit,) = self.getUnit()
        if not ctx.isCommentChanged(unit):
            if callback:
                callback(False)
            return 
        if self._isInCoolDown(settings.REQUEST_TYPE.CHANGE_UNIT_STATE):
            return 
        pPermissions = self.getPermissions()
        if not pPermissions.canChangeComment():
            LOG_ERROR('Player can not change comment', pPermissions)
            if callback:
                callback(False)
            return 
        self._requestsProcessor.doRequest(ctx, 'setComment', cgi.escape(ctx.getComment()), unitIdx=ctx.getUnitIdx())
        self._cooldown.process(settings.REQUEST_TYPE.CHANGE_UNIT_STATE)



    def lock(self, ctx, callback = None):
        isLocked = self.getState().isLocked()
        if isLocked is ctx.isLocked():
            LOG_DEBUG('Unit already is locked/unlocked', ctx)
            if callback:
                callback(True)
            return 
        if self._isInCoolDown(settings.REQUEST_TYPE.CHANGE_UNIT_STATE):
            return 
        pPermissions = self.getPermissions()
        if not pPermissions.canChangeUnitState():
            LOG_ERROR('Player can not change unit state', pPermissions)
            if callback:
                callback(False)
            return 
        self._requestsProcessor.doRequest(ctx, 'lockUnit', isLocked=ctx.isLocked(), unitIdx=ctx.getUnitIdx())
        self._cooldown.process(settings.REQUEST_TYPE.CHANGE_UNIT_STATE)



    def setRostersSlots(self, ctx, callback = None):
        pPermissions = self.getPermissions()
        if not pPermissions.canChangeRosters():
            LOG_ERROR('Player can not change rosters', pPermissions)
            if callback:
                callback(False)
            return 
        self._requestsProcessor.doRequest(ctx, 'setAllRosterSlots', ctx.getRosterSlots(), unitIdx=ctx.getUnitIdx())



    def doAutoSearch(self, ctx, callback = None):
        pPermissions = self.getPermissions()
        if not pPermissions.canInvokeAutoSearch():
            LOG_ERROR('Player can not start/stop auto search', pPermissions)
            if callback:
                callback(False)
            return 
        state = self.getState()
        if state.isSortie():
            LOG_ERROR('Auto search is not enabled in sortie')
            if callback:
                callback(False)
            return 
        if ctx.isRequestToStart():
            if self._isParentControlActivated(callback=callback):
                return 
            if state.isInSearch():
                LOG_DEBUG('Unit already started auto search')
                if callback:
                    callback(True)
                return 
            if not self.isVehicleReadyToBattle():
                LOG_ERROR('Vehicle is not ready to battle', ctx)
                if callback:
                    callback(False)
                return 
            vehInfo = self.getVehicleInfo()
            g_currentVehicle.selectVehicle(vehInfo.vehInvID)
            stats = self.getStats()
            if stats.curTotalLevel >= stats.maxTotalLevel:
                LOG_ERROR('Total level is invalid', stats)
                if callback:
                    callback(False)
                return 
            self._requestsProcessor.doRequest(ctx, 'startAutoSearch')
        elif not state.isInSearch():
            LOG_DEBUG('Unit did not start auto search')
            if callback:
                callback(True)
        else:
            self._requestsProcessor.doRequest(ctx, 'stopAutoSearch')



    def doBattleQueue(self, ctx, callback = None):
        pPermissions = self.getPermissions()
        state = self.getState()
        if ctx.isRequestToStart():
            if self._isParentControlActivated(callback=callback):
                return 
            if not pPermissions.canStartBattleQueue():
                LOG_ERROR('Player can not start battle queue', pPermissions)
                if callback:
                    callback(False)
                return 
            if state.isInQueue():
                LOG_DEBUG('Unit already started battle queue')
                if callback:
                    callback(True)
                return 
            if not state.isReady():
                LOG_DEBUG('team have player who status is "not ready"', ctx)
                if callback:
                    callback(False)
                return 
            if not self.isVehicleReadyToBattle():
                LOG_ERROR('Vehicle is not ready to battle', ctx)
                if callback:
                    callback(False)
                return 
            vehInfo = self.getVehicleInfo()
            g_currentVehicle.selectVehicle(vehInfo.vehInvID)
            stats = self.getStats()
            if stats.curTotalLevel > stats.maxTotalLevel:
                LOG_ERROR('Total level is invalid', stats)
                if callback:
                    callback(False)
                return 
            self._requestsProcessor.doRequest(ctx, 'startBattle')
        elif not pPermissions.canStopBattleQueue():
            LOG_ERROR('Player can not stop battle queue', pPermissions)
            if callback:
                callback(False)
            return 
        if not state.isInQueue():
            LOG_DEBUG('Unit did not start battle queue')
            if callback:
                callback(True)
        else:
            self._requestsProcessor.doRequest(ctx, 'stopBattle')



    def reset(self):
        state = self.getState()
        if self.isCreator() and state.isInSearch():
            self._requestsProcessor.doRawRequest('stopAutoSearch')
        elif self.getPlayerInfo().isReady:
            if not state.isInIdle():
                self._requestsProcessor.doRawRequest('setReady', False)
            else:
                self._deferredReset = True
        g_eventDispatcher.updateUI()



    def doSelectAction(self, action):
        result = False
        if action.actionName == PREBATTLE_ACTION_NAME.FORT and self._prbType in [PREBATTLE_TYPE.SORTIE, PREBATTLE_TYPE.FORT_BATTLE]:
            g_eventDispatcher.showUnitWindow(self._prbType)
            result = True
        return result



    def doAction(self, action = None, dispatcher = None):
        if super(UnitFunctional, self).doAction(action, dispatcher):
            return True
        if self.isCreator():
            stats = self.getStats()
            if stats.freeSlotsCount > self._rosterSettings.getMaxEmptySlots():
                if self._isParentControlActivated():
                    return 
                if self.getState().isDevMode():
                    DialogsInterface.showDialog(rally_dialog_meta.UnitConfirmDialogMeta(PREBATTLE_TYPE.UNIT, 'startBattle'), lambda result: (self.doBattleQueue(unit_ctx.BattleQueueUnitCtx('prebattle/battle_queue')) if result else None))
                else:
                    ctx = unit_ctx.AutoSearchUnitCtx('prebattle/auto_search')
                    LOG_DEBUG('Unit request', ctx)
                    self.doAutoSearch(ctx)
            else:
                ctx = unit_ctx.BattleQueueUnitCtx('prebattle/battle_queue')
                LOG_DEBUG('Unit request', ctx)
                self.doBattleQueue(ctx)
        else:
            isReady = not self.getPlayerInfo().isReady
            if isReady:
                waitingID = 'prebattle/player_ready'
            else:
                waitingID = 'prebattle/player_not_ready'
            ctx = unit_ctx.SetReadyUnitCtx(isReady, waitingID)
            LOG_DEBUG('Unit request', ctx)
            self.setPlayerReady(ctx)
        return True



    def giveLeadership(self, ctx, callback = None):
        pPermissions = self.getPermissions()
        if not pPermissions.canGiveLeadership():
            LOG_ERROR('Player can not give leadership to player players', pPermissions)
            if callback:
                callback(False)
            return 
        otherPPermissions = self.getPermissions(ctx.getPlayerID())
        if not otherPPermissions.canTakeLeadership():
            LOG_ERROR('Player can not take leadership', pPermissions)
            if callback:
                callback(False)
            return 
        self._requestsProcessor.doRequest(ctx, 'giveLeadership', ctx.getPlayerID())



    def unit_onUnitStateChanged(self, prevState, nextState):
        (_, unit,) = self.getUnit()
        isReady = unit.arePlayersReady(ignored=[settings.CREATOR_SLOT_INDEX])
        state = unit_items.UnitState(nextState, prevState, isReady)
        if state.isInIdle():
            timeLeftInIdle = self._getTimeLeftInIdle()
            g_eventDispatcher.setUnitProgressInCarousel(self._prbType, True)
        else:
            timeLeftInIdle = 0
            g_eventDispatcher.setUnitProgressInCarousel(self._prbType, False)
        LOG_DEBUG('onUnitStateChanged', state, timeLeftInIdle)
        if not state.isInIdle() and self._deferredReset:
            self._deferredReset = False
            self.reset()
        for listener in self._listeners:
            listener.onUnitStateChanged(state, timeLeftInIdle)

        g_eventDispatcher.updateUI()



    def unit_onUnitVehicleChanged(self, dbID, vehInvID, vehTypeCD):
        if vehTypeCD:
            (_, nationID, itemID,) = core_vehicles.parseIntCompactDescr(vehTypeCD)
            vehLevel = core_vehicles.g_cache.vehicle(nationID, itemID).level
        else:
            vehLevel = 0
        vInfo = unit_items.VehicleInfo(vehInvID, vehTypeCD, vehLevel)
        LOG_DEBUG('onUnitVehicleChanged', dbID, vInfo)
        if dbID == account_helpers.getPlayerDatabaseID() and not vInfo.isEmpty():
            vehicle = g_itemsCache.items.getItemByCD(vInfo.vehTypeCD)
            if vehicle is not None:
                g_currentVehicle.selectVehicle(vehicle.invID)
        for listener in self._listeners:
            listener.onUnitVehicleChanged(dbID, vInfo)

        g_eventDispatcher.updateUI()



    def unit_onUnitReadyMaskChanged(self, prevMask, nextMask):
        (unitIdx, unit,) = self.getUnit()
        isReadyInSlot = unit.isPlayerReadyInSlot
        members = unit.getMembers()
        players = unit.getPlayers()
        diff = []
        for slotIdx in self._rosterSettings.getAllSlotsRange():
            prevValue = isReadyInSlot(slotIdx, mask=prevMask)
            nextValue = isReadyInSlot(slotIdx, mask=nextMask)
            if prevValue is not nextValue:
                if slotIdx not in members:
                    continue
                dbID = members[slotIdx]['playerID']
                data = players.get(dbID, {})
                pInfo = unit_items.PlayerUnitInfo(dbID, unitIdx, unit, isReady=nextValue, isInSlot=True, slotIdx=slotIdx, **data)
                diff.append(pInfo)

        LOG_DEBUG('onUnitPlayerStateChanged', diff)
        for listener in self._listeners:
            for pInfo in diff:
                listener.onUnitPlayerStateChanged(pInfo)


        g_eventDispatcher.updateUI()



    def unit_onUnitPlayerRoleChanged(self, playerID, prevRoleFlags, nextRoleFlags):
        pInfo = self.getPlayerInfo(dbID=playerID)
        pPermissions = self.getPermissions(dbID=playerID)
        diff = prevRoleFlags ^ nextRoleFlags
        isOnlineChanged = diff & UNIT_ROLE.OFFLINE > 0
        isCreatorChanged = diff & UNIT_ROLE.COMMANDER_UPDATES > 0
        inArenaChanged = diff & UNIT_ROLE.IN_ARENA > 0
        LOG_DEBUG('onUnitPlayerRolesChanged', pInfo, pPermissions)
        for listener in self._listeners:
            if isOnlineChanged:
                listener.onUnitPlayerOnlineStatusChanged(pInfo)
            if isCreatorChanged:
                if pInfo.isCurrentPlayer():
                    self._showLeadershipNotification = True
                listener.onUnitPlayerBecomeCreator(pInfo)
            if inArenaChanged:
                listener.onUnitPlayerEnterOrLeaveArena(pInfo)
            listener.onUnitPlayerRolesChanged(pInfo, pPermissions)

        g_eventDispatcher.updateUI()



    def unit_onUnitPlayerAdded(self, playerID, playerData):
        (unitIdx, unit,) = self.getUnit()
        pInfo = self._buildPlayerInfo(unitIdx, unit, playerID, unit.getPlayerSlotIdx(playerID), playerData)
        self._invokeListeners('onUnitPlayerAdded', pInfo)



    def unit_onUnitPlayerInfoChanged(self, playerID, playerData):
        (unitIdx, unit,) = self.getUnit()
        pInfo = self._buildPlayerInfo(unitIdx, unit, playerID, unit.getPlayerSlotIdx(playerID), playerData)
        self._invokeListeners('onUnitPlayerInfoChanged', pInfo)



    def unit_onUnitPlayerRemoved(self, playerID, playerData):
        (unitIdx, unit,) = self.getUnit()
        pInfo = self._buildPlayerInfo(unitIdx, unit, playerID, -1, playerData)
        self._invokeListeners('onUnitPlayerRemoved', pInfo)



    def unit_onUnitSettingChanged(self, opCode, value):
        self._invokeListeners('onUnitSettingChanged', opCode, value)



    def unit_onUnitRosterChanged(self):
        self._vehiclesWatcher.validate()
        self._invokeListeners('onUnitRosterChanged')



    def unit_onUnitMembersListChanged(self):
        self._invokeListeners('onUnitMembersListChanged')
        g_eventDispatcher.updateUI()



    def unit_onUnitPlayersListChanged(self):
        self._invokeListeners('onUnitPlayersListChanged')



    def unit_onUnitPlayerVehDictChanged(self, playerID):
        (unitIdx, unit,) = self.getUnit()
        pInfo = self._buildPlayerInfo(unitIdx, unit, playerID, unit.getPlayerSlotIdx(playerID), unit.getPlayer(playerID))
        self._invokeListeners('onUnitPlayerVehDictChanged', pInfo)



    def _addClientUnitListeners(self):
        unit = prb_control.getUnit(self.getUnitIdx())
        unit.onUnitStateChanged += self.unit_onUnitStateChanged
        unit.onUnitReadyMaskChanged += self.unit_onUnitReadyMaskChanged
        unit.onUnitVehicleChanged += self.unit_onUnitVehicleChanged
        unit.onUnitSettingChanged += self.unit_onUnitSettingChanged
        unit.onUnitPlayerRoleChanged += self.unit_onUnitPlayerRoleChanged
        unit.onUnitMembersListChanged += self.unit_onUnitMembersListChanged
        unit.onUnitPlayersListChanged += self.unit_onUnitPlayersListChanged
        unit.onUnitRosterChanged += self.unit_onUnitRosterChanged
        unit.onUnitPlayerVehDictChanged += self.unit_onUnitPlayerVehDictChanged
        unit.onUnitPlayerAdded += self.unit_onUnitPlayerAdded
        unit.onUnitPlayerRemoved += self.unit_onUnitPlayerRemoved
        unit.onUnitPlayerInfoChanged += self.unit_onUnitPlayerInfoChanged



    def _removeClientUnitListeners(self):
        unit = prb_control.getUnit(self.getUnitIdx(), safe=True)
        if unit:
            unit.onUnitStateChanged -= self.unit_onUnitStateChanged
            unit.onUnitReadyMaskChanged -= self.unit_onUnitReadyMaskChanged
            unit.onUnitVehicleChanged -= self.unit_onUnitVehicleChanged
            unit.onUnitSettingChanged -= self.unit_onUnitSettingChanged
            unit.onUnitPlayerRoleChanged -= self.unit_onUnitPlayerRoleChanged
            unit.onUnitMembersListChanged -= self.unit_onUnitMembersListChanged
            unit.onUnitPlayersListChanged -= self.unit_onUnitPlayersListChanged
            unit.onUnitRosterChanged -= self.unit_onUnitRosterChanged
            unit.onUnitPlayerVehDictChanged -= self.unit_onUnitPlayerVehDictChanged
            unit.onUnitPlayerAdded -= self.unit_onUnitPlayerAdded
            unit.onUnitPlayerRemoved -= self.unit_onUnitPlayerRemoved
            unit.onUnitPlayerInfoChanged -= self.unit_onUnitPlayerInfoChanged



    def _unassign(self, ctx, callback = None):
        slotIdx = ctx.getSlotIdx()
        dbID = ctx.getPlayerID()
        pPermissions = self.getPermissions()
        if not pPermissions.canAssignToSlot(dbID):
            LOG_ERROR('Player can not unassign from slot', pPermissions)
            if callback:
                callback(False)
            return 
        if slotIdx == settings.CREATOR_SLOT_INDEX:
            LOG_ERROR('In first slot can be creator only')
            if callback:
                callback(False)
            return 
        self._requestsProcessor.doRequest(ctx, 'unassign', dbID, self.getUnitIdx())



    def _assign(self, ctx, callback = None):
        slotIdx = ctx.getSlotIdx()
        dbID = ctx.getPlayerID()
        pPermissions = self.getPermissions()
        if not pPermissions.canAssignToSlot(dbID):
            LOG_ERROR('Player can not assign to slot', pPermissions)
            if callback:
                callback(False)
            return 
        self._requestsProcessor.doRequest(ctx, 'assign', dbID, slotIdx, unitIdx=ctx.getUnitIdx())



    def _reassign(self, ctx, callback = None):
        slotIdx = ctx.getSlotIdx()
        dbID = ctx.getPlayerID()
        unitIdx = self.getUnitIdx()
        pPermissions = self.getPermissions()
        if pPermissions.canReassignToSlot():
            self._requestsProcessor.doRequest(ctx, 'reassign', dbID, slotIdx, unitIdx)
        elif pPermissions.canAssignToSlot(dbID):
            self._requestsProcessor.doRequest(ctx, 'assign', dbID, slotIdx, unitIdx=unitIdx)
        else:
            LOG_ERROR('Player can not (re)assign to slot', pPermissions)
            if callback:
                callback(False)



    def _setVehicle(self, ctx, callback = None):
        vehTypeCD = ctx.getVehTypeCD()
        vehInvID = ctx.getVehInvID()
        invVehs = g_itemsCache.items.getVehicles(REQ_CRITERIA.INVENTORY)
        if vehInvID:
            invMap = invVehs.inventoryMap()
            if vehInvID not in invMap.keys():
                LOG_ERROR('Vehicle is not in inventory', ctx)
                if callback:
                    callback(False)
                return 
        elif vehTypeCD:
            if vehTypeCD not in invVehs:
                LOG_ERROR('Vehicle is not in inventory', ctx)
                if callback:
                    callback(False)
                return 
            vehicle = invVehs[vehTypeCD]
            vehInvID = vehicle.inventoryID
        else:
            LOG_ERROR('Context is invalid', ctx)
            if callback:
                callback(False)
            return 
        vInfo = self.getVehicleInfo()
        if vInfo.vehInvID == vehInvID:
            LOG_DEBUG('Player already selected vehicle', ctx)
            if callback:
                callback(True)
            return 
        self._requestsProcessor.doRequest(ctx, 'setVehicle', vehInvID)



    def _clearVehicle(self, ctx, callback = None):
        vInfo = self.getVehicleInfo()
        if not vInfo.vehInvID:
            LOG_DEBUG('There is not vehicle in slot', ctx)
            if callback:
                callback(True)
            return 
        self._requestsProcessor.doRequest(ctx, 'setVehicle', INV_ID_CLEAR_VEHICLE)



    def _getTimeLeftInIdle(self):
        (_, unit,) = self.getUnit()
        result = 0
        if unit:
            timestamp = unit.getModalTimestamp()
            if timestamp:
                result = max(0, int(time.time() - time_utils.makeLocalServerTime(timestamp)))
        return result



    def _isInCoolDown(self, requestType, callback = None):
        if self._cooldown.validate(requestType):
            if callback:
                callback(False)
            return True
        return False




+++ okay decompyling unit.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:10:06 CET
