# 2015.01.14 13:53:29 CET
import AccountCommands
import items
from functools import partial
from diff_utils import synchronizeDicts
from items import vehicles
from debug_utils import *
_VEHICLE = items.ITEM_TYPE_INDICES['vehicle']
_CHASSIS = items.ITEM_TYPE_INDICES['vehicleChassis']
_TURRET = items.ITEM_TYPE_INDICES['vehicleTurret']
_GUN = items.ITEM_TYPE_INDICES['vehicleGun']
_ENGINE = items.ITEM_TYPE_INDICES['vehicleEngine']
_FUEL_TANK = items.ITEM_TYPE_INDICES['vehicleFuelTank']
_RADIO = items.ITEM_TYPE_INDICES['vehicleRadio']
_TANKMAN = items.ITEM_TYPE_INDICES['tankman']
_OPTIONALDEVICE = items.ITEM_TYPE_INDICES['optionalDevice']
_SHELL = items.ITEM_TYPE_INDICES['shell']
_EQUIPMENT = items.ITEM_TYPE_INDICES['equipment']
_SIMPLE_VALUE_STATS = ('credits', 'gold', 'slots', 'berths', 'freeXP', 'dossier', 'clanInfo', 'accOnline', 'accOffline', 'freeTMenLeft', 'freeVehiclesLeft', 'vehicleSellsLeft', 'captchaTriesLeft', 'hasFinPassword', 'finPswdAttemptsLeft', 'tkillIsSuspected', 'denunciationsLeft', 'tutorialsCompleted', 'battlesTillCaptcha', 'dailyPlayHours', 'playLimits', 'globalRating')
_DICT_STATS = ('vehTypeXP', 'vehTypeLocks', 'restrictions', 'globalVehicleLocks', 'refSystem')
_GROWING_SET_STATS = ('unlocks', 'eliteVehicles', 'multipliedXPVehs')
_ACCOUNT_STATS = ('clanDBID', 'attrs', 'premiumExpiryTime', 'autoBanTime')
_CACHE_STATS = ('isFinPswdVerified', 'mayConsumeWalletResources', 'unitAcceptDeadline')

