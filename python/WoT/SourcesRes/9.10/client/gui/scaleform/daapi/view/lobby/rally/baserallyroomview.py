# 2015.01.14 22:27:17 CET
from CurrentVehicle import g_currentVehicle
from UnitBase import UNIT_SLOT
import account_helpers
from adisp import process
from debug_utils import LOG_DEBUG
from gui import makeHtmlString, DialogsInterface
from gui.Scaleform.daapi.view.lobby.rally import vo_converters
from gui.Scaleform.daapi.view.meta.BaseRallyRoomViewMeta import BaseRallyRoomViewMeta
from gui.Scaleform.framework import ViewTypes, AppRef
from gui.Scaleform.framework.managers.containers import POP_UP_CRITERIA
from gui.Scaleform.genConsts.CYBER_SPORT_ALIASES import CYBER_SPORT_ALIASES
from gui.Scaleform.genConsts.PREBATTLE_ALIASES import PREBATTLE_ALIASES
from gui.prb_control.context import unit_ctx
from gui.prb_control.prb_helpers import UnitListener
from gui.prb_control.settings import CTRL_ENTITY_TYPE, FUNCTIONAL_EXIT, REQUEST_TYPE
from gui.shared import events
from gui.shared.ItemsCache import g_itemsCache
from gui.shared.event_bus import EVENT_BUS_SCOPE
from gui.shared.utils.requesters.ItemsRequester import REQ_CRITERIA
from messenger.gui.Scaleform.sf_settings import MESSENGER_VIEW_ALIAS
from messenger.proto.events import g_messengerEvents

