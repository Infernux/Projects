# 2015.01.14 13:32:35 CET
import cPickle
from ClientUnit import ClientUnit
import Event
import constants
from debug_utils import *
from UnitBase import UnitBase, UNIT_SLOT, UNIT_BROWSER_CMD, CLIENT_UNIT_CMD, INV_ID_CLEAR_VEHICLE
from UnitRoster import UnitRosterSlot
from gui.shared import g_itemsCache
import AccountCommands

class ClientUnitMgr(object):

    def __init__(self, account):
        self.__eManager = Event.EventManager()
        self.onUnitJoined = Event.Event(self.__eManager)
        self.onUnitLeft = Event.Event(self.__eManager)
        self.onUnitErrorReceived = Event.Event(self.__eManager)
        self.onUnitResponseReceived = Event.Event(self.__eManager)
        self.id = 0
        self.unitIdx = 0
        self.battleID = None
        self.__account = account
        self.__requestID = 0
        self.units = {}



    def destroy(self):
        self.battleID = None
        self.__account = None
        self.__eManager.clear()
        self._clearUnits()



    def __getNextRequestID(self):
        self.__requestID += 1
        return self.__requestID



    def onUnitUpdate(self, unitMgrID, unitIdx, packedUnit, packedOps):
        LOG_DAN('onUnitUpdate: unitMgrID=%s, unitIdx=%s, packedUnit=%r, packedOps=%r' % (unitMgrID,
         unitIdx,
         packedUnit,
         packedOps))
        if self.id != unitMgrID:
            prevMgrID = self.id
            prevUnitIdx = self.unitIdx
            self.id = unitMgrID
            self.unitIdx = unitIdx
            self._clearUnits()
            if not self.id and prevMgrID:
                self.onUnitLeft(prevMgrID, prevUnitIdx)
        if packedUnit:
            unit = ClientUnit(packedUnit=packedUnit)
            if unitIdx in self.units:
                self.units[unitIdx].destroy()
            self.units[unitIdx] = unit
            self.onUnitJoined(self.id, self.unitIdx)
        if packedOps:
            unit = self.units.get(unitIdx)
            if unit:
                unit.unpackOps(packedOps)
                unit.onUnitUpdated()



    def setBattleID(self, battleID):
        self.battleID = battleID



    def onUnitError(self, requestID, unitMgrID, unitIdx, errorCode, errorString):
        LOG_DEBUG('onUnitError: unitMgr=%s, unitIdx=%s, errorCode=%s, errorString=%r' % (unitMgrID,
         unitIdx,
         errorCode,
         errorString))
        self.onUnitErrorReceived(requestID, unitMgrID, unitIdx, errorCode, errorString)



    def onUnitCallOk(self, requestID):
        LOG_DEBUG('onUnitCallOk: requestID=%s OK' % requestID)
        self.onUnitResponseReceived(requestID)



    def create(self, unitMgrFlags = 0):
        requestID = self.__getNextRequestID()
        self.__account.base.createUnitMgr(requestID, unitMgrFlags)
        return requestID



    def join(self, unitMgrID, unitIdx = 1, vehInvID = 0, slotIdx = UNIT_SLOT.REMOVE):
        requestID = self.__getNextRequestID()
        self.__account.base.joinUnit(requestID, unitMgrID, unitIdx, slotIdx)
        return requestID



    def __doUnitCmd(self, cmd, unitMgrID = 0, unitIdx = 0, uint64Arg = 0, int32Arg = 0, strArg = ''):
        requestID = self.__getNextRequestID()
        if not unitMgrID:
            unitMgrID = self.id
        if not unitIdx:
            unitIdx = self.unitIdx
        self.__account.base.doUnitCmd(cmd, requestID, unitMgrID, unitIdx, uint64Arg, int32Arg, strArg)
        return requestID



    def leave(self):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.LEAVE_UNIT)



    def setVehicle(self, vehInvID = INV_ID_CLEAR_VEHICLE):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.SET_UNIT_VEHICLE, 0, 0, vehInvID)



    def setMember(self, vehInvID, slotIdx = UNIT_SLOT.ANY):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.SET_UNIT_MEMBER, 0, 0, vehInvID, slotIdx)



    def fit(self, playerID, slotIdx = UNIT_SLOT.ANY, unitIdx = 0):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.FIT_UNIT_MEMBER, self.id, unitIdx, playerID, slotIdx)



    def unfit(self, playerID, unitIdx = 0):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.FIT_UNIT_MEMBER, self.id, unitIdx, playerID, UNIT_SLOT.REMOVE)



    def assign(self, playerID, slotIdx, unitIdx = 0):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.ASSIGN_UNIT_MEMBER, self.id, unitIdx, playerID, slotIdx)



    def unassign(self, playerID, unitIdx = 0):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.ASSIGN_UNIT_MEMBER, self.id, unitIdx, playerID, UNIT_SLOT.REMOVE)



    def reassign(self, playerID, slotIdx, unitIdx = 0):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.REASSIGN_UNIT_MEMBER, self.id, unitIdx, playerID, slotIdx)



    def kick(self, playerID, unitIdx = 0):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.KICK_UNIT_PLAYER, self.id, unitIdx, playerID)



    def setReady(self, isReady = True):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.SET_UNIT_MEMBER_READY, self.id, 0, int(isReady))



    def setRosterSlot(self, rosterSlotIdx, vehTypeID = None, nationNames = [], levels = (1, 8), vehClassNames = [], unitIdx = 0):
        LOG_DAN('setRosterSlot: slot=%s, vehTypeID=%s, nationNames=%s, levels=%s, vehClassNames=%s' % (rosterSlotIdx,
         vehTypeID,
         repr(nationNames),
         repr(levels),
         repr(vehClassNames)))
        rSlot = UnitRosterSlot(vehTypeID, nationNames, levels, vehClassNames)
        return self.__doUnitCmd(CLIENT_UNIT_CMD.SET_ROSTER_SLOT, self.id, self.unitIdx, 0, rosterSlotIdx, rSlot.pack())



    def setAllRosterSlots(self, rosterDefsDict, unitIdx = 0):
        if not unitIdx:
            unitIdx = self.unitIdx
        LOG_DAN('setAllRosterSlots: rosterDefsDict=%r, unitIdx=%s' % (rosterDefsDict, unitIdx))
        rosterSlots = {}
        for (rosterSlotIdx, rosterDict,) in rosterDefsDict.iteritems():
            vehTypeID = rosterDict.get('vehTypeID', None)
            nationNames = rosterDict.get('nationNames', [])
            levels = rosterDict.get('levels', None)
            vehClassNames = rosterDict.get('vehClassNames', [])
            rSlot = UnitRosterSlot(vehTypeID, nationNames, levels, vehClassNames)
            rosterSlots[rosterSlotIdx] = rSlot.pack()

        LOG_DAN('setAllRosterSlots: rosterSlots=%r' % rosterSlots)
        requestID = self.__getNextRequestID()
        self.__account.base.setAllRosterSlots(requestID, self.id, unitIdx, rosterSlots.keys(), rosterSlots.values())
        return requestID



    def lockUnit(self, isLocked = True, unitIdx = 0):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.LOCK_UNIT, self.id, unitIdx, int(isLocked))



    def closeSlot(self, slotIdx, isClosed = True, unitIdx = 0):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.CLOSE_UNIT_SLOT, self.id, unitIdx, int(isClosed), slotIdx)



    def openUnit(self, isOpen = True, unitIdx = 0):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.OPEN_UNIT, self.id, unitIdx, int(isOpen))



    def setDevMode(self, isDevMode = True, unitIdx = 0):
        if constants.IS_DEVELOPMENT:
            return self.__doUnitCmd(CLIENT_UNIT_CMD.SET_UNIT_DEV_MODE, self.id, unitIdx, int(isDevMode))



    def invite(self, accountsToInvite, comment):
        requestID = self.__getNextRequestID()
        self.__account.base.sendUnitInvites(requestID, accountsToInvite, comment)
        return requestID



    def startBattle(self, unitIdx = 0):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.START_UNIT_BATTLE, self.id, unitIdx)



    def stopBattle(self, unitIdx = 0):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.STOP_UNIT_BATTLE, self.id, unitIdx)



    def startAutoSearch(self, unitIdx = 0):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.START_AUTO_SEARCH, self.id, unitIdx)



    def stopAutoSearch(self, unitIdx = 0):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.STOP_AUTO_SEARCH, self.id, unitIdx)



    def setComment(self, strComment, unitIdx = 0):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.SET_UNIT_COMMENT, self.id, unitIdx, 0, 0, strComment)



    def giveLeadership(self, memberDBID, unitIdx = 0):
        return self.__doUnitCmd(CLIENT_UNIT_CMD.GIVE_LEADERSHIP, self.id, unitIdx, memberDBID)



    def _clearUnits(self):
        while len(self.units):
            (_, unit,) = self.units.popitem()
            unit.destroy()





