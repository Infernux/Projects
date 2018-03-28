# 2015.01.14 23:22:09 CET
import chat_shared
from constants import PREBATTLE_TYPE
from debug_utils import LOG_ERROR
from messenger import g_settings
from messenger.gui.Scaleform.channels.bw import lobby_controllers
from messenger.gui.Scaleform.channels.bw import battle_controllers
from messenger.gui.interfaces import IControllerFactory
from messenger.m_constants import LAZY_CHANNEL
from messenger.proto.bw import find_criteria
from messenger.storage import storage_getter

class LobbyControllersFactory(IControllerFactory):

    def __init__(self):
        super(LobbyControllersFactory, self).__init__()



    @storage_getter('channels')
    def channelsStorage(self):
        return None



    def init(self):
        controllers = []
        channels = self.channelsStorage.getChannelsByCriteria(find_criteria.BWLobbyChannelFindCriteria())
        for channel in channels:
            controller = self.factory(channel)
            if controller is not None:
                controllers.append(controller)

        return controllers



    def factory(self, channel):
        controller = None
        if channel.getName() in LAZY_CHANNEL.ALL:
            if channel.getName() == LAZY_CHANNEL.SPECIAL_BATTLES:
                controller = lobby_controllers.BSLazyChannelController(channel)
            else:
                controller = lobby_controllers.LazyChannelController(channel)
        elif channel.isPrebattle():
            if g_settings.server.BW_CHAT2.isEnabled():
                return 
            prbType = channel.getPrebattleType()
            if prbType is 0:
                LOG_ERROR('Prebattle type is not found', channel)
                return 
            if prbType is PREBATTLE_TYPE.TRAINING:
                controller = lobby_controllers.TrainingChannelController(channel)
            else:
                controller = lobby_controllers.PrebattleChannelController(prbType, channel)
        elif not channel.isBattle():
            controller = lobby_controllers.LobbyChannelController(channel)
        return controller




class BattleControllersFactory(IControllerFactory):

    @storage_getter('channels')
    def channelsStorage(self):
        return None



    def init(self):
        controllers = []
        channels = self.channelsStorage.getChannelsByCriteria(find_criteria.BWBattleChannelFindCriteria())
        squad = self.channelsStorage.getChannelByCriteria(find_criteria.BWPrbChannelFindCriteria(PREBATTLE_TYPE.SQUAD))
        if squad is not None:
            channels.append(squad)
        eventSquad = self.channelsStorage.getChannelByCriteria(find_criteria.BWPrbChannelFindCriteria(PREBATTLE_TYPE.EVENT_SQUAD))
        if eventSquad is not None:
            channels.append(eventSquad)
        for channel in channels:
            controller = self.factory(channel)
            if controller is not None:
                controllers.append(controller)

        return controllers



    def factory(self, channel):
        controller = None
        flags = channel.getProtoData().flags
        if flags & chat_shared.CHAT_CHANNEL_BATTLE != 0:
            if flags & chat_shared.CHAT_CHANNEL_BATTLE_TEAM != 0:
                controller = battle_controllers.TeamChannelController(channel)
            else:
                controller = battle_controllers.CommonChannelController(channel)
        elif flags & chat_shared.CHAT_CHANNEL_SQUAD != 0:
            controller = battle_controllers.SquadChannelController(channel)
        return controller




+++ okay decompyling factories.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 23:22:09 CET