class BaseRallyRoomView(BaseRallyRoomViewMeta, AppRef, UnitListener):

    def __init__(self):
        super(BaseRallyRoomView, self).__init__()
        self._candidatesDP = None



    def requestToAssign(self, pID, slotIdx):
        self.sendRequest(unit_ctx.AssignUnitCtx(pID, slotIdx, 'prebattle/assign'))



    def requestToUnassign(self, pID):
        self.sendRequest(unit_ctx.AssignUnitCtx(pID, UNIT_SLOT.REMOVE, 'prebattle/assign'))



    def requestToCloseSlot(self, slotIdx):
        slotState = self.unitFunctional.getSlotState(slotIdx)
        self.sendRequest(unit_ctx.CloseSlotCtx(slotIdx, not slotState.isClosed, 'prebattle/change_settings'))



    def requestToKickUser(self, databaseID):
        self.sendRequest(unit_ctx.KickPlayerCtx(databaseID, 'prebattle/kick'))



    def requestToLock(self, isLocked):
        self.sendRequest(unit_ctx.LockUnitCtx(isLocked, 'prebattle/change_settings'))



    def requestToOpen(self, isOpened):
        self.sendRequest(unit_ctx.ChangeOpenedUnitCtx(isOpened, 'prebattle/change_settings'))



    def requestToChangeComment(self, comment):
        self.sendRequest(unit_ctx.ChangeCommentUnitCtx(comment, 'prebattle/change_settings'))



    def requestToUpdateRoster(self, data):
        c = unit_ctx.SetRostersSlotsCtx('prebattle/change_settings')
        for i in range(0, len(data)):
            c.addRosterSlot(i * 2, self.__getRosterSlotCtx(data[i][0]))
            c.addRosterSlot(i * 2 + 1, self.__getRosterSlotCtx(data[i][1]))

        self.sendRequest(c)



    @process
    def canBeClosed(self, callback):
        meta = self.unitFunctional.getConfirmDialogMeta()
        if meta:
            isConfirmed = yield DialogsInterface.showDialog(meta)
        else:
            isConfirmed = yield lambda callback: callback(True)
        if isConfirmed:
            isConfirmed = yield self.prbDispatcher.leave(unit_ctx.LeaveUnitCtx(waitingID='prebattle/leave', funcExit=FUNCTIONAL_EXIT.INTRO_UNIT))
        callback(isConfirmed)



    @process
    def sendRequest(self, request):
        yield self.prbDispatcher.sendUnitRequest(request)



    def onUnitPlayersListChanged(self):
        self._candidatesDP.rebuild(self.unitFunctional.getCandidates())



    def onUnitPlayerInfoChanged(self, pInfo):
        if pInfo.isInSlot:
            self._updateMembersData()
        else:
            self._candidatesDP.rebuild(self.unitFunctional.getCandidates())



    def onUnitPlayerStateChanged(self, pInfo):
        self.__setMemberStatus(pInfo)
        if pInfo.isCurrentPlayer() or self.unitFunctional.isCreator():
            self._setActionButtonState()



    def onUnitPlayerRolesChanged(self, pInfo, pPermissions):
        if pInfo.isCurrentPlayer():
            self._setActionButtonState()
        self._updateMembersData()



    def onUnitPlayerOnlineStatusChanged(self, pInfo):
        if pInfo.isInSlot:
            self.as_setMemberOfflineS(pInfo.slotIdx, pInfo.isOffline())
        elif self._candidatesDP:
            self._candidatesDP.setOnline(pInfo)



    def onUnitPlayerEnterOrLeaveArena(self, pInfo):
        self.__setMemberStatus(pInfo)



    def onUnitPlayerBecomeCreator(self, pInfo):
        self._updateRallyData()



    def onUnitRejoin(self):
        self._updateRallyData()
        self._setActionButtonState()



    def onUnitPlayerVehDictChanged(self, pInfo):
        if pInfo.isCurrentPlayer() or self.unitFunctional.isCreator():
            self._updateRallyData()
            self._setActionButtonState()



    def onUnitRosterChanged(self):
        self._updateMembersData()



    def _updateRallyData(self):
        pass



    def setData(self, initialData):
        LOG_DEBUG('CyberSportUnitView.setItemId passed team id is:', initialData)



    def getCoolDownRequests(self):
        return [REQUEST_TYPE.SET_PLAYER_STATE, REQUEST_TYPE.CHANGE_UNIT_STATE]



    def initCandidatesDP(self):
        pass



    def rebuildCandidatesDP(self):
        pass



    def _setActionButtonState(self):
        pass



    def startListening(self):
        self.startUnitListening()
        g_currentVehicle.onChanged += self.__handleCurrentVehicleChanged



    def stopListening(self):
        self.stopUnitListening()
        g_currentVehicle.onChanged -= self.__handleCurrentVehicleChanged



    def _populate(self):
        super(BaseRallyRoomView, self)._populate()
        self.startListening()
        self.initCandidatesDP()
        self.addListener(events.CSVehicleSelectEvent.VEHICLE_SELECTED, self._onVehicleSelect)
        self._updateRallyData()
        self._setActionButtonState()
        g_messengerEvents.users.onUserRosterChanged += self._onUserRosterChanged
        g_messengerEvents.users.onUsersRosterReceived += self._onUsersRosterReceived



    def _dispose(self):
        g_messengerEvents.users.onUserRosterChanged -= self._onUserRosterChanged
        g_messengerEvents.users.onUsersRosterReceived -= self._onUsersRosterReceived
        self._closeSendInvitesWindow()
        HideEvent = events.HideWindowEvent
        self.fireEvent(HideEvent(HideEvent.HIDE_VEHICLE_SELECTOR_WINDOW))
        if self._candidatesDP is not None:
            self._candidatesDP.fini()
            self._candidatesDP = None
        self.stopListening()
        self.removeListener(events.CSVehicleSelectEvent.VEHICLE_SELECTED, self._onVehicleSelect)
        super(BaseRallyRoomView, self)._dispose()



    def assignSlotRequest(self, slotIndex, playerId):
        if playerId == -1:
            if self.unitFunctional.getPlayerInfo().isCreator():
                LOG_DEBUG('Request to assign is ignored. Creator can not move to another slots')
                return 
            playerId = account_helpers.getPlayerDatabaseID()
        elif not self.isPlayerInUnit(playerId):
            return 
        self.requestToAssign(playerId, slotIndex)



    def leaveSlotRequest(self, playerId):
        if self.isPlayerInSlot(playerId):
            self.requestToUnassign(playerId)



    def chooseVehicleRequest(self):
        playerInfo = self.unitFunctional.getPlayerInfo()
        levelsRange = self.unitFunctional.getRosterSettings().getLevelsRange()
        slotIdx = playerInfo.slotIdx
        vehicles = playerInfo.getSlotsToVehicles(True).get(slotIdx)
        if vehicles is not None:
            vehicles = g_itemsCache.items.getVehicles(REQ_CRITERIA.VEHICLE.SPECIFIC_BY_CD(vehicles))
        self.fireEvent(events.LoadViewEvent(CYBER_SPORT_ALIASES.VEHICLE_SELECTOR_POPUP_PY, ctx={'isMultiSelect': False,
         'vehicles': vehicles,
         'infoText': self._getVehicleSelectorDescription(),
         'section': 'cs_unit_view_vehicle',
         'levelsRange': levelsRange}), scope=EVENT_BUS_SCOPE.LOBBY)



    def _getVehicleSelectorDescription(self):
        return ''



    def inviteFriendRequest(self):
        self.fireEvent(events.LoadViewEvent(PREBATTLE_ALIASES.SEND_INVITES_WINDOW_PY, ctx={'prbName': 'unit',
         'ctrlType': CTRL_ENTITY_TYPE.UNIT}), scope=EVENT_BUS_SCOPE.LOBBY)



    def toggleReadyStateRequest(self):
        self.unitFunctional.doAction()



    def ignoreUserRequest(self, databaseID):
        playerInfo = self.unitFunctional.getPlayerInfo()
        if playerInfo.isCreator():
            self.requestToKickUser(databaseID)



    def onSlotsHighlihgtingNeed(self, databaseID):
        availableSlots = self.getAvailableSlots(databaseID)
        self.as_highlightSlotsS(availableSlots)
        return availableSlots



    def getAvailableSlots(self, databaseID):
        availableSlots = list(self.unitFunctional.getPlayerInfo(databaseID).getAvailableSlots(True))
        return availableSlots



    def editDescriptionRequest(self, description):
        LOG_DEBUG('EDIT DESCRIPTION: ', description)
        self.requestToChangeComment(description)



    def showFAQWindow(self):
        self.fireEvent(events.LoadViewEvent(MESSENGER_VIEW_ALIAS.FAQ_WINDOW), scope=EVENT_BUS_SCOPE.LOBBY)



    def _onVehicleSelect(self, event):
        items = event.ctx
        if len(items):
            self.sendRequest(unit_ctx.SetVehicleUnitCtx(vTypeCD=items[0], waitingID='prebattle/change_settings'))



    def _onUserRosterChanged(self, _, user):
        self._updateRallyData()
        if self._candidatesDP and self._candidatesDP.hasCandidate(user.getID()):
            self.rebuildCandidatesDP()



    def _onUsersRosterReceived(self):
        self._updateRallyData()



    def _updateVehiclesLabel(self, minVal, maxVal):
        self.as_setVehiclesTitleS(makeHtmlString('html_templates:lobby/rally/', 'vehiclesLabel', {'minValue': minVal,
         'maxValue': maxVal}))



    def _closeSendInvitesWindow(self):
        self._destroyRelatedView(ViewTypes.WINDOW, PREBATTLE_ALIASES.SEND_INVITES_WINDOW_PY)



    def _destroyRelatedView(self, container, alias):
        container = self.app.containerManager.getContainer(container)
        if container is not None:
            view = container.getView(criteria={POP_UP_CRITERIA.VIEW_ALIAS: alias})
            if view is not None:
                view.destroy()



    def isPlayerInUnit(self, databaseID):
        result = False
        players = self.unitFunctional.getPlayers()
        for (dbId, playerInfo,) in players.iteritems():
            if dbId == databaseID:
                result = True
                break

        return result



    def isPlayerInSlot(self, databaseID = None):
        pInfo = self.unitFunctional.getPlayerInfo(dbID=databaseID)
        return pInfo.isInSlot



    def __getRosterSlotCtx(self, item):
        if item is None:
            return unit_ctx.RosterSlotCtx()
        else:
            if type(item) == long:
                return unit_ctx.RosterSlotCtx(item)
            settings = self.unitFunctional.getRosterSettings()
            levels = (settings.getMinLevel(), settings.getMaxLevel())
            if len(item.vLevelRange) == 2:
                i0 = int(item.vLevelRange[0])
                i1 = int(item.vLevelRange[1])
                levels = (i0, i1) if i0 != i1 else i0
            elif len(item.vLevelRange) == 1:
                levels = int(item.vLevelRange[0])
            return unit_ctx.RosterSlotCtx(nationNames=item.nationIDRange, levels=levels, vehClassNames=item.vTypeRange)



    def __setMemberStatus(self, pInfo):
        if pInfo.isInSlot:
            slotIdx = pInfo.slotIdx
            slotState = self.unitFunctional.getSlotState(slotIdx)
            self.as_setMemberStatusS(slotIdx, vo_converters.getPlayerStatus(slotState, pInfo))



    def _updateMembersData(self):
        functional = self.unitFunctional
        self.as_setMembersS(*vo_converters.makeSlotsVOs(functional, functional.getUnitIdx(), app=self.app))
        self._setActionButtonState()



    def __handleCurrentVehicleChanged(self):
        self._setActionButtonState()




+++ okay decompyling baserallyroomview.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:27:18 CET
