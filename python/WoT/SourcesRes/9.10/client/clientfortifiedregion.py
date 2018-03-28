# 2015.01.14 13:32:33 CET
import struct
import itertools
import operator
import BigWorld
from ClientUnit import ClientUnit
from constants import FORT_BUILDING_TYPE, FORT_BUILDING_TYPE_NAMES, FORT_ORDER_TYPE
import Event
from FortifiedRegionBase import FortifiedRegionBase, FORT_STATE, FORT_EVENT_TYPE, NOT_ACTIVATED
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION
import fortified_regions
from gui.Scaleform.locale.FORTIFICATIONS import FORTIFICATIONS
from gui.shared.fortifications import getDirectionFromDirPos
from gui.shared.fortifications.FortBuilding import FortBuilding
from gui.shared.fortifications.FortOrder import FortOrder
from gui.shared.fortifications.fort_seqs import ClanCardItem, AttackItem, DefenceItem, BattleItem
from gui.shared.gui_items.dossier import FortDossier
from gui.shared.utils import CONST_CONTAINER, findFirst
from helpers import time_utils, i18n
UNIT_MGR_ID_CHR = '<qH'

class BUILDING_UPDATE_REASON(CONST_CONTAINER):
    ADDED = 1
    UPDATED = 2
    COMPLETED = 3
    UPGRADED = 4
    DELETED = 5


class ATTACK_PLAN_RESULT(CONST_CONTAINER):
    OK = 'ok'
    MY_FROZEN = 'my_frozen'
    MY_VACATION = 'my_vacation'
    MY_OFF_DAY = 'my_off_day'
    MY_BUSY = 'my_busy'
    MY_NO_DIR = 'my_no_dir'
    OPP_VACATION = 'opponent_vacation'
    OPP_OFF_DAY = 'opponent_off_day'
    OPP_BUSY = 'opponent_busy'
    OPP_NO_DIR = 'opponent_no_dir'
    DEFENCE_HOUR_SAME = 'defence_hour_same'
    PREORDER_TIME = 'preorder_time'
    IN_COOLDOWN = 'in_cooldown'
    WAR_DECLARED = 'war_declared'


