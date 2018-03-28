# 2015.01.14 23:23:17 CET
from constants import PREBATTLE_TYPE
from messenger.gui.Scaleform.channels.bw_chat2 import battle_controllers
from messenger.gui.Scaleform.channels.bw_chat2 import lobby_controllers
from messenger.gui.interfaces import IControllerFactory
from messenger.m_constants import BATTLE_CHANNEL
from messenger.proto.bw_chat2 import find_criteria
from messenger.storage import storage_getter

class LobbyControllersFactory(IControllerFactory):

    @storage_getter('channels')
    def channelsStorage(self):
        return None



    def init(self):
        controllers = []
        channels = self.channelsStorage.getChannelsByCriteria(find_criteria.BWPrebattleChannelFindCriteria())
        for channel in channels:
            controller = self.factory(channel)
            if controller is not None:
                controllers.append(controller)

        return controllers



    def factory(self, channel):
        controller = None
        prbType = channel.getPrebattleType()
        if prbType:
            if prbType == PREBATTLE_TYPE.TRAINING:
                controller = lobby_controllers.TrainingChannelController(channel)
            else:
                controller = lobby_controllers.UnitChannelController(channel)
        return controller




class BattleControllersFactory(IControllerFactory):

    @storage_getter('channels')
    def channelsStorage(self):
        return None



    def init(self):
        controllers = []
        channels = self.channelsStorage.getChannelsByCriteria(find_criteria.BWBattleChannelFindCriteria())
        for channel in channels:
            controller = self.factory(channel)
            if controller is not None:
                controllers.append(controller)

        return controllers



    def factory(self, channel):
        controller = None
        settings = channel.getProtoData()
        if settings == BATTLE_CHANNEL.TEAM:
            controller = battle_controllers.TeamChannelController(channel)
        elif settings == BATTLE_CHANNEL.COMMON:
            controller = battle_controllers.CommonChannelController(channel)
        elif settings == BATTLE_CHANNEL.SQUAD:
            controller = battle_controllers.SquadChannelController(channel)
        return controller




+++ okay decompyling factories.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 23:23:17 CET
