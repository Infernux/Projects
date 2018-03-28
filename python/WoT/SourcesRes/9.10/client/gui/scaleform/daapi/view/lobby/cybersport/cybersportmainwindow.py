# 2015.01.14 22:14:46 CET
from UnitBase import UNIT_BROWSER_ERROR
from adisp import process
from constants import PREBATTLE_TYPE
from debug_utils import LOG_ERROR
from gui import DialogsInterface, SystemMessages
from gui.LobbyContext import g_lobbyContext
from gui.Scaleform.daapi.view.dialogs.rally_dialog_meta import UnitConfirmDialogMeta
from gui.Scaleform.daapi.view.lobby.rally import NavigationStack
from gui.Scaleform.daapi.view.lobby.cyberSport.CyberSportIntroView import CyberSportIntroView
from gui.Scaleform.daapi.view.meta.CyberSportMainWindowMeta import CyberSportMainWindowMeta
from gui.Scaleform.genConsts.CYBER_SPORT_ALIASES import CYBER_SPORT_ALIASES
from gui.Scaleform.locale.CYBERSPORT import CYBERSPORT
from gui.prb_control.events_dispatcher import g_eventDispatcher
from gui.prb_control.context import unit_ctx
from gui.prb_control.formatters import messages
from gui.prb_control.prb_helpers import prbPeripheriesHandlerProperty
from gui.prb_control import settings
from gui.prb_control.settings import SELECTOR_BATTLE_TYPES, FUNCTIONAL_EXIT
from gui.shared import EVENT_BUS_SCOPE, events
from gui.shared.utils import SelectorBattleTypesUtils as selectorUtils
from helpers import i18n
from gui.Scaleform.managers.windows_stored_data import DATA_TYPE, TARGET_ID
from gui.Scaleform.managers.windows_stored_data import stored_window

