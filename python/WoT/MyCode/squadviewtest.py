from gui.Scaleform.daapi.view.lobby.prb_windows.SquadView import SquadView

def new_onPlayerStateChanged(self, functional, roster, playerInfo):
    self._updateRallyData()
    self._setActionButtonState()
    filt = messenger.proto.bw.find_criteria.BWPrbChannelFindCriteria(1)
    chan = messenger.MessengerEntry.g_instance.storage.channels.getChannelByCriteria(filt)
    battle_controllers.SquadChannelController(chan.getID())._broadcast('test')
    from gui import SystemMessages
    SystemMessages.pushMessage("test")

SquadView.my_new=new_onPlayerStateChanged
