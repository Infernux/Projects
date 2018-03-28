# 2015.01.18 11:53:47 CET
from collections import namedtuple
import weakref
from constants import PREBATTLE_TYPE
from debug_utils import LOG_WARNING, LOG_ERROR, LOG_DEBUG
from gui import GUI_SETTINGS
from gui.battle_control.arena_info import getClientArena
from messenger.m_constants import BATTLE_CHANNEL, MESSENGER_SCOPE
from messenger.proto.bw_chat2 import admin_chat_cmd
from messenger.proto.bw_chat2 import entities, limits, wrappers, errors
from messenger.proto.bw_chat2 import provider
from messenger.proto.bw_chat2.battle_chat_cmd import BattleCommandFactory
from messenger.proto.events import g_messengerEvents
from messenger.storage import storage_getter
from messenger_common_chat2 import MESSENGER_ACTION_IDS as _ACTIONS
from messenger_common_chat2 import MESSENGER_LIMITS as _LIMITS
from messenger_common_chat2 import BATTLE_CHAT_COMMANDS
_ActionsCollection = namedtuple('_ActionsCollection', 'initID deInitID onBroadcastID broadcastID')

class _EntityChatHandler(provider.ResponseSeqHandler):

    def __init__(self, provider, adminChat, actions, factory, limits_):
        super(_EntityChatHandler, self).__init__(provider, 10)
        self.__isInited = False
        self.__isEnabled = False
        self.__messagesQueue = []
        self.__adminChat = weakref.proxy(adminChat)
        self.__actions = actions
        self.__factory = factory
        self.__limits = limits_
        self.__msgFilters = None



    @storage_getter('channels')
    def channelsStorage(self):
        return None



    @storage_getter('users')
    def usersStorage(self):
        return None



    def isInited(self):
        return self.__isInited



    def clear(self):
        self.__isInited = False
        self.__isEnabled = False
        self.__messagesQueue = []
        self.__adminChat = None
        super(_EntityChatHandler, self).clear()



    def leave(self):
        self._reqIDs.clear()
        self.__isInited = False



    def disconnect(self):
        self.__isEnabled = False
        self.__messagesQueue = []
        self.leave()



    def registerHandlers(self):
        register = self.provider().registerHandler
        register(self.__actions.initID, self._onEntityChatInit)
        register(self.__actions.deInitID, self._onEntityChatDeInit)
        register(self.__actions.onBroadcastID, self._onMessageBroadcast)
        g_messengerEvents.users.onUsersRosterReceived += self.__me_onUsersRosterReceived
        super(_EntityChatHandler, self).registerHandlers()



    def unregisterHandlers(self):
        unregister = self.provider().unregisterHandler
        unregister(self.__actions.initID, self._onEntityChatInit)
        unregister(self.__actions.deInitID, self._onEntityChatDeInit)
        unregister(self.__actions.onBroadcastID, self._onMessageBroadcast)
        g_messengerEvents.users.onUsersRosterReceived -= self.__me_onUsersRosterReceived
        super(_EntityChatHandler, self).unregisterHandlers()



    def broadcast(self, text, *args):
        if self.__isInited:
            provider = self.provider()
            text = provider.filterOutMessage(text, self.__limits)
            if not text:
                return 
            (result, cmd,) = self.__adminChat.parseLine(text)
            if result:
                if cmd:
                    cmd.setClientID(self._getClientIDForCommand())
                return 
            actionID = self.__actions.broadcastID
            (success, reqID,) = provider.doAction(actionID, self.__factory.broadcastArgs(text, *args), True)
            if reqID:
                self.pushRq(reqID)
            if success:
                cooldown = self.__limits.getBroadcastCoolDown()
                provider.setActionCoolDown(actionID, cooldown)
        else:
            LOG_WARNING('TODO: Adds error message')



    def isBroadcastInCooldown(self):
        return self.provider().isActionInCoolDown(self.__actions.broadcastID)



    def _doInit(self, args):
        raise NotImplementedError



    def _addHistory(self, iterator):
        for message in iterator:
            self._addMessage(message)




    def _getChannel(self, message):
        raise NotImplementedError



    def _getClientIDForCommand(self):
        raise NotImplementedError



    def _addChannel(self, channel):
        if not self.channelsStorage.addChannel(channel):
            return self.channelsStorage.getChannel(channel)
        g_messengerEvents.channels.onChannelInited(channel)
        return channel



    def _removeChannel(self, channel):
        if channel and self.channelsStorage.removeChannel(channel, clear=False):
            g_messengerEvents.channels.onChannelDestroyed(channel)
            channel.clear()



    def _addMessage(self, message):
        message = self.provider().filterInMessage(message)
        if message:
            user = self.usersStorage.getUser(message.accountDBID)
            if not (user and user.isIgnored()):
                g_messengerEvents.channels.onMessageReceived(message, self._getChannel(message))



    def _onEntityChatInit(self, _, args):
        if self.__isInited:
            LOG_WARNING('EntityChat already is inited', self)
            return 
        self.__isInited = True
        self._doInit(dict(args))
        history = self.__factory.historyIter(args)
        if self.__isEnabled:
            self._addHistory(history)
        else:
            self.__messagesQueue.extend(list(history))



    def _onEntityChatDeInit(self, _, args):
        self.leave()



    def _onMessageBroadcast(self, _, args):
        message = self.__factory.messageVO(args)
        if self.__isEnabled:
            self._addMessage(message)
        else:
            self.__messagesQueue.append(message)



    def _onResponseFailure(self, ids, args):
        if super(_EntityChatHandler, self)._onResponseFailure(ids, args):
            error = errors.createBroadcastError(args, self.__actions.broadcastID)
            if error:
                g_messengerEvents.onServerErrorReceived(error)



    def __me_onUsersRosterReceived(self):
        self.__isEnabled = True
        while self.__messagesQueue:
            self._addMessage(self.__messagesQueue.pop(0))





