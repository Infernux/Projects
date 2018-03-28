# 2015.01.14 22:13:50 CET
from constants import PREBATTLE_TYPE, QUEUE_TYPE
from debug_utils import LOG_ERROR, LOG_DEBUG
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework import ViewTypes, g_entitiesFactories as guiFactory, AppRef
from gui.Scaleform.framework.managers.containers import POP_UP_CRITERIA
from gui.Scaleform.genConsts.PREBATTLE_ALIASES import PREBATTLE_ALIASES
from gui.Scaleform.genConsts.CYBER_SPORT_ALIASES import CYBER_SPORT_ALIASES
from gui.Scaleform.locale.CHAT import CHAT
from gui.Scaleform.locale.MENU import MENU
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.shared import g_eventBus, events, EVENT_BUS_SCOPE
from gui.shared.events import ChannelManagementEvent, PreBattleChannelEvent
from messenger.ext import channel_num_gen
from messenger.ext.channel_num_gen import SPECIAL_CLIENT_WINDOWS
from messenger.m_constants import LAZY_CHANNEL
from collections import namedtuple
import weakref
TOOLTIP_PRB_DATA = namedtuple('TOOLTIP_PRB_DATA', ('tooltipId', 'label'))
_CarouselItemCtx = namedtuple('_CarouselItemCtx', ['label',
 'canClose',
 'isNotified',
 'icon',
 'order',
 'criteria',
 'viewType',
 'openHandler',
 'readyData',
 'tooltipData'])
_defCarouselItemCtx = _CarouselItemCtx(label=None, canClose=False, isNotified=False, icon=None, order=channel_num_gen.getOrder4Prebattle(), criteria=None, viewType=ViewTypes.WINDOW, openHandler=None, readyData=None, tooltipData=None)
_LOCKED_SCREENS = (PREBATTLE_ALIASES.TRAINING_ROOM_VIEW_PY, PREBATTLE_ALIASES.TRAINING_LIST_VIEW_PY)

