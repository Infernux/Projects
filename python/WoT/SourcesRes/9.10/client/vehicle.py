# 2015.01.14 13:32:41 CET
import BigWorld
import Math
import functools
import weakref
import random
from itertools import izip
from AvatarInputHandler import ShakeReason
import SoundGroups
from VehicleEffects import DamageFromShotDecoder
from debug_utils import *
import constants
from constants import VEHICLE_HIT_EFFECT
import helpers
from helpers.EffectMaterialCalculation import calcSurfaceMaterialNearPoint
from items import vehicles
import VehicleAppearance
from gui import game_control
from gui.WindowsManager import g_windowsManager
import AreaDestructibles
import DestructiblesCache
import math
import nations
import physics_shared
import ArenaType
import BattleReplay
import TriggersManager
from TriggersManager import TRIGGER_TYPE
from ModelHitTester import segmentMayHitVehicle, SegmentCollisionResult
from gun_rotation_shared import decodeGunAngles
from constants import DESTRUCTIBLE_MATKIND, SPT_MATKIND
from material_kinds import EFFECT_MATERIAL_INDEXES_BY_IDS, EFFECT_MATERIAL_INDEXES_BY_NAMES, EFFECT_MATERIALS

class Vehicle(BigWorld.Entity):
    hornMode = property(lambda self: self.__hornMode)
    isEnteringWorld = property(lambda self: self.__isEnteringWorld)
    isTurretDetached = property(lambda self: self.health == constants.SPECIAL_VEHICLE_HEALTH.TURRET_DETACHED and self.__turretDetachmentConfirmed)
    isTurretMarkedForDetachment = property(lambda self: self.health == constants.SPECIAL_VEHICLE_HEALTH.TURRET_DETACHED)
    isTurretDetachmentConfirmationNeeded = property(lambda self: not self.__turretDetachmentConfirmed)

    def __init__(self):
        self.proxy = weakref.proxy(self)
        self.extras = {}
        self.typeDescriptor = None
        self.appearance = None
        self.isPlayer = False
        self.isStarted = False
        self.__prereqs = None
        self.__hornSounds = (None,)
        self.__hornMode = ''
        self.__stopHornSoundCallback = None
        self.wgPhysics = None
        self.__isEnteringWorld = False
        self.__turretDetachmentConfirmed = False



    def reload(self):
        wasStarted = self.isStarted
        if self.isStarted:
            self.stopVisual()
        vehicles.reload()
        self.typeDescriptor = vehicles.VehicleDescr(compactDescr=self.publicInfo.compDescr)
        if wasStarted:
            self.appearance = VehicleAppearance.VehicleAppearance()
            self.appearance.prerequisites(self)
            self.startVisual()



    def prerequisites(self):
        if self.typeDescriptor is not None:
            return ()
        prereqs = []
        descr = vehicles.VehicleDescr(compactDescr=_stripVehCompDescrIfRoaming(self.publicInfo.compDescr))
        self.typeDescriptor = descr
        prereqs += descr.prerequisites()
        for hitTester in descr.getHitTesters():
            if hitTester.bspModelName is not None and not hitTester.isBspModelLoaded():
                prereqs.append(hitTester.bspModelName)

        self.appearance = VehicleAppearance.VehicleAppearance()
        prereqs += self.appearance.prerequisites(self)
        return prereqs



    def onEnterWorld(self, prereqs):
        self.__isEnteringWorld = True
        descr = self.typeDescriptor
        descr.keepPrereqs(prereqs)
        self.__prereqs = prereqs
        self.__prevDamageStickers = frozenset()
        self.__prevPublicStateModifiers = frozenset()
        self.targetFullBounds = True
        player = BigWorld.player()
        for hitTester in descr.getHitTesters():
            hitTester.loadBspModel()
            player.hitTesters.add(hitTester)

        player.initSpace()
        player.vehicle_onEnterWorld(self)
        self.__isEnteringWorld = False



    def onLeaveWorld(self):
        self.__stopExtras()
        BigWorld.player().vehicle_onLeaveWorld(self)
        assert not self.isStarted



    def showShooting(self, burstCount, isPredictedShot = False):
        if not self.isStarted:
            return 
        if not isPredictedShot and self.isPlayer and not BigWorld.player().isWaitingForShot:
            if not BattleReplay.g_replayCtrl.isPlaying:
                return 
        extra = self.typeDescriptor.extrasDict['shoot']
        data = self.extras.get(extra.index)
        if data is not None:
            extra.stop(data)
        extra.startFor(self, burstCount)
        if not isPredictedShot and self.isPlayer:
            BigWorld.player().cancelWaitingForShot()



    def showDamageFromShot(self, attackerID, points, effectsIndex):
        if not self.isStarted:
            return 
        effectsDescr = vehicles.g_cache.shotEffects[effectsIndex]
        (maxHitEffectCode, decodedPoints,) = DamageFromShotDecoder.decodeHitPoints(points, self.typeDescriptor)
        hasPiercedHit = DamageFromShotDecoder.hasDamaged(maxHitEffectCode)
        for shotPoint in decodedPoints:
            showFullscreenEffs = self.isPlayer and self.isAlive()
            (keyPoints, effects, _,) = effectsDescr[shotPoint.hitEffectGroup]
            self.appearance.modelsDesc[shotPoint.componentName]['boundEffects'].addNew(shotPoint.matrix, effects, keyPoints, isPlayer=self.isPlayer, showShockWave=showFullscreenEffs, showFlashBang=showFullscreenEffs, entity_id=self.id)

        if decodedPoints:
            firstHitPoint = decodedPoints[0]
            compMatrix = Math.Matrix(self.appearance.modelsDesc[firstHitPoint.componentName]['model'].matrix)
            firstHitDirLocal = firstHitPoint.matrix.applyToAxis(2)
            firstHitDir = compMatrix.applyVector(firstHitDirLocal)
            self.appearance.receiveShotImpulse(firstHitDir, effectsDescr['targetImpulse'])
            self.appearance.executeHitVibrations(maxHitEffectCode)
            player = BigWorld.player()
            player.inputHandler.onVehicleShaken(self, compMatrix.translation, firstHitDir, effectsDescr['caliber'], ShakeReason.HIT if hasPiercedHit else ShakeReason.HIT_NO_DAMAGE)
        if not self.isAlive():
            return 
        if attackerID == BigWorld.player().playerVehicleID and maxHitEffectCode is not None and not self.isPlayer:
            marker = getattr(self, 'marker', None)
            if marker is not None:
                manager = g_windowsManager.battleWindow.vMarkersManager
                manager.updateMarkerState(marker, 'hit_pierced' if hasPiercedHit else 'hit')



    def showDamageFromExplosion(self, attackerID, center, effectsIndex):
        if not self.isStarted:
            return 
        impulse = vehicles.g_cache.shotEffects[effectsIndex]['targetImpulse']
        dir = self.position - center
        dir.normalise()
        self.appearance.receiveShotImpulse(dir, impulse / 4.0)
        self.appearance.executeHitVibrations(VEHICLE_HIT_EFFECT.MAX_CODE + 1)
        if not self.isAlive():
            return 
        if self.id == attackerID:
            return 
        player = BigWorld.player()
        player.inputHandler.onVehicleShaken(self, center, dir, vehicles.g_cache.shotEffects[effectsIndex]['caliber'], ShakeReason.SPLASH)
        if attackerID == BigWorld.player().playerVehicleID:
            marker = getattr(self, 'marker', None)
            if marker is not None:
                manager = g_windowsManager.battleWindow.vMarkersManager
                manager.updateMarkerState(marker, 'hit_pierced')



    def showVehicleCollisionEffect(self, pos, delta_spd):
        if not self.isStarted:
            return 
        if delta_spd < 3:
            self.showCollisionEffect(pos, 'collisionVehicleLight')
        else:
            mass = self.typeDescriptor.physics['weight']
            if mass < 18000:
                self.showCollisionEffect(pos, 'collisionVehicleHeavy1')
            elif mass < 46000:
                self.showCollisionEffect(pos, 'collisionVehicleHeavy2')
            else:
                self.showCollisionEffect(pos, 'collisionVehicleHeavy3')
        self.appearance.executeRammingVibrations()



    def showCollisionEffect(self, hitPos, collisionEffectName = 'collisionVehicle', collisionNormal = None):
        hullAppearance = self.appearance.modelsDesc['hull']
        invWorldMatrix = Math.Matrix(hullAppearance['model'].matrix)
        invWorldMatrix.invert()
        rot = Math.Matrix()
        if collisionNormal is None:
            rot.setRotateYPR((random.uniform(-3.14, 3.14), random.uniform(-1.5, 1.5), 0.0))
        else:
            rot.setRotateYPR((0, 0, 0))
        mat = Math.Matrix()
        mat.setTranslate(hitPos)
        mat.preMultiply(rot)
        mat.postMultiply(invWorldMatrix)
        effectsList = self.typeDescriptor.type.effects.get(collisionEffectName, [])
        if effectsList:
            (keyPoints, effects, _,) = random.choice(effectsList)
            hullAppearance['boundEffects'].addNew(mat, effects, keyPoints, entity=self, surfaceNormal=collisionNormal)



    def set_damageStickers(self, prev = None):
        if self.isStarted:
            prev = self.__prevDamageStickers
            curr = frozenset(self.damageStickers)
            self.__prevDamageStickers = curr
            for sticker in prev.difference(curr):
                self.appearance.removeDamageSticker(sticker)

            descr = self.typeDescriptor
            for sticker in curr.difference(prev):
                self.appearance.addDamageSticker(sticker, *DamageFromShotDecoder.decodeSegment(sticker, descr))




    def set_publicStateModifiers(self, prev = None):
        if self.isStarted:
            prev = self.__prevPublicStateModifiers
            curr = frozenset(self.publicStateModifiers)
            self.__prevPublicStateModifiers = curr
            self.__updateModifiers(curr.difference(prev), prev.difference(curr))



    def set_engineMode(self, prev):
        if self.isStarted:
            self.appearance.changeEngineMode(self.engineMode, True)



    def set_isStrafing(self, prev):
        if isinstance(self.filter, BigWorld.WGVehicleFilter):
            self.filter.isStrafing = self.isStrafing



    def set_gunAnglesPacked(self, prev):
        if isinstance(self.filter, BigWorld.WGVehicleFilter):
            (yaw, pitch,) = decodeGunAngles(self.gunAnglesPacked, self.typeDescriptor.gun['pitchLimits']['absolute'])
            self.filter.syncGunAngles(yaw, pitch)



    def set_health(self, prev):
        if self.health > 0 and prev <= 0:
            self.health = prev



    def set_isCrewActive(self, prev):
        if self.isStarted:
            self.appearance.onVehicleHealthChanged()
            if not self.isPlayer:
                marker = getattr(self, 'marker', None)
                if marker is not None:
                    g_windowsManager.battleWindow.vMarkersManager.onVehicleHealthChanged(marker, self.health)
            if not self.isCrewActive and self.health > 0:
                self.__onVehicleDeath()



    def onHealthChanged(self, newHealth, attackerID, attackReasonID):
        if newHealth > 0 and self.health <= 0:
            return 
        if not self.isStarted:
            return 
        if not self.isPlayer:
            marker = getattr(self, 'marker', None)
            if marker is not None:
                g_windowsManager.battleWindow.vMarkersManager.onVehicleHealthChanged(marker, newHealth, attackerID, attackReasonID)
        self.appearance.onVehicleHealthChanged()
        if self.health <= 0 and self.isCrewActive:
            self.__onVehicleDeath()



    def showAmmoBayEffect(self, mode, fireballVolume, projectedTurretSpeed):
        self.appearance.showAmmoBayEffect(mode, fireballVolume)



    def onPushed(self, x, z):
        try:
            distSqr = BigWorld.player().position.distSqrTo(self.position)
            if distSqr > 1600.0:
                self.filter.setPosition(x, z)
        except:
            pass



    def showRammingEffect(self, energy, point):
        if energy < 600:
            self.showCollisionEffect(point, 'rammingCollisionLight')
        else:
            self.showCollisionEffect(point, 'rammingCollisionHeavy')



    def onStaticCollision(self, energy, point, normal, miscFlags):
        if not self.isStarted:
            return 
        self.appearance.stopSwinging()
        BigWorld.player().inputHandler.onVehicleCollision(self, self.getSpeed())
        isTrackCollision = bool(miscFlags & 1)
        isSptCollision = bool(miscFlags >> 1 & 1)
        isSptDestroyed = bool(miscFlags >> 2 & 1)
        hitPoint = point
        surfNormal = normal
        if not isSptCollision:
            surfaceMaterial = calcSurfaceMaterialNearPoint(point, normal, self.spaceID)
            (hitPoint, surfNormal, matKind, effectIdx,) = surfaceMaterial
        elif isSptDestroyed:
            return 
        hitPoint = point
        matKind = SPT_MATKIND.SOLID
        effectIdx = EFFECT_MATERIAL_INDEXES_BY_NAMES['wood']
        self.__showStaticCollisionEffect(energy, matKind, effectIdx, hitPoint, surfNormal, isTrackCollision)



    def getComponents(self):
        res = []
        vehicleDescr = self.typeDescriptor
        m = Math.Matrix()
        m.setIdentity()
        res.append((vehicleDescr.chassis, m, True))
        hullOffset = vehicleDescr.chassis['hullPosition']
        m = Math.Matrix()
        m.setTranslate(-hullOffset)
        res.append((vehicleDescr.hull, m, True))
        turretYaw = Math.Matrix(self.appearance.turretMatrix).yaw
        turretMatrix = Math.Matrix()
        turretMatrix.setTranslate(-hullOffset - vehicleDescr.hull['turretPositions'][0])
        m = Math.Matrix()
        m.setRotateY(-turretYaw)
        turretMatrix.postMultiply(m)
        res.append((vehicleDescr.turret, turretMatrix, not self.isTurretDetached))
        gunPitch = Math.Matrix(self.appearance.gunMatrix).pitch
        gunMatrix = Math.Matrix()
        gunMatrix.setTranslate(-vehicleDescr.turret['gunPosition'])
        m = Math.Matrix()
        m.setRotateX(-gunPitch)
        gunMatrix.postMultiply(m)
        gunMatrix.preMultiply(turretMatrix)
        res.append((vehicleDescr.gun, gunMatrix, not self.isTurretDetached))
        return res



    def segmentMayHitVehicle(self, startPoint, endPoint):
        return segmentMayHitVehicle(self.typeDescriptor, startPoint, endPoint, self.position)



    def collideSegment(self, startPoint, endPoint, skipGun = False):
        filterMethod = getattr(self.filter, 'segmentMayHitEntity', self.segmentMayHitVehicle)
        if not filterMethod(startPoint, endPoint):
            return 
        worldToVehMatrix = Math.Matrix(self.model.matrix)
        worldToVehMatrix.invert()
        startPoint = worldToVehMatrix.applyPoint(startPoint)
        endPoint = worldToVehMatrix.applyPoint(endPoint)
        res = None
        for (compDescr, compMatrix, isAttached,) in self.getComponents():
            if not isAttached:
                continue
            if skipGun and compDescr.get('itemTypeName') == 'vehicleGun':
                continue
            collisions = compDescr['hitTester'].localHitTest(compMatrix.applyPoint(startPoint), compMatrix.applyPoint(endPoint))
            if collisions is None:
                continue
            for (dist, _, hitAngleCos, matKind,) in collisions:
                if res is None or res[0] >= dist:
                    matInfo = compDescr['materials'].get(matKind)
                    res = SegmentCollisionResult(dist, hitAngleCos, matInfo.armor if matInfo is not None else 0)


        return res



    def isAlive(self):
        return self.isCrewActive and self.health > 0



    def getSpeed(self):
        return self.filter.speedInfo.value[0]



    def startVisual(self):
        assert not self.isStarted
        avatar = BigWorld.player()
        self.appearance.preStart(self.typeDescriptor)
        self.appearance.start(self, self.__prereqs)
        self.__prereqs = None
        self.appearance.changeEngineMode(self.engineMode)
        self.appearance.onVehicleHealthChanged()
        if self.isPlayer:
            if self.isAlive():
                BigWorld.wgAddEdgeDetectEntity(self, 0, True)
                self.appearance.setupGunMatrixTargets(avatar.gunRotator)
            self.filter.allowStrafeCompensation = False
        else:
            self.marker = g_windowsManager.battleWindow.vMarkersManager.createMarker(self.proxy)
            self.filter.allowStrafeCompensation = True
        self.isStarted = True
        self.set_publicStateModifiers()
        self.set_damageStickers()
        if not self.isAlive():
            self.__onVehicleDeath(True)
        if self.isTurretMarkedForDetachment:
            self.confirmTurretDetachment()
        minimap = g_windowsManager.battleWindow.minimap
        minimap.notifyVehicleStart(self.id)
        self.__startWGPhysics()
        if self is BigWorld.player().getVehicleAttached():
            nationId = self.typeDescriptor.type.id[0]
            SoundGroups.g_instance.soundModes.setCurrentNation(nations.NAMES[nationId])



    def stopVisual(self):
        assert self.isStarted
        if self.isPlayer:
            BigWorld.wgDelEdgeDetectEntity(self)
        self.__stopExtras()
        if hasattr(self, 'marker'):
            manager = g_windowsManager.battleWindow.vMarkersManager
            manager.destroyMarker(self.marker)
            self.marker = -1
        self.appearance.destroy()
        self.appearance = None
        self.isStarted = False
        minimap = g_windowsManager.battleWindow.minimap
        minimap.notifyVehicleStop(self.id)
        self.__stopWGPhysics()



    def showPlayerMovementCommand(self, flags):
        if not self.isStarted:
            return 
        powerMode = self.engineMode[0]
        if flags == 0 and powerMode != 0:
            self.appearance.changeEngineMode((1, 0))
            return 
        if flags != 0 and powerMode != 0:
            self.appearance.changeEngineMode((3, flags))
            return 



    def _isDestructibleMayBeBroken(self, chunkID, itemIndex, matKind, itemFilename, itemScale, vehSpeed):
        desc = AreaDestructibles.g_cache.getDescByFilename(itemFilename)
        if desc is None:
            return False
        ctrl = AreaDestructibles.g_destructiblesManager.getController(chunkID)
        if ctrl is None:
            return False
        if ctrl.isDestructibleBroken(itemIndex, matKind, desc['type']):
            return True
        mass = self.typeDescriptor.physics['weight']
        instantDamage = 0.5 * mass * vehSpeed * vehSpeed * 0.00015
        if desc['type'] == DestructiblesCache.DESTR_TYPE_STRUCTURE:
            moduleDesc = desc['modules'].get(matKind)
            if moduleDesc is None:
                return False
            refHealth = moduleDesc['health']
        else:
            unitMass = AreaDestructibles.g_cache.unitVehicleMass
            instantDamage *= math.pow(mass / unitMass, desc['kineticDamageCorrection'])
            refHealth = desc['health']
        return DestructiblesCache.scaledDestructibleHealth(itemScale, refHealth) < instantDamage



    def __showStaticCollisionEffect(self, energy, matKind, effectIdx, hitPoint, normal, isTrackCollision):
        heavyVelocities = self.typeDescriptor.type.heavyCollisionEffectVelocities
        heavyEnergy = heavyVelocities['track'] if isTrackCollision else heavyVelocities['hull']
        heavyEnergy = 0.5 * heavyEnergy * heavyEnergy
        postfix = '%sCollisionLight' if energy < heavyEnergy else '%sCollisionHeavy'
        effectName = ''
        if effectIdx < len(EFFECT_MATERIALS):
            effectName = EFFECT_MATERIALS[effectIdx]
        effectName = postfix % effectName
        if effectName in self.typeDescriptor.type.effects:
            self.showCollisionEffect(hitPoint, effectName, normal)
        if self.isPlayer:
            self.appearance.executeRammingVibrations(matKind)



    def __startWGPhysics(self):
        typeDescr = self.typeDescriptor
        self.wgPhysics = BigWorld.WGVehiclePhysics()
        physics = self.wgPhysics
        physics_shared.initVehiclePhysics(physics, typeDescr)
        (arenaMinBound, arenaMaxBound,) = ((-10000, -10000), (10000, 10000))
        physics.setArenaBounds(arenaMinBound, arenaMaxBound)
        physics.enginePower = typeDescr.physics['enginePower'] / 1000.0
        physics.owner = weakref.ref(self)
        physics.staticMode = False
        physics.movementSignals = 0
        physics.damageDestructibleCb = None
        physics.destructibleHealthRequestCb = None
        self.filter.setVehiclePhysics(physics)
        player = BigWorld.player()
        physics.visibilityMask = ArenaType.getVisibilityMask(player.arenaTypeID >> 16)
        (yaw, pitch,) = decodeGunAngles(self.gunAnglesPacked, typeDescr.gun['pitchLimits']['absolute'])
        self.filter.syncGunAngles(yaw, pitch)
        self.appearance.fashion.placingCompensationMatrix = self.filter.placingCompensationMatrix



    def __stopWGPhysics(self):
        self.wgPhysics.damageDestructibleCb = None
        self.wgPhysics.destructibleHealthRequestCb = None
        self.wgPhysics = None



    def __stopExtras(self):
        extraTypes = self.typeDescriptor.extras
        for (index, data,) in self.extras.items():
            extraTypes[index].stop(data)

        if self.extras:
            LOG_CODEPOINT_WARNING()



    def __updateModifiers(self, addedExtras, removedExtras):
        descr = self.typeDescriptor
        for idx in removedExtras:
            data = self.extras.get(idx)
            if data is not None:
                data['extra'].stop(data)
            else:
                LOG_WARNING('Attempt to remove non-existent EntityExtra data', self.typeDescriptor.name, self.typeDescriptor.extras[idx].name)

        for idx in addedExtras:
            if idx < 0 or idx >= len(self.typeDescriptor.extras):
                LOG_WARNING('Attempt to add unknown EntityExtra', self.typeDescriptor.name, idx)
            else:
                try:
                    self.typeDescriptor.extras[idx].startFor(self)
                except Exception:
                    LOG_CURRENT_EXCEPTION()




    def __onVehicleDeath(self, isDeadStarted = False):
        if not self.isPlayer:
            marker = getattr(self, 'marker', None)
            if marker is not None:
                manager = g_windowsManager.battleWindow.vMarkersManager
                manager.updateMarkerState(marker, 'dead', isDeadStarted)
        self.stopHornSound(True)
        TriggersManager.g_manager.fireTrigger(TRIGGER_TYPE.VEHICLE_DESTROYED, vehicleId=self.id)
        self.filter.velocityErrorCompensation = 100.0



    def playHornSound(self, hornID):
        if not self.isStarted:
            return 
        hornDesc = vehicles.g_cache.horns().get(hornID)
        if hornDesc is None:
            return 
        self.stopHornSound(True)
        self.__hornSounds = []
        self.__hornMode = hornDesc['mode']
        model = self.appearance.modelsDesc['turret']['model']
        for sndEventId in hornDesc['sounds']:
            snd = SoundGroups.g_instance.getSound(model, sndEventId)
            snd.volume *= self.typeDescriptor.type.hornVolumeFactor
            self.__hornSounds.append(snd)

        if self.__hornSounds[0] is not None:
            self.__hornSounds[0].play()
            if self.__hornMode == 'continuous' and hornDesc['maxDuration'] > 0:
                self.__stopHornSoundCallback = BigWorld.callback(hornDesc['maxDuration'], self.stopHornSound)



    def stopHornSound(self, forceSilence = False):
        if not forceSilence and self.__hornMode == 'twoSounds':
            if self.__hornSounds[1] is not None:
                self.__hornSounds[1].play()
        else:
            for snd in self.__hornSounds:
                if snd is not None:
                    snd.stop()

            self.__hornSounds = (None,)
        if self.__stopHornSoundCallback is not None:
            BigWorld.cancelCallback(self.__stopHornSoundCallback)
            self.__stopHornSoundCallback = None
        self.__hornMode = ''



    def isHornActive(self):
        if self.__hornMode == 'twoSounds':
            return True
        anySoundPlaying = False
        for snd in self.__hornSounds:
            if snd is not None:
                state = snd.state
                if state is not None and state.find('playing') != -1:
                    return True

        return False



    def confirmTurretDetachment(self):
        self.__turretDetachmentConfirmed = True
        if not self.isTurretDetached:
            LOG_ERROR('Vehicle::confirmTurretDetachment: Confirming turret detachment, though the turret is not detached')
        self.appearance.updateTurretVisibility()




def _stripVehCompDescrIfRoaming(vehCompDescr):
    if game_control.g_instance.roaming.isInRoaming():
        vehCompDescr = vehicles.stripCustomizationFromVehicleCompactDescr(vehCompDescr, True, True, False)[0]
    return vehCompDescr



+++ okay decompyling vehicle.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:32:41 CET