class ArenaChatHandler(_EntityChatHandler):

    def __init__(self, provider, adminChat):
        super(ArenaChatHandler, self).__init__(provider, adminChat, _ActionsCollection(_ACTIONS.INIT_BATTLE_CHAT, _ACTIONS.DEINIT_BATTLE_CHAT, _ACTIONS.ON_BATTLE_MESSAGE_BROADCAST, _ACTIONS.BROADCAST_BATTLE_MESSAGE), wrappers.ArenaDataFactory(), limits.ArenaLimits())
        self.__teamChannel = None
        self.__commonChannel = None



    def getTeamChannel(self):
        return self.__teamChannel



    def getCommonChannel(self):
        return self.__commonChannel



    def leave(self):
        self.__doRemoveChannels()
        super(ArenaChatHandler, self).leave()



    def clear(self):
        self.__doRemoveChannels()
        super(ArenaChatHandler, self).clear()



    def _doInit(self, args):
        self.__teamChannel = self._addChannel(entities.BWBattleChannelEntity(BATTLE_CHANNEL.TEAM))
        self.__commonChannel = self._addChannel(entities.BWBattleChannelEntity(BATTLE_CHANNEL.COMMON))



    def _getChannel(self, message):
        if message.isCommonChannel:
            channel = self.__commonChannel
        else:
            channel = self.__teamChannel
        return channel



    def _getClientIDForCommand(self):
        if self.__teamChannel:
            return self.__teamChannel.getClientID()
        return 0



    def __doRemoveChannels(self):
        self.__teamChannel = self._removeChannel(self.__teamChannel)
        self.__commonChannel = self._removeChannel(self.__commonChannel)




class UnitChatHandler(_EntityChatHandler):

    def __init__(self, provider, adminChat):
        super(UnitChatHandler, self).__init__(provider, adminChat, _ActionsCollection(_ACTIONS.INIT_UNIT_CHAT, _ACTIONS.DEINIT_UNIT_CHAT, _ACTIONS.ON_UNIT_MESSAGE_BROADCAST, _ACTIONS.BROADCAST_UNIT_MESSAGE), wrappers.UnitDataFactory(), limits.UnitLimits())
        self.__channel = None
        self.__history = None



    def getUnitChannel(self):
        return self.__channel



    def addHistory(self):
        if self.__history:
            self._addHistory(self.__history)



    def leave(self):
        self.__doRemoveChannel()
        self.__history = None
        super(UnitChatHandler, self).leave()



    def clear(self):
        self.__doRemoveChannel()
        super(UnitChatHandler, self).clear()



    def _doInit(self, args):
        if 'int32Arg1' in args:
            self.__doCreateChannel(args['int32Arg1'])
        else:
            LOG_ERROR('Type of prebattle is not defined', args)



    def _addHistory(self, iterator):
        if self.__history is None:
            self.__history = iterator
        else:
            super(UnitChatHandler, self)._addHistory(iterator)



    def _getChannel(self, message):
        return self.__channel



    def _getClientIDForCommand(self):
        if self.__channel:
            return self.__channel.getClientID()
        return 0



    def __doCreateChannel(self, prbType):
        if self.__channel:
            return 
        settings = None
        if prbType in PREBATTLE_TYPE.LIKE_SQUAD:
            settings = BATTLE_CHANNEL.SQUAD
        self.__channel = self._addChannel(entities.BWUnitChannelEntity(settings, prbType))



    def __doRemoveChannel(self):
        self.__channel = self._removeChannel(self.__channel)




