# 2015.01.14 13:53:27 CET
import AccountCommands
import items
import collections
from functools import partial
from diff_utils import synchronizeDicts
from items import vehicles, tankmen
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

def getAmmoAsDict(ammo):
    ammoAsDict = collections.defaultdict(int)
    for i in xrange(len(ammo) / 2):
        ammoAsDict[ammo[(2 * i)]] += ammo[(2 * i + 1)]

    return ammoAsDict



class Inventory(object):

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
        invDiff = diff.get('inventory', None)
        if invDiff is not None:
            for (itemTypeIdx, itemInvDiff,) in invDiff.iteritems():
                synchronizeDicts(itemInvDiff, self.__cache.setdefault(itemTypeIdx, {}))

        cacheDiff = diff.get('cache', None)
        if cacheDiff is not None:
            vehsLockDiff = cacheDiff.get('vehsLock', None)
            if vehsLockDiff is not None:
                itemInvCache = self.__cache.setdefault(_VEHICLE, {})
                synchronizeDicts(vehsLockDiff, itemInvCache.setdefault('lock', {}))



    def getCache(self, callback):
        self.__syncData.waitForSync(partial(self.__onGetCacheResponse, callback))



    def getItems(self, itemTypeIdx, callback):
        self.__syncData.waitForSync(partial(self.__onGetItemsResponse, itemTypeIdx, callback))



    def sell(self, itemTypeIdx, itemInvID, count, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        if itemTypeIdx == _VEHICLE:
            self.sellVehicle(itemInvID, True, [], [], callback)
            return 
        if itemTypeIdx == _TANKMAN:
            if callback is not None:
                callback(AccountCommands.RES_WRONG_ARGS)
            return 
        self.__account.shop.waitForSync(partial(self.__sellItem_onShopSynced, itemTypeIdx, itemInvID, count, callback))



    def sellVehicle(self, vehInvID, dismissCrew, itemsFromVehicle, itemsFromInventory, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        self.__account.shop.waitForSync(partial(self.__sellVehicle_onShopSynced, vehInvID, dismissCrew, itemsFromVehicle, itemsFromInventory, callback))



    def dismissTankman(self, tmanInvID, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_DISMISS_TMAN, tmanInvID, 0, 0, proxy)



    def equip(self, vehInvID, itemCompDescr, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, 0, [])
            return 
        itemTypeIdx = vehicles.parseIntCompactDescr(itemCompDescr)[0]
        assert itemTypeIdx in (_CHASSIS,
         _GUN,
         _ENGINE,
         _FUEL_TANK,
         _RADIO)
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID, ext)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_EQUIP, vehInvID, itemCompDescr, 0, proxy)



    def equipTurret(self, vehInvID, turretCompDescr, gunCompDescr, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, 0, [])
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID, ext)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_EQUIP, vehInvID, turretCompDescr, gunCompDescr, proxy)



    def equipOptionalDevice(self, vehInvID, deviceCompDescr, slotIdx, isPaidRemoval, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, 0, [])
            return 
        self.__account.shop.waitForSync(partial(self.__equipOptionDevice_onShopSynced, vehInvID, deviceCompDescr, slotIdx, isPaidRemoval, callback))



    def equipShells(self, vehInvID, shells, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, [])
            return 
        arr = [vehInvID] + [ int(s) for s in shells ]
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdIntArr(AccountCommands.CMD_EQUIP_SHELLS, arr, proxy)



    def equipEquipments(self, vehInvID, eqs, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, [])
            return 
        arr = [vehInvID] + [ int(e) for e in eqs ]
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdIntArr(AccountCommands.CMD_EQUIP_EQS, arr, proxy)



    def setAndFillLayouts(self, vehInvID, shellsLayout, eqsLayout, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, '', {})
            return 
        self.__account.shop.waitForSync(partial(self.__setAndFillLayouts_onShopSynced, vehInvID, shellsLayout, eqsLayout, callback))



    def equipTankman(self, vehInvID, slot, tmanInvID, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, [])
            return 
        if tmanInvID is None:
            tmanInvID = -1
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_EQUIP_TMAN, vehInvID, slot, tmanInvID, proxy)



    def returnCrew(self, vehInvID, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, [])
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_RETURN_CREW, vehInvID, 0, 0, proxy)



    def repair(self, vehInvID, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_REPAIR, vehInvID, 0, 0, proxy)



    def addTankmanSkill(self, tmanInvID, skillName, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        skillIdx = tankmen.SKILL_INDICES[skillName]
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_TMAN_ADD_SKILL, tmanInvID, skillIdx, 0, proxy)



    def dropTankmanSkills(self, tmanInvID, dropSkillsCostIdx, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        self.__account.shop.waitForSync(partial(self.__dropSkillsTman_onShopSynced, tmanInvID, dropSkillsCostIdx, callback))



    def respecTankman(self, tmanInvID, vehTypeCompDescr, tmanCostTypeIdx, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        if vehTypeCompDescr is None:
            vehTypeCompDescr = 0
        self.__account.shop.waitForSync(partial(self.__respecTman_onShopSynced, tmanInvID, vehTypeCompDescr, tmanCostTypeIdx, callback))



    def multiRespecTankman(self, tmenInvIDsAndCostTypeIdx, vehTypeCompDescr, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        if vehTypeCompDescr is None:
            vehTypeCompDescr = 0
        self.__account.shop.waitForSync(partial(self.__multiRespecTman_onShopSynced, tmenInvIDsAndCostTypeIdx, vehTypeCompDescr, callback))



    def replacePassport(self, tmanInvID, isPremium, isFemale, fnGroupID, firstNameID, lnGroupID, lastNameID, iGroupID, iconID, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        self.__account.shop.waitForSync(partial(self.__replacePassport_onShopSynced, tmanInvID, isPremium, isFemale, fnGroupID, firstNameID, lnGroupID, lastNameID, iGroupID, iconID, callback))



    def freeXPToTankman(self, tmanInvID, freeXP, callback):
        if self.__ignore:
            if callback is not None:
                callback('', AccountCommands.RES_NON_PLAYER)
            return 
        self.__account.shop.waitForSync(partial(self.__freeXPToTankman_onShopSynced, tmanInvID, freeXP, callback))



    def changeVehicleSetting(self, vehInvID, setting, isOn, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        isOn = 1 if isOn else 0
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_VEH_SETTINGS, vehInvID, setting, isOn, proxy)



    def changeVehicleCamouflage(self, vehInvID, camouflageKind, camouflageID, periodDays, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        self.__account.shop.waitForSync(partial(self.__changeVehCamouflage_onShopSynced, vehInvID, camouflageKind, camouflageID, periodDays, callback))



    def changeVehicleEmblem(self, vehInvID, position, emblemID, periodDays, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        self.__account.shop.waitForSync(partial(self.__changeVehEmblem_onShopSynced, vehInvID, position, emblemID, periodDays, callback))



    def changeVehicleInscription(self, vehInvID, position, inscriptionID, periodDays, colorID, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        self.__account.shop.waitForSync(partial(self.__changeVehInscription_onShopSynced, vehInvID, position, inscriptionID, periodDays, colorID, callback))



    def changeVehicleHorn(self, vehInvID, hornID, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        self.__account.shop.waitForSync(partial(self.__changeVehHorn_onShopSynced, vehInvID, hornID, callback))



    def addTankmanExperience(self, tmanInvID, xp, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_ADD_TMAN_XP, tmanInvID, xp, 0, proxy)



    def __onGetItemsResponse(self, itemTypeIdx, callback, resultID):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None)
            return 
        if callback is not None:
            callback(resultID, self.__cache.get(itemTypeIdx, None))



    def __onGetCacheResponse(self, callback, resultID):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None)
            return 
        if callback is not None:
            callback(resultID, self.__cache)



    def __sellItem_onShopSynced(self, itemTypeIdx, itemInvID, count, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt4(AccountCommands.CMD_SELL_ITEM, shopRev, itemTypeIdx, itemInvID, count, proxy)



    def __sellVehicle_onShopSynced(self, vehInvID, flags, itemsFromVehicle, itemsFromInventory, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        arr = [shopRev,
         vehInvID,
         flags,
         len(itemsFromVehicle)] + itemsFromVehicle
        arr += [len(itemsFromInventory)] + itemsFromInventory
        self.__account._doCmdIntArr(AccountCommands.CMD_SELL_VEHICLE, arr, proxy)



    def __dropSkillsTman_onShopSynced(self, tmanInvID, dropSkillsCostIdx, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_TMAN_DROP_SKILLS, shopRev, tmanInvID, dropSkillsCostIdx, proxy)



    def __respecTman_onShopSynced(self, tmanInvID, vehTypeCompDescr, tmanCostTypeIdx, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt4(AccountCommands.CMD_TMAN_RESPEC, shopRev, tmanInvID, tmanCostTypeIdx, vehTypeCompDescr, proxy)



    def __multiRespecTman_onShopSynced(self, tmenInvIDsAndCostTypeIdx, vehTypeCompDescr, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        arr = [shopRev, vehTypeCompDescr]
        for (tmanInvID, tmanCostTypeIdx,) in tmenInvIDsAndCostTypeIdx:
            arr.append(tmanInvID)
            arr.append(tmanCostTypeIdx)

        self.__account._doCmdIntArr(AccountCommands.CMD_TMAN_MULTI_RESPEC, arr, proxy)



    def __replacePassport_onShopSynced(self, tmanInvID, isPremium, isFemale, fnGroupID, firstNameID, lnGroupID, lastNameID, iGroupID, iconID, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            return 
        arr = [shopRev, tmanInvID, isPremium]
        if isFemale is None:
            arr.append(-1)
        elif isFemale:
            arr.append(1)
        else:
            arr.append(0)
        arr.append(fnGroupID)
        arr.append(firstNameID if firstNameID is not None else -1)
        arr.append(lnGroupID)
        arr.append(lastNameID if lastNameID is not None else -1)
        arr.append(iGroupID)
        arr.append(iconID if iconID is not None else -1)
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdIntArr(AccountCommands.CMD_TMAN_PASSPORT, arr, proxy)



    def __freeXPToTankman_onShopSynced(self, tmanInvID, freeXP, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback('', resultID)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(errorStr, resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_TRAINING_TMAN, shopRev, tmanInvID, freeXP, proxy)



    def __changeVehCamouflage_onShopSynced(self, vehInvID, camouflageKind, camouflageID, periodDays, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        arr = [shopRev,
         vehInvID,
         camouflageKind,
         camouflageID,
         periodDays]
        self.__account._doCmdIntArr(AccountCommands.CMD_VEH_CAMOUFLAGE, arr, proxy)



    def __setAndFillLayouts_onShopSynced(self, vehInvID, shellsLayout, eqsLayout, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID, '', {})
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID, errorStr, ext)
        else:
            proxy = None
        arr = [shopRev, vehInvID]
        if shellsLayout is not None:
            arr.append(len(shellsLayout))
            arr += shellsLayout
        else:
            arr.append(0)
        if eqsLayout is not None:
            arr.append(len(eqsLayout))
            arr += eqsLayout
        else:
            arr.append(0)
        self.__account._doCmdIntArr(AccountCommands.CMD_SET_AND_FILL_LAYOUTS, arr, proxy)



    def __changeVehEmblem_onShopSynced(self, vehInvID, position, emblemID, periodDays, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        arr = [shopRev,
         vehInvID,
         position,
         emblemID,
         periodDays]
        self.__account._doCmdIntArr(AccountCommands.CMD_VEH_EMBLEM, arr, proxy)



    def __changeVehInscription_onShopSynced(self, vehInvID, position, inscriptionID, periodDays, colorID, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        arr = [shopRev,
         vehInvID,
         position,
         inscriptionID,
         periodDays,
         colorID]
        self.__account._doCmdIntArr(AccountCommands.CMD_VEH_INSCRIPTION, arr, proxy)



    def __equipOptionDevice_onShopSynced(self, vehInvID, deviceCompDescr, slotIdx, isPaidRemoval, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        arr = [shopRev,
         vehInvID,
         deviceCompDescr,
         slotIdx,
         int(isPaidRemoval)]
        self.__account._doCmdIntArr(AccountCommands.CMD_EQUIP_OPTDEV, arr, proxy)



    def __changeVehHorn_onShopSynced(self, vehInvID, hornID, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_VEH_HORN, shopRev, vehInvID, hornID, proxy)




+++ okay decompyling inventory.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:53:28 CET