class ClientFortifiedRegion(FortifiedRegionBase):
    DEF_RES_STEP = 1

    def __init__(self):
        self.__eManager = Event.EventManager()
        self.onSortieChanged = Event.Event(self.__eManager)
        self.onSortieRemoved = Event.Event(self.__eManager)
        self.onSortieUnitReceived = Event.Event(self.__eManager)
        self.onFortBattleChanged = Event.Event(self.__eManager)
        self.onFortBattleRemoved = Event.Event(self.__eManager)
        self.onFortBattleUnitReceived = Event.Event(self.__eManager)
        self.onResponseReceived = Event.Event(self.__eManager)
        self.onBuildingChanged = Event.Event(self.__eManager)
        self.onTransport = Event.Event(self.__eManager)
        self.onDirectionOpened = Event.Event(self.__eManager)
        self.onDirectionClosed = Event.Event(self.__eManager)
        self.onDirectionLockChanged = Event.Event(self.__eManager)
        self.onStateChanged = Event.Event(self.__eManager)
        self.onOrderReady = Event.Event(self.__eManager)
        self.onDossierChanged = Event.Event(self.__eManager)
        self.onPlayerAttached = Event.Event(self.__eManager)
        self.onSettingCooldown = Event.Event(self.__eManager)
        self.onPeripheryChanged = Event.Event(self.__eManager)
        self.onDefenceHourChanged = Event.Event(self.__eManager)
        self.onOffDayChanged = Event.Event(self.__eManager)
        self.onVacationChanged = Event.Event(self.__eManager)
        self.onEnemyClanCardReceived = Event.Event(self.__eManager)
        self.onFavoritesChanged = Event.Event(self.__eManager)
        self.onDefenceHourShutdown = Event.Event(self.__eManager)
        self.onShutdownDowngrade = Event.Event(self.__eManager)
        self.onEmergencyRestore = Event.Event(self.__eManager)
        self.onEnemyStateChanged = Event.Event(self.__eManager)
        self.__battlesMapping = {}
        FortifiedRegionBase.__init__(self)



    def refresh(self):
        if not self.isEmpty():
            self.__updateBattlesMapping()



    def clear(self):
        self.__eManager.clear()
        self.__battlesMapping.clear()



    def getBuildings(self):
        result = {}
        for (buildingID, bcd,) in self.buildings.iteritems():
            result[buildingID] = FortBuilding(bcd)

        return result



    def getBuilding(self, buildingID, default = None):
        return self.getBuildings().get(buildingID, default)



    def isBuildingBuilt(self, buildingID):
        return self.getBuilding(buildingID) is not None



    def getOpenedDirections(self):
        result = []
        for direction in range(1, fortified_regions.g_cache.maxDirections + 1):
            if self.isDirectionOpened(direction):
                result.append(direction)

        return result



    def getDirectionsInBattle(self):
        result = []
        for direction in range(1, fortified_regions.g_cache.maxDirections + 1):
            if self.isDirectionOpened(direction) and self.isDirectionLocked(direction):
                result.append(direction)

        if result:
            result.append(0)
        return result



    def getBuildingsByDirections(self):
        result = {}
        for direction in self.getOpenedDirections():
            buildings = []
            for (dirPos, typeID,) in self._dirPosToBuildType.iteritems():
                if getDirectionFromDirPos(dirPos) == direction:
                    buildings.append(typeID)

            buildingsData = [None, None]
            for buildingId in buildings:
                buildingDescr = self.getBuilding(buildingId)
                if buildingDescr is not None:
                    buildingsData[buildingDescr.position] = buildingDescr

            result[direction] = buildingsData

        return result



    def isPositionAvailable(self, dir, pos):
        for building in self.getBuildingsByDirections().get(dir, []):
            if building is not None and building.position == pos:
                return False

        return True



    def isDirectionOpened(self, direction):
        return bool(self.dirMask & 1 << direction)



    def isDirectionLocked(self, direction):
        return bool(self.lockedDirMask & 1 << direction)



    def getDefResStep(self):
        return self.DEF_RES_STEP



    def getBuildingState(self, buildingTypeID):
        building = self.getBuilding(buildingTypeID)
        return (building.isExportAvailable(), building.isImportAvailable())



    def isFrozen(self):
        return self.state & FORT_STATE.BASE_DESTROYED > 0



    def getOrderData(self, orderID, level = None):
        orderBuildingID = None
        for (buildingID, building,) in fortified_regions.g_cache.buildings.iteritems():
            if building.orderType == orderID:
                orderBuildingID = buildingID

        orderLevel = 0
        orderCount = 0
        orderData = None
        if orderBuildingID is not None:
            if level is None:
                orderBuilding = self.getBuilding(orderBuildingID)
                buildingLevel = orderBuilding.level if orderBuilding is not None else 0
                orderLevel = max(buildingLevel, 1)
            else:
                orderLevel = level
            orderData = fortified_regions.g_cache.orders[orderID].levels.get(orderLevel)
            (orderCount, _,) = self.orders.get(orderID, (0, 0))
        return (orderBuildingID,
         orderCount,
         orderLevel,
         orderData)



    def getOrder(self, orderID):
        return FortOrder(orderID, self)



    def hasActivatedContinualOrders(self):
        for simpleOrder in [ o for o in FORT_ORDER_TYPE.ACTIVATED if o not in FORT_ORDER_TYPE.COMPATIBLES ]:
            checkingOrder = self.getOrder(simpleOrder)
            if checkingOrder.inCooldown:
                return True

        return False



    def getBuildingOrder(self, buildingID):
        return fortified_regions.g_cache.buildings[buildingID].orderType



    def getBuildingsAvailableForImport(self, buildingTypeID = None):
        return set(self.__getBuildingsFor('isImportAvailable', buildingTypeID))



    def getBuildingsAvailableForExport(self, buildingTypeID = None):
        return set(self.__getBuildingsFor('isExportAvailable', buildingTypeID))



    def getBuildingsOnCooldown(self, buildingTypeID = None):
        return set(self.__getBuildingsFor('hasTimer', buildingTypeID))



    def getBuildingsCompleted(self, buildingTypeID = None):
        return set(self.__getBuildingsFor('isReady', buildingTypeID))



    def __getBuildingsFor(self, method, buildingTypeID):

        def filter(item):
            return getattr(item, method)() and (buildingTypeID is None or item.typeID != buildingTypeID)


        return map(operator.attrgetter('typeID'), itertools.ifilter(filter, self.getBuildings().itervalues()))



    def isTransportationAvailable(self):
        forImport = self.getBuildingsAvailableForImport()

        def filter(item):
            return len(self.getBuildingsAvailableForExport(item)) > 0


        return findFirst(filter, forImport) is not None



    def getFortDossier(self):
        return FortDossier(self.statistics, True)



    def getAssignedBuildingID(self, dbID):
        for building in self.getBuildings().itervalues():
            if dbID in building.attachedPlayers:
                return building.typeID

        return 0



    def getTransportationLevel(self):
        base = self.getBuilding(FORT_BUILDING_TYPE.MILITARY_BASE)
        return fortified_regions.g_cache.transportLevels[base.level]



    def getSorties(self):
        if self.isEmpty():
            return {}
        return self.sorties



    def getFortBattles(self):
        if self.isEmpty():
            return {}
        return self.battles



    def getSortieShortData(self, unitMgrID, peripheryID):
        sortieKey = (unitMgrID, peripheryID)
        return self.getSorties().get(sortieKey, None)



    def getSortieUnit(self, unitMgrID, peripheryID):
        sortieKey = (unitMgrID, peripheryID)
        unit = None
        if not self.isEmpty() and sortieKey in self._sortieUnits:
            unit = ClientUnit()
            unit.unpack(self._sortieUnits[sortieKey])
        return unit



    def getFortBattleShortData(self, battleID):
        return self.getFortBattles().get(battleID, None)



    def getFortBattleUnit(self, battleID):
        unit = None
        if not self.isEmpty() and battleID in self.battleUnits:
            unit = ClientUnit()
            unit.unpack(self.battleUnits[battleID])
        return unit



    def getState(self):
        if self.isEmpty():
            return 0
        return self.state



    def isStartingScriptDone(self):
        return self.getState() & FORT_STATE.FIRST_BUILD_DONE > 0



    def isStartingScriptNotStarted(self):
        return self.getState() & FORT_STATE.FIRST_DIR_OPEN == 0



    def getTotalDefRes(self):
        outcome = 0
        for building in self.getBuildings().itervalues():
            outcome += building.storage

        return outcome



    def recalculateOrder(self, orderTypeID, prevCount, prevLevel, newLevel):
        (newCount, resLeft,) = self._recalcOrders(orderTypeID, prevCount, prevLevel, newLevel)
        return (newCount, resLeft)



    def getPeripheryProcessing(self):
        return (False, FORT_EVENT_TYPE.PERIPHERY_COOLDOWN in self.events)



    def isVacationEnabled(self):
        return self.vacationStart > 0 and self.vacationFinish > 0



    def getVacationProcessing(self):
        inProcess = FORT_EVENT_TYPE.VACATION_START in self.events and FORT_EVENT_TYPE.VACATION_FINISH in self.events
        inCooldown = FORT_EVENT_TYPE.VACATION_COOLDOWN in self.events
        return (inProcess, inCooldown)



    def getVacationDate(self):
        if not self.isVacationEnabled():
            return (None, None)
        return (self.vacationStart, self.vacationFinish)



    def getVacationDateStr(self):
        if not self.isVacationEnabled():
            return None
        (start, finish,) = self.getVacationDate()
        return '%s - %s' % (BigWorld.wg_getShortDateFormat(start), BigWorld.wg_getShortDateFormat(finish))



    def getDaysAfterVacation(self):
        if not self.isVacationEnabled():
            return 0
        (start, finish,) = self.getVacationDate()
        return int(time_utils.getTimeDeltaTilNow(finish) / time_utils.ONE_DAY)



    def isOnVacationAt(self, timestamp):
        if not self.isVacationEnabled():
            return False
        (start, finish,) = self.getVacationDate()
        return start < timestamp < finish



    def isOnVacation(self):
        if not self.isVacationEnabled():
            return False
        (start, finish,) = self.getVacationDate()
        return start <= time_utils.getCurrentTimestamp() < finish



    def isDefenceHourEnabled(self):
        return self.defenceHour != NOT_ACTIVATED



    def isDefenceHourShutDown(self):
        return FORT_EVENT_TYPE.DEFENCE_HOUR_SHUTDOWN in self.events



    def getLocalDefenceHour(self):
        from gui.shared.fortifications.fort_helpers import adjustDefenceHourToLocal
        if not self.isDefenceHourEnabled():
            return NOT_ACTIVATED
        return adjustDefenceHourToLocal(self.defenceHour)



    def getDefencePeriod(self):
        if self.isDefenceHourEnabled():
            timestampStart = time_utils.getTimeTodayForUTC(self.defenceHour)
            return (timestampStart, timestampStart + time_utils.ONE_HOUR)
        return (None, None)



    def getClosestDefencePeriod(self):
        if not self.isDefenceHourEnabled():
            return (None, None)
        timestampStart = time_utils.getTimeTodayForUTC(self.defenceHour)
        if time_utils.getTimeDeltaFromNow(timestampStart) < time_utils.ONE_HOUR:
            timestampStart += time_utils.ONE_DAY
        timestampFinish = timestampStart + time_utils.ONE_HOUR
        return (timestampStart, timestampFinish)



    def getDefencePeriodStr(self):
        (start, finish,) = self.getDefencePeriod()
        if start and finish:
            return '%s - %s' % (BigWorld.wg_getShortTimeFormat(start), BigWorld.wg_getShortTimeFormat(finish))
        return ''



    def isOnDefenceHour(self):
        if not self.isDefenceHourEnabled():
            return False
        (start, finish,) = self.getDefencePeriod()
        return start <= time_utils.getCurrentTimestamp() < finish and not self.isOnVacation() and not self.isOnOffDay()



    def getDefenceHourProcessing(self):
        return (FORT_EVENT_TYPE.DEFENCE_HOUR_CHANGE in self.events, FORT_EVENT_TYPE.DEFENCE_HOUR_COOLDOWN in self.events)



    def getNextDefenceHourData(self):
        (dayOfChange, defHour, _,) = self.events.get(FORT_EVENT_TYPE.DEFENCE_HOUR_CHANGE, (NOT_ACTIVATED, self.defenceHour, None))
        return (defHour, dayOfChange)



    def isOffDayEnabled(self):
        return self.offDay != NOT_ACTIVATED



    def isOnOffDay(self):
        return self.getLocalOffDay() == time_utils.getDateTimeInLocal(time_utils.getCurrentTimestamp()).weekday()



    def getLocalOffDay(self):
        from gui.shared.fortifications.fort_helpers import adjustOffDayToLocal
        if not self.isOffDayEnabled():
            return NOT_ACTIVATED
        return adjustOffDayToLocal(self.offDay, self.getLocalDefenceHour())



    def getOffDayStr(self):
        if self.isOffDayEnabled():
            return i18n.makeString('#menu:dateTime/weekDays/full/%d' % (self.getLocalOffDay() + 1))
        return i18n.makeString(FORTIFICATIONS.SETTINGSWINDOW_BLOCKCONDITION_NOWEEKEND)



    def getOffDayProcessing(self):
        return (FORT_EVENT_TYPE.OFF_DAY_CHANGE in self.events, FORT_EVENT_TYPE.OFF_DAY_COOLDOWN in self.events)



    def getAttacksIn(self, clanDBID = None, timePeriod = time_utils.QUARTER_HOUR):

        def filterFunc(item):
            if item.getStartTimeLeft() <= timePeriod and not item.isEnded():
                return True
            return False


        return self.getAttacks(clanDBID, filterFunc)



    def getDefencesIn(self, clanDBID = None, timePeriod = time_utils.QUARTER_HOUR):

        def filterFunc(item):
            if item.getStartTimeLeft() <= timePeriod and not item.isEnded():
                return True
            return False


        return self.getDefences(clanDBID, filterFunc)



    def getAttacksAndDefencesIn(self, clanDBID = None, timePeriod = time_utils.QUARTER_HOUR):
        attacks = self.getAttacksIn(clanDBID, timePeriod)
        defences = self.getDefencesIn(clanDBID, timePeriod)
        return sorted(attacks + defences)



    def getAttacks(self, clanDBID = None, filterFunc = None):
        result = []
        for ((startTime, direction,), data,) in self.attacks.iteritems():
            try:
                item = AttackItem(startTime, direction, *data)
                if (clanDBID is None or item.getOpponentClanDBID() == clanDBID) and (filterFunc is None or filterFunc(item)):
                    result.append(item)
            except Exception:
                LOG_ERROR('Error while building attack item', startTime, direction, data)
                LOG_CURRENT_EXCEPTION()

        return sorted(result)



    def getDefences(self, clanDBID = None, filterFunc = None):
        result = []
        for ((startTime, direction,), data,) in self.defences.iteritems():
            try:
                item = DefenceItem(startTime, direction, self.peripheryID, *data)
                if (clanDBID is None or item.getOpponentClanDBID() == clanDBID) and (filterFunc is None or filterFunc(item)):
                    result.append(item)
            except Exception:
                LOG_ERROR('Error while building defence item', startTime, direction, data)
                LOG_CURRENT_EXCEPTION()

        return sorted(result)



    def getBattleItemByBattleID(self, battleID):
        return self.__battlesMapping.get(battleID)



    def getBattles(self):
        result = []
        for (battleID, itemData,) in self.getFortBattles().iteritems():
            result.append(self.__buildBattle(battleID, itemData))

        return result



    def canPlanAttackOn(self, dayTimestamp, clanFortInfo):
        if self.isFrozen():
            return ATTACK_PLAN_RESULT.MY_FROZEN
        currentDefHourTimestamp = time_utils.getTimeForLocal(dayTimestamp, clanFortInfo.getStartDefHour())
        enemyDefHour = clanFortInfo.getDefHourFor(currentDefHourTimestamp)
        enemyDefHourTimestamp = time_utils.getTimeForLocal(dayTimestamp, enemyDefHour)
        if enemyDefHourTimestamp - time_utils.getCurrentTimestamp() <= fortified_regions.g_cache.attackPreorderTime:
            return ATTACK_PLAN_RESULT.PREORDER_TIME
        if self.isOnVacationAt(enemyDefHourTimestamp):
            return ATTACK_PLAN_RESULT.MY_VACATION
        (vacationStart, vacationEnd,) = clanFortInfo.getVacationPeriod()
        if vacationStart <= enemyDefHourTimestamp <= vacationEnd:
            return ATTACK_PLAN_RESULT.OPP_VACATION
        dayDate = time_utils.getDateTimeInLocal(dayTimestamp)
        localOffDay = clanFortInfo.getLocalOffDayFor(currentDefHourTimestamp)
        if dayDate.weekday() == localOffDay:
            return ATTACK_PLAN_RESULT.OPP_OFF_DAY
        if self.defenceHour == clanFortInfo.getStartDefHour():
            return ATTACK_PLAN_RESULT.DEFENCE_HOUR_SAME

        def filterInFight(item):
            if enemyDefHourTimestamp <= item.getStartTime() < enemyDefHourTimestamp + time_utils.ONE_HOUR:
                return True
            return False


        attacksInFight = self.getAttacks(clanFortInfo.getClanDBID(), filterInFight)
        if attacksInFight:
            return ATTACK_PLAN_RESULT.WAR_DECLARED
        if clanFortInfo.closestAttackInCooldown is not None and dayTimestamp < clanFortInfo.closestAttackInCooldown.getStartTime() + time_utils.ONE_DAY * 7 and not clanFortInfo.counterAttacked:
            return ATTACK_PLAN_RESULT.IN_COOLDOWN
        (hasAvailableDirections, hasFreeDirections,) = (False, False)
        for direction in self.getOpenedDirections():
            eventTypeID = FORT_EVENT_TYPE.DIR_OPEN_ATTACKS_BASE + direction
            (availableTime, _, _,) = self.events.get(eventTypeID, (None, None, None))
            if availableTime <= enemyDefHourTimestamp:
                hasAvailableDirections = True

                def filterAttacks(item):
                    if enemyDefHourTimestamp <= item.getStartTime() <= enemyDefHourTimestamp + time_utils.ONE_HOUR and direction == item.getDirection() and not item.isEnded():
                        return True
                    return False


                if not self.getAttacks(filterFunc=filterAttacks):
                    hasFreeDirections = True
                    break

        if not hasAvailableDirections:
            return ATTACK_PLAN_RESULT.MY_NO_DIR
        if not hasFreeDirections:
            return ATTACK_PLAN_RESULT.MY_BUSY
        (isBusy, isAvailable,) = clanFortInfo.isAvailableForAttack(enemyDefHourTimestamp)
        if not isAvailable:
            return ATTACK_PLAN_RESULT.OPP_NO_DIR
        if isBusy:
            return ATTACK_PLAN_RESULT.OPP_BUSY
        return ATTACK_PLAN_RESULT.OK



    def getBattle(self, battleID):
        itemData = self.getFortBattles().get(battleID)
        if itemData is None:
            return 
        return self.__buildBattle(battleID, itemData)



    def __buildBattle(self, battleID, itemData):
        try:
            additionalData = self.__battlesMapping[battleID]
            return BattleItem(battleID, itemData, additionalData)
        except Exception:
            LOG_ERROR('Error while building battle item', battleID, itemData)
            LOG_CURRENT_EXCEPTION()



    def __updateBattlesMapping(self):
        self.__battlesMapping.clear()
        for item in self.getAttacks():
            self.__battlesMapping[item.getBattleID()] = item

        for item in self.getDefences():
            self.__battlesMapping[item.getBattleID()] = item




    def _setSortie(self, unitMgrID, cmdrDBID, rosterTypeID, state, peripheryID, *args):
        result = FortifiedRegionBase._setSortie(self, unitMgrID, cmdrDBID, rosterTypeID, state, peripheryID, *args)
        self.onSortieChanged(unitMgrID, peripheryID)
        return result



    def _removeSortie(self, unitMgrID, peripheryID):
        FortifiedRegionBase._removeSortie(self, unitMgrID, peripheryID)
        self.onSortieRemoved(unitMgrID, peripheryID)



    def _unpackSortieUnit(self, unpacking):
        result = FortifiedRegionBase._unpackSortieUnit(self, unpacking)
        try:
            (unitMgrID, peripheryID,) = struct.unpack_from(UNIT_MGR_ID_CHR, unpacking)
            self.onSortieUnitReceived(unitMgrID, peripheryID)
        except struct.error as e:
            LOG_ERROR(e)
        return result



    def _addFortBattle(self, battleID, direction, attackTime, attackerClanDBID, defenderClanDBID):
        FortifiedRegionBase._addFortBattle(self, battleID, direction, attackTime, attackerClanDBID, defenderClanDBID)
        self.__updateBattlesMapping()
        self.onFortBattleChanged(battleID)



    def _removeFortBattle(self, battleID):
        FortifiedRegionBase._removeFortBattle(self, battleID)
        self.__updateBattlesMapping()
        self.onFortBattleRemoved(battleID)



    def _unpackFortBattleUnit(self, unpacking):
        result = FortifiedRegionBase._unpackFortBattleUnit(self, unpacking)
        try:
            (battleID,) = struct.unpack_from(self.FORMAT_FORT_BATTLE_UNIT_HEADER, unpacking)
            self.onFortBattleUnitReceived(battleID)
        except struct.error as e:
            LOG_ERROR(e)
        return result



    def _processRequest(self, reqID, callerDBID):
        FortifiedRegionBase._processRequest(self, reqID, callerDBID)
        self.onResponseReceived(reqID, callerDBID)



    def _addBuilding(self, buildingTypeID, dir, pos):
        FortifiedRegionBase._addBuilding(self, buildingTypeID, dir, pos)
        self.onBuildingChanged(buildingTypeID, BUILDING_UPDATE_REASON.ADDED, {'dir': dir,
         'pos': pos})



    def _upgrade(self, buildTypeID, level, decStorage):
        building = self.getBuilding(buildTypeID)
        FortifiedRegionBase._upgrade(self, buildTypeID, level, decStorage)
        self.onBuildingChanged(buildTypeID, BUILDING_UPDATE_REASON.UPGRADED, {'dir': building.direction,
         'pos': building.position})



    def _delBuilding(self, buildingTypeID):
        building = self.getBuilding(buildingTypeID)
        ressignPlayer = BigWorld.player().databaseID in self.getBuilding(buildingTypeID).attachedPlayers
        FortifiedRegionBase._delBuilding(self, buildingTypeID)
        self.onBuildingChanged(buildingTypeID, BUILDING_UPDATE_REASON.DELETED, {'dir': building.direction,
         'pos': building.position})
        if ressignPlayer:
            self.onPlayerAttached(FORT_BUILDING_TYPE.MILITARY_BASE)



    def _addOrders(self, buildingTypeID, count, timeFinish, initiatorDBID):
        FortifiedRegionBase._addOrders(self, buildingTypeID, count, timeFinish, initiatorDBID)
        self.onBuildingChanged(buildingTypeID, BUILDING_UPDATE_REASON.UPDATED)



    def _transport(self, fromBuildTypeID, toBuildTypeID, resCount, timeCooldown):
        reason = BUILDING_UPDATE_REASON.UPDATED
        previousState = self.getBuilding(toBuildTypeID)
        FortifiedRegionBase._transport(self, fromBuildTypeID, toBuildTypeID, resCount, timeCooldown)
        newState = self.getBuilding(toBuildTypeID)
        self.onBuildingChanged(fromBuildTypeID, BUILDING_UPDATE_REASON.UPDATED)
        if previousState.level == 0 and newState.level > 0:
            reason = BUILDING_UPDATE_REASON.COMPLETED
        self.onBuildingChanged(toBuildTypeID, reason)
        self.onTransport()



    def _contribute(self, accDBID, buildingTypeID, resCount, dateStamp):
        reason = BUILDING_UPDATE_REASON.UPDATED
        previousState = self.getBuilding(buildingTypeID)
        FortifiedRegionBase._contribute(self, accDBID, buildingTypeID, resCount, dateStamp)
        newState = self.getBuilding(buildingTypeID)
        if previousState.level == 0 and newState.level > 0:
            reason = BUILDING_UPDATE_REASON.COMPLETED
        self.onBuildingChanged(buildingTypeID, reason)



    def _dmgBuilding(self, buildingTypeID, damage, attackerClanDBID):
        FortifiedRegionBase._dmgBuilding(self, buildingTypeID, damage, attackerClanDBID)
        self.onBuildingChanged(buildingTypeID, BUILDING_UPDATE_REASON.UPDATED)



    def _openDir(self, dir, timestamp, initiatorDBID):
        FortifiedRegionBase._openDir(self, dir, timestamp, initiatorDBID)
        self.onDirectionOpened(dir)



    def _closeDir(self, dir):
        FortifiedRegionBase._closeDir(self, dir)
        self.onDirectionClosed(dir)



    def _setState(self, newState):
        FortifiedRegionBase._setState(self, newState)
        self.onStateChanged(newState)



    def _expireEvent(self, eventTypeID, value):
        buildingTypeID = eventTypeID - FORT_EVENT_TYPE.PRODUCT_ORDERS_BASE
        orderTypeID = 0
        orderCount = 0
        isOrder = buildingTypeID in FORT_BUILDING_TYPE_NAMES
        if isOrder:
            building = self.getBuilding(buildingTypeID)
            orderTypeID = self.getBuildingOrder(buildingTypeID)
            orderCount = building.orderInProduction.get('count')
        FortifiedRegionBase._expireEvent(self, eventTypeID, value)
        if isOrder:
            self.onOrderReady(orderTypeID, orderCount)
        elif eventTypeID == FORT_EVENT_TYPE.DEFENCE_HOUR_CHANGE:
            self.onDefenceHourChanged(value)
        elif eventTypeID == FORT_EVENT_TYPE.OFF_DAY_CHANGE:
            self.onOffDayChanged(value)
        elif eventTypeID in (FORT_EVENT_TYPE.PERIPHERY_COOLDOWN,
         FORT_EVENT_TYPE.DEFENCE_HOUR_COOLDOWN,
         FORT_EVENT_TYPE.OFF_DAY_COOLDOWN,
         FORT_EVENT_TYPE.VACATION_COOLDOWN):
            self.onSettingCooldown(eventTypeID)



    def _syncFortDossier(self, compDossierDescr):
        FortifiedRegionBase._syncFortDossier(self, compDossierDescr)
        self.onDossierChanged(compDossierDescr)



    def _attach(self, buildTypeID, accDBID):
        FortifiedRegionBase._attach(self, buildTypeID, accDBID)
        self.onPlayerAttached(buildTypeID)



    def _addFavorite(self, clanDBID):
        FortifiedRegionBase._addFavorite(self, clanDBID)
        self.onFavoritesChanged(clanDBID)



    def _removeFavorite(self, clanDBID):
        FortifiedRegionBase._removeFavorite(self, clanDBID)
        self.onFavoritesChanged(clanDBID)



    def _shutdownDowngrade(self):
        FortifiedRegionBase._shutdownDowngrade(self)
        self.onShutdownDowngrade()



    def _shutdownDefHour(self, timeActivation, initiatorDBID):
        FortifiedRegionBase._shutdownDefHour(self, timeActivation, initiatorDBID)
        self.onDefenceHourShutdown()



    def _cancelEvent(self, eventTypeID):
        FortifiedRegionBase._cancelEvent(self, eventTypeID)
        if eventTypeID == FORT_EVENT_TYPE.DEFENCE_HOUR_SHUTDOWN:
            self.onDefenceHourShutdown()



    def _changePeriphery(self, peripheryID, timeCooldown):
        FortifiedRegionBase._changePeriphery(self, peripheryID, timeCooldown)
        self.onPeripheryChanged(peripheryID)



    def _changeDefHour(self, newValue, timeActivation, timeCooldown, initiatorDBID):
        FortifiedRegionBase._changeDefHour(self, newValue, timeActivation, timeCooldown, initiatorDBID)
        self.onDefenceHourChanged(newValue)



    def _changeOffDay(self, offDay, timeActivation, timeCooldown, initiatorDBID):
        FortifiedRegionBase._changeOffDay(self, offDay, timeActivation, timeCooldown, initiatorDBID)
        self.onOffDayChanged(offDay)



    def _changeVacation(self, timeVacationStart, timeVacationEnd, timeCooldown, initiatorDBID):
        FortifiedRegionBase._changeVacation(self, timeVacationStart, timeVacationEnd, timeCooldown, initiatorDBID)
        self.onVacationChanged(timeVacationStart, timeVacationEnd)



    def _setLockedDirMask(self, lockedDirMask):
        FortifiedRegionBase._setLockedDirMask(self, lockedDirMask)
        self.onDirectionLockChanged()



    def _setFortBattleBuildnum(self, battleID, packBuildsNum, roundStart = 0):
        FortifiedRegionBase._setFortBattleBuildnum(self, battleID, packBuildsNum, roundStart)
        self.__updateBattlesMapping()
        self.onFortBattleChanged(battleID)



    def _setEnemyReadyForBattle(self, battleID, isReady):
        FortifiedRegionBase._setEnemyReadyForBattle(self, battleID, isReady)
        self.onEnemyStateChanged(battleID, isReady)



    def _setFortBattleRound(self, battleID, isBattleRound):
        FortifiedRegionBase._setFortBattleRound(self, battleID, isBattleRound)
        self.__updateBattlesMapping()
        self.onFortBattleChanged(battleID)



    def _addAttack(self, timeAttack, dirFrom, dirTo, defClanDBID, battleID, peripheryID, attackResult, attackResource, defClanAbbrev):
        FortifiedRegionBase._addAttack(self, timeAttack, dirFrom, dirTo, defClanDBID, battleID, peripheryID, attackResult, attackResource, defClanAbbrev)
        self.__updateBattlesMapping()
        self.onFortBattleChanged(battleID)



    def _addDefence(self, timeAttack, dirFrom, dirTo, attackerClanDBID, battleID, attackResult, attackResource, attackerClanAbbrev):
        FortifiedRegionBase._addDefence(self, timeAttack, dirFrom, dirTo, attackerClanDBID, battleID, attackResult, attackResource, attackerClanAbbrev)
        self.__updateBattlesMapping()
        self.onFortBattleChanged(battleID)



    def _onDeleteBattle(self, key, args, reason, isDefence):
        battleID = args[3]
        FortifiedRegionBase._onDeleteBattle(self, key, args, reason, isDefence)
        self.onFortBattleRemoved(battleID)



    def _onEnemyClanCard(self, *args):
        self.onEnemyClanCardReceived(ClanCardItem(args, fort=self))



    def _onEmergencyRestore(self, unpacking):
        self.onEmergencyRestore()
        return FortifiedRegionBase._onEmergencyRestore(self, unpacking)




+++ okay decompyling clientfortifiedregion.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:32:34 CET
