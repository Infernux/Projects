# 2015.01.14 22:10:02 CET
import BigWorld
from PlayerEvents import g_playerEvents
import account_helpers
from adisp import process
from constants import PREBATTLE_ACCOUNT_STATE, REQUEST_COOLDOWN
from debug_utils import LOG_ERROR, LOG_DEBUG, LOG_CURRENT_EXCEPTION
from gui import prb_control, SystemMessages, DialogsInterface
from gui.Scaleform.daapi.view.dialogs import rally_dialog_meta
from gui.prb_control import restrictions
from gui.prb_control.context import prb_ctx, pre_queue_ctx
from gui.prb_control.ctrl_events import g_prbCtrlEvents
from gui.prb_control.formatters import messages
from gui.prb_control.functional import interfaces
from gui.prb_control import isParentControlActivated
from gui.prb_control.items import prb_items, prb_seqs
from gui.prb_control.prb_cooldown import PrbCooldownManager
from gui.prb_control.restrictions.limits import DefaultLimits
from gui.prb_control.restrictions.permissions import DefaultPrbPermissions
from gui.prb_control.settings import *
from gui.shared.utils.ListenersCollection import ListenersCollection
from prebattle_shared import decodeRoster
from gui.prb_control.events_dispatcher import g_eventDispatcher

class PrbIntro(interfaces.IPrbEntry):

    def __init__(self, prbType):
        super(PrbIntro, self).__init__()
        self._prbType = prbType



    def makeDefCtx(self):
        return prb_ctx.JoinModeCtx(self._prbType)



    def create(self, ctx, callback = None):
        raise Exception, 'PrbIntro is not create entity'



    def join(self, ctx, callback = None):
        if not prb_control.hasModalEntity() or ctx.isForced():
            g_prbCtrlEvents.onPrebattleIntroModeJoined(ctx.getPrbType(), prb_control.hasModalEntity())
            if callback:
                callback(True)
        else:
            LOG_ERROR('First, player has to confirm exit from the current entity.')
            if callback:
                callback(False)



    def select(self, ctx, callback = None):
        self.join(ctx, callback=callback)




class PrbEntry(interfaces.IPrbEntry):

    def create(self, ctx, callback = None):
        LOG_ERROR('Routine "create" must be implemented in subclass')



    def join(self, ctx, callback = None):
        if prb_control.getClientPrebattle() is None or ctx.isForced():
            ctx.startProcessing(callback=callback)
            BigWorld.player().prb_join(ctx.getID())
        else:
            LOG_ERROR('First, player has to confirm exit from the current prebattle', prb_control.getPrebattleType())
            if callback:
                callback(False)



    def select(self, ctx, callback = None):
        LOG_ERROR('Routine "select" must be implemented in subclass')




class _PrbFunctional(ListenersCollection, interfaces.IPrbFunctional):

    def __init__(self, listenerClass, requestHandlers = None):
        super(_PrbFunctional, self).__init__()
        self._setListenerClass(listenerClass)
        self._requestHandlers = requestHandlers or {}
        self._exit = FUNCTIONAL_EXIT.NO_FUNC
        self._deferredReset = False



    def getExit(self):
        return self._exit



    def setExit(self, exit):
        if exit in FUNCTIONAL_EXIT.PREBATTLE_RANGE:
            self._exit = exit



    def fini(self, clientPrb = None, woEvents = False):
        self._setListenerClass(None)
        self._requestHandlers.clear()
        self._deferredReset = False



    def request(self, ctx, callback = None):
        requestType = ctx.getRequestType()
        handler = None
        if requestType in self._requestHandlers:
            handler = self._requestHandlers[requestType]
        if handler:
            LOG_DEBUG('Prebattle request', ctx)
            handler(ctx, callback=callback)
        else:
            LOG_ERROR('Handler not found', ctx)
            if callback:
                callback(False)



    @process
    def doLeaveAction(self, dispatcher, ctx = None):
        meta = self.getConfirmDialogMeta()
        if meta is not None:
            isConfirmed = yield DialogsInterface.showDialog(meta)
        else:
            isConfirmed = yield lambda callback: callback(True)
        if isConfirmed:
            if ctx is None:
                ctx = prb_ctx.LeavePrbCtx(waitingID='prebattle/leave')
            if dispatcher._setRequestCtx(ctx):
                self.leave(ctx)