class BattleChatCommandHandler(provider.ResponseDictHandler):

    def __init__(self, provider):
        super(BattleChatCommandHandler, self).__init__(provider)
        self.__factory = BattleCommandFactory()
        self.__targetIDs = []



    @property
    def factory(self):
        return self.__factory



    def clear(self):
        self.__factory = None
        self.__targetIDs = []
        super(BattleChatCommandHandler, self).clear()



    def switch(self, scope):
        self.__targetIDs = []
        if scope != MESSENGER_SCOPE.BATTLE:
            return 
        arena = getClientArena()
        if arena:
            arena.onVehicleKilled += self.__onVehicleKilled



    def send(self, decorator):
        command = decorator.getCommand()
        if command:
            provider = self.provider()
            (success, reqID,) = provider.doAction(command.id, decorator.getProtoData(), True, not GUI_SETTINGS.isBattleCmdCoolDownVisible)
            if reqID:
                self.pushRq(reqID, command)
            if success:
                if decorator.isEnemyTarget():
                    self.__targetIDs.append(decorator.getTargetID())
                provider.setActionCoolDown(command.id, command.cooldownPeriod)
        else:
            LOG_ERROR('Battle command is not found', decorator)



    def registerHandlers(self):
        register = self.provider().registerHandler
        for command in BATTLE_CHAT_COMMANDS:
            register(command.id, self.__onCommandReceived)

        super(BattleChatCommandHandler, self).registerHandlers()



    def unregisterHandlers(self):
        unregister = self.provider().unregisterHandler
        for command in BATTLE_CHAT_COMMANDS:
            unregister(command.id, self.__onCommandReceived)

        super(BattleChatCommandHandler, self).unregisterHandlers()



    def _onResponseFailure(self, ids, args):
        command = super(BattleChatCommandHandler, self)._onResponseFailure(ids, args)
        if command:
            error = errors.createBattleCommandError(args, command)
            if error:
                g_messengerEvents.onServerErrorReceived(error)
            else:
                LOG_WARNING('Error is not resolved on the client', command, args)



    def __onCommandReceived(self, ids, args):
        (actionID, _,) = ids
        cmd = self.__factory.createByAction(actionID, args)
        if cmd.isIgnored():
            LOG_DEBUG('Chat command is ignored', cmd)
            return 
        if cmd.isPrivate() and not (cmd.isReceiver() or cmd.isSender()):
            return 
        g_messengerEvents.channels.onCommandReceived(cmd)



    def __onVehicleKilled(self, victimID, killerID, reason):
        provider = self.provider()
        if victimID in self.__targetIDs:
            self.__targetIDs.remove(victimID)
            for actionID in self.__factory.getEnemyTargetCommandsIDs():
                provider.clearActionCoolDown(actionID)





class AdminChatCommandHandler(provider.ResponseDictHandler):

    def __init__(self, provider):
        super(AdminChatCommandHandler, self).__init__(provider)



    def parseLine(self, text, clientID = 0):
        (cmd, result,) = (None, admin_chat_cmd.parseCommandLine(text))
        if not result:
            return (False, None)
        if result.hasError():
            g_messengerEvents.onServerErrorReceived(result.getError())
        else:
            decorator = admin_chat_cmd.makeDecorator(result, clientID)
            if self.send(decorator):
                cmd = decorator
        return (True, cmd)



    def send(self, decorator):
        provider = self.provider()
        commandID = decorator.getID()
        (success, reqID,) = provider.doAction(commandID, decorator.getProtoData(), True)
        if reqID:
            self.pushRq(reqID, decorator)
        if success:
            provider.setActionCoolDown(commandID, _LIMITS.ADMIN_COMMANDS_FROM_CLIENT_COOLDOWN_SEC)
        return success



    def _onResponseFailure(self, ids, args):
        if super(AdminChatCommandHandler, self)._onResponseFailure(ids, args):
            error = errors.createAdminCommandError(args)
            if error:
                g_messengerEvents.onServerErrorReceived(error)
            else:
                LOG_WARNING('Error is not resolved on the client', ids, args)



    def _onResponseSuccess(self, ids, args):
        cmd = super(AdminChatCommandHandler, self)._onResponseSuccess(ids, args)
        if cmd:
            g_messengerEvents.channels.onCommandReceived(cmd)




+++ okay decompyling chat_handlers.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.18 11:53:47 CET
