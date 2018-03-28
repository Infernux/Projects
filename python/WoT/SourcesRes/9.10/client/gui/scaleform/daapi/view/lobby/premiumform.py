# 2015.01.14 22:14:36 CET
import BigWorld
from adisp import process
from gui.ClientUpdateManager import g_clientUpdateManager
from gui.Scaleform.daapi.view.meta.PremiumFormMeta import PremiumFormMeta
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView
from gui.Scaleform.daapi.view.dialogs import I18nConfirmDialogMeta
from gui.Scaleform.framework.entities.View import View
from gui.shared import g_itemsCache
from gui.shared.utils.requesters import DeprecatedStatsRequester, StatsRequester
import account_helpers
from gui import SystemMessages, DialogsInterface
from gui.Scaleform.locale.SYSTEM_MESSAGES import SYSTEM_MESSAGES
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.framework import AppRef
from gui.shared.utils.gui_items import formatPrice

class PremiumForm(View, AbstractWindowView, PremiumFormMeta, AppRef):

    def _populate(self):
        super(PremiumForm, self)._populate()
        g_clientUpdateManager.addCallbacks({'stats.gold': self.onSetGoldHndlr,
         'cache.mayConsumeWalletResources': self.onSetGoldHndlr})
        g_itemsCache.onSyncCompleted += self.__premiumDataRequest



    def _dispose(self):
        g_itemsCache.onSyncCompleted -= self.__premiumDataRequest
        g_clientUpdateManager.removeObjectCallbacks(self)
        super(PremiumForm, self)._dispose()



    def onWindowClose(self):
        self.destroy()



    def onPremiumDataRequest(self):
        self.__premiumDataRequest()



    def onPremiumBuy(self, days, price):
        self.__premiumBuyRequest(days, price)



    def onSetGoldHndlr(self, _):
        self.as_setGoldS(g_itemsCache.items.stats.gold)



    @process
    def __premiumBuyRequest(self, days, price):
        stats = yield StatsRequester().request()
        if account_helpers.isPremiumAccount(stats.attributes):
            dialogId = 'premiumContinueConfirmation'
        else:
            dialogId = 'premiumBuyConfirmation'
        isOk = yield DialogsInterface.showDialog(I18nConfirmDialogMeta(dialogId, messageCtx={'days': int(days),
         'gold': BigWorld.wg_getGoldFormat(price)}))
        if isOk and days:
            if stats.gold < price:
                self.__systemErrorMessage(SYSTEM_MESSAGES.PREMIUM_NOT_ENOUGH_GOLD, days, SystemMessages.SM_TYPE.Warning)
            else:
                self.__upgradeToPremium(days)
            self.destroy()



    def __premiumDataRequest(self, *args):
        stats = g_itemsCache.items.stats
        premiumCost = g_itemsCache.items.shop.premiumCost
        premiumCost = sorted(premiumCost.items(), reverse=True)
        defaultPremiumCost = g_itemsCache.items.shop.defaults.premiumCost
        defaultPremiumCost = sorted(defaultPremiumCost.items(), reverse=True)
        args = []
        for (idx, (period, cost,),) in enumerate(premiumCost):
            (_, defaultCost,) = defaultPremiumCost[idx]
            args.append({'days': period,
             'price': defaultCost,
             'discountPrice': cost})

        gold = stats.gold
        isPremiumAccount = account_helpers.isPremiumAccount(stats.attributes)
        self.as_setCostsS(args)
        self.as_setPremiumS(isPremiumAccount)
        self.as_setGoldS(gold)



    @process
    def __upgradeToPremium(self, days):
        Waiting.show('loadStats')
        attrs = yield DeprecatedStatsRequester().getAccountAttrs()
        isPremium = account_helpers.isPremiumAccount(attrs)
        success = yield DeprecatedStatsRequester().upgradeToPremium(days)
        if success:
            premiumCost = yield DeprecatedStatsRequester().getPremiumCost()
            if premiumCost:
                if isPremium:
                    successMessage = SYSTEM_MESSAGES.PREMIUM_CONTINUESUCCESS
                else:
                    successMessage = SYSTEM_MESSAGES.PREMIUM_BUYINGSUCCESS
                SystemMessages.pushI18nMessage(successMessage, days, formatPrice((0, premiumCost[int(days)])), type=SystemMessages.SM_TYPE.PurchaseForGold)
        else:
            self.__systemErrorMessage(SYSTEM_MESSAGES.PREMIUM_SERVER_ERROR, days, SystemMessages.SM_TYPE.Error)
        Waiting.hide('loadStats')



    def __systemErrorMessage(self, systemMessage, days, typeMessage):
        SystemMessages.g_instance.pushI18nMessage(systemMessage, days, type=typeMessage)




+++ okay decompyling premiumform.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:14:36 CET