class IntroPrbFunctional(_PrbFunctional):

    def __init__(self, prbType, listReq, requestHandlers = None):
        super(IntroPrbFunctional, self).__init__(interfaces.IIntoPrbListener, requestHandlers)
        self._prbType = prbType
        self._listReq = listReq
        self._hasEntity = False



    def init(self, clientPrb = None, ctx = None):
        self._hasEntity = True
        for listener in self._listeners:
            listener.onIntroPrbFunctionalInited()

        if self._listReq:
            self._listReq.start(self._onPrbListReceived)
        return FUNCTIONAL_INIT_RESULT.INITED



    def fini(self, clientPrb = None, woEvents = False):
        self._hasEntity = False
        if self._listReq:
            self._listReq.stop()
            self._listReq = None
        super(IntroPrbFunctional, self).fini(clientPrb, woEvents)
        try:
            for listener in self._listeners:
                listener.onIntroPrbFunctionalFinished()

        except:
            LOG_CURRENT_EXCEPTION()



    def getPrbType(self):
        return self._prbType



    def getPrbTypeName(self):
        return prb_control.getPrebattleTypeName(self.getPrbType())



    def hasEntity(self):
        return self._hasEntity



    def getConfirmDialogMeta(self, funcExit = FUNCTIONAL_EXIT.NO_FUNC):
        return rally_dialog_meta.createPrbIntroLeaveMeta(funcExit, self._prbType)



    def leave(self, ctx, callback = None):
        self._exit = ctx.getFuncExit()
        g_prbCtrlEvents.onPrebattleIntroModeLeft()
        if callback:
            callback(True)



    def _onPrbListReceived(self, prebattles):
        self._invokeListeners('onPrbListReceived', prebattles)




class PrbInitFunctional(interfaces.IPrbFunctional):

    def __init__(self):
        self.__prbInitSteps = 0



    def init(self, clientPrb = None, ctx = None):
        if clientPrb is None:
            clientPrb = prb_control.getClientPrebattle()
        if clientPrb is not None:
            clientPrb.onSettingsReceived += self.prb_onSettingsReceived
            clientPrb.onRosterReceived += self.prb_onRosterReceived
            if prb_control.isPrebattleSettingsReceived(prebattle=clientPrb):
                self.prb_onSettingsReceived()
            if len(prb_control.getPrebattleRosters(prebattle=clientPrb)):
                self.prb_onRosterReceived()
        return FUNCTIONAL_INIT_RESULT.INITED



    def fini(self, clientPrb = None, woEvents = False):
        self.__dispatcher = None
        if clientPrb is None:
            clientPrb = prb_control.getClientPrebattle()
        if clientPrb is not None:
            clientPrb.onSettingsReceived -= self.prb_onSettingsReceived
            clientPrb.onRosterReceived -= self.prb_onRosterReceived



    def prb_onSettingsReceived(self):
        LOG_DEBUG('prb_onSettingsReceived')
        self.__prbInitSteps |= PREBATTLE_INIT_STEP.SETTING_RECEIVED
        self.__isPrebattleInited()



    def prb_onRosterReceived(self):
        LOG_DEBUG('prb_onRosterReceived')
        self.__prbInitSteps |= PREBATTLE_INIT_STEP.ROSTERS_RECEIVED
        self.__isPrebattleInited()



    def __isPrebattleInited(self):
        result = False
        if self.__prbInitSteps is PREBATTLE_INIT_STEP.INITED:
            g_prbCtrlEvents.onPrebattleInited()
            result = True
            self.__prbInitSteps = 0
        return result




class PrbRosterRequester(interfaces.IPrbListRequester):

    def __init__(self):
        self.__callback = None
        self.__prebattleID = 0
        self.__ctx = None



    def start(self, callback):
        if callback is not None and callable(callback):
            self.__callback = callback
        else:
            LOG_ERROR('Callback is None or is not callable')
            return 
        g_playerEvents.onPrebattleRosterReceived += self.__pe_onPrebattleRosterReceived



    def stop(self):
        g_playerEvents.onPrebattleRosterReceived -= self.__pe_onPrebattleRosterReceived
        self.__callback = None
        if self.__ctx:
            self.__ctx.stopProcessing(False)
            self.__ctx = None



    def request(self, ctx = None):
        self.__ctx = ctx
        BigWorld.player().requestPrebattleRoster(self.__ctx.getPrbID())



    def __pe_onPrebattleRosterReceived(self, prebattleID, roster):
        self.__callback(prebattleID, prb_seqs.RosterIterator(roster))
        if self.__ctx:
            self.__ctx.stopProcessing(True)
            self.__ctx = None




