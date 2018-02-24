# 2015.01.14 13:53:29 CET
import AccountCommands
import offers
from functools import partial
from debug_utils import *

class Trader(object):

    def __init__(self, syncData):
        self.__account = None
        self.__syncData = syncData
        self.__offersData = {'out': {},
         'in': {}}
        self.__outOffers = offers.OutOffers(self.__offersData)
        self.__inOffers = offers.InOffers(self.__offersData)



    def onAccountBecomePlayer(self):
        self.__ignore = False



    def onAccountBecomeNonPlayer(self):
        self.__ignore = True



    def setAccount(self, account):
        self.__account = account



    def synchronize(self, isFullSync, diff):
        if isFullSync:
            self.__offersData['out'].clear()
            self.__offersData['in'].clear()
        offersDiff = diff.get('offers', None)
        if offersDiff is None:
            return 
        for kind in ('in', 'out'):
            subdiff = offersDiff.get(kind)
            if subdiff is None:
                continue
            data = self.__offersData[kind]
            for (offerID, offerData,) in subdiff.iteritems():
                if offerData is None:
                    data.pop(offerID, None)
                else:
                    data[offerID] = offerData





    def getOffers(self, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, None, None)
            return 
        self.__syncData.waitForSync(partial(self.__onGetResponse, callback))



    def makeOffer_sellGold(self, passwd, dstClassName, dstDBID, validSec, outGold, inCredits, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errorStr: callback(resultID, errorStr)
        else:
            proxy = None
        flags = offers.makeOfferFlags(offers.OFFER_SELL, offers.SRC_WARE_GOLD, offers.DST_WARE_CREDITS, offers.ENTITY_TYPE_IDS_BY_NAMES['Account'], offers.ENTITY_TYPE_IDS_BY_NAMES[dstClassName])
        self.__account._makeTradeOffer(passwd, flags, dstDBID, validSec, inCredits, outGold, 0, proxy)



    def revokeOffer(self, outOfferID, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errString, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_REVOKE_TRADE_OFFER, outOfferID, 0, 0, proxy)



    def acceptOffer(self, passwd, inOfferID, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errString, ext = {}: callback(resultID, errString)
        else:
            proxy = None
        self.__account._doCmdInt2Str(AccountCommands.CMD_ACCEPT_TRADE_OFFER, inOfferID, 0, passwd, proxy)



    def declineOffer(self, inOfferID, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            return 
        if callback is not None:
            proxy = lambda requestID, resultID, errString, ext = {}: callback(resultID)
        else:
            proxy = None
        self.__account._doCmdInt3(AccountCommands.CMD_DECLINE_TRADE_OFFER, inOfferID, 0, 0, proxy)



    def __onGetResponse(self, callback, resultID):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None, None)
            return 
        if callback is not None:
            callback(resultID, self.__inOffers, self.__outOffers)




+++ okay decompyling trader.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:53:29 CET
