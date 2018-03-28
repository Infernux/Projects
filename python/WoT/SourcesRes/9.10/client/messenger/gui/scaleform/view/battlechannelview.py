# 2015.01.14 23:18:55 CET
import weakref
from gui import makeHtmlString
from gui.Scaleform.CommandArgsParser import CommandArgsParser
from gui.Scaleform.windows import UIInterface
from messenger import g_settings
from messenger.gui.Scaleform import BTMS_COMMANDS
from messenger.gui.interfaces import IBattleChannelView
from messenger.m_constants import BATTLE_CHANNEL

class BattleChannelView(UIInterface, IBattleChannelView):
    _lastReceiver = BATTLE_CHANNEL.TEAM.name

    def __init__(self, sharedHistory):
        super(BattleChannelView, self).__init__()
        self.__controllers = {}
        self.__sharedHistory = weakref.ref(sharedHistory)



    def populateUI(self, proxy):
        super(BattleChannelView, self).populateUI(proxy)
        self.uiHolder.addExternalCallbacks({BTMS_COMMANDS.CheckCooldownPeriod(): self.__onCheckCooldownPeriod,
         BTMS_COMMANDS.SendMessage(): self.__onSendChannelMessage,
         BTMS_COMMANDS.ReceiverChanged(): self.__onReceiverChanged})



    def dispossessUI(self):
        if self.uiHolder:
            self.uiHolder.removeExternalCallback(BTMS_COMMANDS.CheckCooldownPeriod(), self.__onCheckCooldownPeriod)
            self.uiHolder.removeExternalCallback(BTMS_COMMANDS.SendMessage(), self.__onSendChannelMessage)
            self.uiHolder.removeExternalCallback(BTMS_COMMANDS.ReceiverChanged(), self.__onReceiverChanged)
        super(BattleChannelView, self).dispossessUI()
        self.__controllers.clear()
        self.__sharedHistory = lambda : None



    @classmethod
    def resetReceiver(cls):
        if not g_settings.userPrefs.storeReceiverInBattle:
            cls._lastReceiver = BATTLE_CHANNEL.TEAM[1]



    def addController(self, controller):
        channel = controller.getChannel()
        clientID = channel.getClientID()
        self.__controllers[clientID] = weakref.ref(controller)
        if channel.isJoined():
            self.__setReceiverToView(clientID, controller)



    def removeController(self, controller):
        self.__controllers.pop(controller.getChannel().getClientID(), None)



    def updateReceiversData(self):
        for (clientID, ctrlRef,) in self.__controllers.iteritems():
            controller = ctrlRef()
            if controller and controller.getChannel().isJoined():
                self.__setReceiverToView(clientID, controller)




    def updateReceiversLabels(self):
        result = []
        for (clientID, ctrlRef,) in self.__controllers.iteritems():
            controller = ctrlRef()
            if controller:
                result.append(clientID)
                result.append(self.__getRecvConfig(controller)[0])

        if len(result):
            self.__flashCall(BTMS_COMMANDS.UpdateReceivers(), result)



    def addMessage(self, message, isCurrentPlayer = False):
        history = self.__sharedHistory()
        if history:
            history.addMessage(message, isCurrentPlayer)
        self.__flashCall(BTMS_COMMANDS.ReceiveMessage(), [0, message, isCurrentPlayer])



    def __getRecvConfig(self, controller):
        config = ['', 0, False]
        receivers = g_settings.battle.receivers
        isChatEnabled = controller.isEnabled()
        receiverName = controller.getSettings().name
        if receiverName in receivers:
            getter = g_settings.getColorScheme
            color = getter('battle/receiver').getHexStr(receiverName)
            inputColor = getter('battle/message').getHexStr(receiverName)
            receiver = receivers[receiverName]._asdict()
            byDefault = False
            if g_settings.userPrefs.storeReceiverInBattle:
                byDefault = receiverName == BattleChannelView._lastReceiver
            if isChatEnabled:
                recLabel = receiver['label'] % color
            else:
                recLabel = makeHtmlString('html_templates:battle', 'battleChatIsLocked', {})
            config = [recLabel,
             receiver['order'],
             byDefault,
             inputColor,
             isChatEnabled]
            config.extend(receiver['modifiers'])
        return config



    def __setReceiverToView(self, clientID, controller):
        result = self.__getRecvConfig(controller)
        result.insert(0, clientID)
        self.__flashCall(BTMS_COMMANDS.JoinToChannel(), result)



    def __getController(self, clientID):
        controller = None
        if clientID in self.__controllers:
            ctrlRef = self.__controllers[clientID]
            if ctrlRef:
                controller = ctrlRef()
        return controller



    def __flashCall(self, funcName, args = None):
        if self.uiHolder:
            self.uiHolder.call(funcName, args)



    def __flashRespond(self, args = None):
        self.uiHolder.respond(args)



    def __onReceiverChanged(self, *args):
        parser = CommandArgsParser(self.__onReceiverChanged.__name__, 1, [long])
        (clientID,) = parser.parse(*args)
        controller = self.__getController(clientID)
        if controller:
            BattleChannelView._lastReceiver = controller.getSettings().name



    def __onCheckCooldownPeriod(self, *args):
        parser = CommandArgsParser(self.__onCheckCooldownPeriod.__name__, 1, [long])
        (clientID,) = parser.parse(*args)
        controller = self.__getController(clientID)
        if not controller:
            return 
        (result, errorMsg,) = controller.canSendMessage()
        parser.addArgs([clientID, result])
        self.__flashRespond(parser.args())
        if not result:
            message = g_settings.htmlTemplates.format('battleErrorMessage', ctx={'error': errorMsg})
            history = self.__sharedHistory()
            if history:
                history.addMessage(message, False)
            self.__flashCall(BTMS_COMMANDS.ReceiveMessage(), [clientID, message, False])



    def __onSendChannelMessage(self, *args):
        parser = CommandArgsParser(self.__onSendChannelMessage.__name__, 2, [long])
        (clientID, rawMsgText,) = parser.parse(*args)
        controller = self.__getController(clientID)
        if controller:
            controller.sendMessage(rawMsgText)




+++ okay decompyling battlechannelview.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 23:18:55 CET
