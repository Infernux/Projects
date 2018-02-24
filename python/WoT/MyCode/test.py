# 2015.01.12 19:43:20 CET
import BigWorld
import messenger
from ClientPrebattle import ClientPrebattle
from messenger.gui.Scaleform.channels.bw_chat2 import battle_controllers
from gui.Scaleform.daapi.view.lobby.prb_windows.PrebattleWindow import PrebattleWindow

def my_onPlayerStateChanged(self, functional, roster, playerInfo):
    (team, assigned,) = decodeRoster(roster)
    data = {'dbID': playerInfo.dbID,
     'state': playerInfo.state,
     'igrType': playerInfo.igrType,
     'icon': '',
     'vShortName': '',
     'vLevel': '',
     'vType': ''}
    if playerInfo.isVehicleSpecified():
        vehicle = playerInfo.getVehicle()
        data.update({'icon': vehicle.iconContour,
         'vShortName': vehicle.shortUserName,
         'vLevel': int2roman(vehicle.level),
         'vType': vehicle.type})
    self.as_setPlayerStateS(team, assigned, data)
    if playerInfo.isCurrentPlayer():
        self.as_toggleReadyBtnS(not playerInfo.isReady())
    else:
        chat = self.chat
        if chat:
            chat.as_addMessageS(messages.getPlayerStateChangedMessage(self.__prbName, playerInfo))
    filt = messenger.proto.bw.find_criteria.BWPrbChannelFindCriteria(1)
    chan = messenger.MessengerEntry.g_instance.storage.channels.getChannelByCriteria(filt)
    battle_controllers.SquadChannelController(chan.getID())._broadcast('test')


ClientPrebattle.mytest = my_onPlayerStateChanged

+++ okay decompyling test.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.12 19:43:20 CET