class EventDispatcher(AppRef):

    def __init__(self):
        super(EventDispatcher, self).__init__()
        self.__loadingEvent = None



    def init(self, dispatcher):
        self._setPrebattleDispatcher(dispatcher)
        self.app.containerManager.onViewAddedToContainer += self.__onViewAddedToContainer



    def fini(self):
        self._setPrebattleDispatcher(None)
        self.__loadingEvent = None
        if self.app and self.app.containerManager:
            self.app.containerManager.onViewAddedToContainer -= self.__onViewAddedToContainer



    def isTrainingLoaded(self):
        return self.__getLoadedEvent() in _LOCKED_SCREENS or self.__loadingEvent in _LOCKED_SCREENS



    def updateUI(self):
        self._fireEvent(events.FightButtonEvent(events.FightButtonEvent.FIGHT_BUTTON_UPDATE))



    def loadHangar(self):
        self._fireLoadEvent(VIEW_ALIAS.LOBBY_HANGAR)



    def loadBattleQueue(self):
        self._fireLoadEvent(VIEW_ALIAS.BATTLE_QUEUE)



    def loadSquad(self, isInvitesOpen = False, isReady = False):
        self.addSquadToCarousel(isReady)
        self.showSquadWindow(isInvitesOpen=isInvitesOpen)



    def loadEventSquad(self, isInvitesOpen = False, isReady = False):
        self.addEventSquadToCarousel(isReady)
        self.showEventSquadWindow(isInvitesOpen=isInvitesOpen)



    def loadTrainingList(self):
        self.removeTrainingFromCarousel(False)
        self.addTrainingToCarousel()
        self._showTrainingList()



    def loadTrainingRoom(self):
        self.removeTrainingFromCarousel()
        self.addTrainingToCarousel(False)
        self._showTrainingRoom()



    def loadCompany(self):
        self.addCompanyToCarousel()
        self.showCompanyWindow()



    def loadBattleSessionWindow(self, prbType):
        self.addSpecBattleToCarousel(prbType)
        self.showBattleSessionWindow()



    def loadBattleSessionList(self):
        self._fireShowEvent(PREBATTLE_ALIASES.BATTLE_SESSION_LIST_WINDOW_PY)



    def loadUnit(self, prbType, modeFlags = 0):
        self.addUnitToCarousel(prbType)
        self.showUnitWindow(prbType, modeFlags)



    def loadHistoryBattles(self):
        self.addHistoryBattlesToCarousel()
        self.showHistoryBattlesWindow()



    def unloadHistoryBattles(self):
        self._closeHistoryBattlesWindow()
        self.removeHistoryBattlesFromCarousel()



    def unloadBattleSessionWindow(self, prbType):
        self._closeBattleSessionWindow()
        self.removeSpecBattleFromCarousel(prbType)
        self.requestToDestroyPrbChannel(prbType)



    def unloadTrainingRoom(self):
        self.removeTrainingFromCarousel()
        self.requestToDestroyPrbChannel(PREBATTLE_TYPE.TRAINING)



    def unloadUnit(self, prbType):
        self._closeUnitWindow()
        self.removeUnitFromCarousel(prbType)
        self.requestToDestroyPrbChannel(PREBATTLE_TYPE.UNIT)



    def unloadSquad(self):
        self._closeSquadWindow()
        self.removeSquadFromCarousel()
        self.requestToDestroyPrbChannel(PREBATTLE_TYPE.SQUAD)



    def unloadEventSquad(self):
        self._closeEventSquadWindow()
        self.removeEventSquadFromCarousel()
        self.requestToDestroyPrbChannel(PREBATTLE_TYPE.EVENT_SQUAD)



    def unloadCompany(self):
        self._fireHideEvent(events.HideWindowEvent.HIDE_COMPANY_WINDOW)
        self.removeCompanyFromCarousel()
        self.requestToDestroyPrbChannel(PREBATTLE_TYPE.COMPANY)



    def removeTrainingFromCarousel(self, isList = True):
        clientType = SPECIAL_CLIENT_WINDOWS.TRAINING_LIST if isList else SPECIAL_CLIENT_WINDOWS.TRAINING_ROOM
        clientID = channel_num_gen.getClientID4SpecialWindow(clientType)
        if not clientID:
            LOG_ERROR('Client ID not found', 'removeTrainingToCarousel')
            return 
        self._handleRemoveRequest(clientID)



    def addTrainingToCarousel(self, isList = True):
        if isList:
            clientType = SPECIAL_CLIENT_WINDOWS.TRAINING_LIST
            alias = PREBATTLE_ALIASES.TRAINING_LIST_VIEW_PY
            handler = self._showTrainingList
        else:
            clientType = SPECIAL_CLIENT_WINDOWS.TRAINING_ROOM
            alias = PREBATTLE_ALIASES.TRAINING_ROOM_VIEW_PY
            handler = self._returnToTrainingRoom
        clientID = channel_num_gen.getClientID4SpecialWindow(clientType)
        if not clientID:
            LOG_ERROR('Client ID not found', 'addTrainingToCarousel')
            return 
        currCarouselItemCtx = _defCarouselItemCtx._replace(label=MENU.HEADERBUTTONS_BATTLE_TYPES_TRAINING, criteria={POP_UP_CRITERIA.VIEW_ALIAS: alias}, viewType=ViewTypes.LOBBY_SUB, openHandler=handler)
        self._handleAddPreBattleRequest(clientID, currCarouselItemCtx._asdict())



    def addSquadToCarousel(self, isReady = False):
        clientID = channel_num_gen.getClientID4Prebattle(PREBATTLE_TYPE.SQUAD)
        if not clientID:
            LOG_ERROR('Client ID not found', 'addSquadToCarousel')
            return 
        currCarouselItemCtx = _defCarouselItemCtx._replace(label=CHAT.CHANNELS_SQUAD, icon=RES_ICONS.MAPS_ICONS_MESSENGER_SQUAD_ICON, criteria={POP_UP_CRITERIA.VIEW_ALIAS: PREBATTLE_ALIASES.SQUAD_WINDOW_PY}, openHandler=self.showSquadWindow, readyData=self.__getReadyPrbData(isReady), tooltipData=self.__getTooltipPrbData(CHAT.CHANNELS_SQUADREADY_TOOLTIP if isReady else CHAT.CHANNELS_SQUADNOTREADY_TOOLTIP))
        self._handleAddPreBattleRequest(clientID, currCarouselItemCtx._asdict())



    def removeSquadFromCarousel(self):
        clientID = channel_num_gen.getClientID4Prebattle(PREBATTLE_TYPE.SQUAD)
        if not clientID:
            LOG_ERROR('Client ID not found', '_removeSquadFromCarousel')
            return 
        self._handleRemoveRequest(clientID)



    def addEventSquadToCarousel(self, isReady = False):
        clientID = channel_num_gen.getClientID4Prebattle(PREBATTLE_TYPE.EVENT_SQUAD)
        if not clientID:
            LOG_ERROR('Client ID not found', 'addSquadToCarousel')
            return 
        currCarouselItemCtx = _defCarouselItemCtx._replace(label=CHAT.CHANNELS_EVENTSQUAD, icon=RES_ICONS.MAPS_ICONS_MESSENGER_SQUAD_ICON, criteria={POP_UP_CRITERIA.VIEW_ALIAS: PREBATTLE_ALIASES.SQUAD_WINDOW_NY_PY}, openHandler=self.showEventSquadWindow, readyData=self.__getReadyPrbData(isReady), tooltipData=self.__getTooltipPrbData(CHAT.CHANNELS_EVENTSQUADREADY_TOOLTIP if isReady else CHAT.CHANNELS_EVENTSQUADNOTREADY_TOOLTIP))
        self._handleAddPreBattleRequest(clientID, currCarouselItemCtx._asdict())



    def removeEventSquadFromCarousel(self):
        clientID = channel_num_gen.getClientID4Prebattle(PREBATTLE_TYPE.EVENT_SQUAD)
        if not clientID:
            LOG_ERROR('Client ID not found', '_removeSquadFromCarousel')
            return 
        self._handleRemoveRequest(clientID)



    def addCompanyToCarousel(self):
        clientID = self.__getClientIDForCompany()
        if not clientID:
            LOG_ERROR('Client ID not found', 'addCompanyToCarousel')
            return 
        currCarouselItemCtx = _defCarouselItemCtx._replace(label=CHAT.CHANNELS_TEAM, criteria={POP_UP_CRITERIA.VIEW_ALIAS: PREBATTLE_ALIASES.COMPANY_WINDOW_PY}, openHandler=self.showCompanyWindow)
        self._handleAddPreBattleRequest(clientID, currCarouselItemCtx._asdict())



    def removeCompanyFromCarousel(self):
        clientID = channel_num_gen.getClientID4Prebattle(PREBATTLE_TYPE.COMPANY)
        if not clientID:
            LOG_ERROR('Client ID not found', 'removeCompanyFromCarousel')
            return 
        self._handleRemoveRequest(clientID)



    def addSpecBattleToCarousel(self, prbType):
        clientID = channel_num_gen.getClientID4Prebattle(prbType)
        if not clientID:
            LOG_ERROR('Client ID not found', 'addSpecBattleToCarousel')
            return 
        if prbType is PREBATTLE_TYPE.CLAN:
            label = CHAT.CHANNELS_CLAN
        elif prbType is PREBATTLE_TYPE.TOURNAMENT:
            label = CHAT.CHANNELS_TOURNAMENT
        else:
            LOG_ERROR('Prebattle type is not valid', prbType)
            return 
        currCarouselItemCtx = _defCarouselItemCtx._replace(label=label, criteria={POP_UP_CRITERIA.VIEW_ALIAS: PREBATTLE_ALIASES.BATTLE_SESSION_ROOM_WINDOW_PY}, openHandler=self.showBattleSessionWindow)
        self._handleAddPreBattleRequest(clientID, currCarouselItemCtx._asdict())



    def addSpecBattlesToCarousel(self):
        clientID = channel_num_gen.getClientID4LazyChannel(LAZY_CHANNEL.SPECIAL_BATTLES)
        if not clientID:
            LOG_ERROR('Client ID not found', 'addSpecBattlesToCarousel')
            return 
        currCarouselItemCtx = _defCarouselItemCtx._replace(label=LAZY_CHANNEL.SPECIAL_BATTLES, order=channel_num_gen.getOrder4LazyChannel(LAZY_CHANNEL.SPECIAL_BATTLES), isNotified=True, criteria={POP_UP_CRITERIA.VIEW_ALIAS: PREBATTLE_ALIASES.BATTLE_SESSION_LIST_WINDOW_PY}, openHandler=self.loadBattleSessionList)
        self._fireEvent(ChannelManagementEvent(clientID, PreBattleChannelEvent.REQUEST_TO_ADD, currCarouselItemCtx._asdict()))



    def addUnitToCarousel(self, prbType):
        clientID = channel_num_gen.getClientID4Prebattle(prbType)
        if not clientID:
            LOG_ERROR('Client ID not found', 'addUnitToCarousel')
            return 
        if prbType in (PREBATTLE_TYPE.SORTIE, PREBATTLE_TYPE.FORT_BATTLE):
            from gui.Scaleform.locale.FORTIFICATIONS import FORTIFICATIONS
            from gui.Scaleform.genConsts.FORTIFICATION_ALIASES import FORTIFICATION_ALIASES
            label = FORTIFICATIONS.SORTIE_INTROVIEW_TITLE
            criteria = {POP_UP_CRITERIA.VIEW_ALIAS: FORTIFICATION_ALIASES.FORT_BATTLE_ROOM_WINDOW_ALIAS}
        else:
            from gui.Scaleform.locale.CYBERSPORT import CYBERSPORT
            label = CYBERSPORT.WINDOW_TITLE
            criteria = {POP_UP_CRITERIA.VIEW_ALIAS: CYBER_SPORT_ALIASES.CYBER_SPORT_WINDOW_PY}
        currCarouselItemCtx = _defCarouselItemCtx._replace(label=label, criteria=criteria, viewType=ViewTypes.WINDOW, openHandler=lambda : self.showUnitWindow(prbType))
        self._handleAddPreBattleRequest(clientID, currCarouselItemCtx._asdict())



    def addHistoryBattlesToCarousel(self):
        from gui.Scaleform.locale.HISTORICAL_BATTLES import HISTORICAL_BATTLES
        clientID = channel_num_gen.getClientID4PreQueue(QUEUE_TYPE.HISTORICAL)
        if not clientID:
            LOG_ERROR('Client ID not found', 'addHistoryBattlesToCarousel')
            return 
        currCarouselItemCtx = _defCarouselItemCtx._replace(label=HISTORICAL_BATTLES.WINDOW_MAIN_TITLE, criteria={POP_UP_CRITERIA.VIEW_ALIAS: PREBATTLE_ALIASES.HISTORICAL_BATTLES_LIST_WINDOW_PY}, openHandler=self.showHistoryBattlesWindow)
        self._handleAddPreBattleRequest(clientID, currCarouselItemCtx._asdict())



    def removeSpecBattleFromCarousel(self, prbType):
        clientID = channel_num_gen.getClientID4Prebattle(prbType)
        if not clientID:
            LOG_ERROR('Client ID not found', '_removeSpecBattleFromCarousel')
            return 
        self._handleRemoveRequest(clientID)



    def showHistoryBattlesWindow(self):
        self._fireShowEvent(PREBATTLE_ALIASES.HISTORICAL_BATTLES_LIST_WINDOW_PY)



    def removeSpecBattlesFromCarousel(self):
        clientID = channel_num_gen.getClientID4LazyChannel(LAZY_CHANNEL.SPECIAL_BATTLES)
        if not clientID:
            LOG_ERROR('Client ID not found', 'removeSpecBattlesFromCarousel')
            return 
        self._fireEvent(ChannelManagementEvent(clientID, PreBattleChannelEvent.REQUEST_TO_REMOVE))



    def showUnitWindow(self, prbType, modeFlags = 0):
        if prbType in (PREBATTLE_TYPE.SORTIE, PREBATTLE_TYPE.FORT_BATTLE):
            from gui.Scaleform.genConsts.FORTIFICATION_ALIASES import FORTIFICATION_ALIASES
            self._fireEvent(events.LoadViewEvent(FORTIFICATION_ALIASES.FORT_BATTLE_ROOM_WINDOW_ALIAS, ctx={'modeFlags': modeFlags}))
        else:
            self._fireShowEvent(CYBER_SPORT_ALIASES.CYBER_SPORT_WINDOW_PY)



    def removeUnitFromCarousel(self, prbType):
        clientID = channel_num_gen.getClientID4Prebattle(prbType)
        if not clientID:
            LOG_ERROR('Client ID not found', 'removeUnitFromCarousel', prbType)
            return 
        self._handleRemoveRequest(clientID)



    def setUnitProgressInCarousel(self, prbType, isInProgress):
        clientID = channel_num_gen.getClientID4Prebattle(prbType)
        if not clientID:
            LOG_ERROR('Client ID not found', 'setUnitProgressInCarousel', prbType)
            return 
        self._fireEvent(events.ChannelManagementEvent(clientID, events.ChannelManagementEvent.REQUEST_TO_CHANGE, {'key': 'isInProgress',
         'value': isInProgress,
         'isShowByReq': isInProgress,
         'showIfClosed': True}))



    def showUnitProgressInCarousel(self, prbType):
        self._showUnitProgress(prbType, True)



    def hideUnitProgressInCarousel(self, prbType):
        self._showUnitProgress(prbType, False)



    def removeHistoryBattlesFromCarousel(self):
        clientID = channel_num_gen.getClientID4PreQueue(QUEUE_TYPE.HISTORICAL)
        if not clientID:
            LOG_ERROR('Client ID not found', 'removeHistoryBattlesFromCarousel')
            return 
        self._handleRemoveRequest(clientID)



    def requestToDestroyPrbChannel(self, prbType):
        self._fireEvent(events.MessengerEvent(events.MessengerEvent.PRB_CHANNEL_CTRL_REQUEST_DESTROY, {'prbType': prbType}))



    def fireAutoInviteReceived(self, invite):
        self._fireEvent(events.AutoInviteEvent(invite, events.AutoInviteEvent.INVITE_RECEIVED))



    def showParentControlNotification(self):
        from gui import game_control, DialogsInterface
        if game_control.g_instance.gameSession.isPlayTimeBlock:
            key = 'koreaPlayTimeNotification'
        else:
            key = 'koreaParentNotification'
        DialogsInterface.showI18nInfoDialog(key, lambda *args: None)



    def showSquadWindow(self, isInvitesOpen = False):
        self._fireShowEvent(PREBATTLE_ALIASES.SQUAD_WINDOW_PY, {'isInvitesOpen': isInvitesOpen})



    def showEventSquadWindow(self, isInvitesOpen = False):
        self._fireShowEvent(PREBATTLE_ALIASES.SQUAD_WINDOW_NY_PY, {'isInvitesOpen': isInvitesOpen})



    def showCompanyWindow(self):
        self._fireShowEvent(PREBATTLE_ALIASES.COMPANY_WINDOW_PY, self.__getCompanyWindowContext())



    def showBattleSessionWindow(self):
        self._fireShowEvent(PREBATTLE_ALIASES.BATTLE_SESSION_ROOM_WINDOW_PY)



    def setSquadTeamReadyInCarousel(self, prbType, isTeamReady):
        clientID = channel_num_gen.getClientID4Prebattle(prbType)
        if not clientID:
            LOG_ERROR('Client ID not found', 'setSquadTeamReadyInCarousel', prbType)
            return 
        readyData = self.__getReadyPrbData(isTeamReady)
        g_eventBus.handleEvent(events.ChannelManagementEvent(clientID, events.ChannelManagementEvent.REQUEST_TO_CHANGE, {'key': 'readyData',
         'value': readyData,
         'isShowByReq': False,
         'showIfClosed': True}), scope=EVENT_BUS_SCOPE.LOBBY)
        g_eventBus.handleEvent(events.ChannelManagementEvent(clientID, events.ChannelManagementEvent.REQUEST_TO_CHANGE, {'key': 'tooltipData',
         'value': self.__getTooltipPrbData(CHAT.CHANNELS_SQUADREADY_TOOLTIP if isTeamReady else CHAT.CHANNELS_SQUADNOTREADY_TOOLTIP),
         'isShowByReq': False,
         'showIfClosed': True}), scope=EVENT_BUS_SCOPE.LOBBY)



    def setEventSquadTeamReadyInCarousel(self, prbType, isTeamReady):
        clientID = channel_num_gen.getClientID4Prebattle(prbType)
        if not clientID:
            LOG_ERROR('Client ID not found', 'setEventSquadTeamReadyInCarousel', prbType)
            return 
        readyData = self.__getReadyPrbData(isTeamReady)
        g_eventBus.handleEvent(events.ChannelManagementEvent(clientID, events.ChannelManagementEvent.REQUEST_TO_CHANGE, {'key': 'readyData',
         'value': readyData,
         'isShowByReq': False,
         'showIfClosed': True}), scope=EVENT_BUS_SCOPE.LOBBY)
        g_eventBus.handleEvent(events.ChannelManagementEvent(clientID, events.ChannelManagementEvent.REQUEST_TO_CHANGE, {'key': 'tooltipData',
         'value': self.__getTooltipPrbData(CHAT.CHANNELS_EVENTSQUADREADY_TOOLTIP if isTeamReady else CHAT.CHANNELS_EVENTSQUADNOTREADY_TOOLTIP),
         'isShowByReq': False,
         'showIfClosed': True}), scope=EVENT_BUS_SCOPE.LOBBY)



    def _showUnitProgress(self, prbType, show):
        clientID = channel_num_gen.getClientID4Prebattle(prbType)
        if not clientID:
            LOG_ERROR('Client ID not found', '_showUnitStatus', prbType)
            return 
        self._fireEvent(events.ChannelManagementEvent(clientID, events.ChannelManagementEvent.REQUEST_TO_SHOW, {'show': show}))



    def _showTrainingRoom(self):
        self._fireLoadEvent(PREBATTLE_ALIASES.TRAINING_ROOM_VIEW_PY)



    def _returnToTrainingRoom(self):
        if self.__prbDispatcher is not None:
            functional = self.__prbDispatcher.getPrbFunctional()
            if functional:
                functional.doAction()



    def _closeHistoryBattlesWindow(self):
        self._fireHideEvent(events.HideWindowEvent.HIDE_HISTORICAL_BATTLES_WINDOW)



    def _closeSquadWindow(self):
        self._fireHideEvent(events.HideWindowEvent.HIDE_SQUAD_WINDOW)



    def _closeEventSquadWindow(self):
        self._fireHideEvent(events.HideWindowEvent.HIDE_EVENT_SQUAD_WINDOW)



    def _fireEvent(self, event):
        g_eventBus.handleEvent(event, scope=EVENT_BUS_SCOPE.LOBBY)



    def _fireHideEvent(self, event):
        self._fireEvent(events.HideWindowEvent(event))



    def _fireShowEvent(self, eventName, arg = None):
        if arg is None:
            self._fireEvent(events.LoadViewEvent(eventName))
        else:
            self._fireEvent(events.LoadViewEvent(eventName, ctx=arg))



    def _fireLoadEvent(self, eventName):
        if self.__getLoadedEvent() == eventName:
            LOG_DEBUG('View already is loaded', eventName)
            return 
        if self.__loadingEvent:
            LOG_DEBUG('View is still loading. It is ignored', self.__loadingEvent, eventName)
        else:
            self.__loadingEvent = eventName
            self._fireEvent(events.LoadViewEvent(eventName))



    def _handleRemoveRequest(self, clientID):
        self._fireEvent(ChannelManagementEvent(clientID, PreBattleChannelEvent.REQUEST_TO_REMOVE_PRE_BATTLE_CHANNEL))



    def _handleAddPreBattleRequest(self, clientID, carouselItemCtx):
        self._fireEvent(ChannelManagementEvent(clientID, PreBattleChannelEvent.REQUEST_TO_ADD_PRE_BATTLE_CHANNEL, carouselItemCtx))



    def _closeBattleSessionWindow(self):
        self._fireHideEvent(events.HideWindowEvent.HIDE_BATTLE_SESSION_WINDOW)



    def _closeUnitWindow(self):
        self._fireHideEvent(events.HideWindowEvent.HIDE_UNIT_WINDOW)



    def _setPrebattleDispatcher(self, prbDispatcher):
        if prbDispatcher is not None:
            self.__prbDispatcher = weakref.proxy(prbDispatcher)
        else:
            self.__prbDispatcher = None



    def _showTrainingList(self):
        self._fireLoadEvent(PREBATTLE_ALIASES.TRAINING_LIST_VIEW_PY)



    def __getReadyPrbData(self, isReady):
        return {'isReady': isReady}



    def __getTooltipPrbData(self, tooltipId, label = ''):
        return TOOLTIP_PRB_DATA(tooltipId=tooltipId, label=label)._asdict()



    def __getCompanyWindowContext(self):
        return {'clientID': self.__getClientIDForCompany()}



    def __getClientIDForCompany(self):
        return channel_num_gen.getClientID4Prebattle(PREBATTLE_TYPE.COMPANY)



    def __onViewAddedToContainer(self, _, pyEntity):
        settings = pyEntity.settings
        if settings.event == self.__loadingEvent:
            self.__loadingEvent = None
        if settings.type == ViewTypes.LOBBY_SUB:
            self.updateUI()



    def __getLoadedEvent(self):
        if self.app and self.app.colorManager:
            container = self.app.containerManager.getContainer(ViewTypes.LOBBY_SUB)
            if container:
                view = container.getView()
                if view:
                    return view.settings.event



g_eventDispatcher = EventDispatcher()

+++ okay decompyling events_dispatcher.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:13:50 CET