class PrbDispatcher(_PrbFunctional):

    def __init__(self, settings, permClass = None, limits = None, requestHandlers = None):
        super(PrbDispatcher, self).__init__(interfaces.IPrbListener, requestHandlers)
        self._settings = settings
        self._permClass = permClass or DefaultPrbPermissions
        self._limits = limits or DefaultLimits(self)
        self._hasEntity = False
        self._cooldown = PrbCooldownManager()



    def init(self, clientPrb = None, ctx = None):
        self._hasEntity = True
        if clientPrb is None:
            clientPrb = prb_control.getClientPrebattle()
        if clientPrb is not None:
            clientPrb.onSettingUpdated += self.prb_onSettingUpdated
            clientPrb.onRosterReceived += self.prb_onRosterReceived
            clientPrb.onTeamStatesReceived += self.prb_onTeamStatesReceived
            clientPrb.onPlayerStateChanged += self.prb_onPlayerStateChanged
            clientPrb.onPlayerRosterChanged += self.prb_onPlayerRosterChanged
            clientPrb.onPlayerAdded += self.prb_onPlayerAdded
            clientPrb.onPlayerRemoved += self.prb_onPlayerRemoved
            clientPrb.onKickedFromQueue += self.prb_onKickedFromQueue
            for listener in self._listeners:
                listener.onPrbFunctionalInited()

        else:
            LOG_ERROR('ClientPrebattle is not defined')
        return FUNCTIONAL_INIT_RESULT.INITED



    def fini(self, clientPrb = None, woEvents = False):
        self._hasEntity = False
        self._settings = None
        super(PrbDispatcher, self).fini(clientPrb, woEvents)
        if self._limits is not None:
            self._limits.clear()
            self._limits = None
        if not woEvents:
            try:
                for listener in self._listeners:
                    listener.onPrbFunctionalFinished()

            except:
                LOG_CURRENT_EXCEPTION()
        if clientPrb is None:
            clientPrb = prb_control.getClientPrebattle()
        if clientPrb is not None:
            clientPrb.onSettingUpdated -= self.prb_onSettingUpdated
            clientPrb.onTeamStatesReceived -= self.prb_onTeamStatesReceived
            clientPrb.onPlayerStateChanged -= self.prb_onPlayerStateChanged
            clientPrb.onPlayerRosterChanged -= self.prb_onPlayerRosterChanged
            clientPrb.onPlayerAdded -= self.prb_onPlayerAdded
            clientPrb.onPlayerRemoved -= self.prb_onPlayerRemoved
            clientPrb.onKickedFromQueue -= self.prb_onKickedFromQueue



    def isPlayerJoined(self, ctx):
        return ctx.getCtrlType() is CTRL_ENTITY_TYPE.PREBATTLE and ctx.getID() == self.getID()



    def getID(self):
        return prb_control.getPrebattleID()



    def getPrbType(self):
        if self._settings:
            return self._settings['type']
        return 0



    def getPrbTypeName(self):
        return prb_control.getPrebattleTypeName(self.getPrbType())



    def getSettings(self):
        return self._settings



    def getLimits(self):
        return self._limits



    def getPermissions(self, pID = None):
        return restrictions.createPermissions(self, pID=pID)



    def isCreator(self, pDatabaseID = None):
        return self._permClass.isCreator(self.getRoles(pDatabaseID=pDatabaseID))



    def hasEntity(self):
        return self._hasEntity



    def hasLockedState(self):
        (team, assigned,) = decodeRoster(self.getRosterKey())
        return self.getTeamState().isInQueue() and self.getPlayerInfo().isReady() and assigned



    def getConfirmDialogMeta(self, funcExit = FUNCTIONAL_EXIT.NO_FUNC):
        if not self._settings:
            return None
        prbType = self.getPrbType()
        if self.hasLockedState():
            meta = rally_dialog_meta.RallyLeaveDisabledDialogMeta(CTRL_ENTITY_TYPE.PREBATTLE, prbType)
        else:
            meta = rally_dialog_meta.createPrbLeaveMeta(funcExit, prbType)
        return meta



    def prb_onSettingUpdated(self, settingName):
        settingValue = self._settings[settingName]
        LOG_DEBUG('prb_onSettingUpdated', settingName, settingValue)
        for listener in self._listeners:
            listener.onSettingUpdated(self, settingName, settingValue)




    def prb_onTeamStatesReceived(self):
        team1State = self.getTeamState(team=1)
        team2State = self.getTeamState(team=2)
        LOG_DEBUG('prb_onTeamStatesReceived', team1State, team2State)
        if self._deferredReset and not self.getTeamState().isInQueue():
            self._deferredReset = False
            self.reset()
        for listener in self._listeners:
            listener.onTeamStatesReceived(self, team1State, team2State)




    def prb_onPlayerStateChanged(self, pID, roster):
        accountInfo = self.getPlayerInfo(pID=pID)
        LOG_DEBUG('prb_onPlayerStateChanged', accountInfo)
        for listener in self._listeners:
            listener.onPlayerStateChanged(self, roster, accountInfo)




    def prb_onRosterReceived(self):
        LOG_DEBUG('prb_onRosterReceived')
        rosters = self.getRosters()
        for listener in self._listeners:
            listener.onRostersChanged(self, rosters, True)

        team = self.getPlayerTeam()
        for listener in self._listeners:
            listener.onPlayerTeamNumberChanged(self, team)




    def prb_onPlayerRosterChanged(self, pID, prevRoster, roster, actorID):
        LOG_DEBUG('prb_onPlayerRosterChanged', pID, prevRoster, roster, actorID)
        rosters = self.getRosters(keys=[prevRoster, roster])
        actorInfo = self.getPlayerInfo(pID=actorID)
        playerInfo = self.getPlayerInfo(pID=pID)
        for listener in self._listeners:
            if actorInfo and playerInfo:
                listener.onPlayerRosterChanged(self, actorInfo, playerInfo)
            listener.onRostersChanged(self, rosters, False)

        if pID == account_helpers.getPlayerID():
            (prevTeam, _,) = decodeRoster(prevRoster)
            (currentTeam, _,) = decodeRoster(roster)
            if currentTeam is not prevTeam:
                for listener in self._listeners:
                    listener.onPlayerTeamNumberChanged(self, currentTeam)




    def prb_onPlayerAdded(self, pID, roster):
        LOG_DEBUG('prb_onPlayerAdded', pID, roster)
        rosters = self.getRosters(keys=[roster])
        playerInfo = self.getPlayerInfo(pID=pID, rosterKey=roster)
        for listener in self._listeners:
            listener.onPlayerAdded(self, playerInfo)
            listener.onRostersChanged(self, rosters, False)




    def prb_onPlayerRemoved(self, pID, roster, name):
        LOG_DEBUG('prb_onPlayerRemoved', pID, roster, name)
        rosters = self.getRosters(keys=[roster])
        playerInfo = prb_items.PlayerPrbInfo(pID, name=name)
        for listener in self._listeners:
            listener.onPlayerRemoved(self, playerInfo)
            listener.onRostersChanged(self, rosters, False)




    def prb_onKickedFromQueue(self, *args):
        LOG_DEBUG('prb_onKickedFromQueue', args)
        message = messages.getPrbKickedFromQueueMessage(self.getPrbTypeName())
        if len(message):
            SystemMessages.pushMessage(message, type=SystemMessages.SM_TYPE.Warning)




