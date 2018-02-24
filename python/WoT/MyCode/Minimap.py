import BigWorld
import Math
import ResMgr
from Math import Matrix, Vector3
import Keys
from messenger import MessengerEntry
from AvatarInputHandler import mathUtils
from gui.battle_control import g_sessionProvider
import GUI
from CTFManager import g_ctfManager
from constants import REPAIR_POINT_ACTION, RESOURCE_POINT_STATE, FLAG_STATE
from gui.battle_control.avatar_getter import getPlayerVehicleID
from gui.battle_control.dyn_squad_arena_controllers import IDynSquadEntityClient
from ids_generators import SequenceIDGenerator
from shared_utils import findFirst
from gui.battle_control.battle_constants import PLAYER_ENTITY_NAME, FEEDBACK_EVENT_ID, NEUTRAL_TEAM
from gui.battle_control.arena_info import isLowLevelBattle, hasFlags, hasRepairPoints, hasResourcePoints
from gui.shared.utils.sound import Sound
from gui.shared.gui_items import Vehicle
from gui import GUI_SETTINGS, g_repeatKeyHandlers, makeHtmlString
from functools import partial
from weakref import proxy
from helpers.gui_utils import *
from debug_utils import *
import string
import CommandMapping
import xml.dom.minidom
import ResMgr
import math
import re
from items.vehicles import VEHICLE_CLASS_TAGS
from account_helpers.AccountSettings import AccountSettings
from gui.battle_control import vehicle_getter
from gui.battle_control import arena_info
CURSOR_NORMAL = 'cursorNormal'
CURSOR_NORMAL_WITH_DIRECTION = 'cursorNormalWithDirection'
CURSOR_STRATEGIC = 'cursorStrategic'
CAMERA_NORMAL = 'cameraNormal'
CAMERA_VIDEO = 'cameraVideo'
CAMERA_STRATEGIC = 'cameraStrategic'
MARKER = 'marker'
MODE_VIDEO = 'video'
MODE_POSTMORTEM = 'postmortem'
MODE_SNIPER = 'sniper'
MODE_ARCADE = 'arcade'
MODE_STRATEGIC = 'strategic'
MODE_BATTLE_CONSUME = 'mapcase'

def _isStrategic(ctrlMode):
    return ctrlMode in (MODE_STRATEGIC, MODE_BATTLE_CONSUME)



class VehicleLocation():
    AOI = 0
    FAR = 1
    AOI_TO_FAR = 2


class MARKER_TYPE():
    CONSUMABLE = 'fortConsumables'
    FLAG = 'flags'
    RESOURCE_POINT = 'resourcePoints'


class FLAG_TYPE():
    ALLY = 'ally'
    ENEMY = 'enemy'
    NEUTRAL = 'neutral'
    ALLY_CAPTURE = 'allyCapture'
    ENEMY_CAPTURE = 'enemyCapture'
    ALLY_CAPTURE_ANIMATION = 'allyCaptureAnimation'
    COOLDOWN = 'cooldown'


class RESOURCE_POINT_TYPE():
    CONFLICT = 'conflict'
    COOLDOWN = 'cooldown'
    READY = 'ready'
    OWN_MINING = 'ownMining'
    ENEMY_MINING = 'enemyMining'

_CAPTURE_STATE_BY_TEAMS = {True: RESOURCE_POINT_TYPE.OWN_MINING,
 False: RESOURCE_POINT_TYPE.ENEMY_MINING}
_CAPTURE_FROZEN_STATE_BY_TEAMS = {True: RESOURCE_POINT_TYPE.OWN_MINING,
 False: RESOURCE_POINT_TYPE.ENEMY_MINING}

