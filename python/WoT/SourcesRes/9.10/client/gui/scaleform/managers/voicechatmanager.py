# 2015.01.17 22:02:09 CET
import BigWorld
import Event
import BattleReplay
from VOIP.voip_constants import VOIP_SUPPORTED_API
from adisp import async, process
from debug_utils import LOG_WARNING
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework import AppRef, ViewTypes
from helpers import isPlayerAccount, isPlayerAvatar
from VOIP import getVOIPManager
from PlayerEvents import g_playerEvents
from gui import GUI_SETTINGS, DialogsInterface
from gui.shared.utils import CONST_CONTAINER
from gui.Scaleform.framework.entities.abstract.VoiceChatManagerMeta import VoiceChatManagerMeta
from account_helpers.settings_core.SettingsCore import g_settingsCore
from account_helpers.settings_core.settings_constants import SOUND

class VoiceChatManager(VoiceChatManagerMeta, AppRef):

    class PROVIDERS(CONST_CONTAINER):
        UNKNOWN = 'unknown'
        VIVOX = 'vivox'
        YY = 'YY'

    onPlayerSpeaking = Event.Event()
    onStateToggled = Event.Event()

    def __init__(self):
        super(VoiceChatManager, self).__init__()
        self._VoiceChatManager__failedEventRaised = False
        self._VoiceChatManager__callbacks = []
        self._VoiceChatManager__captureDevicesCallbacks = []
        self._VoiceChatManager__pendingMessage = None
        self._VoiceChatManager__enterToLobby = False



    def __initResponse(self, _):
        self._VoiceChatManager__showChatInitSuccessMessage()
        while len(self._VoiceChatManager__callbacks):
            self._VoiceChatManager__callbacks.pop(0)(self.ready)




    def __captureDevicesResponse(self):
        devices = getVOIPManager().getCaptureDevices()
        while len(self._VoiceChatManager__captureDevicesCallbacks):
            self._VoiceChatManager__captureDevicesCallbacks.pop(0)(devices)

        option = g_settingsCore.options.getSetting(SOUND.CAPTURE_DEVICES)
        option.apply(option.get())



    def __showChatInitSuccessMessage(self):
        if GUI_SETTINGS.voiceChat and not BattleReplay.isPlaying():
            if self._VoiceChatManager__failedEventRaised and self.ready:
                self._VoiceChatManager__failedEventRaised = False
                self._VoiceChatManager__pendingMessage = None
                if self._VoiceChatManager__enterToLobby:
                    self._VoiceChatManager__showDialog('voiceChatInitSucceded')



    def __showChatInitErrorMessage(self):
        if GUI_SETTINGS.voiceChat and not BattleReplay.isPlaying():
            if not self._VoiceChatManager__failedEventRaised and not self.ready:
                self._VoiceChatManager__failedEventRaised = True
                if self._VoiceChatManager__enterToLobby:
                    self._VoiceChatManager__showDialog('voiceChatInitFailed')
                else:
                    self._VoiceChatManager__pendingMessage = 'voiceChatInitFailed'



    def _populate(self):
        super(VoiceChatManager, self)._populate()
        g_playerEvents.onAccountBecomePlayer += self.onAccountBecomePlayer
        self.app.containerManager.onViewAddedToContainer += self._VoiceChatManager__onViewAddedToContainer
        voipMgr = getVOIPManager()
        voipMgr.onInitialized += self._VoiceChatManager__initResponse
        voipMgr.onFailedToConnect += self.checkForInitialization
        voipMgr.OnCaptureDevicesUpdated += self._VoiceChatManager__captureDevicesResponse
        voipMgr.onPlayerSpeaking += self._VoiceChatManager__onPlayerSpeaking
        voipMgr.onStateToggled += self._VoiceChatManager__onStateToggled



    def _dispose(self):
        self._VoiceChatManager__callbacks = None
        self._VoiceChatManager__captureDevicesCallbacks = None
        containerMgr = self.app.containerManager
        if containerMgr:
            containerMgr.onViewAddedToContainer -= self._VoiceChatManager__onViewAddedToContainer
        voipMgr = getVOIPManager()
        voipMgr.onFailedToConnect -= self.checkForInitialization
        voipMgr.onPlayerSpeaking -= self._VoiceChatManager__onPlayerSpeaking
        voipMgr.onInitialized -= self._VoiceChatManager__initResponse
        voipMgr.OnCaptureDevicesUpdated -= self._VoiceChatManager__captureDevicesResponse
        voipMgr.onStateToggled -= self._VoiceChatManager__onStateToggled
        g_playerEvents.onAccountBecomePlayer -= self.onAccountBecomePlayer
        super(VoiceChatManager, self)._dispose()



    def checkForInitialization(self, *args):
        self._VoiceChatManager__showChatInitErrorMessage()



    @property
    def state(self):
        return getVOIPManager().getState()



    @property
    def ready(self):
        return getVOIPManager().isInitialized()



    @process
    def onAccountBecomePlayer(self):
        yield self.initialize(BigWorld.player().serverSettings['voipDomain'])
        yield self.requestCaptureDevices()



    @async
    def initialize(self, domain, callback):
        if self.ready:
            callback(True)
            return 
        if domain == '':
            LOG_WARNING('Initialize. Vivox is not supported')
            return 
        self._VoiceChatManager__callbacks.append(callback)
        voipMgr = getVOIPManager()
        if not voipMgr.isNotInitialized():
            return 
        voipMgr.initialize(domain)
        voipMgr.enable(g_settingsCore.getSetting(SOUND.VOIP_ENABLE))



    @async
    def requestCaptureDevices(self, callback):
        if getVOIPManager().getVOIPDomain() == '':
            LOG_WARNING('RequestCaptureDevices. Vivox is not supported')
            callback([])
            return 
        if not self.ready:
            LOG_WARNING('RequestCaptureDevices. Vivox has not been initialized')
            callback([])
            return 
        self._VoiceChatManager__captureDevicesCallbacks.append(callback)
        getVOIPManager().requestCaptureDevices()



    def getPlayerDBID(self):
        p = BigWorld.player()
        if isPlayerAccount():
            return p.databaseID
        if isPlayerAvatar() and hasattr(p, 'playerVehicleID'):
            return p.arena.vehicles[p.playerVehicleID].get('accountDBID', None)



    def __onPlayerSpeaking(self, accountDBID, isSpeak):
        if not GUI_SETTINGS.voiceChat:
            return 
        self.onPlayerSpeaking(accountDBID, bool(isSpeak))
        self.as_onPlayerSpeakS(accountDBID, isSpeak, accountDBID == self.getPlayerDBID())



    def __onStateToggled(self, isEnabled, _):
        if not GUI_SETTINGS.voiceChat:
            return 
        self.onStateToggled(isEnabled)



    def isPlayerSpeaking(self, accountDBID):
        if GUI_SETTINGS.voiceChat:
            return bool(getVOIPManager().isParticipantTalking(accountDBID))
        return False



    def isVivox(self):
        return getVOIPManager().getAPI() == VOIP_SUPPORTED_API.VIVOX



    def isYY(self):
        return getVOIPManager().getAPI() == VOIP_SUPPORTED_API.YY



    @property
    def provider(self):
        if self.isVivox():
            return self.PROVIDERS.VIVOX
        if self.isYY():
            return self.PROVIDERS.YY
        return self.PROVIDERS.UNKNOWN



    def isVOIPEnabled(self):
        return GUI_SETTINGS.voiceChat



    def __onViewAddedToContainer(self, _, pyView):
        settings = pyView.settings
        viewType = settings.type
        if viewType == ViewTypes.DEFAULT:
            viewAlias = settings.alias
            if viewAlias == VIEW_ALIAS.LOBBY:
                self._VoiceChatManager__enterToLobby = True
                if self._VoiceChatManager__pendingMessage is not None:
                    self._VoiceChatManager__showDialog(self._VoiceChatManager__pendingMessage)
                    self._VoiceChatManager__pendingMessage = None
            else:
                self._VoiceChatManager__enterToLobby = False



    def __showDialog(self, key):
        DialogsInterface.showI18nInfoDialog(key, lambda result: None)




+++ okay decompyling voicechatmanager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.17 22:02:09 CET
