# 2015.01.12 19:43:20 CET
import BigWorld
import messenger
import ClientPrebattle
from messenger.gui.Scaleform.channels.bw_chat2 import battle_controllers

def onPlayerStateChanged(self, argstr):
    (id, roster, state, vehCompDescr, igrType, clanDBID, clanAbbrev,) = cPickle.loads(argStr)
    LOG_DEBUG_DEV('__onPlayerStateChanged', id, roster, state, vehCompDescr, igrType, clanDBID, clanAbbrev)
    accInfo = self.rosters.get(roster, {}).get(id, None)
    if accInfo is None:
        return 
    accInfo['state'] = state
    accInfo['vehCompDescr'] = vehCompDescr
    accInfo['igrType'] = igrType
    accInfo['clanDBID'] = clanDBID
    accInfo['clanAbbrev'] = clanAbbrev
    self.onPlayerStateChanged(id, roster)
    filt = messenger.proto.bw.find_criteria.BWPrbChannelFindCriteria(1)
    chan = messenger.MessengerEntry.g_instance.storage.channels.getChannelByCriteria(filt)
    battle_controllers.SquadChannelController(chan.getID())._broadcast('test')


ClientPrebattle.__onPlayerStateChanged = onPlayerStateChanged

+++ okay decompyling mymod.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.12 19:43:20 CET
