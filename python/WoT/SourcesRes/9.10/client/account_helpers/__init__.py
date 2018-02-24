# 2015.01.14 13:53:29 CET
import BigWorld
import constants
import datetime

def __checkAccountAttr(attrs, attrID):
    return attrs is not None and attrs & attrID != 0



def isPremiumAccount(attrs):
    return __checkAccountAttr(attrs, constants.ACCOUNT_ATTR.PREMIUM)



def isMoneyTransfer(attrs):
    return __checkAccountAttr(attrs, constants.ACCOUNT_ATTR.TRADING)



def isDemonstrator(attrs):
    return __checkAccountAttr(attrs, constants.ACCOUNT_ATTR.ARENA_CHANGE)



def isRoamingEnabled(attrs):
    return __checkAccountAttr(attrs, constants.ACCOUNT_ATTR.ROAMING)



def getPremiumExpiryDelta(expiryTime):
    check = datetime.datetime.utcfromtimestamp(expiryTime)
    now = datetime.datetime.utcnow()
    return check - now



def convertGold(gold):
    return gold



def getPlayerID():
    return getattr(BigWorld.player(), 'id', 0L)



def getPlayerDatabaseID():
    return getattr(BigWorld.player(), 'databaseID', 0L)



+++ okay decompyling __init__.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:53:29 CET
