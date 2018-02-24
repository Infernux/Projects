# 2015.01.14 13:32:34 CET
from FortifiedRegionBase import FORT_CLIENT_METHOD, makeDirPosByte, SECONDS_PER_DAY, SECONDS_PER_HOUR, ALL_DIRS
from ClientFortifiedRegion import ClientFortifiedRegion
import Event
from debug_utils import LOG_DAN, LOG_DEBUG, LOG_ERROR
from gui.shared.utils import CONST_CONTAINER
import time
import fortified_regions

class ClientFortMgr(object):

    class WIZARD_PROGRESS(CONST_CONTAINER):
        NO_PROGRESS = 0
        FIRST_DIRECTION = 1
        FIRST_BUILDING = 2
        FIRST_TRANSPORTATION = 3
        COMPLETED = FIRST_TRANSPORTATION


    def __init__(self, account = None):
        self._ClientFortMgr__eManager = Event.EventManager()
        self.onFortResponseReceived = Event.Event(self._ClientFortMgr__eManager)
        self.onFortUpdateReceived = Event.Event(self._ClientFortMgr__eManager)
        self.onFortStateChanged = Event.Event(self._ClientFortMgr__eManager)
        self.onFortPublicInfoReceived = Event.Event(self._ClientFortMgr__eManager)
        self._ClientFortMgr__account = account
        self._fort = ClientFortifiedRegion()
        self._ClientFortMgr__requestID = 0
        self.state = None



    def __callFortMethod(self, *args):
        LOG_DAN('base.callFortMethod', args)
        self._ClientFortMgr__account.base.callFortMethod(*args)



    def _setAccount(self, account = None):
        self._ClientFortMgr__account = account



    def clear(self):
        self._ClientFortMgr__account = None
        self._ClientFortMgr__eManager.clear()
        self._fort.clear()



    def __getNextRequestID(self):
        self._ClientFortMgr__requestID += 1
        return self._ClientFortMgr__requestID



    def onFortReply(self, reqID, resultCode, resultString):
        LOG_DAN('onFortReply: reqID=%s, resultCode=%s, resultString=%r' % (reqID, resultCode, resultString))
        self.onFortResponseReceived(reqID, resultCode, resultString)



    def onFortUpdate(self, packedOps, packedUpdate):
        LOG_DAN('onFortUpdate: packedOps len=%s, packedUpdate len=%s' % (len(packedOps), len(packedUpdate)))
        isFullUpdate = False
        if packedUpdate:
            self._fort.unpack(packedUpdate)
            isFullUpdate = True
        elif packedOps:
            self._fort.unpackOps(packedOps)
        self._fort.refresh()
        self.onFortUpdateReceived(isFullUpdate)
        LOG_DAN('after onFortUpdate:', self._fort)



    def onFortStateDiff(self, newState):
        LOG_DAN('onFortStateDiff: state %s (was %s)' % (newState, self.state))
        self.state = newState
        self.onFortStateChanged()



    def create(self):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.CREATE, 0, 0, 0)
        return requestID



    def delete(self):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.DELETE, 0, 0, 0)
        return requestID



    def subscribe(self):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.SUBSCRIBE, 0, 0, 0)
        return requestID



    def unsubscribe(self):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.UNSUBSCRIBE, 0, 0, 0)
        return requestID



    def addBuilding(self, buildingTypeID, dir, pos):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.ADD_BUILDING, buildingTypeID, dir, pos)
        return requestID



    def delBuilding(self, buildingTypeID):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.DEL_BUILDING, buildingTypeID, 0, 0)
        return requestID



    def contribute(self, resCount):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.CONTRIBUTE, resCount, 0, 0)
        return requestID



    def dmgBuilding(self, buildingTypeID, damage):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.DMG_BUILDING, buildingTypeID, damage, 0)
        return requestID



    def deletePlannedBattles(self, timeStart = 1, timeFinish = 2000000000, dir = ALL_DIRS):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.DELETE_PLANNED_BATTLES, timeStart, timeFinish, dir)
        return requestID



    def changeAttackResult(self, attackResult, attackResource, attackTime):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.CHANGE_ATTACK_RESULT, attackResult, attackResource, attackTime)
        return requestID



    def upgrade(self, buildingTypeID):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.UPGRADE, buildingTypeID, 0, 0)
        return requestID



    def transport(self, fromBuildingTypeID, toBuildingTypeID, resCount):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.TRANSPORT, fromBuildingTypeID, toBuildingTypeID, resCount)
        return requestID



    def attach(self, buildingTypeID):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.ATTACH, 0, buildingTypeID, 0)
        return requestID



    def addOrder(self, buildingTypeID, count):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.ADD_ORDER, buildingTypeID, count, 0)
        return requestID



    def activateOrder(self, orderTypeID):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.ACTIVATE_ORDER, orderTypeID, 0, 0)
        return requestID



    def openDir(self, direction):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.OPEN_DIR, direction, 0, 0)
        return requestID



    def closeDir(self, direction):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.CLOSE_DIR, direction, 0, 0)
        return requestID



    def createSortie(self, divisionLevel = 10):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.CREATE_SORTIE, divisionLevel, 0, 0)
        return requestID



    def createOrJoinFortBattle(self, battleID, slotIdx = -1):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.CREATE_JOIN_FORT_BATTLE, battleID, slotIdx, 0)
        return requestID



    def _scheduleBattle(self, battleID, direction, isDefence, attackTime):
        requestID = self._ClientFortMgr__getNextRequestID()
        if direction <= 0:
            LOG_ERROR('_scheduleBattle: Bad direction (should be >0)')
            return 
        if isDefence:
            direction = -direction
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.SCHEDULE_FORT_BATTLE, battleID, direction, attackTime)
        return requestID



    def getSortieData(self, unitMgrID, peripheryID):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.GET_SORTIE_DATA, unitMgrID, peripheryID, 0)
        return requestID



    def getFortBattleData(self, battleID):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.GET_FORT_BATTLE_DATA, battleID, 0, 0)
        return requestID



    def changeDefHour(self, defHour):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.CHANGE_DEF_HOUR, defHour, 0, 0)
        return requestID



    def shutdownDefHour(self):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.SHUTDOWN_DEF_HOUR, 0, 0, 0)
        return requestID



    def cancelDefHourShutdown(self):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.CANCEL_SHUTDOWN, 0, 0, 0)
        return requestID



    def changeOffDay(self, offDay):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.CHANGE_OFF_DAY, offDay, 0, 0)
        return requestID



    def changePeriphery(self, peripheryID):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.CHANGE_PERIPHERY, peripheryID, 0, 0)
        return requestID



    def changeVacation(self, timeVacationStart, timeVacationDuration):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.CHANGE_VACATION, timeVacationStart, timeVacationDuration, 0)
        return requestID



    def setDevMode(self, isOn = True):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.SET_DEV_MODE, int(isOn), 0, 0)
        return requestID



    def addTimeShift(self, timeShiftSeconds = 3600):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.ADD_TIME_SHIFT, timeShiftSeconds, 0, 0)
        return requestID



    def keepalive(self):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.KEEPALIVE, 0, 0, 0)
        return requestID



    def onResponseFortPublicInfo(self, requestID, errorID, resultSet):
        self.onFortPublicInfoReceived(requestID, errorID, resultSet)



    def getEnemyClanCard(self, enemyClanDBID):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.GET_ENEMY_CLAN_CARD, enemyClanDBID, 0, 0)
        return requestID



    def addFavorite(self, clanDBID):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.ADD_FAVORITE, clanDBID, 0, 0)
        return requestID



    def removeFavorite(self, clanDBID):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.REMOVE_FAVORITE, clanDBID, 0, 0)
        return requestID



    def planAttack(self, enemyClanDBID, timeAttack, dirFrom, dirTo):
        requestID = self._ClientFortMgr__getNextRequestID()
        dirFromToByte = makeDirPosByte(dirFrom, dirTo)
        if isinstance(timeAttack, basestring):
            try:
                fmt = '%d.%m.%Y %H:%M'
                timeAttack = int(time.mktime(time.strptime(timeAttack, fmt)))
            except:
                LOG_DEBUG('timeAttack should be either int(unixtime) or "%d.%m.%Y %H:%M" format.')
                return 
        elif timeAttack < 0:
            defHour = -timeAttack
            timeAttack = self._ClientFortMgr__getClosestAttackHour(defHour)
            LOG_DEBUG('timeAttack<0: plan attack for earliest possible defHour(%s), timeAttack=%s' % (defHour, timeAttack))
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.PLAN_ATTACK, enemyClanDBID, timeAttack, dirFromToByte)
        return requestID



    def activateConsumable(self, consumableTypeID, slotIndex = -1):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.ACTIVATE_CONSUMABLE, 0, consumableTypeID, slotIndex)
        return requestID



    def returnConsumable(self, consumableTypeID):
        requestID = self._ClientFortMgr__getNextRequestID()
        self._ClientFortMgr__callFortMethod(requestID, FORT_CLIENT_METHOD.RETURN_CONSUMABLE, 0, consumableTypeID, 0)
        return requestID



    def __getClosestAttackHour(self, defHour):
        t = self._fort._getTime() + fortified_regions.g_cache.attackPreorderTime
        nextDayDefHour = t - t % SECONDS_PER_DAY + defHour * SECONDS_PER_HOUR
        if nextDayDefHour < t:
            nextDayDefHour += SECONDS_PER_DAY
        return nextDayDefHour




+++ okay decompyling clientfortmgr.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:32:34 CET
