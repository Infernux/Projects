# 2015.01.14 13:32:38 CET
import account_helpers
import BigWorld
import ResMgr
import FMOD
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_DEBUG
from constants import ARENA_PERIOD
from items import _xml
from PlayerEvents import g_playerEvents
from ConnectionManager import connectionManager
from helpers import isPlayerAvatar
import SoundGroups
MUSIC_EVENT_NONE = 0
MUSIC_EVENT_LOGIN = 1
MUSIC_EVENT_LOBBY = 2
MUSIC_EVENT_COMBAT = 3
MUSIC_EVENT_COMBAT_LOADING = 4
MUSIC_EVENT_COMBAT_VICTORY = 5
MUSIC_EVENT_COMBAT_LOSE = 6
MUSIC_EVENT_COMBAT_DRAW = 7
_BATTLE_RESULT_MUSIC_EVENTS = (MUSIC_EVENT_COMBAT_VICTORY, MUSIC_EVENT_COMBAT_LOSE, MUSIC_EVENT_COMBAT_DRAW)
AMBIENT_EVENT_NONE = 1000
AMBIENT_EVENT_LOBBY = 1001
AMBIENT_EVENT_SHOP = 1002
AMBIENT_EVENT_STATISTICS = 1003
AMBIENT_EVENT_COMBAT = 1004
AMBIENT_EVENT_LOBBY_FORT = 1005
AMBIENT_EVENT_LOBBY_FORT_FINANCIAL_DEPT = 1006
AMBIENT_EVENT_LOBBY_FORT_TANKODROME = 1007
AMBIENT_EVENT_LOBBY_FORT_TRAINING_DEPT = 1008
AMBIENT_EVENT_LOBBY_FORT_MILITARY_ACADEMY = 1009
AMBIENT_EVENT_LOBBY_FORT_TRANSPORT_DEPT = 1010
AMBIENT_EVENT_LOBBY_FORT_INTENDANT_SERVICE = 1011
AMBIENT_EVENT_LOBBY_FORT_TROPHY_BRIGADE = 1012
AMBIENT_EVENT_LOBBY_FORT_OFFICE = 1013
AMBIENT_EVENT_LOBBY_FORT_MILITARY_SHOP = 1014
FORT_MAPPING = {'fort': AMBIENT_EVENT_LOBBY_FORT,
 'fort_building_financial_dept': AMBIENT_EVENT_LOBBY_FORT_FINANCIAL_DEPT,
 'fort_building_tankodrome': AMBIENT_EVENT_LOBBY_FORT_TANKODROME,
 'fort_building_training_dept': AMBIENT_EVENT_LOBBY_FORT_TRAINING_DEPT,
 'fort_building_military_academy': AMBIENT_EVENT_LOBBY_FORT_MILITARY_ACADEMY,
 'fort_building_transport_dept': AMBIENT_EVENT_LOBBY_FORT_TRANSPORT_DEPT,
 'fort_building_intendant_service': AMBIENT_EVENT_LOBBY_FORT_INTENDANT_SERVICE,
 'fort_building_trophy_brigade': AMBIENT_EVENT_LOBBY_FORT_TROPHY_BRIGADE,
 'fort_building_office': AMBIENT_EVENT_LOBBY_FORT_OFFICE,
 'fort_building_military_shop': AMBIENT_EVENT_LOBBY_FORT_MILITARY_SHOP}
_ARENA_EVENTS = (MUSIC_EVENT_COMBAT, AMBIENT_EVENT_COMBAT, MUSIC_EVENT_COMBAT_LOADING)
_CMD_SERVER_CHANGE_HANGAR_AMBIENT = 'cmd_change_hangar_ambient'
_CMD_SERVER_CHANGE_HANGAR_MUSIC = 'cmd_change_hangar_music'
_SERVER_OVERRIDDEN = 0
_CLIENT_OVERRIDDEN = 1
g_musicController = None

def init():
    global g_musicController
    g_musicController = MusicController()