class PrbFunctional(PrbDispatcher):

    def getRosterKey(self, pID = None):
        rosters = prb_control.getPrebattleRosters()
        rosterRange = PREBATTLE_ROSTER.getRange(self.getPrbType())
        if pID is None:
            pID = account_helpers.getPlayerID()
        for roster in rosterRange:
            if roster in rosters and pID in rosters[roster].keys():
                return roster

        return PREBATTLE_ROSTER.UNKNOWN



    def getPlayerInfo(self, pID = None, rosterKey = None):
        rosters = prb_control.getPrebattleRosters()
        if pID is None:
            pID = account_helpers.getPlayerID()
        if rosterKey is not None:
            if rosterKey in rosters and pID in rosters[rosterKey].keys():
                return prb_items.PlayerPrbInfo(pID, functional=self, roster=rosterKey, **rosters[rosterKey][pID])
        else:
            rosterRange = PREBATTLE_ROSTER.getRange(self.getPrbType())
            for roster in rosterRange:
                if roster in rosters and pID in rosters[roster].keys():
                    return prb_items.PlayerPrbInfo(pID, functional=self, roster=roster, **rosters[roster][pID])

        return prb_items.PlayerPrbInfo(-1L)



    def getPlayerInfoByDbID(self, dbID):
        rosters = prb_control.getPrebattleRosters()
        rosterRange = PREBATTLE_ROSTER.getRange(self.getPrbType())
        for roster in rosterRange:
            if roster in rosters:
                for (pID, data,) in rosters[roster].iteritems():
                    if data['dbID'] == dbID:
                        return prb_items.PlayerPrbInfo(pID, functional=self, roster=roster, **rosters[roster][pID])


        return prb_items.PlayerPrbInfo(-1L)



    def getPlayerTeam(self, pID = None):
        team = 0
        roster = self.getRosterKey(pID=pID)
        if roster is not PREBATTLE_ROSTER.UNKNOWN:
            (team, _,) = decodeRoster(roster)
        return team



    def getTeamState(self, team = None):
        result = prb_items.TeamStateInfo(0)
        if team is None:
            roster = self.getRosterKey()
            if roster is not PREBATTLE_ROSTER.UNKNOWN:
                (team, _,) = decodeRoster(self.getRosterKey())
        teamStates = prb_control.getPrebattleTeamStates()
        if team is not None and team < len(teamStates):
            result = prb_items.TeamStateInfo(teamStates[team])
        return result



    def getRoles(self, pDatabaseID = None, clanDBID = None, team = None):
        result = 0
        if self._settings is None:
            return result
        if pDatabaseID is None:
            pDatabaseID = account_helpers.getPlayerDatabaseID()
        roles = self._settings['roles']
        if pDatabaseID in roles:
            result = roles[pDatabaseID]
        if not result and clanDBID:
            roles = self._settings['clanRoles']
            if clanDBID in roles:
                result = roles[clanDBID]
        if not result and team:
            roles = self._settings['teamRoles']
            if team in roles:
                result = roles[team]
        return result



    def getProps(self):
        return prb_items.PrbPropsInfo(**prb_control.getPrebattleProps())



    def leave(self, ctx, callback = None):
        ctx.startProcessing(callback)
        self._exit = ctx.getFuncExit()
        BigWorld.player().prb_leave(ctx.onResponseReceived)



    def reset(self):

        def setNotReady(code):
            if code >= 0:
                BigWorld.player().prb_notReady(PREBATTLE_ACCOUNT_STATE.NOT_READY, lambda *args: None)


        if self.isCreator() and self.getTeamState().isInQueue():
            BigWorld.player().prb_teamNotReady(self.getPlayerTeam(), setNotReady)
        elif self.getPlayerInfo().isReady():
            if self.getTeamState().isInQueue():
                self._deferredReset = True
            else:
                setNotReady(0)



    def assign(self, ctx, callback = None):
        (prevTeam, _,) = decodeRoster(self.getRosterKey(pID=ctx.getPlayerID()))
        (nextTeam, assigned,) = decodeRoster(ctx.getRoster())
        pPermissions = self.getPermissions()
        if prevTeam is nextTeam:
            if not pPermissions.canAssignToTeam(team=nextTeam):
                LOG_ERROR('Player can not change roster', nextTeam, assigned)
                if callback:
                    callback(False)
                return 
        elif not pPermissions.canChangePlayerTeam():
            LOG_ERROR('Player can not change team', prevTeam, nextTeam)
            if callback:
                callback(False)
            return 
        (result, restriction,) = self.getLimits().isMaxCountValid(nextTeam, assigned)
        if not result:
            LOG_ERROR('Max count limit', nextTeam, assigned)
            if callback:
                callback(False)
            return 
        ctx.startProcessing(callback)
        BigWorld.player().prb_assign(ctx.getPlayerID(), ctx.getRoster(), ctx.onResponseReceived)



    def setTeamState(self, ctx, callback = None):
        team = ctx.getTeam()
        if not self.getPermissions().canSetTeamState(team=team):
            LOG_ERROR('Player can not change state of team', team)
            if callback:
                callback(False)
            return 
        teamState = self.getTeamState()
        setReady = ctx.isReadyState()
        if setReady and teamState.isNotReady():
            if teamState.isLocked():
                LOG_ERROR('Team is locked')
                if callback:
                    callback(False)
            else:
                self._setTeamReady(ctx, callback=callback)
        elif not setReady and teamState.isInQueue():
            self._setTeamNotReady(ctx, callback=callback)
        elif callback:
            callback(True)



    def setPlayerState(self, ctx, callback = None):
        playerInfo = self.getPlayerInfo()
        if playerInfo is not None:
            playerIsReady = playerInfo.isReady()
            setReady = ctx.isReadyState()
            if setReady and not playerIsReady:
                self._setPlayerReady(ctx, callback=callback)
            elif not setReady and playerIsReady:
                self._setPlayerNotReady(ctx, callback=callback)
            elif callback:
                callback(True)
        else:
            LOG_ERROR('Account info not found in prebattle.rosters', ctx)
            if callback:
                callback(False)



    def kickPlayer(self, ctx, callback = None):
        pID = ctx.getPlayerID()
        rosterKey = self.getRosterKey(pID=pID)
        (team, assigned,) = decodeRoster(rosterKey)
        pPermissions = self.getPermissions()
        if not pPermissions.canKick(team=team):
            LOG_ERROR('Player can not kick from team', team, pPermissions)
            if callback:
                callback(False)
            return 
        if assigned:
            if self.getPlayerInfo(pID=pID, rosterKey=rosterKey).isReady() and self.getTeamState(team=team).isInQueue():
                LOG_ERROR('Player is ready, assigned and team is ready or locked', ctx)
                if callback:
                    callback(False)
                return 
        ctx.startProcessing(callback)
        BigWorld.player().prb_kick(ctx.getPlayerID(), ctx.onResponseReceived)



    def swapTeams(self, ctx, callback = None):
        if self._cooldown.validate(REQUEST_TYPE.SWAP_TEAMS):
            if callback:
                callback(False)
            return 
        pPermissions = self.getPermissions()
        if self.getPermissions().canChangePlayerTeam():
            ctx.startProcessing(callback)
            BigWorld.player().prb_swapTeams(ctx.onResponseReceived)
            self._cooldown.process(REQUEST_TYPE.SWAP_TEAMS)
        else:
            LOG_ERROR('Player can not swap teams', pPermissions)
            if callback:
                callback(False)



    def sendInvites(self, ctx, callback = None):
        if self._cooldown.validate(REQUEST_TYPE.SEND_INVITE):
            if callback:
                callback(False)
            return 
        pPermissions = self.getPermissions()
        if self.getPermissions().canSendInvite():
            BigWorld.player().prb_sendInvites(ctx.getDatabaseIDs(), ctx.getComment())
            self._cooldown.process(REQUEST_TYPE.SEND_INVITE, coolDown=REQUEST_COOLDOWN.PREBATTLE_INVITES)
            if callback:
                callback(True)
        else:
            LOG_ERROR('Player can not send invite', pPermissions)
            if callback:
                callback(False)



    def _setTeamNotReady(self, ctx, callback = None):
        if self._cooldown.validate(REQUEST_TYPE.SET_TEAM_STATE):
            if callback:
                callback(False)
            return 
        ctx.startProcessing(callback)
        BigWorld.player().prb_teamNotReady(ctx.getTeam(), ctx.onResponseReceived)
        self._cooldown.process(REQUEST_TYPE.SET_TEAM_STATE, coolDown=REQUEST_COOLDOWN.PREBATTLE_TEAM_NOT_READY)



    def _setTeamReady(self, ctx, callback = None):
        if isParentControlActivated():
            g_eventDispatcher.showParentControlNotification()
            if callback:
                callback(False)
            return 
        (isValid, notValidReason,) = self._limits.isTeamValid()

        def _requestResponse(code, errStr):
            msg = messages.getInvalidTeamServerMessage(errStr, functional=self)
            if msg is not None:
                SystemMessages.pushMessage(msg, type=SystemMessages.SM_TYPE.Error)
            ctx.onResponseReceived(code)


        if isValid:
            ctx.startProcessing(callback)
            BigWorld.player().prb_teamReady(ctx.getTeam(), ctx.isForced(), ctx.getGamePlayMask(), _requestResponse)
        else:
            LOG_ERROR('Team is invalid', notValidReason)
            if callback:
                callback(False)
            SystemMessages.pushMessage(messages.getInvalidTeamMessage(notValidReason, functional=self), type=SystemMessages.SM_TYPE.Error)



    def _setPlayerNotReady(self, ctx, callback = None):
        if self._cooldown.validate(REQUEST_TYPE.SET_PLAYER_STATE, REQUEST_COOLDOWN.PREBATTLE_NOT_READY):
            if callback:
                callback(False)
            return 
        rosterKey = self.getRosterKey()
        (team, assigned,) = decodeRoster(rosterKey)
        if assigned and self.getTeamState(team=team).isInQueue():
            LOG_ERROR('Account assigned and team is ready or locked')
            if callback:
                callback(False)
            return 
        ctx.startProcessing(callback)
        BigWorld.player().prb_notReady(PREBATTLE_ACCOUNT_STATE.NOT_READY, ctx.onResponseReceived)
        self._cooldown.process(REQUEST_TYPE.SET_PLAYER_STATE, REQUEST_COOLDOWN.PREBATTLE_NOT_READY)



    def _setPlayerReady(self, ctx, callback = None):
        if isParentControlActivated():
            g_eventDispatcher.showParentControlNotification()
            if callback:
                callback(False)
            return 
        if ctx.doVehicleValidation():
            (isValid, notValidReason,) = self._limits.isVehicleValid()
            if not isValid:
                SystemMessages.pushMessage(messages.getInvalidVehicleMessage(notValidReason, self), type=SystemMessages.SM_TYPE.Error)
                if callback:
                    callback(False)
                return 
        rosterKey = self.getRosterKey()
        (team, assigned,) = decodeRoster(rosterKey)
        if assigned and self.getTeamState(team=team).isInQueue():
            LOG_ERROR('Account assigned and team is ready or locked')
            if callback:
                callback(False)
            return 
        ctx.startProcessing(callback)
        BigWorld.player().prb_ready(ctx.getVehicleInventoryID(), ctx.onResponseReceived)



    def _getPlayersStateStats(self, rosterKey):
        clientPrb = prb_control.getClientPrebattle()
        notReadyCount = 0
        playersCount = 0
        limitMaxCount = 0
        haveInBattle = False
        if clientPrb:
            players = clientPrb.rosters.get(rosterKey, {})
            playersCount = len(players)
            (team, assigned,) = decodeRoster(rosterKey)
            teamLimits = self._settings.getTeamLimits(team)
            limitMaxCount = teamLimits['maxCount'][(not assigned)]
            for (_, accInfo,) in players.iteritems():
                state = accInfo.get('state', PREBATTLE_ACCOUNT_STATE.UNKNOWN)
                if not state & PREBATTLE_ACCOUNT_STATE.READY:
                    notReadyCount += 1
                    if not haveInBattle and state & PREBATTLE_ACCOUNT_STATE.IN_BATTLE:
                        haveInBattle = True

        return prb_items.PlayersStateStats(notReadyCount, haveInBattle, playersCount, limitMaxCount)