class ClientUnitBrowser(object):

    def __init__(self, account):
        self.__account = account
        self.__eManager = Event.EventManager()
        self.onResultsReceived = Event.Event(self.__eManager)
        self.onResultsUpdated = Event.Event(self.__eManager)
        self.onSearchSuccessReceived = Event.Event(self.__eManager)
        self.onErrorReceived = Event.Event(self.__eManager)
        self.results = {}
        self._acceptUnitMgrID = 0
        self._acceptUnitIdx = 0
        self._acceptDeadlineUTC = 0



    def destroy(self):
        self.__account = None
        self.__eManager.clear()
        self.results.clear()



    def subscribe(self, vehTypes = [], showOtherLocations = False):
        self.results = {}
        self.__account.base.subscribeUnitBrowser(vehTypes, showOtherLocations)



    def unsubscribe(self):
        self.results = {}
        self.__account.base.unsubscribeUnitBrowser()



    def recenter(self, targetRating, vehTypes = [], showOtherLocations = False):
        self.results = {}
        self.__account.base.recenterUnitBrowser(targetRating, vehTypes, showOtherLocations)



    def left(self):
        self.__account.base.doUnitBrowserCmd(UNIT_BROWSER_CMD.LEFT)



    def right(self):
        self.__account.base.doUnitBrowserCmd(UNIT_BROWSER_CMD.RIGHT)



    def refresh(self):
        self.results = {}
        self.__account.base.doUnitBrowserCmd(UNIT_BROWSER_CMD.REFRESH)



    def onError(self, errorCode, errorString):
        LOG_DAN('unitBrowser.onError: errorCode=%s, errorString=%r' % (errorCode, errorString))
        self.onErrorReceived(errorCode, errorString)



    def onResultsSet(self, pickledBrowserResultsList):
        browserResultsList = cPickle.loads(pickledBrowserResultsList)
        LOG_DAN('unitBrowser.onResultsSet: %s' % browserResultsList)
        self.results.clear()
        for row in browserResultsList:
            try:
                (cfdUnitID, unitMgrID, cmdrRating, peripheryID, strUnitPack,) = row
                unit = ClientUnit(packedUnit=strUnitPack)
                self.results[cfdUnitID] = dict(unitMgrID=unitMgrID, cmdrRating=cmdrRating, peripheryID=peripheryID, unit=unit)
            except:
                LOG_CURRENT_EXCEPTION()

        LOG_DAN('unitBrowser results=%r' % self.results)
        self.onResultsReceived(self.results)



    def onResultsUpdate(self, pickledBrowserUpdatesDict):
        browserUpdatesDict = cPickle.loads(pickledBrowserUpdatesDict)
        LOG_DAN('unitBrowser.onResultsUpdate: %s' % browserUpdatesDict)
        res = {}
        for (cfdUnitID, (cmdrRating, strUnitPack,),) in browserUpdatesDict.iteritems():
            try:
                if strUnitPack is None:
                    self.results.pop(cfdUnitID, None)
                    res[cfdUnitID] = None
                else:
                    unit = ClientUnit(packedUnit=strUnitPack)
                    if cfdUnitID in self.results:
                        self.results[cfdUnitID]['unit'] = unit
                        self.results[cfdUnitID]['cmdrRating'] = cmdrRating
                        res[cfdUnitID] = self.results[cfdUnitID]
            except:
                LOG_CURRENT_EXCEPTION()

        self.onResultsUpdated(res)



    def startSearch(self, vehTypes = [], useOtherLocations = False):
        self.__account.enqueueUnitAssembler(vehTypes)



    def _search(self, vehInvIDs = []):
        vehTypes = []
        for vehInvID in vehInvIDs:
            vehicle = g_itemsCache.items.getVehicle(vehInvID)
            LOG_DAN('vehicle[%s]=%r' % (vehInvID, vehicle))




    def stopSearch(self):
        self.__account.dequeueUnitAssembler()



    def onSearchSuccess(self, unitMgrID, unitIdx, acceptDeadlineUTC):
        LOG_DAN('onSearchSuccess: unitMgrID=%s, unitIdx=%s, acceptDeadlineUTC=%s' % (unitMgrID, unitIdx, acceptDeadlineUTC))
        self._acceptUnitMgrID = unitMgrID
        self._acceptUnitIdx = unitIdx
        self._acceptDeadlineUTC = acceptDeadlineUTC
        self.onSearchSuccessReceived(unitMgrID, unitIdx, acceptDeadlineUTC)



    def acceptSearch(self, unitMgrID = 0, unitIdx = 0):
        if not unitMgrID:
            unitMgrID = self._acceptUnitMgrID
            unitIdx = self._acceptUnitIdx
        self.__account.base.acceptUnitAutoSearch(unitMgrID, unitIdx)



    def declineSearch(self, unitMgrID = 0, unitIdx = 0):
        if not unitMgrID:
            unitMgrID = self._acceptUnitMgrID
            unitIdx = self._acceptUnitIdx
        self.__account.base.doCmdInt3(AccountCommands.REQUEST_ID_NO_RESPONSE, AccountCommands.CMD_DEQUEUE_UNIT_ASSEMBLER, unitMgrID, unitIdx, 0)




+++ okay decompyling clientunitmgr.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:32:35 CET