class MusicController(object):

    class MusicEvent:

        def __init__(self, event = None):
            self.__muted = False
            self.__event = event
            self.__eventID = None



        def replace(self, event, eventId, playNew, stopPrev):
            if self.__event == event:
                return 
            if self.__event is not None and stopPrev is True:
                self.__event.stop()
            self.__event = event
            self.__eventID = eventId
            if playNew is True:
                self.play()



        def play(self):
            if self.__event is not None and self.__muted is False:
                self.__event.play()



        def mute(self, isMute):
            if self.__event is not None:
                if isMute != self.__muted:
                    self.__muted = isMute
                    if self.__muted:
                        self.__event.stop()
                    else:
                        self.__event.play()



        def stop(self):
            if self.__event is not None:
                self.__event.stop()



        def param(self, paramName):
            if self.__event is not None:
                return self.__event.param(paramName)



        def getEventId(self):
            return self.__eventID



        def isPlaying(self):
            return self.__event is not None and self.__event.state.find('playing') != -1



        def destroy(self):
            if self.__event is not None:
                self.__event.stop()
                self.__event = None
                self.__eventID = None



    _MUSIC_EVENT = 0
    _AMBIENT_EVENT = 1
    __lastBattleResultEventName = ''
    __lastBattleResultEventId = None

    def __init__(self):
        self._MusicController__overriddenEvents = {}
        self._MusicController__musicEvents = (MusicController.MusicEvent(), MusicController.MusicEvent())
        self._MusicController__sndEventMusic = None
        self._MusicController__soundEvents = {MUSIC_EVENT_NONE: None,
         AMBIENT_EVENT_NONE: None}
        self.init()



    def init(self):
        self._MusicController__battleResultEventWaitCb = None
        self._MusicController__isOnArena = False
        self._MusicController__isPremiumAccount = False
        self._MusicController__loadConfig()
        g_playerEvents.onEventNotificationsChanged += self._MusicController__onEventNotificationsChanged
        connectionManager.onDisconnected += self._MusicController__onDisconnected
        muteMusic = SoundGroups.g_instance.getMasterVolume() == 0 or SoundGroups.g_instance.getVolume('music') == 0
        muteAmbient = SoundGroups.g_instance.getMasterVolume() == 0 or SoundGroups.g_instance.getVolume('ambient') == 0
        self._MusicController__musicEvents[MusicController._MUSIC_EVENT].mute(muteMusic)
        self._MusicController__musicEvents[MusicController._AMBIENT_EVENT].mute(muteAmbient)
        SoundGroups.SoundGroups.onMusicVolumeChanged += self._MusicController__onVolumeChanged



    def destroy(self):
        g_playerEvents.onEventNotificationsChanged -= self._MusicController__onEventNotificationsChanged
        connectionManager.onDisconnected -= self._MusicController__onDisconnected
        SoundGroups.SoundGroups.onMusicVolumeChanged -= self._MusicController__onVolumeChanged
        self._MusicController__cancelWaitBattleResultsEventFinish()



    def __del__(self):
        self.stop()
        self._MusicController__soundEvents.clear()



    def restart(self):
        for musicEvent in self._MusicController__musicEvents:
            musicEvent.play()




    def play(self, eventId, params = None, stopPrev = True):
        if eventId is None:
            return 
        if eventId == MUSIC_EVENT_LOBBY:
            if MusicController._MusicController__lastBattleResultEventId is not None:
                eventId = MusicController._MusicController__lastBattleResultEventId
                MusicController._MusicController__lastBattleResultEventId = None
                if self._MusicController__battleResultEventWaitCb is None:
                    self._MusicController__battleResultEventWaitCb = BigWorld.callback(0.1, self._MusicController__waitBattleResultEventFinish)
        elif eventId < AMBIENT_EVENT_NONE:
            self._MusicController__cancelWaitBattleResultsEventFinish()
        newSoundEvent = self._MusicController__getEvent(eventId)
        if newSoundEvent is None:
            return 
        musicEventId = MusicController._MUSIC_EVENT if eventId < AMBIENT_EVENT_NONE else MusicController._AMBIENT_EVENT
        self._MusicController__musicEvents[musicEventId].replace(newSoundEvent, eventId, True, stopPrev)
        if params is not None:
            for (paramName, paramValue,) in params.iteritems():
                self.setEventParam(eventId, paramName, paramValue)




    def stopMusic(self):
        for musicEvent in self._MusicController__musicEvents:
            musicEvent.destroy()

        self._MusicController__cancelWaitBattleResultsEventFinish()



    def stopAmbient(self):
        ambientEvent = self._MusicController__musicEvents[MusicController._AMBIENT_EVENT]
        if ambientEvent is not None:
            ambientEvent.destroy()
        FMOD.enableLightSound(0)



    def stop(self):
        self.stopAmbient()
        self.stopMusic()



    def stopEvent(self, eventId):
        e = self._MusicController__getEvent(eventId)
        if e is not None:
            e.stop()



    def setEventParam(self, eventId, paramName, paramValue):
        e = self._MusicController__getEvent(eventId)
        if e is None:
            return 
        try:
            soundEventParam = e.param(paramName)
            if soundEventParam is not None and soundEventParam.value != paramValue:
                soundEventParam.value = paramValue
        except Exception:
            LOG_DEBUG('There is error while assigning parameter to the sound', e, paramName)
            LOG_CURRENT_EXCEPTION()



    def onEnterArena(self):
        BigWorld.player().arena.onPeriodChange += self._MusicController__onArenaStateChanged
        self._MusicController__isOnArena = True
        self._MusicController__onArenaStateChanged()
        FMOD.enableLightSound(1)



    def onLeaveArena(self):
        self._MusicController__isOnArena = False
        BigWorld.player().arena.onPeriodChange -= self._MusicController__onArenaStateChanged
        FMOD.enableLightSound(0)



    def setAccountAttrs(self, accAttrs, restart = False):
        wasPremiumAccount = self._MusicController__isPremiumAccount
        self._MusicController__isPremiumAccount = account_helpers.isPremiumAccount(accAttrs)
        musicEventId = self._MusicController__musicEvents[MusicController._MUSIC_EVENT].getEventId()
        if restart and self._MusicController__isPremiumAccount != wasPremiumAccount and musicEventId == MUSIC_EVENT_LOBBY:
            self.play(musicEventId)
            self.play(self._MusicController__musicEvents[MusicController._AMBIENT_EVENT].getEventId())



    def __getEvent(self, eventId):
        soundEvent = None
        if eventId in _ARENA_EVENTS or eventId in _BATTLE_RESULT_MUSIC_EVENTS:
            soundEvent = self._MusicController__getArenaSoundEvent(eventId)
        if soundEvent is None:
            soundEvent = self._MusicController__soundEvents.get(eventId)
            if soundEvent is not None:
                if isinstance(soundEvent, list):
                    isPremium = self._MusicController__isPremiumAccount
                    idx = 1 if isPremium and len(soundEvent) > 1 else 0
                    soundEvent = soundEvent[idx]
        return soundEvent



    def __onArenaStateChanged(self, *args):
        arena = BigWorld.player().arena
        period = arena.period
        if (period == ARENA_PERIOD.PREBATTLE or period == ARENA_PERIOD.BATTLE) and self._MusicController__isOnArena:
            self.play(AMBIENT_EVENT_COMBAT)
        if period == ARENA_PERIOD.BATTLE and self._MusicController__isOnArena:
            self.play(MUSIC_EVENT_COMBAT)
        elif period == ARENA_PERIOD.AFTERBATTLE:
            self.stopAmbient()
            MusicController._MusicController__lastBattleResultEventId = None
            MusicController._MusicController__lastBattleResultEventName = ''
            winnerTeam = arena.periodAdditionalInfo[0]
            if winnerTeam == BigWorld.player().team:
                MusicController._MusicController__lastBattleResultEventId = MUSIC_EVENT_COMBAT_VICTORY
                MusicController._MusicController__lastBattleResultEventName = arena.arenaType.battleVictoryMusic if hasattr(arena.arenaType, 'battleVictoryMusic') else ''
            elif winnerTeam == 0:
                MusicController._MusicController__lastBattleResultEventId = MUSIC_EVENT_COMBAT_DRAW
                MusicController._MusicController__lastBattleResultEventName = arena.arenaType.battleDrawMusic if hasattr(arena.arenaType, 'battleDrawMusic') else ''
            MusicController._MusicController__lastBattleResultEventId = MUSIC_EVENT_COMBAT_LOSE
            MusicController._MusicController__lastBattleResultEventName = arena.arenaType.battleLoseMusic if hasattr(arena.arenaType, 'battleLoseMusic') else ''



    def __getArenaSoundEvent(self, eventId):
        soundEvent = None
        soundEventName = None
        if eventId in _BATTLE_RESULT_MUSIC_EVENTS:
            soundEventName = MusicController._MusicController__lastBattleResultEventName
        else:
            player = BigWorld.player()
            if not isPlayerAvatar():
                return 
            if player.arena is None:
                return 
            arenaType = player.arena.arenaType
            if eventId == MUSIC_EVENT_COMBAT:
                soundEventName = arenaType.music
            elif eventId == MUSIC_EVENT_COMBAT_LOADING:
                soundEventName = arenaType.loadingMusic
            elif eventId == AMBIENT_EVENT_COMBAT:
                soundEventName = arenaType.ambientSound
        if soundEventName:
            soundEvent = SoundGroups.g_instance.FMODgetSound(soundEventName)
            if soundEvent is not None:
                soundEvent.stop()
        return soundEvent



    def __loadConfig(self):
        eventNames = {}
        xmlPath = 'gui/music_events.xml'
        section = ResMgr.openSection(xmlPath)
        if section is None:
            _xml.raiseWrongXml(None, xmlPath, 'can not open or read')
        for i in section.items():
            s = i[1]
            if i[0] == 'music':
                eventNames[MUSIC_EVENT_LOGIN] = s.readString('login')
                eventNames[MUSIC_EVENT_LOBBY] = (s.readString('lobby'), s.readString('lobby'))
                eventNames[MUSIC_EVENT_COMBAT_VICTORY] = s.readString('combat_victory')
                eventNames[MUSIC_EVENT_COMBAT_LOSE] = s.readString('combat_lose')
                eventNames[MUSIC_EVENT_COMBAT_DRAW] = s.readString('combat_draw')
            elif i[0] == 'ambient':
                eventNames[AMBIENT_EVENT_LOBBY] = (s.readString('lobby'), s.readString('lobby'))
                eventNames[AMBIENT_EVENT_SHOP] = (s.readString('shop'), s.readString('lobby'))
                eventNames[AMBIENT_EVENT_STATISTICS] = (s.readString('rating'), s.readString('lobby'))
                for (key, const,) in FORT_MAPPING.iteritems():
                    eventNames[const] = (s.readString(key), s.readString(key))


        fallbackEventNames = eventNames.copy()
        self._MusicController__overrideEvents(eventNames)
        soundsByName = {}
        for (eventId, names,) in eventNames.items():
            lstEvents = []
            if not isinstance(names, tuple):
                names = (names,)
            fallbackNames = fallbackEventNames[eventId]
            if not isinstance(fallbackNames, tuple):
                fallbackNames = (fallbackNames,)
            for i in xrange(len(names)):
                eventName = names[i]
                fallbackEventName = fallbackNames[i]
                sound = soundsByName.get(eventName)
                if sound is None:
                    sound = SoundGroups.g_instance.FMODgetSound(eventName) if eventName != '' else None
                    if sound is None:
                        sound = SoundGroups.g_instance.FMODgetSound(fallbackEventName) if fallbackEventName != '' else None
                soundsByName[eventName] = sound
                lstEvents.append(sound)
                if sound is not None:
                    sound.stop()

            self._MusicController__soundEvents[eventId] = lstEvents

        for musicEvent in self._MusicController__musicEvents:
            self.play(musicEvent.getEventId())




    def __overrideEvents(self, eventNames):
        for (eventId, overriddenNames,) in self._MusicController__overriddenEvents.iteritems():
            if overriddenNames:
                if overriddenNames[_SERVER_OVERRIDDEN]:
                    eventNames[eventId] = overriddenNames[_SERVER_OVERRIDDEN]
                elif overriddenNames[_CLIENT_OVERRIDDEN]:
                    eventNames[eventId] = overriddenNames[_CLIENT_OVERRIDDEN]




    def __waitBattleResultEventFinish(self):
        self._MusicController__battleResultEventWaitCb = None
        musicEvent = self._MusicController__musicEvents[MusicController._MUSIC_EVENT]
        musicEventId = musicEvent.getEventId()
        if musicEventId not in _BATTLE_RESULT_MUSIC_EVENTS:
            return 
        if not musicEvent.isPlaying():
            self.play(MUSIC_EVENT_LOBBY)
            return 
        self._MusicController__battleResultEventWaitCb = BigWorld.callback(0.1, self._MusicController__waitBattleResultEventFinish)



    def __cancelWaitBattleResultsEventFinish(self):
        if self._MusicController__battleResultEventWaitCb is not None:
            BigWorld.cancelCallback(self._MusicController__battleResultEventWaitCb)
            self._MusicController__battleResultEventWaitCb = None



    def __reloadSounds(self):
        self._MusicController__loadConfig()



    def __onEventNotificationsChanged(self, notificationsDiff):
        hasChanges = False
        for notification in notificationsDiff['removed']:
            if notification['type'] == _CMD_SERVER_CHANGE_HANGAR_AMBIENT:
                self._MusicController__updateOverridden(AMBIENT_EVENT_LOBBY, _SERVER_OVERRIDDEN, None)
                self._MusicController__updateOverridden(AMBIENT_EVENT_SHOP, _SERVER_OVERRIDDEN, None)
                self._MusicController__updateOverridden(AMBIENT_EVENT_STATISTICS, _SERVER_OVERRIDDEN, None)
                hasChanges = True
            elif notification['type'] == _CMD_SERVER_CHANGE_HANGAR_MUSIC:
                self._MusicController__updateOverridden(MUSIC_EVENT_LOBBY, _SERVER_OVERRIDDEN, None)
                hasChanges = True

        for notification in notificationsDiff['added']:
            if notification['type'] == _CMD_SERVER_CHANGE_HANGAR_AMBIENT:
                ambientEventName = notification['data']
                self._MusicController__updateOverridden(AMBIENT_EVENT_LOBBY, _SERVER_OVERRIDDEN, (ambientEventName, ambientEventName))
                self._MusicController__updateOverridden(AMBIENT_EVENT_SHOP, _SERVER_OVERRIDDEN, (ambientEventName, ambientEventName))
                self._MusicController__updateOverridden(AMBIENT_EVENT_STATISTICS, _SERVER_OVERRIDDEN, (ambientEventName, ambientEventName))
                hasChanges = True
            elif notification['type'] == _CMD_SERVER_CHANGE_HANGAR_MUSIC:
                musicEventNames = [ event.strip() for event in notification['data'].split('|') ]
                musicEventName = musicEventNames[0]
                premiumMusicEventName = musicEventNames[1] if len(musicEventNames) > 1 else musicEventName
                self._MusicController__updateOverridden(MUSIC_EVENT_LOBBY, _SERVER_OVERRIDDEN, (musicEventName, premiumMusicEventName))
                hasChanges = True

        if hasChanges:
            self._MusicController__reloadSounds()



    def __onVolumeChanged(self, categoryName, masterVolume, musicVolume):
        muted = masterVolume == 0 or musicVolume == 0
        if categoryName == 'music':
            self._MusicController__musicEvents[MusicController._MUSIC_EVENT].mute(muted)
        elif categoryName == 'ambient':
            self._MusicController__musicEvents[MusicController._AMBIENT_EVENT].mute(muted)



    def __onDisconnected(self):
        self._MusicController__eraseOverridden(_SERVER_OVERRIDDEN)
        self._MusicController__loadConfig()



    def changeHangarSound(self, notificationsDiff):
        self._MusicController__onEventNotificationsChanged(notificationsDiff)



    def loadCustomSounds(self, spacePath):
        xmlName = spacePath.split('/')[-1]
        settings = ResMgr.openSection('scripts/arena_defs/' + xmlName + '.xml')
        if settings is None:
            return 
        hasChanges = False
        music_name = settings.readString('music')
        ambient_name = settings.readString('ambientSound')
        if music_name:
            self._MusicController__updateOverridden(MUSIC_EVENT_LOBBY, _CLIENT_OVERRIDDEN, (music_name, music_name))
            hasChanges = True
        if ambient_name:
            self._MusicController__updateOverridden(AMBIENT_EVENT_LOBBY, _CLIENT_OVERRIDDEN, (ambient_name, ambient_name))
            self._MusicController__updateOverridden(AMBIENT_EVENT_SHOP, _CLIENT_OVERRIDDEN, (ambient_name, ambient_name))
            self._MusicController__updateOverridden(AMBIENT_EVENT_STATISTICS, _CLIENT_OVERRIDDEN, (ambient_name, ambient_name))
            hasChanges = True
        if hasChanges:
            self._MusicController__reloadSounds()



    def __updateOverridden(self, eventID, typeId, value):
        music_list = self._MusicController__overriddenEvents.setdefault(eventID, [None, None])
        music_list[typeId] = value



    def unloadCustomSounds(self):
        self._MusicController__eraseOverridden(_CLIENT_OVERRIDDEN)
        self._MusicController__reloadSounds()



    def __eraseOverridden(self, index):
        for (eventId, overriddenNames,) in self._MusicController__overriddenEvents.iteritems():
            self._MusicController__overriddenEvents[eventId][index] = None





+++ okay decompyling musiccontroller.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:32:38 CET
