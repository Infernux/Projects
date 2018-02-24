# 2015.01.14 13:32:32 CET
from chat_shared import CHAT_ACTIONS, CHAT_CHANNEL_BATTLE, CHAT_CHANNEL_BATTLE_TEAM
import Event
from Singleton import Singleton

class ChatManager(Singleton):

    @staticmethod
    def instance():
        return ChatManager()



    def _singleton_init(self):
        self.battleTeamChannelID = 0
        self.battleCommonChannelID = 0
        self.playerProxy = None
        self.__chatActionCallbacks = {}



    def subscribeChatAction(self, callback, action, channelId = None):
        cbs = self.__getChatActionCallbacks(action, channelId)
        cbs += callback



    def unsubscribeChatAction(self, callback, action, channelId = None):
        cbs = self.__getChatActionCallbacks(action, channelId)
        cbs -= callback



    def unsubcribeAllChatActions(self):
        for handlers in self.__chatActionCallbacks.values():
            handlers.clear()




    def __getChatActionCallbacks(self, action, channelId):
        channelId = channelId if channelId is not None else 0
        key = (action, channelId)
        if key not in self.__chatActionCallbacks:
            handlers = self.__chatActionCallbacks[key] = Event.Event()
        else:
            handlers = self.__chatActionCallbacks[key]
        return handlers



    def switchPlayerProxy(self, proxy):
        self.__cleanupMyCallbacks()
        self.__setProxyChatActionsCallbacks({})
        self.playerProxy = proxy
        self.__setProxyChatActionsCallbacks(self.__chatActionCallbacks)
        self.__setupMyCallbacks()



    def __setProxyChatActionsCallbacks(self, callbacks):
        if self.playerProxy is not None:
            self.playerProxy.setChatActionsCallbacks(callbacks)



    def __cleanupMyCallbacks(self):
        if self.playerProxy is not None:
            self.battleTeamChannelID = 0
            self.battleCommonChannelID = 0
            self.playerProxy.unsubscribeChatAction(self.__onChannelsListReceived, CHAT_ACTIONS.requestChannels)



    def __setupMyCallbacks(self):
        if self.playerProxy is not None:
            self.playerProxy.subscribeChatAction(self.__onChannelsListReceived, CHAT_ACTIONS.requestChannels)



    def __onChannelsListReceived(self, chatActionData):
        for chInfo in chatActionData['data']:
            flags = chInfo.get('flags', 0)
            if flags & CHAT_CHANNEL_BATTLE == CHAT_CHANNEL_BATTLE:
                if flags & CHAT_CHANNEL_BATTLE_TEAM == CHAT_CHANNEL_BATTLE_TEAM:
                    self.battleTeamChannelID = chInfo.get('id', 0)
                else:
                    self.battleCommonChannelID = chInfo.get('id', 0)




chatManager = ChatManager.instance()

+++ okay decompyling chatmanager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:32:33 CET