@stored_window(DATA_TYPE.UNIQUE_WINDOW, TARGET_ID.CHANNEL_CAROUSEL)
class CyberSportMainWindow(CyberSportMainWindowMeta):

    def __init__(self, ctx = None):
        super(CyberSportMainWindow, self).__init__()
        self.currentState = ''
        selectorUtils.setBattleTypeAsKnown(SELECTOR_BATTLE_TYPES.UNIT)



    def getIntroViewAlias(self):
        return CYBER_SPORT_ALIASES.INTRO_VIEW_UI



    def getFlashAliases(self):
        return CYBER_SPORT_ALIASES.FLASH_ALIASES



    def getPythonAliases(self):
        return CYBER_SPORT_ALIASES.PYTHON_ALIASES



    def getPrbType(self):
        return PREBATTLE_TYPE.UNIT



    def getNavigationKey(self):
        return 'CyberSportMainWindow'



    @prbPeripheriesHandlerProperty
    def prbPeripheriesHandler(self):
        return None



    def onUnitFunctionalInited(self):
        self._requestViewLoad(CYBER_SPORT_ALIASES.UNIT_VIEW_UI, self.unitFunctional.getID())



    def onUnitFunctionalFinished(self):
        CyberSportIntroView._selectedVehicles = None
        if self.unitFunctional.getExit() == settings.FUNCTIONAL_EXIT.INTRO_UNIT:
            if self.unitFunctional.isKicked():
                self._goToNextView(closeForced=True)
        else:
            NavigationStack.clear(self.getNavigationKey())



    def onUnitRejoin(self):
        if not self.unitFunctional.getState().isInIdle():
            self.__clearState()



    def onUnitStateChanged(self, state, timeLeft):
        if state.isInIdle():
            if state.isInSearch():
                self.as_enableWndCloseBtnS(False)
                self.currentState = CYBER_SPORT_ALIASES.AUTO_SEARCH_WAITING_PLAYERS_STATE
            elif state.isInQueue():
                self.as_enableWndCloseBtnS(False)
                self.currentState = CYBER_SPORT_ALIASES.AUTO_SEARCH_ENEMY_STATE
            else:
                LOG_ERROR('View for modal state is not resolved', state)
            self.__initState(timeLeft=timeLeft)
        else:
            self.__clearState()



    def onUnitPlayerStateChanged(self, pInfo):
        if self.unitFunctional.getState().isInIdle():
            self.__initState()



    def onUnitErrorReceived(self, errorCode):
        self.as_autoSearchEnableBtnS(True)



    def onUnitPlayerOnlineStatusChanged(self, pInfo):
        if pInfo.isOffline():
            key = settings.UNIT_NOTIFICATION_KEY.PLAYER_OFFLINE
        else:
            key = settings.UNIT_NOTIFICATION_KEY.PLAYER_ONLINE
        self.__addPlayerNotification(key, pInfo)



    def onUnitPlayerAdded(self, pInfo):
        if not pInfo.isInvite():
            self.__addPlayerNotification(settings.UNIT_NOTIFICATION_KEY.PLAYER_ADDED, pInfo)



    def onUnitPlayerRemoved(self, pInfo):
        if not pInfo.isInvite():
            self.__addPlayerNotification(settings.UNIT_NOTIFICATION_KEY.PLAYER_REMOVED, pInfo)



    def onUnitPlayerBecomeCreator(self, pInfo):
        if pInfo.isCurrentPlayer():
            self._showLeadershipNotification()
        chat = self.chat
        if chat:
            chat.as_addMessageS(messages.getUnitPlayerNotification(settings.UNIT_NOTIFICATION_KEY.GIVE_LEADERSHIP, pInfo))



    def onIntroUnitFunctionalFinished(self):
        if self.unitFunctional.getExit() != settings.FUNCTIONAL_EXIT.UNIT:
            NavigationStack.clear(self.getNavigationKey())



    def onUnitAutoSearchStarted(self, timeLeft):
        self.currentState = CYBER_SPORT_ALIASES.AUTO_SEARCH_COMMANDS_STATE
        self.as_enableWndCloseBtnS(False)
        self.__initState(timeLeft=timeLeft)



    def onUnitAutoSearchFinished(self):
        self.__clearState()



    def onUnitAutoSearchSuccess(self, acceptDelta):
        self.currentState = CYBER_SPORT_ALIASES.AUTO_SEARCH_CONFIRMATION_STATE
        self.__initState(acceptDelta=acceptDelta)
        from BigWorld import WGWindowsNotifier
        WGWindowsNotifier.onInvitation()



    def onUnitBrowserErrorReceived(self, errorCode):
        if errorCode == UNIT_BROWSER_ERROR.ACCEPT_TIMEOUT:
            self.currentState = CYBER_SPORT_ALIASES.AUTO_SEARCH_ERROR_STATE
            self.__initState()
        else:
            self.as_autoSearchEnableBtnS(True)



    def onWindowClose(self):
        self.prbDispatcher.doLeaveAction(unit_ctx.LeaveUnitCtx(waitingID='prebattle/leave', funcExit=FUNCTIONAL_EXIT.NO_FUNC))



    def onWindowMinimize(self):
        self.destroy()
        g_eventDispatcher.showUnitProgressInCarousel(PREBATTLE_TYPE.UNIT)



    def onAutoMatch(self, value, vehTypes):
        if value == CYBER_SPORT_ALIASES.INTRO_VIEW_UI:
            self.unitFunctional.request(unit_ctx.AutoSearchUnitCtx(vehTypes=vehTypes))



    def onBrowseRallies(self):
        self._requestViewLoad(CYBER_SPORT_ALIASES.UNITS_LIST_VIEW_UI, None)



    def onCreateRally(self):
        self.__requestToCreate()



    def onJoinRally(self, rallyId, slotIndex, peripheryID):
        ctx = unit_ctx.JoinUnitCtx(rallyId, self.getPrbType(), slotIndex, waitingID='prebattle/join')
        if g_lobbyContext.isAnotherPeriphery(peripheryID):
            if g_lobbyContext.isPeripheryAvailable(peripheryID):
                self.__requestToReloginAndJoin(peripheryID, ctx)
            else:
                SystemMessages.pushI18nMessage('#system_messages:periphery/errors/isNotAvailable', type=SystemMessages.SM_TYPE.Error)
        else:
            self.__requestToJoin(ctx)



    def autoSearchApply(self, value):
        if value == CYBER_SPORT_ALIASES.AUTO_SEARCH_CONFIRMATION_STATE:
            self.unitFunctional.request(unit_ctx.AcceptSearchUnitCtx())
        elif value == CYBER_SPORT_ALIASES.AUTO_SEARCH_ERROR_STATE:
            self.currentState = CYBER_SPORT_ALIASES.AUTO_SEARCH_COMMANDS_STATE
            self.unitFunctional.request(unit_ctx.AutoSearchUnitCtx())



    def autoSearchCancel(self, value):
        self.currentState = value
        if value == CYBER_SPORT_ALIASES.AUTO_SEARCH_COMMANDS_STATE or value == CYBER_SPORT_ALIASES.AUTO_SEARCH_ERROR_STATE or value == CYBER_SPORT_ALIASES.AUTO_SEARCH_WAITING_PLAYERS_STATE:
            self.unitFunctional.request(unit_ctx.AutoSearchUnitCtx(action=0))
        elif value == CYBER_SPORT_ALIASES.AUTO_SEARCH_CONFIRMATION_STATE:
            self.unitFunctional.request(unit_ctx.DeclineSearchUnitCtx())
        elif value == CYBER_SPORT_ALIASES.AUTO_SEARCH_ENEMY_STATE:
            self.unitFunctional.request(unit_ctx.BattleQueueUnitCtx(action=0))



    def _populate(self):
        super(CyberSportMainWindow, self)._populate()
        self.addListener(events.HideWindowEvent.HIDE_UNIT_WINDOW, self.__handleUnitWindowHide, scope=EVENT_BUS_SCOPE.LOBBY)
        unitMgrID = self.unitFunctional.getID()
        if unitMgrID > 0:
            self._requestViewLoad(CYBER_SPORT_ALIASES.UNIT_VIEW_UI, unitMgrID)
        else:
            self.__initIntroUnitView()
        self.unitFunctional.initEvents(self)
        g_eventDispatcher.hideUnitProgressInCarousel(PREBATTLE_TYPE.UNIT)



    def _dispose(self):
        self._itemIdMap = None
        super(CyberSportMainWindow, self)._dispose()
        self.removeListener(events.HideWindowEvent.HIDE_UNIT_WINDOW, self.__handleUnitWindowHide, scope=EVENT_BUS_SCOPE.LOBBY)



    @process
    def __requestToCreate(self):
        yield self.prbDispatcher.create(unit_ctx.CreateUnitCtx(self.getPrbType(), waitingID='prebattle/create'))



    @process
    def __requestToJoin(self, ctx):
        yield self.prbDispatcher.join(ctx)



    @process
    def __requestToReloginAndJoin(self, peripheryID, ctx):
        result = yield DialogsInterface.showDialog(UnitConfirmDialogMeta(PREBATTLE_TYPE.UNIT, 'changePeriphery', messageCtx={'host': g_lobbyContext.getPeripheryName(peripheryID)}))
        if result:
            self.prbPeripheriesHandler.join(peripheryID, ctx)



    def __handleUnitWindowHide(self, _):
        self.destroy()



    def __initIntroUnitView(self):
        navKey = self.getNavigationKey()
        NavigationStack.exclude(navKey, CYBER_SPORT_ALIASES.UNIT_VIEW_UI)
        if NavigationStack.hasHistory(navKey):
            (flashAlias, _, itemID,) = NavigationStack.current(navKey)
            self._requestViewLoad(flashAlias, itemID)
        else:
            self._requestViewLoad(CYBER_SPORT_ALIASES.INTRO_VIEW_UI, None)



    def __initState(self, timeLeft = 0, acceptDelta = 0):
        model = None
        if self.currentState == CYBER_SPORT_ALIASES.AUTO_SEARCH_COMMANDS_STATE:
            message = i18n.makeString(CYBERSPORT.WINDOW_AUTOSEARCH_SEARCHCOMMAND_CXTDNMMESSAGE, settings.AUTO_SEARCH_UNITS_ARG_TIME)
            model = self.__createAutoUpdateModel(self.currentState, timeLeft, message, [])
        elif self.currentState == CYBER_SPORT_ALIASES.AUTO_SEARCH_CONFIRMATION_STATE:
            model = self.__createAutoUpdateModel(self.currentState, acceptDelta, '', [])
        elif self.currentState == CYBER_SPORT_ALIASES.AUTO_SEARCH_WAITING_PLAYERS_STATE:
            model = self.__createAutoUpdateModel(self.currentState, timeLeft, '', self.unitFunctional.getReadyStates())
        elif self.currentState == CYBER_SPORT_ALIASES.AUTO_SEARCH_ENEMY_STATE:
            model = self.__createAutoUpdateModel(self.currentState, timeLeft, '', [])
        elif self.currentState == CYBER_SPORT_ALIASES.AUTO_SEARCH_ERROR_STATE:
            model = self.__createAutoUpdateModel(self.currentState, 0, '', [])
        if model is not None:
            self.as_changeAutoSearchStateS(model)



    def __clearState(self):
        self.currentState = ''
        self.as_enableWndCloseBtnS(True)
        self.as_hideAutoSearchS()



    def __createAutoUpdateModel(self, state, countDownSeconds, ctxMessage, playersReadiness):
        permissions = self.unitFunctional.getPermissions(unitIdx=self.unitFunctional.getUnitIdx())
        model = {'state': state,
         'countDownSeconds': countDownSeconds,
         'contextMessage': ctxMessage,
         'playersReadiness': playersReadiness,
         'canInvokeAutoSearch': permissions.canInvokeAutoSearch(),
         'canInvokeBattleQueue': permissions.canStopBattleQueue()}
        return model



    def __addPlayerNotification(self, key, pInfo):
        chat = self.chat
        if chat and not pInfo.isCurrentPlayer():
            chat.as_addMessageS(messages.getUnitPlayerNotification(key, pInfo))




+++ okay decompyling cybersportmainwindow.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:14:46 CET