class Minimap(IDynSquadEntityClient):
    __MINIMAP_SIZE = (210, 210)
    __MINIMAP_CELLS = (10, 10)
    __AOI_ESTIMATE = 450.0
    __AOI_TO_FAR_TIME = 5.0
    __yawLimits = (0, 0)
    BigWorld.minimapIsInstantied = False
    try:
        xmlfile = xml.dom.minidom.parse('res_mods/Mmap.xml')
        __msize = xmlfile.getElementsByTagName('bigmapsize')[0].childNodes[0].nodeValue
        __keyc = xmlfile.getElementsByTagName('keycode')[0].childNodes[0].nodeValue
        __mrkscale = xmlfile.getElementsByTagName('markerscale')[0].childNodes[0].nodeValue
        __fontsize = xmlfile.getElementsByTagName('fontsize')[0].childNodes[0].nodeValue
        __shownames = xmlfile.getElementsByTagName('shownames')[0].childNodes[0].nodeValue
        __calph = xmlfile.getElementsByTagName('circlealpha')[0].childNodes[0].nodeValue
        __ccolor = xmlfile.getElementsByTagName('circlecolor')[0].childNodes[0].nodeValue
        __lalph = xmlfile.getElementsByTagName('laseralpha')[0].childNodes[0].nodeValue
        __lcolor = xmlfile.getElementsByTagName('lasercolor')[0].childNodes[0].nodeValue
        __acolor = xmlfile.getElementsByTagName('allytextcolor')[0].childNodes[0].nodeValue
        __ecolor = xmlfile.getElementsByTagName('enemytextcolor')[0].childNodes[0].nodeValue
        __scolor = xmlfile.getElementsByTagName('squadtextcolor')[0].childNodes[0].nodeValue
        __shadstr = xmlfile.getElementsByTagName('textshadow')[0].childNodes[0].nodeValue
        __mapname = 'Mapname'
        __anametag = xmlfile.getElementsByTagName('allynamecontent')[0].childNodes[0].nodeValue
        __enametag = xmlfile.getElementsByTagName('enemynamecontent')[0].childNodes[0].nodeValue
        __snametag = xmlfile.getElementsByTagName('squadnamecontent')[0].childNodes[0].nodeValue
        __fifalph = xmlfile.getElementsByTagName('fiftymalpha')[0].childNodes[0].nodeValue
        __fifcolor = xmlfile.getElementsByTagName('fiftymcolor')[0].childNodes[0].nodeValue
        __dcolor = xmlfile.getElementsByTagName('drawboxcolor')[0].childNodes[0].nodeValue
        __dalph = xmlfile.getElementsByTagName('drawboxalpha')[0].childNodes[0].nodeValue
        __dstyle = xmlfile.getElementsByTagName('drawboxstyle')[0].childNodes[0].nodeValue
        __cstyle = xmlfile.getElementsByTagName('circlestyle')[0].childNodes[0].nodeValue
        __lstyle = xmlfile.getElementsByTagName('laserstyle')[0].childNodes[0].nodeValue
        __xshift = xmlfile.getElementsByTagName('bigmapx')[0].childNodes[0].nodeValue
        __yshift = xmlfile.getElementsByTagName('bigmapy')[0].childNodes[0].nodeValue
        __csize = xmlfile.getElementsByTagName('circlesize')[0].childNodes[0].nodeValue
        __acsize = '3000'
        __hlalph = xmlfile.getElementsByTagName('hlaseralpha')[0].childNodes[0].nodeValue
        __hlstyle = xmlfile.getElementsByTagName('hlaserstyle')[0].childNodes[0].nodeValue
        __hlcolor = xmlfile.getElementsByTagName('hlasercolor')[0].childNodes[0].nodeValue
        __acalph = xmlfile.getElementsByTagName('artycirclealpha')[0].childNodes[0].nodeValue
        __acstyle = xmlfile.getElementsByTagName('artycirclestyle')[0].childNodes[0].nodeValue
        __accolor = xmlfile.getElementsByTagName('artycirclecolor')[0].childNodes[0].nodeValue
        __belem = xmlfile.getElementsByTagName('bigmapelements')[0].childNodes[0].nodeValue
        __selem = xmlfile.getElementsByTagName('smallmapelements')[0].childNodes[0].nodeValue
        __artcurcol = xmlfile.getElementsByTagName('artycursorcolor')[0].childNodes[0].nodeValue
        __skulls = True if xmlfile.getElementsByTagName('skullmarkers')[0].childNodes[0].nodeValue == 'true' else False
        __lostmark = xmlfile.getElementsByTagName('marklastpos')[0].childNodes[0].nodeValue
        __lostalph = xmlfile.getElementsByTagName('lastposalpha')[0].childNodes[0].nodeValue
        __lostcol = xmlfile.getElementsByTagName('lastposcolor')[0].childNodes[0].nodeValue
        __shownewicons = xmlfile.getElementsByTagName('showMinimapSuperHeavy')[0].childNodes[0].nodeValue
        __sshiftx = xmlfile.getElementsByTagName('smallmapx')[0].childNodes[0].nodeValue
        __sshifty = xmlfile.getElementsByTagName('smallmapy')[0].childNodes[0].nodeValue
        __cucirsize = xmlfile.getElementsByTagName('customcirclesize')[0].childNodes[0].nodeValue
        __cucirstyle = xmlfile.getElementsByTagName('customcirclestyle')[0].childNodes[0].nodeValue
        __cucircolor = xmlfile.getElementsByTagName('customcirclecolor')[0].childNodes[0].nodeValue
        __cuciralpha = xmlfile.getElementsByTagName('customcirclealpha')[0].childNodes[0].nodeValue
        __binocs = xmlfile.getElementsByTagName('binocircle')[0].childNodes[0].nodeValue
        __binalpha = xmlfile.getElementsByTagName('binocirclealpha')[0].childNodes[0].nodeValue
        __binstyle = xmlfile.getElementsByTagName('binocirclestyle')[0].childNodes[0].nodeValue
        __bincolor = xmlfile.getElementsByTagName('binocirclecolor')[0].childNodes[0].nodeValue
        __vrtenabled = True if xmlfile.getElementsByTagName('vrtextenabled')[0].childNodes[0].nodeValue == 'true' else False
        __vrtcolor = xmlfile.getElementsByTagName('vrtextcolor')[0].childNodes[0].nodeValue
        __vrtpos = [ float(v) for v in xmlfile.getElementsByTagName('vrtextposition')[0].childNodes[0].nodeValue.split(':') ]
        __vrtfont = xmlfile.getElementsByTagName('vrtextfont')[0].childNodes[0].nodeValue
        __shorten = False if xmlfile.getElementsByTagName('shortenplayernames')[0].childNodes[0].nodeValue == 'false' else int(xmlfile.getElementsByTagName('shortenplayernames')[0].childNodes[0].nodeValue)
        __teamgame = [ int(v) for v in xmlfile.getElementsByTagName('teamgames')[0].childNodes[0].nodeValue.split(':') ]
        __tview = 0
    except Exception as e:
        LOG_CURRENT_EXCEPTION()
        LOG_ERROR('Mmap.xml Problem! File not found or invalid. Using defaults.')
        __msize = 800
        __keyc = 'KEY_LSHIFT'
        __mrkscale = 1
        __fontsize = 6
        __shownames = 'true'
        __calph = 100
        __ccolor = 0
        __lalph = 100
        __lcolor = 0
        __acolor = 10483585
        __ecolor = 16220545
        __scolor = 16685614
        __shadstr = 15
        __mapname = 'Mapname'
        __anametag = 'ERROR'
        __enametag = 'ERROR'
        __snametag = 'ERROR'
        __fifalph = 20
        __fifcolor = 0
        __dcolor = 16711680
        __dalph = 50
        __dstyle = 'line'
        __cstyle = 'dashed'
        __lstyle = 'line'
        __xshift = 0
        __yshift = 0
        __csize = 'viewrange'
        __acsize = '3000'
        __hlalph = 50
        __hlstyle = 'line'
        __hlcolor = 16777215
        __acalph = 100
        __acstyle = 'line'
        __accolor = 5308240
        __belem = 'show:circle,fiftymcircle,drawbox,artycircle,sqlegend,hulllaser,gunconstraints'
        __selem = 'show:circle,fiftymcircle,drawbox,artycircle,sqlegend,hulllaser,gunconstraints'
        __artcurcol = 4259584
        __skulls = True
        __lostmark = 'true'
        __lostalph = 50
        __lostcol = 16777215
        __shownewicons = 'true'
        __sshiftx = 0
        __sshifty = 0
        __cucirsize = 445
        __cucirstyle = 'line'
        __cucircolor = 16711680
        __cuciralpha = 100
        __binocs = 'replace'
        __binalpha = 100
        __binstyle = 'line'
        __bincolor = 16711680
        __vrtenabled = True
        __vrtcolor = '#FF8000'
        __vrtpos = (0.23, -0.86, 1)
        __vrtfont = 'system_tiny.font'
        __shorten = False
        __teamgame = [3,
         4,
         5,
         7,
         10]
        __tview = 0

    def parseHotkeys(hotkeyString):
        return filter(lambda keycode: keycode > 0, map(lambda code: getattr(Keys, code, 0), hotkeyString.split('+')))


    __KEY_ZOOM = parseHotkeys(__keyc)

    @staticmethod
    def binocs(self, isOn):
        from gui.WindowsManager import g_windowsManager
        if self.__ownEntry.has_key('handle'):
            g_windowsManager._WindowsManager__battleWindow._Battle__minimap.__ownUI.entryInvoke(g_windowsManager._WindowsManager__battleWindow._Battle__minimap.__ownEntry['handle'], ('binoculars', [isOn]))



    def __hook(self):
        import game
        from gui.Scaleform import Battle
        from gui.battle_control import g_sessionProvider
        optDevicesCtrl = g_sessionProvider.getOptDevicesCtrl()
        optDevicesCtrl.onOptionalDeviceAdded += self.newaddOptionalDevice
        optDevicesCtrl.onOptionalDeviceUpdated += self.newsetOptionalDeviceState
        if BigWorld.minimapIsInstantied != True:
            BigWorld.handleKeyBkup = game.handleKeyEvent
            game.handleKeyEvent = self.hkKeyEvent
        if Minimap.__vrtenabled:
            BPA = BigWorld.player().arena
            BPA.viewtext = GUI.Text('')
            BPA.viewtext.visible = True
            BPA.viewtext.font = Minimap.__vrtfont
            BPA.viewtext.colourFormatting = True
            BPA.viewtext.position = (Minimap.__vrtpos[0], Minimap.__vrtpos[1], Minimap.__vrtpos[2])
            GUI.addRoot(BPA.viewtext)
        self.__pressedKeys = []



    def newaddOptionalDevice(self, intCD, descriptor, isOn):
        if descriptor.name == 'stereoscope':
            Minimap.binocs(self, isOn)
            BigWorld.player().arena.binoOn = isOn



    def newsetOptionalDeviceState(self, intCD, isOn):
        try:
            from items.vehicles import g_cache
            if g_cache.optionalDevices()[4] in BigWorld.entities[BigWorld.player().playerVehicleID].typeDescriptor.optionalDevices:
                Minimap.binocs(self, isOn)
                BigWorld.player().arena.binoOn = isOn
                if Minimap.__csize != 'viewrange':
                    BPA = BigWorld.player().arena
                    if str(Minimap.__tview) != '0':
                        Theory = float(Minimap.__tview) * 1.25
                    else:
                        Theory = float(Minimap.__csize) * 1.25
                    if Minimap.__vrtenabled:
                        color = Minimap.__vrtcolor
                        color = '\\c' + re.sub('[^A-Za-z0-9]+', '', color) + 'FF;'
                        BPA.viewtext.text = color + '%s %.1fm / %s %.1fm' % ('V:',
                         float(Minimap.__csize),
                         'T:',
                         float(Theory))
                if isOn == 1 and BigWorld.player().arena.binoOn != 1:
                    Minimap.binocs(self, isOn)
                    BigWorld.player().arena.binoOn = 1
                elif isOn == 0 and BigWorld.player().arena.binoOn == 1:
                    Minimap.binocs(self, isOn)
                    BigWorld.player().arena.binoOn = 0
        except Exception as e:
            LOG_CURRENT_EXCEPTION()



    def hkKeyEvent(self, event):
        try:
            from gui.WindowsManager import g_windowsManager
            import CommandMapping
            cmdMap = CommandMapping.g_instance
            if hasattr(BigWorld.player(), 'playerVehicleID') and hasattr(g_windowsManager._WindowsManager__battleWindow, '_Battle__minimap'):
                import game
                (isDown, key, mods, isRepeat,) = game.convertKeyEvent(event)
                if hasattr(BigWorld.player(), 'arena'):
                    if Minimap.__vrtenabled:
                        BPA = BigWorld.player().arena
                        if cmdMap.isFired(CommandMapping.CMD_TOGGLE_GUI, key) and isDown:
                            BPA.viewtext.visible = not BPA.viewtext.visible
                if not isRepeat and key in Minimap.__KEY_ZOOM:
                    if isDown:
                        self.__pressedKeys.append(key)
                        if self.__ownEntry.has_key('handle'):
                            g_windowsManager._WindowsManager__battleWindow._Battle__minimap.__ownUI.entryInvoke(g_windowsManager._WindowsManager__battleWindow._Battle__minimap.__ownEntry['handle'], ('zoom', [True]))
                    else:
                        if key in self.__pressedKeys:
                            self.__pressedKeys.remove(key)
                            if self.__ownEntry.has_key('handle'):
                                g_windowsManager._WindowsManager__battleWindow._Battle__minimap.__ownUI.entryInvoke(g_windowsManager._WindowsManager__battleWindow._Battle__minimap.__ownEntry['handle'], ('zoom', [False]))
                        else:
                            LOG_ERROR('ERROR! keycode %s NOT in Minimap.__pressedKeys' % key)
                        return 
        except Exception as e:
            LOG_CURRENT_EXCEPTION()
        finally:
            return BigWorld.handleKeyBkup(event)



    def __init__(self, parentUI):
        self.proxy = proxy(self)
        self.__cfg = dict()
        self.__hook()
        BigWorld.minimapIsInstantied = True
        player = BigWorld.player()
        arena = player.arena
        arenaType = arena.arenaType
        Minimap.__battletype = ('fallout' if arena_info.isEventBattle() else 'normal',)
        Minimap.__mapname = arenaType.minimap
        try:
            Minimap.__csize = Minimap.xmlfile.getElementsByTagName('circlesize')[0].childNodes[0].nodeValue
        except:
            Minimap.__csize = 'viewrange'
        if Minimap.__csize == 'viewrange':
            try:
                viewcache = xml.dom.minidom.parse('res_mods/viewrange.xml')
                tankname = viewcache.getElementsByTagName('tankname')[0].childNodes[0].nodeValue
                if tankname == BigWorld.player().vehicleTypeDescriptor.type.name.split(':')[1].lower().replace('-', '_'):
                    Minimap.__csize = viewcache.getElementsByTagName('view')[0].childNodes[0].nodeValue
                    Minimap.__tview = viewcache.getElementsByTagName('theoryview')[0].childNodes[0].nodeValue
                else:
                    Minimap.__csize = min(445, math.floor(BigWorld.player().vehicleTypeDescriptor.turret['circularVisionRadius'] * (math.ceil(BigWorld.player().vehicleTypeDescriptor.miscAttrs['circularVisionRadiusFactor'] * 100) / 100)))
                    Minimap.__tview = '0'
            except:
                Minimap.__csize = math.floor(BigWorld.player().vehicleTypeDescriptor.turret['circularVisionRadius'] * (math.ceil(BigWorld.player().vehicleTypeDescriptor.miscAttrs['circularVisionRadiusFactor'] * 100) / 100))
                LOG_NOTE('Viewrange.xml error. Using old method.')
        if 'SPG' in player.vehicleTypeDescriptor.type.tags:
            Minimap.__acsize = math.ceil(BigWorld.player().vehicleTypeDescriptor.shot['speed'] * BigWorld.player().vehicleTypeDescriptor.shot['speed'] / BigWorld.player().vehicleTypeDescriptor.shot['gravity'])
        else:
            Minimap.__acsize = 3000
        self.__cfg['texture'] = arenaType.minimap
        self.__cfg['teamBasePositions'] = arenaType.teamBasePositions
        if isLowLevelBattle() and player.team - 1 in arenaType.teamLowLevelSpawnPoints and len(arenaType.teamLowLevelSpawnPoints[(player.team - 1)]):
            self.__cfg['teamSpawnPoints'] = arenaType.teamLowLevelSpawnPoints
        else:
            self.__cfg['teamSpawnPoints'] = arenaType.teamSpawnPoints
        self.__cfg['controlPoints'] = arenaType.controlPoints
        self.__cfg['repairPoints'] = []
        if hasFlags():
            self.__cfg['flagAbsorptionPoints'] = arenaType.flagAbsorptionPoints
            self.__cfg['flagSpawnPoints'] = arenaType.flagSpawnPoints
        if hasRepairPoints():
            self.__cfg['repairPoints'] = arenaType.repairPoints
        self.__points = {'base': {},
         'spawn': {}}
        self.__backMarkers = {}
        self.__entries = {}
        self.__enemyEntries = {}
        self.__entrieLits = {}
        self.__entrieMarkers = {}
        self.__vehicleIDToFlagUniqueID = {}
        self.__main = None
        self.__vehiclesWaitStart = []
        self.__isStarted = False
        self.__parentUI = parentUI
        self.__ownUI = None
        self.__ownEntry = dict()
        self.__aoiToFarCallbacks = dict()
        self.__deadCallbacks = dict()
        self.__sndAttention = Sound('/GUI/notifications_FX/minimap_attention')
        self.__isFirstEnemyNonSPGMarked = False
        self.__isFirstEnemySPGMarkedById = dict()
        self.__checkEnemyNonSPGLengthID = None
        self.__resetSPGMarkerTimoutCbckId = None
        self.zIndexManager = MinimapZIndexManager()
        self.__observedVehicleId = -1
        self.__currentMode = None
        self.__normalMarkerScale = None
        self._actualSize = {'width': 0,
         'height': 0}
        self.__markerScale = None
        self.__markerIDGenerator = None
        self.__updateSettings()



    def updateSquadmanVeh(self, vID):
        self.__callEntryFlash(vID, 'setEntryName', [PLAYER_ENTITY_NAME.squadman.name()])



    def __del__(self):
        LOG_DEBUG('Minimap deleted')



    def start(self):
        self.__ownUI = GUI.WGMinimapFlash(self.__parentUI.movie)
        self.__ownUI.wg_inputKeyMode = 2
        self.__parentUI.component.addChild(self.__ownUI, 'minimap')
        self.__ownUI.mapSize = Math.Vector2(self.__MINIMAP_SIZE)
        (bl, tr,) = BigWorld.player().arena.arenaType.boundingBox
        self.__ownUI.setArenaBB(bl, tr)
        player = BigWorld.player()
        self.__playerTeam = player.team
        self.__playerVehicleID = player.playerVehicleID
        tex = BigWorld.PyTextureProvider(self.__cfg['texture'])
        if not self.__ownUI.setBackground(tex):
            LOG_ERROR("Failed to set minimap texture: '%s'" % self.__cfg['texture'])
        self.__cameraHandle = None
        self.__cameraMatrix = None
        BigWorld.player().inputHandler.onCameraChanged += self.__resetCamera
        BigWorld.player().inputHandler.onPostmortemVehicleChanged += self.__clearCamera
        self.__parentUI.addExternalCallbacks({'minimap.onClick': self._onMapClicked,
         'minimap.playAttantion': self._playAttention,
         'minimap.setSize': self.onSetSize,
         'minimap.lightPlayer': self.onLightPlayer,
         'minimap.scaleMarkers': self.onScaleMarkers})
        arena = player.arena
        arena.onPositionsUpdated += self.__onFarPosUpdated
        arena.onNewVehicleListReceived += self.__validateEntries
        arena.onVehicleKilled += self.__onVehicleKilled
        arena.onVehicleAdded += self.__onVehicleAdded
        arena.onTeamKiller += self.__onTeamKiller
        ctrl = g_sessionProvider.getEquipmentsCtrl()
        if ctrl:
            ctrl.onEquipmentMarkerShown += self.__onEquipmentMarkerShown
        ctrl = g_sessionProvider.getFeedback()
        if ctrl:
            ctrl.onMinimapFeedbackReceived += self.__onMinimapFeedbackReceived
        self.__markerIDGenerator = SequenceIDGenerator()
        isFlagBearer = False
        if hasFlags():
            g_ctfManager.onFlagSpawning += self.__onFlagSpawning
            Minimap.__battletype = 'fallout'
            g_ctfManager.onFlagSpawnedAtBase += self.__onFlagSpawnedAtBase
            g_ctfManager.onFlagCapturedByVehicle += self.__onFlagCapturedByVehicle
            g_ctfManager.onFlagDroppedToGround += self.__onFlagDroppedToGround
            g_ctfManager.onFlagAbsorbed += self.__onFlagAbsorbed
            g_ctfManager.onCarriedFlagsPositionUpdated += self.__onCarriedFlagsPositionUpdated
            for (flagID, flagInfo,) in g_ctfManager.getFlags():
                vehicleID = flagInfo['vehicle']
                if vehicleID is None:
                    if flagInfo['state'] == FLAG_STATE.WAITING_FIRST_SPAWN:
                        self.__onFlagSpawning(flagID, flagInfo['respawnTime'])
                    else:
                        self.__onFlagSpawnedAtBase(flagID, flagInfo['team'], flagInfo['minimapPos'])
                elif vehicleID == self.__playerVehicleID:
                    isFlagBearer = True

            self.__addFlagCaptureMarkers(isFlagBearer)
        if hasRepairPoints():
            g_sessionProvider.getRepairCtrl().onRepairPointStateChanged += self.__onRepairPointStateChanged
        arenaDP = g_sessionProvider.getArenaDP()
        if hasResourcePoints():
            g_ctfManager.onResPointIsFree += self.__onResPointIsFree
            g_ctfManager.onResPointCooldown += self.__onResPointCooldown
            g_ctfManager.onResPointCaptured += self.__onResPointCaptured
            g_ctfManager.onResPointCapturedLocked += self.__onResPointCapturedLocked
            g_ctfManager.onResPointBlocked += self.__onResPointBlocked
            for (pointID, point,) in g_ctfManager.getResourcePoints():
                pointState = point['state']
                if pointState == RESOURCE_POINT_STATE.FREE:
                    state = RESOURCE_POINT_TYPE.READY
                elif pointState == RESOURCE_POINT_STATE.COOLDOWN:
                    state = RESOURCE_POINT_TYPE.COOLDOWN
                elif pointState == RESOURCE_POINT_STATE.CAPTURED:
                    state = RESOURCE_POINT_TYPE.OWN_MINING if arenaDP.isAllyTeam(point['team']) else RESOURCE_POINT_TYPE.ENEMY_MINING
                else:
                    state = RESOURCE_POINT_TYPE.CONFLICT
                self.__addResourcePointMarker(pointID, point['minimapPos'], state)

        self.__marks = {}
        if not g_sessionProvider.getCtx().isPlayerObserver():
            mp = BigWorld.player().getOwnVehicleMatrix()
            self.__ownEntry['handle'] = self.__ownUI.addEntry(mp, self.zIndexManager.getIndexByName('self'))
            entryName = 'normal'
            self.__ownUI.entryInvoke(self.__ownEntry['handle'], ('init', ['player',
              entryName + 'Flag' if isFlagBearer else entryName,
              '',
              '',
              '',
              Minimap.__msize,
              Minimap.__keyc,
              Minimap.__fontsize,
              Minimap.__shownames,
              Minimap.__calph,
              Minimap.__ccolor,
              Minimap.__lalph,
              Minimap.__lcolor,
              Minimap.__acolor,
              Minimap.__ecolor,
              Minimap.__scolor,
              Minimap.__shadstr,
              Minimap.__mapname,
              Minimap.__fifalph,
              Minimap.__fifcolor,
              Minimap.__dcolor,
              Minimap.__dalph,
              Minimap.__dstyle,
              Minimap.__cstyle,
              Minimap.__lstyle,
              Minimap.__xshift,
              Minimap.__yshift,
              Minimap.__csize,
              Minimap.__acsize,
              Minimap.__hlalph,
              Minimap.__hlcolor,
              Minimap.__hlstyle,
              Minimap.__acstyle,
              Minimap.__accolor,
              Minimap.__acalph,
              Minimap.__belem,
              Minimap.__selem,
              Minimap.__artcurcol,
              0,
              'false' if Minimap.__battletype == 'fallout' else Minimap.__lostmark,
              Minimap.__mrkscale,
              Minimap.__lostalph,
              Minimap.__lostcol,
              Minimap.__sshiftx,
              Minimap.__sshifty,
              Minimap.__cucirsize,
              Minimap.__cucirstyle,
              Minimap.__cucircolor,
              Minimap.__cuciralpha,
              Minimap.__binocs,
              Minimap.__binalpha,
              Minimap.__binstyle,
              Minimap.__bincolor]))
            self.__ownEntry['matrix'] = player.getOwnVehicleMatrix()
            self.__ownEntry['location'] = None
            self.__ownEntry['entryName'] = entryName
        self.__resetCamera(MODE_ARCADE)
        self.__isStarted = True
        for id in self.__vehiclesWaitStart:
            self.notifyVehicleStart(id)

        self.__vehiclesWaitStart = []
        self.__mapSizeIndex = self.getStoredMinimapSize()
        from account_helpers.settings_core.SettingsCore import g_settingsCore
        g_settingsCore.onSettingsChanged += self.setupMinimapSettings
        self.setupMinimapSettings()
        self.setTeamPoints()
        g_repeatKeyHandlers.add(self.handleRepeatKeyEvent)
        Minimap.__yawLimits = vehicle_getter.getYawLimits(BigWorld.player().vehicle.typeDescriptor)
        if Minimap.__yawLimits == None:
            Minimap.__yawLimits = (0, 0)
        print ('Yaw Limits: ', Minimap.__yawLimits)
        self.__ownUI.entryInvoke(self.__ownEntry['handle'], ('setGunConstraints', [math.degrees(Minimap.__yawLimits[0]), math.degrees(Minimap.__yawLimits[1])]))



    def __showSector(self):
        vehicle = BigWorld.entity(self.__playerVehicleID)
        vTypeDesc = vehicle.typeDescriptor
        yawLimits = vehicle_getter.getYawLimits(vTypeDesc)
        entryName = 'normalWithSector'
        self.__ownUI.entryInvoke(self.__ownEntry['handle'], ('setEntryName', [entryName + 'Flag' if g_ctfManager.isFlagBearer(self.__playerVehicleID) else entryName]))
        self.__ownEntry['entryName'] = entryName
        self.__ownUI.entryInvoke(self.__ownEntry['handle'], ('showSector', [math.degrees(yawLimits[0]), math.degrees(yawLimits[1])]))



    def __hideSector(self):
        self.__ownUI.entryInvoke(self.__ownEntry['handle'], ('hideSector', []))



    def onScaleMarkers(self, callbackID, oscale, normalScale):
        self.__markerScale = float(Minimap.__mrkscale)
        self.__normalMarkerScale = self.__markerScale
        bases = self.__points['base']
        for team in bases:
            for base in bases[team]:
                self.scaleMarker(bases[team][base].handle, bases[team][base].matrix, 1)


        spawns = self.__points['spawn']
        for team in spawns:
            for spawn in spawns[team]:
                self.scaleMarker(spawns[team][spawn].handle, spawns[team][spawn].matrix, 1)


        if 'control' in self.__points:
            controls = self.__points['control']
            for point in controls:
                self.scaleMarker(point.handle, point.matrix, 1)

        if 'repair' in self.__points:
            repairs = self.__points['repair']
            for (point, pointCooldown,) in repairs.itervalues():
                self.scaleMarker(point.handle, point.matrix, self.__markerScale)
                self.scaleMarker(pointCooldown.handle, pointCooldown.matrix, 1)

        if not _isStrategic(self.__currentMode) and self.__cameraHandle is not None and self.__cameraMatrix is not None:
            self.scaleMarker(self.__cameraHandle, self.__cameraMatrix, self.__normalMarkerScale)
        if self.__ownEntry.has_key('handle'):
            self.scaleMarker(self.__ownEntry['handle'], self.__ownEntry['matrix'], 1)
        for id in self.__entries:
            originalMatrix = self.__entries[id]['matrix']
            handle = self.__entries[id]['handle']
            self.scaleMarker(handle, originalMatrix, self.__markerScale)

        for id in self.__entrieLits:
            originalMatrix = self.__entrieLits[id]['matrix']
            handle = self.__entrieLits[id]['handle']
            self.scaleMarker(handle, originalMatrix, self.__markerScale)

        for item in self.__entrieMarkers.itervalues():
            originalMatrix = item['matrix']
            handle = item['handle']
            self.scaleMarker(handle, originalMatrix, self.__markerScale)




    def scaleMarker(self, handle, originalMatrix, scale):
        if handle is not None and originalMatrix is not None:
            scaleMatrix = Matrix()
            scaleMatrix.setScale(Vector3(scale, scale, scale))
            mp = mathUtils.MatrixProviders.product(scaleMatrix, originalMatrix)
            self.__ownUI.entrySetMatrix(handle, mp)



    def getStoredMinimapSize(self):
        return AccountSettings.getSettings('minimapSize')



    def storeMinimapSize(self):
        AccountSettings.setSettings('minimapSize', self.__mapSizeIndex)



    def getStoredMinimapAlpha(self):
        from account_helpers.settings_core.SettingsCore import g_settingsCore
        return g_settingsCore.getSetting('minimapAlpha')



    def setupMinimapSettings(self, diff = None):
        from account_helpers.settings_core import settings_constants
        if diff is None or 'minimapSize' in diff:
            self.__parentUI.call('minimap.setupSize', [self.getStoredMinimapSize()])
        if diff is None or settings_constants.GAME.MINIMAP_ALPHA in diff:
            self.__parentUI.call('minimap.setupAlpha', [self.getStoredMinimapAlpha(), Minimap.__mrkscale])



    def setTeamPoints(self):
        if hasattr(BigWorld.player().arena, 'viewtext') and Minimap.__csize != 'viewrange' and Minimap.__vrtenabled:
            BPA = BigWorld.player().arena
            color = Minimap.__vrtcolor
            color = '\\c' + re.sub('[^A-Za-z0-9]+', '', color) + 'FF;'
            if str(Minimap.__tview) != '0':
                BPA.viewtext.text = color + '%s %.1fm / %s %.1fm' % ('V:',
                 float(Minimap.__csize),
                 'T:',
                 float(Minimap.__tview))
            else:
                BPA.viewtext.text = color + '%s %.1fm' % ('Viewrange:', float(Minimap.__csize))
        if self.__cfg['teamBasePositions'] or self.__cfg['teamSpawnPoints'] or self.__cfg['controlPoints'] or self.__cfg['repairPoints']:
            player = BigWorld.player()
            currentTeam = player.team
            for (team, teamSpawnPoints,) in enumerate(self.__cfg['teamSpawnPoints'], 1):
                teamSpawnData = {}
                self.__points['spawn'][team] = teamSpawnData
                for (spawn, spawnPoint,) in enumerate(teamSpawnPoints, 1):
                    pos = (spawnPoint[0], 0, spawnPoint[1])
                    m = Math.Matrix()
                    m.setTranslate(pos)
                    teamSpawnData[spawn] = EntryInfo(self.__ownUI.addEntry(m, self.zIndexManager.getTeamPointIndex()), m)
                    self.__ownUI.entryInvoke(teamSpawnData[spawn].handle, ('init', ['points',
                      'spawn',
                      'blue' if team == currentTeam else 'red',
                      spawn + 1 if len(teamSpawnPoints) > 1 else 1,
                      '',
                      Minimap.__msize,
                      Minimap.__keyc,
                      Minimap.__fontsize,
                      Minimap.__shownames,
                      Minimap.__calph,
                      Minimap.__ccolor,
                      Minimap.__lalph,
                      Minimap.__lcolor,
                      Minimap.__acolor,
                      Minimap.__ecolor,
                      Minimap.__scolor,
                      Minimap.__shadstr,
                      Minimap.__mapname,
                      Minimap.__fifalph,
                      Minimap.__fifcolor,
                      Minimap.__dcolor,
                      Minimap.__dalph,
                      Minimap.__dstyle,
                      Minimap.__cstyle,
                      Minimap.__lstyle,
                      Minimap.__xshift,
                      Minimap.__yshift,
                      Minimap.__csize,
                      Minimap.__acsize,
                      Minimap.__hlalph,
                      Minimap.__hlcolor,
                      Minimap.__hlstyle,
                      Minimap.__acstyle,
                      Minimap.__accolor,
                      Minimap.__acalph,
                      Minimap.__belem,
                      Minimap.__selem,
                      Minimap.__artcurcol,
                      0,
                      'false' if Minimap.__battletype == 'fallout' else Minimap.__lostmark,
                      Minimap.__mrkscale,
                      Minimap.__lostalph,
                      Minimap.__lostcol,
                      Minimap.__sshiftx,
                      Minimap.__sshifty,
                      Minimap.__cucirsize,
                      Minimap.__cucirstyle,
                      Minimap.__cucircolor,
                      Minimap.__cuciralpha,
                      Minimap.__binocs,
                      Minimap.__binalpha,
                      Minimap.__binstyle,
                      Minimap.__bincolor]))


            for (team, teamBasePoints,) in enumerate(self.__cfg['teamBasePositions'], 1):
                teamBaseData = {}
                self.__points['base'][team] = teamBaseData
                for (base, basePoint,) in teamBasePoints.items():
                    pos = (basePoint[0], 0, basePoint[1])
                    m = Math.Matrix()
                    m.setTranslate(pos)
                    teamBaseData[base] = EntryInfo(self.__ownUI.addEntry(m, self.zIndexManager.getTeamPointIndex()), m)
                    self.__ownUI.entryInvoke(teamBaseData[base].handle, ('init', ['points',
                      'base',
                      'blue' if team == currentTeam else 'red',
                      len(teamBaseData) + 1 if len(teamBasePoints) > 1 else 1,
                      '',
                      Minimap.__msize,
                      Minimap.__keyc,
                      Minimap.__fontsize,
                      Minimap.__shownames,
                      Minimap.__calph,
                      Minimap.__ccolor,
                      Minimap.__lalph,
                      Minimap.__lcolor,
                      Minimap.__acolor,
                      Minimap.__ecolor,
                      Minimap.__scolor,
                      Minimap.__shadstr,
                      Minimap.__mapname,
                      Minimap.__fifalph,
                      Minimap.__fifcolor,
                      Minimap.__dcolor,
                      Minimap.__dalph,
                      Minimap.__dstyle,
                      Minimap.__cstyle,
                      Minimap.__lstyle,
                      Minimap.__xshift,
                      Minimap.__yshift,
                      Minimap.__csize,
                      Minimap.__acsize,
                      Minimap.__hlalph,
                      Minimap.__hlcolor,
                      Minimap.__hlstyle,
                      Minimap.__acstyle,
                      Minimap.__accolor,
                      Minimap.__acalph,
                      Minimap.__belem,
                      Minimap.__selem,
                      Minimap.__artcurcol,
                      0,
                      'false' if Minimap.__battletype == 'fallout' else Minimap.__lostmark,
                      Minimap.__mrkscale,
                      Minimap.__lostalph,
                      Minimap.__lostcol,
                      Minimap.__sshiftx,
                      Minimap.__sshifty,
                      Minimap.__cucirsize,
                      Minimap.__cucirstyle,
                      Minimap.__cucircolor,
                      Minimap.__cuciralpha,
                      Minimap.__binocs,
                      Minimap.__binalpha,
                      Minimap.__binstyle,
                      Minimap.__bincolor]))


            if self.__cfg['controlPoints']:
                controlData = []
                self.__points['control'] = controlData
                for (index, controlPoint,) in enumerate(self.__cfg['controlPoints'], 2):
                    pos = (controlPoint[0], 0, controlPoint[1])
                    m = Math.Matrix()
                    m.setTranslate(pos)
                    newPoint = EntryInfo(self.__ownUI.addEntry(m, self.zIndexManager.getTeamPointIndex()), m)
                    controlData.append(newPoint)
                    self.__ownUI.entryInvoke(newPoint.handle, ('init', ['points',
                      'control',
                      'empty',
                      index if len(self.__cfg['controlPoints']) > 1 else 1,
                      '',
                      Minimap.__msize,
                      Minimap.__keyc,
                      Minimap.__fontsize,
                      Minimap.__shownames,
                      Minimap.__calph,
                      Minimap.__ccolor,
                      Minimap.__lalph,
                      Minimap.__lcolor,
                      Minimap.__acolor,
                      Minimap.__ecolor,
                      Minimap.__scolor,
                      Minimap.__shadstr,
                      Minimap.__mapname,
                      Minimap.__fifalph,
                      Minimap.__fifcolor,
                      Minimap.__dcolor,
                      Minimap.__dalph,
                      Minimap.__dstyle,
                      Minimap.__cstyle,
                      Minimap.__lstyle,
                      Minimap.__xshift,
                      Minimap.__yshift,
                      Minimap.__csize,
                      Minimap.__acsize,
                      Minimap.__hlalph,
                      Minimap.__hlcolor,
                      Minimap.__hlstyle,
                      Minimap.__acstyle,
                      Minimap.__accolor,
                      Minimap.__acalph,
                      Minimap.__belem,
                      Minimap.__selem,
                      Minimap.__artcurcol,
                      0,
                      'false' if Minimap.__battletype == 'fallout' else Minimap.__lostmark,
                      Minimap.__mrkscale,
                      Minimap.__lostalph,
                      Minimap.__lostcol,
                      Minimap.__sshiftx,
                      Minimap.__sshifty,
                      Minimap.__cucirsize,
                      Minimap.__cucirstyle,
                      Minimap.__cucircolor,
                      Minimap.__cuciralpha,
                      Minimap.__binocs,
                      Minimap.__binalpha,
                      Minimap.__binstyle,
                      Minimap.__bincolor]))

            if self.__cfg['repairPoints']:
                repairData = {}
                self.__points['repair'] = repairData
                for (index, repairPoint,) in enumerate(self.__cfg['repairPoints']):
                    pos = repairPoint['position']
                    m = Math.Matrix()
                    m.setTranslate(pos)
                    newPoint = EntryInfo(self.__ownUI.addEntry(m, self.zIndexManager.getTeamPointIndex()), m)
                    self.__ownUI.entryInvoke(newPoint.handle, ('init', ['repairPoints',
                      'active',
                      '',
                      0,
                      '',
                      Minimap.__msize,
                      Minimap.__keyc,
                      Minimap.__fontsize,
                      Minimap.__shownames,
                      Minimap.__calph,
                      Minimap.__ccolor,
                      Minimap.__lalph,
                      Minimap.__lcolor,
                      Minimap.__acolor,
                      Minimap.__ecolor,
                      Minimap.__scolor,
                      Minimap.__shadstr,
                      Minimap.__mapname,
                      Minimap.__fifalph,
                      Minimap.__fifcolor,
                      Minimap.__dcolor,
                      Minimap.__dalph,
                      Minimap.__dstyle,
                      Minimap.__cstyle,
                      Minimap.__lstyle,
                      Minimap.__xshift,
                      Minimap.__yshift,
                      Minimap.__csize,
                      Minimap.__acsize,
                      Minimap.__hlalph,
                      Minimap.__hlcolor,
                      Minimap.__hlstyle,
                      Minimap.__acstyle,
                      Minimap.__accolor,
                      Minimap.__acalph,
                      Minimap.__belem,
                      Minimap.__selem,
                      Minimap.__artcurcol,
                      0,
                      'false' if Minimap.__battletype == 'fallout' else Minimap.__lostmark,
                      Minimap.__mrkscale,
                      Minimap.__lostalph,
                      Minimap.__lostcol,
                      Minimap.__sshiftx,
                      Minimap.__sshifty,
                      Minimap.__cucirsize,
                      Minimap.__cucirstyle,
                      Minimap.__cucircolor,
                      Minimap.__cuciralpha,
                      Minimap.__binocs,
                      Minimap.__binalpha,
                      Minimap.__binstyle,
                      Minimap.__bincolor]))
                    newPointCooldown = EntryInfo(self.__ownUI.addEntry(m, self.zIndexManager.getTeamPointIndex()), m)
                    self.__ownUI.entryInvoke(newPointCooldown.handle, ('init', ['repairPoints',
                      'cooldown',
                      '',
                      0,
                      '',
                      Minimap.__msize,
                      Minimap.__keyc,
                      Minimap.__fontsize,
                      Minimap.__shownames,
                      Minimap.__calph,
                      Minimap.__ccolor,
                      Minimap.__lalph,
                      Minimap.__lcolor,
                      Minimap.__acolor,
                      Minimap.__ecolor,
                      Minimap.__scolor,
                      Minimap.__shadstr,
                      Minimap.__mapname,
                      Minimap.__fifalph,
                      Minimap.__fifcolor,
                      Minimap.__dcolor,
                      Minimap.__dalph,
                      Minimap.__dstyle,
                      Minimap.__cstyle,
                      Minimap.__lstyle,
                      Minimap.__xshift,
                      Minimap.__yshift,
                      Minimap.__csize,
                      Minimap.__acsize,
                      Minimap.__hlalph,
                      Minimap.__hlcolor,
                      Minimap.__hlstyle,
                      Minimap.__acstyle,
                      Minimap.__accolor,
                      Minimap.__acalph,
                      Minimap.__belem,
                      Minimap.__selem,
                      Minimap.__artcurcol,
                      0,
                      'false' if Minimap.__battletype == 'fallout' else Minimap.__lostmark,
                      Minimap.__mrkscale,
                      Minimap.__lostalph,
                      Minimap.__lostcol,
                      Minimap.__sshiftx,
                      Minimap.__sshifty,
                      Minimap.__cucirsize,
                      Minimap.__cucirstyle,
                      Minimap.__cucircolor,
                      Minimap.__cuciralpha,
                      Minimap.__binocs,
                      Minimap.__binalpha,
                      Minimap.__binstyle,
                      Minimap.__bincolor]))
                    self.__ownUI.entryInvoke(newPointCooldown.handle, ('setVisible', [False]))
                    repairData[index] = (newPoint, newPointCooldown)

            self.__parentUI.call('minimap.entryInited', [])



    def onSetSize(self, calbackID, index):
        self.__mapSizeIndex = int(index)
        self.__parentUI.call('minimap.setupSize', [self.__mapSizeIndex])



    def onLightPlayer(self, calbackID, vehicleID, visibility):
        self.__callEntryFlash(vehicleID, 'lightPlayer', [visibility])



    def destroy(self):
        if not self.__isStarted:
            self.__vehiclesWaitStart = []
            return 
        while len(self.__aoiToFarCallbacks):
            (_, callbackID,) = self.__aoiToFarCallbacks.popitem()
            if callbackID is not None:
                BigWorld.cancelCallback(callbackID)

        self.__isStarted = False
        self.__entries = {}
        self.__entrieLits = {}
        self.__entrieMarkers = {}
        self.__cameraHandle = None
        self.__cameraMatrix = None
        from gui.battle_control import g_sessionProvider
        ctrl = g_sessionProvider.getEquipmentsCtrl()
        if ctrl:
            ctrl.onEquipmentMarkerShown -= self.__onEquipmentMarkerShown
        ctrl = g_sessionProvider.getFeedback()
        if ctrl:
            ctrl.onMinimapFeedbackReceived -= self.__onMinimapFeedbackReceived
        self.__markerIDGenerator = None
        if hasFlags():
            g_ctfManager.onFlagSpawning -= self.__onFlagSpawning
            g_ctfManager.onFlagSpawnedAtBase -= self.__onFlagSpawnedAtBase
            g_ctfManager.onFlagCapturedByVehicle -= self.__onFlagCapturedByVehicle
            g_ctfManager.onFlagDroppedToGround -= self.__onFlagDroppedToGround
            g_ctfManager.onFlagAbsorbed -= self.__onFlagAbsorbed
            g_ctfManager.onCarriedFlagsPositionUpdated -= self.__onCarriedFlagsPositionUpdated
        if hasRepairPoints():
            g_sessionProvider.getRepairCtrl().onRepairPointStateChanged -= self.__onRepairPointStateChanged
        if hasResourcePoints():
            g_ctfManager.onResPointIsFree -= self.__onResPointIsFree
            g_ctfManager.onResPointCooldown -= self.__onResPointCooldown
            g_ctfManager.onResPointCaptured -= self.__onResPointCaptured
            g_ctfManager.onResPointCapturedLocked -= self.__onResPointCapturedLocked
            g_ctfManager.onResPointBlocked -= self.__onResPointBlocked
        self.__marks = None
        self.__backMarkers.clear()
        setattr(self.__parentUI.component, 'minimap', None)
        from account_helpers.settings_core.SettingsCore import g_settingsCore
        g_settingsCore.onSettingsChanged -= self.setupMinimapSettings
        self.storeMinimapSize()
        self.__parentUI = None
        g_repeatKeyHandlers.remove(self.handleRepeatKeyEvent)
        if hasattr(BigWorld.player().arena, 'viewtext'):
            BPA = BigWorld.player().arena
            BPA.viewtext.visible = False
        from gui.battle_control import g_sessionProvider
        optDevicesCtrl = g_sessionProvider.getOptDevicesCtrl()
        optDevicesCtrl.onOptionalDeviceAdded -= self.newaddOptionalDevice
        optDevicesCtrl.onOptionalDeviceUpdated -= self.newsetOptionalDeviceState



    def prerequisites(self):
        return []



    def setVisible(self, visible):
        pass



    def notifyVehicleStop(self, vehicleId):
        if not self.__isStarted:
            if vehicleId in self.__vehiclesWaitStart:
                self.__vehiclesWaitStart.remove(vehicleId)
            return 
        if vehicleId == self.__playerVehicleID:
            return 
        info = BigWorld.player().arena.vehicles.get(vehicleId)
        if info is None or not info['isAlive']:
            return 
        entries = self.__entries
        if vehicleId in entries:
            location = entries[vehicleId]['location']
            if location == VehicleLocation.AOI:
                ownPos = Math.Matrix(BigWorld.camera().invViewMatrix).translation
                entryPos = Math.Matrix(entries[vehicleId]['matrix']).translation
                inAoI = bool(abs(ownPos.x - entryPos.x) < self.__AOI_ESTIMATE and abs(ownPos.z - entryPos.z) < self.__AOI_ESTIMATE)
                self.__delEntry(vehicleId)
                if not inAoI:
                    self.__addEntry(vehicleId, VehicleLocation.AOI_TO_FAR, False)
            else:
                LOG_DEBUG('notifyVehicleOnStop, unknown minimap entry location', location)



    def notifyVehicleStart(self, vehicleId):
        if not self.__isStarted:
            self.__vehiclesWaitStart.append(vehicleId)
            return 
        if vehicleId == self.__playerVehicleID:
            return 
        info = BigWorld.player().arena.vehicles.get(vehicleId)
        if info is None or not info['isAlive']:
            return 
        entries = self.__entries
        doMark = True
        if vehicleId in entries:
            doMark = False
            self.__delEntry(vehicleId)
        self.__addEntry(vehicleId, VehicleLocation.AOI, doMark)
        self.__delEntryLit(vehicleId)
        self.__delCarriedFlagMarker(vehicleId)



    def _playAttention(self, _):
        self.__sndAttention.play()



    def markCell(self, cellIndexes, duration):
        if not self.__isStarted:
            return 
        if cellIndexes < 0:
            return 
        (columnCount, rowCount,) = Minimap.__MINIMAP_CELLS
        column = cellIndexes / columnCount % columnCount
        row = cellIndexes % columnCount
        if self.__marks.has_key(cellIndexes):
            BigWorld.cancelCallback(self.__marks[cellIndexes][1])
            self._removeCellMark(cellIndexes)
        arenaDesc = BigWorld.player().arena.arenaType
        (bottomLeft, upperRight,) = arenaDesc.boundingBox
        viewpoint = (upperRight + bottomLeft) * 0.5
        viewpointTranslate = Math.Matrix()
        viewpointTranslate.setTranslate((viewpoint.x, 0.0, viewpoint.y))
        spaceSize = upperRight - bottomLeft
        pos = (column * spaceSize[0] / columnCount - spaceSize[0] * 0.5, 0, -row * spaceSize[1] / rowCount + spaceSize[0] * 0.5)
        m = Math.Matrix()
        m.setTranslate(Math.Matrix(viewpointTranslate).applyPoint(pos))
        player = BigWorld.player()
        if player.isTeleport:
            tmpPointUp = (pos[0], 1000.0, pos[2])
            tmpPointDown = (pos[0], -1000.0, pos[2])
            colRes = BigWorld.collide(player.spaceID, tmpPointUp, tmpPointDown)
            height = colRes[0][1]
            player.base.vehicle_teleport((pos[0], height, pos[2]), 0)
        mark = self.__ownUI.addEntry(m, self.zIndexManager.getIndexByName('cell'))
        self.__ownUI.entryInvoke(mark, ('gotoAndStop', ['cellFlash']))
        self._playAttention(None)
        callbackID = BigWorld.callback(duration, partial(self._removeCellMark, cellIndexes))
        self.__marks[cellIndexes] = (mark, callbackID)



    def getCellName(self, cellIndexes):
        (columnCount, rowCount,) = Minimap.__MINIMAP_CELLS
        column = cellIndexes / columnCount % columnCount
        row = cellIndexes % columnCount
        if row < 8:
            name = string.ascii_uppercase[row]
        else:
            name = string.ascii_uppercase[(row + 1)]
        name += str((column + 1) % 10)
        return name



    def _removeCellMark(self, cellIndexes):
        if self.__isStarted:
            mark = self.__marks[cellIndexes][0]
            del self.__marks[cellIndexes]
            self.__ownUI.delEntry(mark)



    def _onMapClicked(self, _, x, y, bHighlightCellNVehicleSpecific = True):
        localPos = (x - 0.5, y - 0.5)
        mapSize = Minimap.__MINIMAP_SIZE
        player = BigWorld.player()
        if bHighlightCellNVehicleSpecific:
            cellCount = Minimap.__MINIMAP_CELLS
            row = int(cellCount[0] * localPos[0] / mapSize[0])
            column = int(cellCount[1] * localPos[1] / mapSize[1])
            g_sessionProvider.getChatCommands().sendAttentionToCell(row * int(cellCount[1]) + column)
        else:
            arenaDesc = BigWorld.player().arena.arenaType
            (bottomLeft, upperRight,) = arenaDesc.boundingBox
            spaceSize = upperRight - bottomLeft
            viewpoint = (upperRight + bottomLeft) * 0.5
            viewpointTranslate = Math.Matrix()
            viewpointTranslate.setTranslate((viewpoint.x, 0.0, viewpoint.y))
            pos = ((localPos[0] - mapSize[0] * 0.5) / mapSize[0], (localPos[1] - mapSize[1] * 0.5) / mapSize[1])
            worldPos = Math.Matrix(viewpointTranslate).applyPoint((pos[0] * spaceSize[0], 0.0, -pos[1] * spaceSize[1]))
            player.inputHandler.onMinimapClicked(worldPos)



    def __onVehicleAdded(self, id):
        arena = BigWorld.player().arena
        if not arena.vehicles[id]['isAlive']:
            return 
        location = self.__detectLocation(id)
        if location is not None:
            self.__addEntry(id, location, True)



    def __onTeamKiller(self, id):
        arena = BigWorld.player().arena
        entryVehicle = arena.vehicles[id]
        if BigWorld.player().team == entryVehicle.get('team') and g_sessionProvider.getCtx().isSquadMan(vID=id):
            return 
        self.__callEntryFlash(id, 'setEntryName', [PLAYER_ENTITY_NAME.teamKiller.name()])



    def __onVehicleRemoved(self, id):
        if self.__entries.has_key(id):
            self.__delEntry(id)
        self.__delEntryLit(id)



    def __onVehicleKilled(self, victimId, killerID, reason):
        self.__delEntryLit(victimId)
        if self.__entries.has_key(victimId):
            entry = self.__delEntry(victimId)
            if GUI_SETTINGS.showMinimapDeath:
                self.__addDeadEntry(entry, victimId)



    def __onFarPosUpdated(self):
        entries = self.__entries
        arena = BigWorld.player().arena
        vehicles = arena.vehicles
        for (id, pos,) in arena.positions.iteritems():
            entry = entries.get(id)
            with open('locations', 'w+') as f:
                f.write(id)
                f.write(pos)
            if entry is not None:
                location = entry['location']
                if location == VehicleLocation.FAR:
                    entry['matrix'].source.setTranslate(pos)
                    self.scaleMarker(entry['handle'], entry['matrix'], float(Minimap.__mrkscale))
                elif location == VehicleLocation.AOI_TO_FAR:
                    self.__delEntry(id)
                    self.__addEntry(id, VehicleLocation.FAR, False)
            elif vehicles[id]['isAlive']:
                self.__addEntry(id, VehicleLocation.FAR, True)

        for id in set(entries).difference(set(arena.positions)):
            location = entries[id]['location']
            if location in (VehicleLocation.FAR, VehicleLocation.AOI_TO_FAR):
                if self.__permanentNamesShow or self.__onAltNamesShow:
                    if hasattr(entries[id]['matrix'], 'source'):
                        self.__addEntryLit(id, entries[id]['matrix'].source, not self.__onAltNamesShow)
                self.__delEntry(id)




    def __validateEntries(self):
        entrySet = set(self.__entries.iterkeys())
        vehiclesSet = set(BigWorld.player().arena.vehicles.iterkeys())
        playerOnlySet = {self.__playerVehicleID}
        for id in vehiclesSet.difference(entrySet) - playerOnlySet:
            self.__onVehicleAdded(id)

        for id in entrySet.difference(vehiclesSet) - playerOnlySet:
            self.__onVehicleRemoved(id)




    def __detectLocation(self, id):
        vehicle = BigWorld.entities.get(id)
        if vehicle is not None and vehicle.isStarted:
            return VehicleLocation.AOI
        else:
            if BigWorld.player().arena.positions.has_key(id):
                return VehicleLocation.FAR
            return 



    def __delEntry(self, id, inCallback = False):
        entry = self.__entries.get(id)
        if entry is None:
            return 
        self.__ownUI.delEntry(entry['handle'])
        if entry.get('location') == VehicleLocation.AOI_TO_FAR:
            callbackId = self.__aoiToFarCallbacks.pop(id, None)
            if callbackId is not None:
                BigWorld.cancelCallback(callbackId)
        if id in self.__enemyEntries:
            self.__enemyEntries.pop(id)
            if not len(self.__enemyEntries):
                if self.__checkEnemyNonSPGLengthID:
                    BigWorld.cancelCallback(self.__checkEnemyNonSPGLengthID)
                self.__checkEnemyNonSPGLengthID = BigWorld.callback(5, self.__checkEnemyNonSPGLength)
        if id in self.__deadCallbacks:
            callbackId = self.__deadCallbacks.pop(id)
            BigWorld.cancelCallback(callbackId)
        return self.__entries.pop(id)



    def __addDeadEntry(self, entry, id):
        """
        adding death animation to minimap (WOTD-5884)
        """
        if id in BigWorld.entities.keys():
            m = self.__getEntryMatrixByLocation(id, entry['location'])
            scaledMatrix = None
            if self.__markerScale is not None:
                scaleMatrix = Matrix()
                scaleMatrix.setScale(Vector3(self.__markerScale, self.__markerScale, self.__markerScale))
                scaledMatrix = mathUtils.MatrixProviders.product(scaleMatrix, m)
            if scaledMatrix is None:
                entry['handle'] = self.__ownUI.addEntry(m, self.zIndexManager.getDeadVehicleIndex(id))
            else:
                entry['handle'] = self.__ownUI.addEntry(scaledMatrix, self.zIndexManager.getVehicleIndex(id))
            self.__entries[id] = entry
            vClass = entry['vClass']
            if vClass == 'mediumAT-SPG':
                vClass = 'AT-SPG'
            if vClass == 'heavyAT-SPG':
                vClass = 'AT-SPG'
            if vClass == 'mediumSPG':
                vClass = 'SPG'
            if vClass == 'heavySPG':
                vClass = 'SPG'
            if vClass == 'superheavyTank':
                vClass = 'heavyTank'
            if vClass == 'supermediumTank':
                vClass = 'mediumTank'
            if Minimap.__skulls:
                vClass = 'skull'
            if not GUI_SETTINGS.permanentMinimapDeath:
                self.__deadCallbacks[id] = BigWorld.callback(GUI_SETTINGS.minimapDeathDuration / 1000, partial(self.__delEntry, id))
            self.__callEntryFlash(id, 'setDead', [GUI_SETTINGS.permanentMinimapDeath])
            self.__callEntryFlash(id, 'init', [entry['markerType'],
             entry['entryName'],
             vClass,
             '',
             entry['vShortName'],
             Minimap.__msize,
             Minimap.__keyc,
             Minimap.__fontsize,
             Minimap.__shownames,
             Minimap.__calph,
             Minimap.__ccolor,
             Minimap.__lalph,
             Minimap.__lcolor,
             Minimap.__acolor,
             Minimap.__ecolor,
             Minimap.__scolor,
             Minimap.__shadstr,
             Minimap.__mapname,
             Minimap.__fifalph,
             Minimap.__fifcolor,
             Minimap.__dcolor,
             Minimap.__dalph,
             Minimap.__dstyle,
             Minimap.__cstyle,
             Minimap.__lstyle,
             Minimap.__xshift,
             Minimap.__yshift,
             Minimap.__csize,
             Minimap.__acsize,
             Minimap.__hlalph,
             Minimap.__hlcolor,
             Minimap.__hlstyle,
             Minimap.__acstyle,
             Minimap.__accolor,
             Minimap.__acalph,
             Minimap.__belem,
             Minimap.__selem,
             Minimap.__artcurcol,
             0,
             'false' if Minimap.__battletype == 'fallout' else Minimap.__lostmark,
             Minimap.__mrkscale,
             Minimap.__lostalph,
             Minimap.__lostcol,
             Minimap.__sshiftx,
             Minimap.__sshifty,
             Minimap.__cucirsize,
             Minimap.__cucirstyle,
             Minimap.__cucircolor,
             Minimap.__cuciralpha,
             Minimap.__binocs,
             Minimap.__binalpha,
             Minimap.__binstyle,
             Minimap.__bincolor])
            if self.__markerScale is None:
                self.__parentUI.call('minimap.entryInited', [])
            self.onScaleMarkers(None, 1, 1)



    def __checkEnemyNonSPGLength(self):
        self.__checkEnemyNonSPGLengthID = None
        self.__isFirstEnemyNonSPGMarked = not len(self.__enemyEntries) == 0



    def __getEntryMatrixByLocation(self, id, location):
        m = None
        matrix = None
        if location == VehicleLocation.AOI:
            m = Math.WGTranslationOnlyMP()
            matrix = BigWorld.entities[id].matrix
        elif location == VehicleLocation.AOI_TO_FAR:
            m = Math.WGTranslationOnlyMP()
            matrix = Math.Matrix(BigWorld.entities[id].matrix)
        elif location == VehicleLocation.FAR:
            matrix = Math.Matrix()
            pos = BigWorld.player().arena.positions[id]
            matrix.setTranslate(pos)
            m = Math.WGReplayAwaredSmoothTranslationOnlyMP()
        m.source = matrix
        return m



    def addBackEntry(self, id, name, position, type):
        viewpointTranslate = Math.Matrix()
        viewpointTranslate.setTranslate((0.0, 0.0, 0.0))
        m = Math.Matrix()
        m.setTranslate(Math.Matrix(viewpointTranslate).applyPoint(position))
        markerType = 'backgroundMarker'
        marker = dict()
        marker['handle'] = self.__ownUI.addEntry(m, self.zIndexManager.getBackIconIndex(id))
        marker['markerType'] = markerType
        marker['entryName'] = name
        marker['type'] = type
        self.__backMarkers[marker['handle']] = marker
        self.__ownUI.entryInvoke(marker['handle'], ('init', [markerType,
          name,
          '',
          type,
          '',
          Minimap.__msize,
          Minimap.__keyc,
          Minimap.__fontsize,
          Minimap.__shownames,
          Minimap.__calph,
          Minimap.__ccolor,
          Minimap.__lalph,
          Minimap.__lcolor,
          Minimap.__acolor,
          Minimap.__ecolor,
          Minimap.__scolor,
          Minimap.__shadstr,
          Minimap.__mapname,
          Minimap.__fifalph,
          Minimap.__fifcolor,
          Minimap.__dcolor,
          Minimap.__dalph,
          Minimap.__dstyle,
          Minimap.__cstyle,
          Minimap.__lstyle,
          Minimap.__xshift,
          Minimap.__yshift,
          Minimap.__csize,
          Minimap.__acsize,
          Minimap.__hlalph,
          Minimap.__hlcolor,
          Minimap.__hlstyle,
          Minimap.__acstyle,
          Minimap.__accolor,
          Minimap.__acalph,
          Minimap.__belem,
          Minimap.__selem,
          Minimap.__artcurcol,
          0,
          'false' if Minimap.__battletype == 'fallout' else Minimap.__lostmark,
          Minimap.__mrkscale,
          Minimap.__lostalph,
          Minimap.__lostcol,
          Minimap.__sshiftx,
          Minimap.__sshifty,
          Minimap.__cucirsize,
          Minimap.__cucirstyle,
          Minimap.__cucircolor,
          Minimap.__cuciralpha,
          Minimap.__binocs,
          Minimap.__binalpha,
          Minimap.__binstyle,
          Minimap.__bincolor]))
        if self.__markerScale is None:
            self.__parentUI.call('minimap.entryInited', [])
        return marker['handle']



    def removeBackEntry(self, handle):
        marker = self.__backMarkers.pop(handle, None)
        if marker is not None and self.__ownUI is not None:
            self.__ownUI.delEntry(handle)



    def onAltPress(self, value):
        pass



    def showVehicleNames(self, value):
        pass



    def __addEntryLit(self, id, matrix, visible = True):
        pass



    def __addEntryMarker(self, markerType, marker, uniqueID, zIndex, matrix, isVisible = True, index = None):
        if matrix is None:
            return 
        mp = Math.WGReplayAwaredSmoothTranslationOnlyMP()
        mp.source = matrix
        scaledMatrix = None
        if self.__markerScale is not None:
            scaleMatrix = Matrix()
            scaleMatrix.setScale(Vector3(self.__markerScale, self.__markerScale, self.__markerScale))
            scaledMatrix = mathUtils.MatrixProviders.product(scaleMatrix, mp)
        if scaledMatrix is None:
            handle = self.__ownUI.addEntry(mp, zIndex)
        else:
            handle = self.__ownUI.addEntry(scaledMatrix, zIndex)
        entry = {'matrix': mp,
         'handle': handle}
        self.__entrieMarkers[uniqueID] = entry
        indexNumber = str(index) if index is not None else ''
        self.__ownUI.entryInvoke(entry['handle'], ('init', [markerType,
          marker,
          '',
          indexNumber,
          '']))
        if not isVisible:
            self.__ownUI.entryInvoke(entry['handle'], ('setVisible', [False]))
        if self.__markerScale is None:
            self.__parentUI.call('minimap.entryInited', [])



    def __delEntryMarker(self, uniqueID):
        entry = self.__entrieMarkers.pop(uniqueID, None)
        if entry is not None:
            self.__ownUI.delEntry(entry['handle'])



    def __delEntryLit(self, id):
        pass



    def __addEntry(self, id, location, doMark):
        battleCtx = g_sessionProvider.getCtx()
        if battleCtx.isObserver(id):
            return 
        arena = BigWorld.player().arena
        entry = dict()
        m = self.__getEntryMatrixByLocation(id, location)
        scaledMatrix = None
        if self.__markerScale is not None:
            scaleMatrix = Matrix()
            scaleMatrix.setScale(Vector3(self.__markerScale, self.__markerScale, self.__markerScale))
            scaledMatrix = mathUtils.MatrixProviders.product(scaleMatrix, m)
        if location == VehicleLocation.AOI_TO_FAR:
            self.__aoiToFarCallbacks[id] = BigWorld.callback(self.__AOI_TO_FAR_TIME, partial(self.__delEntry, id))
        entry['location'] = location
        entry['matrix'] = m
        if scaledMatrix is None:
            entry['handle'] = self.__ownUI.addEntry(m, self.zIndexManager.getVehicleIndex(id))
        else:
            entry['handle'] = self.__ownUI.addEntry(scaledMatrix, self.zIndexManager.getVehicleIndex(id))
        self.__entries[id] = entry
        entryVehicle = arena.vehicles[id]
        entityName = battleCtx.getPlayerEntityName(id, entryVehicle.get('team'))
        markerType = entityName.base
        entryName = entityName.name()
        markMarker = ''
        if not entityName.isFriend:
            if doMark and not g_sessionProvider.getCtx().isPlayerObserver():
                if 'SPG' in entryVehicle['vehicleType'].type.tags:
                    if not self.__isFirstEnemySPGMarkedById.has_key(id):
                        self.__isFirstEnemySPGMarkedById[id] = False
                    isFirstEnemySPGMarked = self.__isFirstEnemySPGMarkedById[id]
                    if not isFirstEnemySPGMarked:
                        markMarker = 'enemySPG'
                        self.__isFirstEnemySPGMarkedById[id] = True
                        self.__resetSPGMarkerTimoutCbckId = BigWorld.callback(5, partial(self.__resetSPGMarkerCallback, id))
                elif not self.__isFirstEnemyNonSPGMarked and markMarker == '':
                    if not len(self.__enemyEntries):
                        markMarker = 'firstEnemy'
                        self.__isFirstEnemyNonSPGMarked = True
                if markMarker != '':
                    BigWorld.player().soundNotifications.play('enemy_sighted_for_team')
            self.__enemyEntries[id] = entry
        if entryVehicle['vehicleType'] is not None:
            tags = set(entryVehicle['vehicleType'].type.tags & VEHICLE_CLASS_TAGS)
            if Minimap.__shorten != False:
                playerName = entryVehicle['name'][:Minimap.__shorten] + '..' if len(entryVehicle['name']) > Minimap.__shorten + 2 else entryVehicle['name']
            else:
                playerName = entryVehicle['name']
            if entryName == 'ally':
                if BigWorld.player().arena.bonusType in Minimap.__teamgame:
                    vShortName = playerName
                elif Minimap.__anametag == 'off':
                    vShortName = ''
                if Minimap.__anametag == 'Aoff' and BigWorld.player().arena.vehicles.get(BigWorld.player().playerVehicleID)['prebattleID'] != 0:
                    vShortName = ''
                elif Minimap.__anametag == 'player' or Minimap.__anametag == 'Aoff':
                    vShortName = playerName
                if Minimap.__anametag == 'tankplayer':
                    vShortName = '%s | %s' % (entryVehicle['vehicleType'].type.shortUserString, playerName)
                elif Minimap.__anametag == 'playertank':
                    vShortName = '%s | %s' % (playerName, entryVehicle['vehicleType'].type.shortUserString)
                elif Minimap.__anametag == 'ERROR':
                    vShortName = 'Invalid or missing Mmap.xml!'
                vShortName = entryVehicle['vehicleType'].type.shortUserString
            elif entryName == 'squadman':
                if Minimap.__snametag == 'off':
                    vShortName = ''
                elif Minimap.__snametag == 'player':
                    vShortName = playerName
                elif Minimap.__snametag == 'tankplayer':
                    vShortName = '%s | %s' % (entryVehicle['vehicleType'].type.shortUserString, playerName)
                elif Minimap.__snametag == 'playertank':
                    vShortName = '%s | %s' % (playerName, entryVehicle['vehicleType'].type.shortUserString)
                elif Minimap.__snametag == 'ERROR':
                    vShortName = 'Invalid or missing Mmap.xml!'
                else:
                    vShortName = entryVehicle['vehicleType'].type.shortUserString
            elif entryName == 'enemy':
                if Minimap.__enametag == 'off':
                    vShortName = ''
                elif Minimap.__enametag == 'player':
                    vShortName = playerName
                elif Minimap.__enametag == 'tankplayer':
                    vShortName = '%s | %s' % (entryVehicle['vehicleType'].type.shortUserString, playerName)
                elif Minimap.__enametag == 'playertank':
                    vShortName = '%s | %s' % (playerName, entryVehicle['vehicleType'].type.shortUserString)
                elif Minimap.__enametag == 'ERROR':
                    vShortName = 'Invalid or missing Mmap.xml!'
                else:
                    vShortName = entryVehicle['vehicleType'].type.shortUserString
            vShortName = entryVehicle['vehicleType'].type.shortUserString
        else:
            LOG_ERROR('Try to show minimap marker without vehicle info.')
            return 
        vClass = tags.pop() if len(tags) > 0 else ''
        if Minimap.__shownewicons == 'true' and entryVehicle['vehicleType'].type.level == 7 and vClass == 'AT-SPG':
            vClass = 'medium' + vClass
        if Minimap.__shownewicons == 'true' and entryVehicle['vehicleType'].type.level == 8 and vClass == 'AT-SPG':
            vClass = 'medium' + vClass
        if Minimap.__shownewicons == 'true' and entryVehicle['vehicleType'].type.level == 9 and vClass == 'AT-SPG':
            vClass = 'medium' + vClass
        if Minimap.__shownewicons == 'true' and entryVehicle['vehicleType'].type.level == 10 and vClass == 'AT-SPG':
            vClass = 'heavy' + vClass
        if Minimap.__shownewicons == 'true' and entryVehicle['vehicleType'].type.level == 7 and vClass == 'SPG':
            vClass = 'medium' + vClass
        if Minimap.__shownewicons == 'true' and entryVehicle['vehicleType'].type.level == 8 and vClass == 'SPG':
            vClass = 'medium' + vClass
        if Minimap.__shownewicons == 'true' and entryVehicle['vehicleType'].type.level == 9 and vClass == 'SPG':
            vClass = 'medium' + vClass
        if Minimap.__shownewicons == 'true' and entryVehicle['vehicleType'].type.level == 10 and vClass == 'SPG':
            vClass = 'heavy' + vClass
        if Minimap.__shownewicons == 'true' and entryVehicle['vehicleType'].type.level == 10 and vClass == 'heavyTank':
            vClass = 'super' + vClass
        if Minimap.__shownewicons == 'true' and entryVehicle['vehicleType'].type.level == 10 and vClass == 'mediumTank':
            vClass = 'super' + vClass
        self.__callEntryFlash(id, 'init', [markerType,
         entryName,
         vClass,
         markMarker,
         vShortName,
         Minimap.__msize,
         Minimap.__keyc,
         Minimap.__fontsize,
         Minimap.__shownames,
         Minimap.__calph,
         Minimap.__ccolor,
         Minimap.__lalph,
         Minimap.__lcolor,
         Minimap.__acolor,
         Minimap.__ecolor,
         Minimap.__scolor,
         Minimap.__shadstr,
         Minimap.__mapname,
         Minimap.__fifalph,
         Minimap.__fifcolor,
         Minimap.__dcolor,
         Minimap.__dalph,
         Minimap.__dstyle,
         Minimap.__cstyle,
         Minimap.__lstyle,
         Minimap.__xshift,
         Minimap.__yshift,
         Minimap.__csize,
         Minimap.__acsize,
         Minimap.__hlalph,
         Minimap.__hlcolor,
         Minimap.__hlstyle,
         Minimap.__acstyle,
         Minimap.__accolor,
         Minimap.__acalph,
         Minimap.__belem,
         Minimap.__selem,
         Minimap.__artcurcol,
         entryVehicle['accountDBID'],
         'false' if Minimap.__battletype == 'fallout' else Minimap.__lostmark,
         Minimap.__mrkscale,
         Minimap.__lostalph,
         Minimap.__lostcol,
         Minimap.__sshiftx,
         Minimap.__sshifty,
         Minimap.__cucirsize,
         Minimap.__cucirstyle,
         Minimap.__cucircolor,
         Minimap.__cuciralpha,
         Minimap.__binocs,
         Minimap.__binalpha,
         Minimap.__binstyle,
         Minimap.__bincolor])
        if g_ctfManager.isFlagBearer(id):
            self.__callEntryFlash(id, 'setVehicleClass', vClass + 'Flag')
        entry['markerType'] = markerType
        entry['entryName'] = entryName
        entry['vClass'] = vClass
        entry['vShortName'] = vShortName
        if self.__markerScale is None:
            self.__parentUI.call('minimap.entryInited', [])
        originalMatrix = self.__entries[id]['matrix']
        handle = self.__entries[id]['handle']
        self.scaleMarker(handle, originalMatrix, float(Minimap.__mrkscale))



    def __resetSPGMarkerCallback(self, id):
        self.__isFirstEnemySPGMarkedById[id] = False



    def updateEntries(self):
        self.__parentUI.call('minimap.updatePoints', [])
        for id in self.__entries:
            self.__callEntryFlash(id, 'update')

        for handle in self.__backMarkers:
            self.__ownUI.entryInvoke(handle, ('update', None))

        for entry in self.__entrieMarkers.itervalues():
            handle = entry['handle']
            self.__ownUI.entryInvoke(handle, ('update', None))




    def __callEntryFlash(self, id, methodName, args = None):
        if not self.__isStarted:
            return 
        if args is None:
            args = []
        if self.__entries.has_key(id):
            self.__ownUI.entryInvoke(self.__entries[id]['handle'], (methodName, args))
        elif id == BigWorld.player().playerVehicleID:
            if self.__ownEntry.has_key('handle'):
                self.__ownUI.entryInvoke(self.__ownEntry['handle'], (methodName, args))



    def __resetVehicleIfObserved(self, id):
        if self.__observedVehicleId > 0 and id == self.__observedVehicleId:
            self.__callEntryFlash(self.__observedVehicleId, 'setPostmortem', [False])
            if self.__entries.has_key(self.__observedVehicleId):
                entry = self.__entries[self.__observedVehicleId]
                if entry.has_key('handle'):
                    mp1 = self.__getEntryMatrixByLocation(self.__observedVehicleId, entry['location'])
                    self.__ownUI.entrySetMatrix(entry['handle'], mp1)
                    entry['matrix'] = mp1
            self.__observedVehicleId = -1



    def __resetCamera(self, mode, vehicleId = None):
        self.__currentMode = mode
        if self.__cameraHandle is not None:
            self.__ownUI.delEntry(self.__cameraHandle)
        if _isStrategic(mode):
            m = Math.WGStrategicAreaViewMP()
            m.source = BigWorld.camera().invViewMatrix
            m.baseScale = (1.0, 1.0)
        elif mode == MODE_ARCADE or mode == MODE_SNIPER:
            m = Math.WGCombinedMP()
            m.translationSrc = BigWorld.player().getOwnVehicleMatrix()
            m.rotationSrc = BigWorld.camera().invViewMatrix
        elif mode == MODE_POSTMORTEM:
            m = Math.WGCombinedMP()
            if vehicleId is not None:
                translationSrc = Math.WGTranslationOnlyMP()
                translationSrc.source = BigWorld.entities[vehicleId].matrix
            else:
                translationSrc = BigWorld.player().getOwnVehicleMatrix()
            m.translationSrc = translationSrc
            m.rotationSrc = BigWorld.camera().invViewMatrix
        elif mode == MODE_VIDEO:
            m = BigWorld.camera().invViewMatrix
        else:
            m = BigWorld.camera().invViewMatrix
        if mode == MODE_VIDEO:
            self.__cameraHandle = self.__ownUI.addEntry(m, self.zIndexManager.getIndexByName(CAMERA_VIDEO))
            self.__cameraMatrix = m
            self.__ownUI.entryInvoke(self.__cameraHandle, ('init', ['player', mode]))
        else:
            vehicle = BigWorld.entity(self.__playerVehicleID)
            self.__cameraHandle = self.__ownUI.addEntry(m, self.zIndexManager.getIndexByName(CAMERA_STRATEGIC if _isStrategic(mode) else CAMERA_NORMAL))
            self.__cameraMatrix = m
            cursorType = CURSOR_NORMAL
            if _isStrategic(mode):
                cursorType = CURSOR_STRATEGIC
            self.__ownUI.entryInvoke(self.__cameraHandle, ('gotoAndStop', [cursorType]))
        playerMarker = 'normal'
        if _isStrategic(mode):
            playerMarker = 'strategic'
        elif mode == MODE_POSTMORTEM or mode == MODE_VIDEO:
            self.__resetVehicleIfObserved(self.__observedVehicleId)
            playerMarker = mode
            if vehicleId is not None and vehicleId != BigWorld.player().playerVehicleID:
                self.__observedVehicleId = vehicleId
                self.__callEntryFlash(vehicleId, 'setPostmortem', [True])
                mp = BigWorld.player().getOwnVehicleMatrix()
                if self.__entries.has_key(vehicleId):
                    entry = self.__entries[vehicleId]
                    if entry.has_key('handle'):
                        mp1 = BigWorld.entities[vehicleId].matrix
                        self.__ownUI.entrySetMatrix(entry['handle'], mp1)
                        entry['matrix'] = mp1
            else:
                playerMarker += 'Camera'
                mp = Math.WGCombinedMP()
                mp.translationSrc = BigWorld.player().getOwnVehicleMatrix()
                mp.rotationSrc = BigWorld.camera().invViewMatrix
            if self.__ownEntry.has_key('handle'):
                self.__ownUI.entrySetMatrix(self.__ownEntry['handle'], mp)
            self.__callEntryFlash(BigWorld.player().playerVehicleID, 'init', ['player',
             playerMarker,
             '',
             '',
             '',
             Minimap.__msize,
             Minimap.__keyc,
             Minimap.__fontsize,
             Minimap.__shownames,
             Minimap.__calph,
             Minimap.__ccolor,
             Minimap.__lalph,
             Minimap.__lcolor,
             Minimap.__acolor,
             Minimap.__ecolor,
             Minimap.__scolor,
             Minimap.__shadstr,
             Minimap.__mapname,
             Minimap.__fifalph,
             Minimap.__fifcolor,
             Minimap.__dcolor,
             Minimap.__dalph,
             Minimap.__dstyle,
             Minimap.__cstyle,
             Minimap.__lstyle,
             Minimap.__xshift,
             Minimap.__yshift,
             Minimap.__csize,
             Minimap.__acsize,
             Minimap.__hlalph,
             Minimap.__hlcolor,
             Minimap.__hlstyle,
             Minimap.__acstyle,
             Minimap.__accolor,
             Minimap.__acalph,
             Minimap.__belem,
             Minimap.__selem,
             Minimap.__artcurcol,
             0,
             'false' if Minimap.__battletype == 'fallout' else Minimap.__lostmark,
             Minimap.__mrkscale,
             Minimap.__lostalph,
             Minimap.__lostcol,
             Minimap.__sshiftx,
             Minimap.__sshifty,
             Minimap.__cucirsize,
             Minimap.__cucirstyle,
             Minimap.__cucircolor,
             Minimap.__cuciralpha,
             Minimap.__binocs,
             Minimap.__binalpha,
             Minimap.__binstyle,
             Minimap.__bincolor])
        if not _isStrategic(mode) and self.__markerScale is not None:
            self.scaleMarker(self.__cameraHandle, self.__cameraMatrix, self.__markerScale)
        if self.__markerScale is None:
            self.__parentUI.call('minimap.entryInited', [])
        else:
            self.onScaleMarkers(None, float(Minimap.__mrkscale), self.__normalMarkerScale * 100)



    def __clearCamera(self, vehicleId):
        if self.__cameraHandle is not None:
            self.__ownUI.delEntry(self.__cameraHandle)
            self.__cameraHandle = None
            self.__cameraMatrix = None



    def isSpg(self):
        vehicle = BigWorld.entity(self.__playerVehicleID)
        if not vehicle:
            return False
        vTypeDesc = vehicle.typeDescriptor
        return 'SPG' in vTypeDesc.type.tags and vehicle_getter.hasYawLimits(vTypeDesc)



    def handleRepeatKeyEvent(self, event):
        if not MessengerEntry.g_instance.gui.isEditing(event):
            if GUI_SETTINGS.minimapSize:
                from game import convertKeyEvent
                cmdMap = CommandMapping.g_instance
                (isDown, key, mods, isRepeat,) = convertKeyEvent(event)
                if isRepeat and isDown and not BigWorld.isKeyDown(Keys.KEY_RSHIFT) and cmdMap.isFiredList((CommandMapping.CMD_MINIMAP_SIZE_DOWN, CommandMapping.CMD_MINIMAP_SIZE_UP), key):
                    self.handleKey(key)



    def handleKey(self, key):
        if GUI_SETTINGS.minimapSize:
            cmdMap = CommandMapping.g_instance
            if cmdMap.isFired(CommandMapping.CMD_MINIMAP_SIZE_DOWN, key):
                self.__parentUI.call('minimap.sizeDown', [])
            elif cmdMap.isFired(CommandMapping.CMD_MINIMAP_SIZE_UP, key):
                self.__parentUI.call('minimap.sizeUp', [])
            elif cmdMap.isFired(CommandMapping.CMD_MINIMAP_VISIBLE, key):
                self.__parentUI.call('minimap.visible', [])



    def showActionMarker(self, vehicleID, newState):
        self.__callEntryFlash(vehicleID, 'showAction', [newState])



    def __updateSettings(self):
        from account_helpers.settings_core.SettingsCore import g_settingsCore
        from account_helpers.settings_core import settings_constants
        setting = g_settingsCore.options.getSetting(settings_constants.GAME.SHOW_VEH_MODELS_ON_MAP)
        value = setting.get()
        valueName = setting.VEHICLE_MODELS_TYPES[value]
        self.__permanentNamesShow = valueName == setting.OPTIONS.ALWAYS
        self.__onAltNamesShow = valueName == setting.OPTIONS.ALT
        self.__showDirectionLine = g_settingsCore.getSetting(settings_constants.GAME.SHOW_VECTOR_ON_MAP)
        self.__showSectorLine = g_settingsCore.getSetting(settings_constants.GAME.SHOW_SECTOR_ON_MAP)



    def __onEquipmentMarkerShown(self, item, pos, dir, time):
        markerType = MARKER_TYPE.CONSUMABLE
        marker = item.getMarker()
        mp = Math.Matrix()
        mp.translation = pos
        uniqueID = '%s%s%d' % (markerType, marker, self.__markerIDGenerator.next())
        zIndex = self.zIndexManager.getMarkerIndex(uniqueID)
        if zIndex is not None:
            self.__addEntryMarker(markerType, marker, uniqueID, zIndex, mp)

            def callback():
                self.zIndexManager.clearMarkerIndex(uniqueID)
                self.__delEntryMarker(uniqueID)


            BigWorld.callback(int(time), callback)



    def __onFlagSpawning(self, flagID, respawnTime):
        flagType = FLAG_TYPE.COOLDOWN
        flagPos = self.__cfg['flagSpawnPoints'][flagID]['position']
        self.__addFlagMarker(flagID, flagPos, flagType)



    def __onFlagSpawnedAtBase(self, flagID, flagTeam, flagPos):
        flagType = self.__getFlagMarkerType(flagID, flagTeam)
        self.__delFlagMarker(flagID, FLAG_TYPE.COOLDOWN)
        self.__delFlagMarker(flagID, flagType)
        self.__addFlagMarker(flagID, flagPos, flagType)



    def __onFlagCapturedByVehicle(self, flagID, flagTeam, vehicleID):
        flagType = self.__getFlagMarkerType(flagID, flagTeam)
        self.__updateVehicleFlagState(vehicleID, True)
        self.__delFlagMarker(flagID, flagType)
        if vehicleID == self.__playerVehicleID:
            self.__toggleFlagCaptureAnimation(True)



    def __onFlagDroppedToGround(self, flagID, flagTeam, loserVehicleID, flagPos, respawnTime):
        flagType = self.__getFlagMarkerType(flagID, flagTeam)
        self.__updateVehicleFlagState(loserVehicleID)
        self.__addFlagMarker(flagID, flagPos, flagType)
        self.__delCarriedFlagMarker(loserVehicleID)
        if loserVehicleID == self.__playerVehicleID:
            self.__toggleFlagCaptureAnimation(False)



    def __onFlagAbsorbed(self, flagID, flagTeam, vehicleID, respawnTime):
        flagType = self.__getFlagMarkerType(flagID, flagTeam)
        self.__updateVehicleFlagState(vehicleID)
        self.__delFlagMarker(flagID, flagType)
        self.__delCarriedFlagMarker(vehicleID)
        if vehicleID == self.__playerVehicleID:
            self.__toggleFlagCaptureAnimation(False)



    def __onCarriedFlagsPositionUpdated(self, flagIDs):
        for flagID in flagIDs:
            flagInfo = g_ctfManager.getFlagInfo(flagID)
            vehID = flagInfo['vehicle']
            if vehID is not None and vehID != self.__playerVehicleID and vehID not in self.__entries:
                flagPos = g_ctfManager.getFlagMinimapPos(flagID)
                battleCtx = g_sessionProvider.getCtx()
                if battleCtx.isObserver(vehID):
                    marker = FLAG_TYPE.NEUTRAL
                else:
                    arena = BigWorld.player().arena
                    entryVehicle = arena.vehicles[vehID]
                    entityName = battleCtx.getPlayerEntityName(vehID, entryVehicle.get('team'))
                    marker = FLAG_TYPE.ALLY if entityName.isFriend else FLAG_TYPE.ENEMY
                uniqueID = self.__makeFlagUniqueID(flagID, marker)
                if uniqueID in self.__entrieMarkers:
                    item = self.__entrieMarkers[uniqueID]
                    mp = Math.Matrix()
                    mp.translation = flagPos
                    self.__ownUI.entrySetMatrix(item['handle'], mp)
                    item['matrix'] = mp
                else:
                    self.__addFlagMarker(flagID, flagPos, marker)
                self.__vehicleIDToFlagUniqueID[vehID] = uniqueID




    def __makeFlagUniqueID(self, flagID, marker):
        markerType = MARKER_TYPE.FLAG
        return '%s%s%d' % (markerType, marker, flagID)



    def __updateVehicleFlagState(self, vehicleID, isBearer = False):
        if vehicleID == self.__playerVehicleID:
            entryName = self.__ownEntry['entryName']
            self.__ownUI.entryInvoke(self.__ownEntry['handle'], ('setEntryName', [entryName + 'Flag' if isBearer else entryName]))
        elif vehicleID in self.__entries:
            entry = self.__entries[vehicleID]
            vClass = entry['vClass']
            self.__callEntryFlash(vehicleID, 'setVehicleClass', vClass + 'Flag' if isBearer else vClass)



    def __addFlagMarker(self, flagID, flagPos, marker, isVisible = True):
        uniqueID = self.__makeFlagUniqueID(flagID, marker)
        mp = Math.Matrix()
        mp.translation = flagPos
        if marker == FLAG_TYPE.ALLY_CAPTURE:
            zIndex = self.zIndexManager.getTeamPointIndex()
        elif marker == FLAG_TYPE.ALLY_CAPTURE_ANIMATION:
            zIndex = self.zIndexManager.getAnimationIndex(uniqueID)
        else:
            zIndex = self.zIndexManager.getFlagIndex(uniqueID)
        if zIndex is not None:
            self.__addEntryMarker(MARKER_TYPE.FLAG, marker, uniqueID, zIndex, mp, isVisible)



    def __delFlagMarker(self, flagID, marker):
        uniqueID = self.__makeFlagUniqueID(flagID, marker)
        if marker == FLAG_TYPE.ALLY_CAPTURE_ANIMATION:
            self.zIndexManager.clearAnimationIndex(uniqueID)
        elif marker != FLAG_TYPE.ALLY_CAPTURE:
            self.zIndexManager.clearFlagIndex(uniqueID)
        self.__delEntryMarker(uniqueID)



    def __delCarriedFlagMarker(self, vehicleID):
        uniqueID = self.__vehicleIDToFlagUniqueID.pop(vehicleID, None)
        if uniqueID is not None:
            self.zIndexManager.clearFlagIndex(uniqueID)
            self.__delEntryMarker(uniqueID)



    def __addFlagCaptureMarkers(self, isCarried = False):
        player = BigWorld.player()
        currentTeam = player.team
        playerVehID = getPlayerVehicleID()
        isSquadMan = g_sessionProvider.getArenaDP().isSquadMan(playerVehID)
        for (pointIndex, point,) in enumerate(self.__cfg['flagAbsorptionPoints']):
            position = point['position']
            isMyTeam = isSquadMan and point['team'] in (NEUTRAL_TEAM, currentTeam)
            marker = FLAG_TYPE.ALLY_CAPTURE if isMyTeam else FLAG_TYPE.ENEMY_CAPTURE
            self.__addFlagMarker(pointIndex, position, marker, not isMyTeam or not isCarried)
            if isMyTeam:
                self.__addFlagMarker(pointIndex, position, FLAG_TYPE.ALLY_CAPTURE_ANIMATION, isCarried)




    def __toggleFlagCaptureAnimation(self, isCarried = False):
        player = BigWorld.player()
        currentTeam = player.team
        playerVehID = getPlayerVehicleID()
        isSquadMan = g_sessionProvider.getArenaDP().isSquadMan(playerVehID)
        for (pointIndex, point,) in enumerate(self.__cfg['flagAbsorptionPoints']):
            if isSquadMan and point['team'] in (NEUTRAL_TEAM, currentTeam):
                captureUniqueID = self.__makeFlagUniqueID(pointIndex, FLAG_TYPE.ALLY_CAPTURE)
                captureEntry = self.__entrieMarkers.get(captureUniqueID)
                self.__ownUI.entryInvoke(captureEntry['handle'], ('setVisible', [not isCarried]))
                captureAnumationUniqueID = self.__makeFlagUniqueID(pointIndex, FLAG_TYPE.ALLY_CAPTURE_ANIMATION)
                captureAnimationEntry = self.__entrieMarkers.get(captureAnumationUniqueID)
                self.__ownUI.entryInvoke(captureAnimationEntry['handle'], ('setVisible', [isCarried]))




    def __getFlagMarkerType(self, flagID, flagTeam = 0):
        player = BigWorld.player()
        currentTeam = player.team
        if flagTeam > 0:
            if flagTeam == currentTeam:
                return FLAG_TYPE.ALLY
            return FLAG_TYPE.ENEMY
        return FLAG_TYPE.NEUTRAL



    def __onRepairPointStateChanged(self, repairPointID, action, timeLeft = 0):
        if repairPointID not in self.__points['repair']:
            LOG_ERROR('Got repair point state changed for not available repair point: ', repairPointID, action, timeLeft)
            return 
        if action in (REPAIR_POINT_ACTION.START_REPAIR, REPAIR_POINT_ACTION.COMPLETE_REPAIR, REPAIR_POINT_ACTION.BECOME_READY):
            (point, pointCooldown,) = self.__points['repair'][repairPointID]
            (pointVisible, pointCooldownVisible,) = (True, False) if action != REPAIR_POINT_ACTION.COMPLETE_REPAIR else (False, True)
            self.__ownUI.entryInvoke(point.handle, ('setVisible', [pointVisible]))
            self.__ownUI.entryInvoke(pointCooldown.handle, ('setVisible', [pointCooldownVisible]))



    def __onMinimapFeedbackReceived(self, eventID, entityID, value):
        if eventID == FEEDBACK_EVENT_ID.MINIMAP_MARK_CELL:
            self.markCell(*value)
        elif eventID == FEEDBACK_EVENT_ID.MINIMAP_SHOW_MARKER:
            self.showActionMarker(entityID, value)



    def __makeResourcePointUniqueID(self, pointID):
        markerType = MARKER_TYPE.RESOURCE_POINT
        return '%s%d' % (markerType, pointID)



    def __addResourcePointMarker(self, pointID, pointPos, state):
        uniqueID = self.__makeResourcePointUniqueID(pointID)
        mp = Math.Matrix()
        mp.translation = pointPos
        self.__addEntryMarker(MARKER_TYPE.RESOURCE_POINT, state, uniqueID, self.zIndexManager.getTeamPointIndex(), mp, index=pointID)



    def __delResourcePointMarker(self, pointID):
        uniqueID = self.__makeResourcePointUniqueID(pointID)
        self.__delEntryMarker(uniqueID)



    def __setResourcePointState(self, pointID, state):
        uniqueID = self.__makeResourcePointUniqueID(pointID)
        entry = self.__entrieMarkers[uniqueID]
        self.__ownUI.entryInvoke(entry['handle'], ('setEntryName', [state]))



    def __onResPointIsFree(self, pointID):
        self.__setResourcePointState(pointID, RESOURCE_POINT_TYPE.READY)



    def __onResPointCooldown(self, pointID, serverTime):
        self.__setResourcePointState(pointID, RESOURCE_POINT_TYPE.COOLDOWN)



    def __onResPointCaptured(self, pointID, team):
        state = _CAPTURE_STATE_BY_TEAMS[g_sessionProvider.getArenaDP().isAllyTeam(team)]
        self.__setResourcePointState(pointID, state)



    def __onResPointCapturedLocked(self, pointID, team):
        state = _CAPTURE_FROZEN_STATE_BY_TEAMS[g_sessionProvider.getArenaDP().isAllyTeam(team)]
        self.__setResourcePointState(pointID, state)



    def __onResPointBlocked(self, pointID):
        self.__setResourcePointState(pointID, RESOURCE_POINT_TYPE.CONFLICT)