class PreQueueFunctional(ListenersCollection, interfaces.IPreQueueFunctional):

    def __init__(self, queueType, eventsMap, settings = None):
        super(PreQueueFunctional, self).__init__()
        self._queueType = queueType
        self._eventsMap = eventsMap
        self._setListenerClass(interfaces.IPreQueueListener)
        self._settings = settings or {}
        self._hasEntity = False



    def init(self, ctx = None):
        self._hasEntity = True
        if QUEUE_EVENT_TYPE.ENQUEUED in self._eventsMap:
            self._eventsMap[QUEUE_EVENT_TYPE.ENQUEUED] += self.onEnqueued
        if QUEUE_EVENT_TYPE.DEQUEUED in self._eventsMap:
            self._eventsMap[QUEUE_EVENT_TYPE.DEQUEUED] += self.onDequeued
        if QUEUE_EVENT_TYPE.ENQUEUE_ERROR in self._eventsMap:
            self._eventsMap[QUEUE_EVENT_TYPE.ENQUEUE_ERROR] += self.onEnqueueError
        if QUEUE_EVENT_TYPE.KICKED_FROM_QUEUE in self._eventsMap:
            self._eventsMap[QUEUE_EVENT_TYPE.KICKED_FROM_QUEUE] += self.onKickedFromQueue
        if QUEUE_EVENT_TYPE.KICKED_FROM_ARENA in self._eventsMap:
            self._eventsMap[QUEUE_EVENT_TYPE.KICKED_FROM_ARENA] += self.onKickedFromArena
        for l in self._listeners:
            l.onPreQueueFunctionalInited()

        return FUNCTIONAL_INIT_RESULT.INITED



    def fini(self, woEvents = False):
        self._settings.clear()
        self._hasEntity = False
        for l in self._listeners:
            l.onPreQueueFunctionalFinished()

        self._setListenerClass(None)
        if QUEUE_EVENT_TYPE.KICKED_FROM_ARENA in self._eventsMap:
            self._eventsMap[QUEUE_EVENT_TYPE.KICKED_FROM_ARENA] += self.onKickedFromArena
        if QUEUE_EVENT_TYPE.KICKED_FROM_QUEUE in self._eventsMap:
            self._eventsMap[QUEUE_EVENT_TYPE.KICKED_FROM_QUEUE] -= self.onKickedFromQueue
        if QUEUE_EVENT_TYPE.ENQUEUE_ERROR in self._eventsMap:
            self._eventsMap[QUEUE_EVENT_TYPE.ENQUEUE_ERROR] -= self.onEnqueueError
        if QUEUE_EVENT_TYPE.DEQUEUED in self._eventsMap:
            self._eventsMap[QUEUE_EVENT_TYPE.DEQUEUED] -= self.onDequeued
        if QUEUE_EVENT_TYPE.ENQUEUED in self._eventsMap:
            self._eventsMap[QUEUE_EVENT_TYPE.ENQUEUED] -= self.onEnqueued



    def hasLockedState(self):
        return self.isInQueue()



    def getQueueType(self):
        return self._queueType



    def onEnqueued(self, *args):
        for listener in self._listeners:
            listener.onEnqueued(*args)




    def onDequeued(self, *args):
        for listener in self._listeners:
            listener.onDequeued(*args)




    def onEnqueueError(self, *args):
        for listener in self._listeners:
            listener.onEnqueueError(*args)




    def onKickedFromQueue(self, *args):
        for listener in self._listeners:
            listener.onKickedFromQueue(*args)




    def onKickedFromArena(self, *args):
        for listener in self._listeners:
            listener.onKickedFromArena(*args)




    def getConfirmDialogMeta(self, funcExit = FUNCTIONAL_EXIT.NO_FUNC):
        if self.hasLockedState():
            meta = rally_dialog_meta.RallyLeaveDisabledDialogMeta(CTRL_ENTITY_TYPE.PREBATTLE, self._queueType)
        else:
            meta = rally_dialog_meta.createLeavePreQueueMeta(funcExit, self._queueType)
        return meta



    def canPlayerDoAction(self):
        return (not self.isInQueue(), '')



    def exitFromQueue(self):
        self.doAction()



    def hasEntity(self):
        return self._hasEntity



    def doLeaveAction(self, dispatcher, ctx = None, showConfirmation = True):
        if ctx is None:
            ctx = pre_queue_ctx.LeavePreQueueCtx(waitingID='prebattle/leave')
        if dispatcher._setRequestCtx(ctx):
            self.leave(ctx)



    def leave(self, ctx, callback = None):
        if callback:
            callback(True)
        g_prbCtrlEvents.onPreQueueFunctionalDestroyed()



    def changeSetting(self, settingName, settingValue):
        LOG_DEBUG('Changing setting for PreQueueFunctional: ', settingName, settingValue)
        self.changeSettings({settingName: settingValue})



    def changeSettings(self, settings):
        unsuportedSettings = set(settings.keys()) - set(PREQUEUE_SETTING_NAME.ALL())
        if unsuportedSettings:
            LOG_ERROR('Trying to set unsupported settings: ', unsuportedSettings)
            return 
        self._settings.update(settings)
        for l in self._listeners:
            l.onPreQueueSettingsChanged(settings)

        self._applySettings(settings)



    def getSettings(self):
        return self._settings



    def getSetting(self, settingName, defaultValue = None):
        if settingName not in PREQUEUE_SETTING_NAME.ALL():
            LOG_ERROR('Trying to get unsupported settings: ', settingName)
            return None
        return self._settings.get(settingName, defaultValue)



    def _applySettings(self, settings):
        pass




+++ okay decompyling default.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:10:03 CET
