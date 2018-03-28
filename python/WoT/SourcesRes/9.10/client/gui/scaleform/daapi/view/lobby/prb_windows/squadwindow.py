# 2015.01.17 21:34:02 CET
from constants import PREBATTLE_TYPE
from prebattle_shared import decodeRoster
from gui.Scaleform.daapi.view.meta.SquadWindowMeta import SquadWindowMeta
from gui.Scaleform.managers.windows_stored_data import DATA_TYPE, TARGET_ID
from gui.Scaleform.managers.windows_stored_data import stored_window
from gui.Scaleform.genConsts.PREBATTLE_ALIASES import PREBATTLE_ALIASES
from gui.prb_control.context import prb_ctx
from gui.prb_control.formatters import messages
from gui.shared import events, EVENT_BUS_SCOPE

@stored_window(DATA_TYPE.UNIQUE_WINDOW, TARGET_ID.CHANNEL_CAROUSEL)
class SquadWindow(SquadWindowMeta):

    def __init__(self, ctx = None):
        super(SquadWindow, self).__init__()
        self._isInvitesOpen = ctx.get('isInvitesOpen', False)



    def getPrbType(self):
        return PREBATTLE_TYPE.SQUAD



    def onWindowClose(self):
        self.prbDispatcher.doLeaveAction(prb_ctx.LeavePrbCtx(waitingID='prebattle/leave'))



    def onWindowMinimize(self):
        self.destroy()



    @property
    def squadViewComponent(self):
        return self.components.get(PREBATTLE_ALIASES.SQUAD_VIEW_PY)



    def onPlayerAdded(self, functional, playerInfo):
        self.__addPlayerNotification(playerInfo, messages.getPlayerAddedMessage)



    def onPlayerRemoved(self, functional, playerInfo):
        self.__addPlayerNotification(playerInfo, messages.getPlayerRemovedMessage)



    def onPlayerRosterChanged(self, functional, actorInfo, playerInfo):
        self.__addPlayerNotification(playerInfo, messages.getPlayerAssignFlagChanged)



    def onPlayerStateChanged(self, functional, roster, playerInfo):
        self.__addPlayerNotification(playerInfo, messages.getPlayerStateChangedMessage)



    def onTeamStatesReceived(self, functional, team1State, team2State):
        self.as_enableWndCloseBtnS(self._isLeaveBtnEnabled())



    def _populate(self):
        super(SquadWindow, self)._populate()
        self.addListener(events.HideWindowEvent.HIDE_SQUAD_WINDOW, self.__handleSquadWindowHide, scope=EVENT_BUS_SCOPE.LOBBY)
        self.__processInvitesWindow()



    def _dispose(self):
        self.removeListener(events.HideWindowEvent.HIDE_SQUAD_WINDOW, self.__handleSquadWindowHide, scope=EVENT_BUS_SCOPE.LOBBY)
        super(SquadWindow, self)._dispose()



    def _showLeadershipNotification(self):
        pass



    def _isLeaveBtnEnabled(self):
        functional = self.prbFunctional
        (team, assigned,) = decodeRoster(functional.getRosterKey())
        return not (functional.getTeamState().isInQueue() and functional.getPlayerInfo().isReady() and assigned)



    def __handleSquadWindowHide(self, _):
        self.destroy()



    def __addPlayerNotification(self, pInfo, formatter):
        if self.chat and not pInfo.isCurrentPlayer():
            self.chat.as_addMessageS(formatter('squad', pInfo))



    def __processInvitesWindow(self):
        squadView = self.squadViewComponent
        if self._isInvitesOpen and squadView is not None:
            squadView.inviteFriendRequest()




+++ okay decompyling squadwindow.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.17 21:34:02 CET