class EntryInfo(object):

    def __init__(self, handle, matrix):
        self.__handle = handle
        self.__matrix = matrix



    @property
    def handle(self):
        return self.__handle



    @property
    def matrix(self):
        return self.__matrix




class MinimapZIndexManager(object):
    _BASES_RANGE = (0, 99)
    _BACK_ICONS_RANGE = (100, 124)
    _MARKER_RANGE = (200, 299)
    _DEAD_VEHICLE_RANGE = (300, 349)
    _VEHICLE_RANGE = (350, 399)
    _FLAG_RANGE = (400, 449)
    _ANIMATION_RANGE = (450, 500)
    _FIXED_INDEXES = {CAMERA_NORMAL: 1000,
     'self': 1001,
     CAMERA_STRATEGIC: 1002,
     'cell': 1003,
     CAMERA_VIDEO: 1004}

    def __init__(self):
        self.__indexes = {}
        self.__indexesDead = {}
        self.__lastPointIndex = MinimapZIndexManager._BASES_RANGE[0]
        self.__lastVehIndex = MinimapZIndexManager._VEHICLE_RANGE[0]
        self.__lastDeadVehIndex = MinimapZIndexManager._DEAD_VEHICLE_RANGE[0]
        self.__lastBackIconIndex = MinimapZIndexManager._BACK_ICONS_RANGE[0]
        self.__markers = {}
        self.__flags = {}
        self.__animations = {}



    def getTeamPointIndex(self):
        self.__lastPointIndex += 1
        return self.__lastPointIndex



    def getVehicleIndex(self, id):
        if id not in self.__indexes:
            self.__indexes[id] = self.__lastVehIndex
            self.__lastVehIndex += 1
        return self.__indexes[id]



    def getDeadVehicleIndex(self, id):
        if id not in self.__indexesDead:
            self.__indexesDead[id] = self.__lastDeadVehIndex
            self.__lastDeadVehIndex += 1
        return self.__indexesDead[id]



    def getBackIconIndex(self, id):
        if id not in self.__indexes:
            self.__indexes[id] = self.__lastBackIconIndex
            self.__lastBackIconIndex += 1
        return self.__indexes[id]



    def getMarkerIndex(self, id):
        index = findFirst(lambda idx: idx not in self.__markers.values(), range(*self._MARKER_RANGE))
        if index is not None:
            self.__markers[id] = index
        return index



    def clearMarkerIndex(self, id):
        if id in self.__markers:
            del self.__markers[id]



    def getFlagIndex(self, id):
        index = findFirst(lambda idx: idx not in self.__flags.values(), range(*self._FLAG_RANGE))
        if index is not None:
            self.__flags[id] = index
        return index



    def clearFlagIndex(self, id):
        if id in self.__flags:
            del self.__flags[id]



    def getAnimationIndex(self, id):
        index = findFirst(lambda idx: idx not in self.__animations.values(), range(*self._ANIMATION_RANGE))
        if index is not None:
            self.__animations[id] = index
        return index



    def clearAnimationIndex(self, id):
        if id in self.__animations:
            del self.__animations[id]



    def getIndexByName(self, name):
        return MinimapZIndexManager._FIXED_INDEXES[name]