class Stats(object):

    def __init__(self, syncData):
        self.__account = None
        self.__syncData = syncData
        self.__cache = {}
        self.__ignore = True



    def onAccountBecomePlayer(self):
        self.__ignore = False



    def onAccountBecomeNonPlayer(self):
        self.__ignore = True



    def setAccount(self, account):
        self.__account = account



    def synchronize(self, isFullSync, diff):
        if isFullSync:
            self.__cache.clear()
        cache = self.__cache
        statsDiff = diff.get('stats', None)
        if statsDiff is not None:
            for stat in _SIMPLE_VALUE_STATS:
                if stat in statsDiff:
                    cache[stat] = statsDiff[stat]

            for stat in _DICT_STATS:
                stat_r = (stat, '_r')
                if stat_r in statsDiff:
                    cache[stat] = statsDiff[stat_r]
                if stat in statsDiff:
                    synchronizeDicts(statsDiff[stat], cache.setdefault(stat, dict()))

            for stat in _GROWING_SET_STATS:
                stat_r = (stat, '_r')
                if stat_r in statsDiff:
                    cache[stat] = statsDiff[stat_r]
                if stat in statsDiff:
                    cache.setdefault(stat, set()).update(statsDiff[stat])

        accountDiff = diff.get('account', None)
        if accountDiff is not None:
            for stat in _ACCOUNT_STATS:
                if stat in accountDiff:
                    cache[stat] = accountDiff[stat]

        economicsDiff = diff.get('economics', None)
        if economicsDiff is not None:
            for stat in ('unlocks', 'eliteVehicles'):
                if stat in economicsDiff:
                    cache.setdefault(stat, set()).update(economicsDiff[stat])

        cacheDiff = diff.get('cache', None)
        if cacheDiff is not None:
            for stat in _CACHE_STATS:
                if stat in cacheDiff:
                    cache[stat] = cacheDiff[stat]




    def getCache(self, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, None)
            return 
        self.__syncData.waitForSync(partial(self.__onGetCacheResponse, callback))



    def get(self, statName, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, None)
            return 
        self.__syncData.waitForSync(partial(self.__onGetResponse, statName, callback))



    def unlock(self, vehTypeCompDescr, unlockIdx, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_UNLOCK, vehTypeCompDescr, unlockIdx, 0, proxy)



    def setCurrentVehicle(self, vehInvID, callback = None):
        LOG_WARNING('Deprecated. setCurrentVehicle')



    def exchange(self, gold, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        self.__account.shop.getExchangeRate(partial(self.__exchange_onGetRate, gold, callback))



    def convertToFreeXP(self, vehTypeCompDescrs, xp, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        self.__account.shop.getFreeXPConversion(partial(self.__convertToFreeXP_onGetParameters, vehTypeCompDescrs, xp, callback))



    def upgradeToPremium(self, days, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, 0)
            return 
        self.__account.shop.getPremiumCost(partial(self.__premium_onGetPremCost, days, callback))



    def buySlot(self, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, 0)
            return 
        self.__account.shop.waitForSync(partial(self.__slot_onShopSynced, callback))



    def buyPotapovQuestSlot(self, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, 0)
            return 
        self.__account.shop.waitForSync(partial(self.__potapovQuestSlot_onShopSynced, callback))



    def buyPotapovQuestTile(self, tileID, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, 0)
            return 
        self.__account.shop.waitForSync(partial(self.__potapovQuestTile_onShopSynced, tileID, callback))



    def buyBerths(self, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, 0)
            return 
        self.__account.shop.waitForSync(partial(self.__berths_onShopSynced, callback))



    def setMoney(self, credits, gold = 0, freeXP = 0, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_SET_MONEY, credits, gold, freeXP, proxy)



    def addExperience(self, vehTypeName, xp, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        vehTypeCompDescr = vehicles.makeIntCompactDescrByID('vehicle', *vehicles.g_list.getIDsByName(vehTypeName))
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_ADD_XP, vehTypeCompDescr, xp, 0, proxy)



    def unlockAll(self, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_UNLOCK_ALL, 0, 0, 0, proxy)



    def __onGetResponse(self, statName, callback, resultID):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None)
            return 
        if callback is not None:
            callback(resultID, self.__cache.get(statName, None))



    def __onGetCacheResponse(self, callback, resultID):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None)
            return 
        if callback is not None:
            callback(resultID, self.__cache)



    def __exchange_onGetRate(self, gold, callback, resultID, exchRate, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None)
            return 
        if exchRate is None:
            LOG_ERROR('Result of the getExchangeRate request is None')
            if callback is not None:
                callback(AccountCommands.RES_FAILURE)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_EXCHANGE, shopRev, gold, 0, proxy)



    def __convertToFreeXP_onGetParameters(self, vehTypeCompDescrs, xp, callback, resultID, freeXPConversion, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None)
            return 
        if freeXPConversion is None:
            LOG_ERROR('Result of the getFreeXPConversion request is None')
            if callback is not None:
                callback(AccountCommands.RES_FAILURE)
            return 
        arr = [shopRev, xp] + list(vehTypeCompDescrs)
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdIntArr(AccountCommands.CMD_FREE_XP_CONV, arr, proxy)



    def __premium_onGetPremCost(self, days, callback, resultID, premCost, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None)
            return 
        if premCost is None:
            LOG_ERROR('Result of the getPremiumCost request is None')
            if callback is not None:
                callback(AccountCommands.RES_FAILURE)
            return 
        gold = premCost.get(days, None)
        if gold is None:
            LOG_ERROR('Wrong days number')
            if callback is not None:
                callback(AccountCommands.RES_WRONG_ARGS)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_PREMIUM, shopRev, days, 0, proxy)



    def __slot_onShopSynced(self, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_BUY_SLOT, shopRev, 0, 0, proxy)



    def __potapovQuestSlot_onShopSynced(self, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_BUY_POTAPOV_QUEST_SLOT, shopRev, 0, 0, proxy)



    def __potapovQuestTile_onShopSynced(self, tileID, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_BUY_POTAPOV_QUEST_TILE, shopRev, tileID, 0, proxy)



    def __berths_onShopSynced(self, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_BUY_BERTHS, shopRev, 0, 0, proxy)




+++ okay decompyling stats.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:53:29 CET
