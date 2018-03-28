# 2015.01.14 13:32:43 CET
import BigWorld
import Math
import weakref
import math
from AvatarInputHandler import AimingSystems
from AvatarInputHandler.CallbackDelayer import CallbackDelayer
from constants import SERVER_TICK_LENGTH, SHELL_TRAJECTORY_EPSILON_CLIENT, AIMING_MODE
import ProjectileMover
from projectile_trajectory import getShotAngles
from debug_utils import *
from math import pi, sin, cos, atan, atan2, sqrt, fmod
from projectile_trajectory import computeProjectileTrajectory
import BattleReplay
from gun_rotation_shared import calcPitchLimitsFromDesc
import SoundGroups
_ENABLE_TURRET_ROTATOR_SOUND = True
g__attachToCam = False

class VehicleGunRotator(object):
    __INSUFFICIENT_TIME_DIFF = 0.02
    __MAX_TIME_DIFF = 0.2
    __ROTATION_TICK_LENGTH = SERVER_TICK_LENGTH
    USE_LOCK_PREDICTION = True

    def __init__(self, avatar):
        self.__avatar = weakref.proxy(avatar)
        self.__isStarted = False
        self.__prevSentShotPoint = None
        self.__targetLastShotPoint = False
        self.__lastShotPoint = Math.Vector3(0, 0, 0)
        self.__shotPointSourceFunctor = self.__shotPointSourceFunctor_Default
        self.__maxTurretRotationSpeed = None
        self.__maxGunRotationSpeed = None
        self.__turretYaw = 0.0
        self.__gunPitch = 0.0
        self.__turretRotationSpeed = 0.0
        self.__dispersionAngle = 0.0
        self.__markerInfo = (Math.Vector3(0.0, 0.0, 0.0), Math.Vector3(0.0, 1.0, 0.0), 1.0)
        self.__clientMode = True
        self.__showServerMarker = False
        self.__time = None
        self.__timerID = None
        self.__turretMatrixAnimator = _MatrixAnimator(self.__avatar)
        self.__gunMatrixAnimator = _MatrixAnimator(self.__avatar)
        self.__isLocked = False
        self.estimatedTurretRotationTime = 0
        self.__turretRotationSoundEffect = _PlayerTurretRotationSoundEffect()
        BigWorld.player().inputHandler.onCameraChanged += self.__onCameraChanged
        g__attachToCam = False



    def init_sound(self):
        self.__turretRotationSoundEffect.init_sound()



    def destroy(self):
        self.stop()
        self.__turretMatrixAnimator.destroy(self.__avatar)
        self.__gunMatrixAnimator.destroy(self.__avatar)
        self.__avatar = None
        self.__shotPointSourceFunctor = None
        if self.__turretRotationSoundEffect is not None:
            self.__turretRotationSoundEffect.destroy()
            self.__turretRotationSoundEffect = None
        BigWorld.player().inputHandler.onCameraChanged -= self.__onCameraChanged



    def start(self):
        if self.__isStarted:
            return 
        if self.__maxTurretRotationSpeed is None:
            return 
        if not self.__avatar.isOnArena or not self.__avatar.isVehicleAlive:
            return 
        from account_helpers.settings_core.SettingsCore import g_settingsCore
        g_settingsCore.onSettingsChanged += self.applySettings
        self.showServerMarker = g_settingsCore.getSetting('useServerAim')
        self.__isStarted = True
        self.__updateGunMarker()
        self.__timerID = BigWorld.callback(self.__ROTATION_TICK_LENGTH, self.__onTick)
        if self.__clientMode:
            self.__time = BigWorld.time()
            if self.__showServerMarker:
                self.__avatar.inputHandler.showGunMarker2(True)



    def stop(self):
        if not self.__isStarted:
            return 
        from account_helpers.settings_core.SettingsCore import g_settingsCore
        g_settingsCore.onSettingsChanged -= self.applySettings
        if self.__timerID is not None:
            BigWorld.cancelCallback(self.__timerID)
            self.__timerID = None
        if self.__avatar.inputHandler is None:
            return 
        if self.__clientMode and self.__showServerMarker:
            self.__avatar.inputHandler.showGunMarker2(False)
        self.__isStarted = False
        if self.__turretRotationSoundEffect is not None:
            self.__turretRotationSoundEffect.destroy()
            self.__turretRotationSoundEffect = None



    def applySettings(self, diff):
        if 'useServerAim' in diff:
            self.showServerMarker = diff['useServerAim']



    def lock(self, isLocked):
        self.__isLocked = isLocked



    def update(self, turretYaw, gunPitch, maxTurretRotationSpeed, maxGunRotationSpeed):
        if self.__timerID is None or maxTurretRotationSpeed < self.__maxTurretRotationSpeed:
            self.__turretYaw = turretYaw
            self.__gunPitch = gunPitch
            self.__updateTurretMatrix(turretYaw, 0.0)
            self.__updateGunMatrix(gunPitch, 0.0)
        self.__maxTurretRotationSpeed = maxTurretRotationSpeed
        self.__maxGunRotationSpeed = maxGunRotationSpeed
        self.__turretRotationSpeed = 0.0
        self.__dispersionAngle = self.__avatar.getOwnVehicleShotDispersionAngle(0.0)
        self.start()



    def setShotPosition(self, shotPos, shotVec, dispersionAngle):
        if self.__clientMode and not self.__showServerMarker:
            return 
        self.__dispersionAngle = dispersionAngle
        if not self.__clientMode and VehicleGunRotator.USE_LOCK_PREDICTION:
            lockEnabled = BigWorld.player().inputHandler.getAimingMode(AIMING_MODE.TARGET_LOCK)
            if lockEnabled:
                predictedTargetPos = self.predictLockedTargetShotPoint()
                dirToTarget = predictedTargetPos - shotPos
                dirToTarget.normalise()
                shotDir = Math.Vector3(shotVec)
                shotDir.normalise()
                if shotDir.dot(dirToTarget) > 0.0:
                    return 
        (markerPos, markerDir, markerSize, collData,) = self.__getGunMarkerPosition(shotPos, shotVec, dispersionAngle)
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isRecording:
            replayCtrl.setGunMarkerParams(markerSize, markerPos, markerDir)
        if self.__clientMode and self.__showServerMarker:
            self.__avatar.inputHandler.updateGunMarker2(markerPos, markerDir, markerSize, SERVER_TICK_LENGTH, collData)
        if not self.__clientMode:
            self.__lastShotPoint = markerPos
            self.__avatar.inputHandler.updateGunMarker(markerPos, markerDir, markerSize, SERVER_TICK_LENGTH, collData)
            (self.__turretYaw, self.__gunPitch,) = getShotAngles(self.__avatar.vehicleTypeDescriptor, self.__avatar.getOwnVehicleMatrix(), (self.__turretYaw, self.__gunPitch), markerPos, True)
            descr = self.__avatar.vehicleTypeDescriptor
            turretYawLimits = descr.gun['turretYawLimits']
            closestLimit = self.__isOutOfLimits(self.__turretYaw, turretYawLimits)
            if closestLimit is not None:
                self.__turretYaw = closestLimit
            self.__updateTurretMatrix(self.__turretYaw, SERVER_TICK_LENGTH)
            self.__updateGunMatrix(self.__gunPitch, SERVER_TICK_LENGTH)
            self.__markerInfo = (markerPos, markerDir, markerSize)



    def predictLockedTargetShotPoint(self):
        autoAimVehicle = BigWorld.player().autoAimVehicle
        if autoAimVehicle is not None:
            autoAimPosition = Math.Vector3(autoAimVehicle.position)
            td = autoAimVehicle.typeDescriptor
            hullBox = td.hull['hitTester'].bbox
            middleX = (hullBox[0][0] + hullBox[1][0]) / 2.0
            middleZ = (hullBox[0][2] + hullBox[1][2]) / 2.0
            hullPosition = Math.Vector3(middleX, td.chassis['hullPosition'][1], middleZ)
            offset = td.hull['turretPositions'][0] / 2.0 + hullPosition
            autoAimPosition += Math.Matrix(autoAimVehicle.matrix).applyVector(offset)
            return autoAimPosition



    def getShotParams(self, targetPoint, ignoreYawLimits = False):
        descr = self.__avatar.vehicleTypeDescriptor
        (shotTurretYaw, shotGunPitch,) = getShotAngles(descr, self.__avatar.getOwnVehicleMatrix(), (self.__turretYaw, self.__gunPitch), targetPoint)
        gunPitchLimits = calcPitchLimitsFromDesc(shotTurretYaw, descr.gun['pitchLimits'])
        closestLimit = self.__isOutOfLimits(shotGunPitch, gunPitchLimits)
        if closestLimit is not None:
            shotGunPitch = closestLimit
        turretYawLimits = descr.gun['turretYawLimits']
        if not ignoreYawLimits:
            closestLimit = self.__isOutOfLimits(shotTurretYaw, turretYawLimits)
            if closestLimit is not None:
                shotTurretYaw = closestLimit
        (pos, vel,) = self.__getShotPosition(shotTurretYaw, shotGunPitch)
        grav = Math.Vector3(0.0, -descr.shot['gravity'], 0.0)
        return (pos, vel, grav)



    def __set_clientMode(self, value):
        if self.__clientMode == value:
            return 
        self.__clientMode = value
        if not self.__isStarted:
            return 
        if self.__clientMode:
            self.__time = BigWorld.time()
        if self.__showServerMarker:
            self.__avatar.inputHandler.showGunMarker2(self.__clientMode)


    clientMode = property(lambda self: self.__clientMode, __set_clientMode)

    def __set_showServerMarker(self, value):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying:
            return 
        if self.__showServerMarker == value:
            return 
        self.__showServerMarker = value
        BigWorld.player().enableServerAim(self.showServerMarker)
        if not self.__isStarted:
            return 
        if self.__clientMode:
            self.__avatar.inputHandler.showGunMarker2(self.__showServerMarker)


    showServerMarker = property(lambda self: self.__showServerMarker, __set_showServerMarker)

    def __set_targetLastShotPoint(self, value):
        self.__targetLastShotPoint = value


    targetLastShotPoint = property(lambda self: self.__targetLastShotPoint, __set_targetLastShotPoint)

    def __set_shotPointSourceFunctor(self, value):
        if value is not None:
            self.__shotPointSourceFunctor = value
        else:
            self.__shotPointSourceFunctor = self.__shotPointSourceFunctor_Default


    shotPointSourceFunctor = property(lambda self: self.__shotPointSourceFunctor, __set_shotPointSourceFunctor)

    def __shotPointSourceFunctor_Default(self):
        return self.__avatar.inputHandler.getDesiredShotPoint()


    turretMatrix = property(lambda self: self.__turretMatrixAnimator.matrix)
    gunMatrix = property(lambda self: self.__gunMatrixAnimator.matrix)
    turretRotationSpeed = property(lambda self: self.__turretRotationSpeed)
    dispersionAngle = property(lambda self: self.__dispersionAngle)
    markerInfo = property(lambda self: self.__markerInfo)
    turretYaw = property(lambda self: self.__turretYaw)
    gunPitch = property(lambda self: self.__gunPitch)

    def __onTick(self):
        self.__timerID = BigWorld.callback(self.__ROTATION_TICK_LENGTH, self.__onTick)
        lockEnabled = BigWorld.player().inputHandler.getAimingMode(AIMING_MODE.TARGET_LOCK)
        usePredictedLockShotPoint = lockEnabled and VehicleGunRotator.USE_LOCK_PREDICTION
        replayCtrl = BattleReplay.g_replayCtrl
        if not self.__clientMode and not replayCtrl.isPlaying and not usePredictedLockShotPoint:
            return 
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying:
            shotPoint = replayCtrl.getGunRotatorTargetPoint()
        else:
            predictedLockShotPoint = self.predictLockedTargetShotPoint() if usePredictedLockShotPoint else None
            shotPoint = self.__shotPointSourceFunctor() if predictedLockShotPoint is None else predictedLockShotPoint
        if shotPoint is None and self.__targetLastShotPoint:
            shotPoint = self.__lastShotPoint
        if replayCtrl.isRecording:
            if shotPoint is not None:
                replayCtrl.setGunRotatorTargetPoint(shotPoint)
        self.__updateShotPointOnServer(shotPoint)
        timeDiff = self.__getTimeDiff()
        if timeDiff is None:
            return 
        self.__time = BigWorld.time()
        self.__rotate(shotPoint, timeDiff)
        self.__updateGunMarker()
        if replayCtrl.isPlaying:
            replayCtrl.resetUpdateGunOnTimeWarp()



    def __getTimeDiff(self):
        timeDiff = BigWorld.time() - self.__time
        if timeDiff < self.__INSUFFICIENT_TIME_DIFF:
            return None
        if timeDiff > self.__MAX_TIME_DIFF:
            timeDiff = self.__MAX_TIME_DIFF
        return timeDiff



    def __updateShotPointOnServer(self, shotPoint):
        if shotPoint == self.__prevSentShotPoint:
            return 
        self.__prevSentShotPoint = shotPoint
        avatar = self.__avatar
        if shotPoint is None:
            avatar.base.vehicle_stopTrackingWithGun(self.__turretYaw, self.__gunPitch)
        else:
            vehicle = BigWorld.entity(avatar.playerVehicleID)
            if vehicle is not None and vehicle is avatar.vehicle:
                vehicle.cell.trackPointWithGun(shotPoint)
            else:
                avatar.base.vehicle_trackPointWithGun(shotPoint)



    def __rotate(self, shotPoint, timeDiff):
        self.__turretRotationSpeed = 0.0
        if shotPoint is None or self.__isLocked:
            self.__dispersionAngle = self.__avatar.getOwnVehicleShotDispersionAngle(0.0)
            return 
        avatar = self.__avatar
        descr = avatar.vehicleTypeDescriptor
        turretYawLimits = descr.gun['turretYawLimits']
        maxTurretRotationSpeed = self.__maxTurretRotationSpeed
        prevTurretYaw = self.__turretYaw
        (shotTurretYaw, shotGunPitch,) = getShotAngles(descr, avatar.getOwnVehicleMatrix(), (prevTurretYaw, self.__gunPitch), shotPoint)
        self.__turretYaw = turretYaw = self.__getNextTurretYaw(prevTurretYaw, shotTurretYaw, maxTurretRotationSpeed * timeDiff, turretYawLimits)
        if maxTurretRotationSpeed != 0:
            self.estimatedTurretRotationTime = abs(turretYaw - shotTurretYaw) / maxTurretRotationSpeed
        else:
            self.estimatedTurretRotationTime = 0
        gunPitchLimits = calcPitchLimitsFromDesc(turretYaw, descr.gun['pitchLimits'])
        self.__gunPitch = self.__getNextGunPitch(self.__gunPitch, shotGunPitch, timeDiff, gunPitchLimits)
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isUpdateGunOnTimeWarp:
            self.__updateTurretMatrix(turretYaw, 0.001)
            self.__updateGunMatrix(self.__gunPitch, 0.001)
        else:
            self.__updateTurretMatrix(turretYaw, self.__ROTATION_TICK_LENGTH)
            self.__updateGunMatrix(self.__gunPitch, self.__ROTATION_TICK_LENGTH)
        diff = abs(turretYaw - prevTurretYaw)
        if diff > pi:
            diff = 2 * pi - diff
        self.__turretRotationSpeed = diff / timeDiff
        self.__dispersionAngle = avatar.getOwnVehicleShotDispersionAngle(self.__turretRotationSpeed)



    def __updateGunMarker(self):
        (shotPos, shotVec,) = self.__getCurShotPosition()
        (markerPos, markerDir, markerSize, collData,) = self.__getGunMarkerPosition(shotPos, shotVec, self.__dispersionAngle)
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isRecording and not replayCtrl.isServerAim:
            replayCtrl.setGunMarkerParams(markerSize, markerPos, markerDir)
        if not self.__targetLastShotPoint:
            self.__lastShotPoint = markerPos
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isUpdateGunOnTimeWarp:
            self.__avatar.inputHandler.updateGunMarker(markerPos, markerDir, markerSize, 0.001, collData)
        else:
            self.__avatar.inputHandler.updateGunMarker(markerPos, markerDir, markerSize, self.__ROTATION_TICK_LENGTH, collData)
        self.__markerInfo = (markerPos, markerDir, markerSize)



    def __getNextTurretYaw(self, curAngle, shotAngle, speedLimit, angleLimits):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying:
            turretYaw = replayCtrl.getTurretYaw()
            if turretYaw > -100000:
                return turretYaw
        if curAngle == shotAngle:
            return curAngle
        (shortWayDiff, longWayDiff,) = self.__getRotationWays(curAngle, shotAngle)
        if speedLimit < 1e-05:
            return curAngle
        closestLimit = self.__isOutOfLimits(curAngle, angleLimits)
        if closestLimit is not None:
            return closestLimit
        shortWayDiffLimited = self.__applyTurretYawLimits(shortWayDiff, curAngle, angleLimits)
        if shortWayDiffLimited == shortWayDiff:
            return self.__getTurretYawWithSpeedLimit(curAngle, shortWayDiff, speedLimit)
        longWayDiffLimited = self.__applyTurretYawLimits(longWayDiff, curAngle, angleLimits)
        if longWayDiffLimited == longWayDiff:
            return self.__getTurretYawWithSpeedLimit(curAngle, longWayDiff, speedLimit)
        return self.__getTurretYawWithSpeedLimit(curAngle, shortWayDiffLimited, speedLimit)



    def __getRotationWays(self, curAngle, shotAngle):
        shotDiff1 = shotAngle - curAngle
        if shotDiff1 < 0:
            shotDiff2 = 2 * pi + shotDiff1
        else:
            shotDiff2 = -2 * pi + shotDiff1
        if abs(shotDiff1) <= pi:
            return (shotDiff1, shotDiff2)
        else:
            return (shotDiff2, shotDiff1)



    def __isOutOfLimits(self, angle, limits):
        if limits is None:
            return 
        else:
            if abs(limits[1] - angle) < 1e-05 or abs(limits[0] - angle) < 1e-05:
                return 
            dpi = 2 * pi
            minDiff = fmod(limits[0] - angle + dpi, dpi)
            maxDiff = fmod(limits[1] - angle + dpi, dpi)
            if minDiff > maxDiff:
                return 
            if minDiff < dpi - maxDiff:
                return limits[0]
            return limits[1]



    def __applyTurretYawLimits(self, diff, angle, limits):
        if limits is None:
            return diff
        else:
            dpi = 2 * pi
            if diff > 0:
                if abs(limits[1] - angle) < 1e-05:
                    return 0
                maxDiff = fmod(limits[1] - angle + dpi, dpi)
                return min(maxDiff, diff)
            if abs(limits[0] - angle) < 1e-05:
                return 0
            maxDiff = fmod(limits[0] - angle - dpi, dpi)
            return max(maxDiff, diff)



    def __getTurretYawWithSpeedLimit(self, angle, diff, limit):
        dpi = 2 * pi
        if diff > 0:
            return fmod(pi + angle + min(diff, limit), dpi) - pi
        else:
            return fmod(-pi + angle + max(diff, -limit), dpi) + pi



    def __getNextGunPitch(self, curAngle, shotAngle, timeDiff, angleLimits):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying:
            gunPitch = replayCtrl.getGunPitch()
            if gunPitch > -100000:
                return gunPitch
        if self.__maxGunRotationSpeed == 0.0:
            shotAngle = curAngle
            shotDiff = 0.0
            descr = self.__avatar.vehicleTypeDescriptor
            speedLimit = descr.gun['rotationSpeed'] * timeDiff
        elif curAngle == shotAngle:
            return curAngle
        shotDiff = shotAngle - curAngle
        speedLimit = self.__maxGunRotationSpeed * timeDiff
        if angleLimits is not None:
            if shotAngle < angleLimits[0]:
                shotDiff = angleLimits[0] - curAngle
            elif shotAngle > angleLimits[1]:
                shotDiff = angleLimits[1] - curAngle
        if shotDiff > 0:
            return curAngle + min(shotDiff, speedLimit)
        else:
            return curAngle + max(shotDiff, -speedLimit)



    def __getShotPosition(self, turretYaw, gunPitch):
        descr = self.__avatar.vehicleTypeDescriptor
        turretOffs = descr.hull['turretPositions'][0] + descr.chassis['hullPosition']
        gunOffs = descr.turret['gunPosition']
        shotSpeed = descr.shot['speed']
        turretWorldMatrix = Math.Matrix()
        turretWorldMatrix.setRotateY(turretYaw)
        turretWorldMatrix.translation = turretOffs
        turretWorldMatrix.postMultiply(Math.Matrix(self.__avatar.getOwnVehicleMatrix()))
        position = turretWorldMatrix.applyPoint(gunOffs)
        gunWorldMatrix = Math.Matrix()
        gunWorldMatrix.setRotateX(gunPitch)
        gunWorldMatrix.postMultiply(turretWorldMatrix)
        vector = gunWorldMatrix.applyVector(Math.Vector3(0, 0, shotSpeed))
        return (position, vector)



    def __getCurShotPosition(self):
        return self.__getShotPosition(self.__turretYaw, self.__gunPitch)



    def __getGunMarkerPosition(self, shotPos, shotVec, dispersionAngle):
        shotDescr = self.__avatar.vehicleTypeDescriptor.shot
        gravity = Math.Vector3(0.0, -shotDescr['gravity'], 0.0)
        maxDist = shotDescr['maxDistance']
        testStartPoint = shotPos
        testEndPoint = shotPos + shotVec * 10000.0
        testEntities = ProjectileMover.getCollidableEntities((self.__avatar.playerVehicleID,), testStartPoint, testEndPoint)
        collideVehiclesAndStaticScene = ProjectileMover.collideVehiclesAndStaticScene
        collideWithSpaceBB = self.__avatar.arena.collideWithSpaceBB
        prevPos = shotPos
        prevVelocity = shotVec
        dt = 0.0
        maxDistCheckFlag = False
        while True:
            dt += SERVER_TICK_LENGTH
            checkPoints = computeProjectileTrajectory(prevPos, prevVelocity, gravity, SERVER_TICK_LENGTH, SHELL_TRAJECTORY_EPSILON_CLIENT)
            prevCheckPoint = prevPos
            bBreak = False
            for curCheckPoint in checkPoints:
                testRes = collideVehiclesAndStaticScene(prevCheckPoint, curCheckPoint, testEntities)
                if testRes is not None:
                    collData = testRes[1]
                    if collData is not None and not collData.isVehicle():
                        collData = None
                    dir = testRes[0] - prevCheckPoint
                    endPos = testRes[0]
                    bBreak = True
                    break
                pos = collideWithSpaceBB(prevCheckPoint, curCheckPoint)
                if pos is not None:
                    collData = None
                    maxDistCheckFlag = True
                    dir = pos - prevCheckPoint
                    endPos = pos
                    bBreak = True
                    break
                prevCheckPoint = curCheckPoint

            if bBreak:
                break
            prevPos = shotPos + shotVec.scale(dt) + gravity.scale(dt * dt * 0.5)
            prevVelocity = shotVec + gravity.scale(dt)

        dir.normalise()
        distance = (endPos - shotPos).length
        markerDiameter = 2.0 * distance * dispersionAngle
        if maxDistCheckFlag:
            if endPos.distTo(shotPos) >= maxDist:
                dir = endPos - shotPos
                dir.normalise()
                endPos = shotPos + dir.scale(maxDist)
                distance = maxDist
                markerDiameter = 2.0 * distance * dispersionAngle
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isClientReady:
            (markerDiameter, endPos, dir,) = replayCtrl.getGunMarkerParams(endPos, dir)
        return (endPos,
         dir,
         markerDiameter,
         collData)



    def __updateTurretMatrix(self, yaw, time):
        m = Math.Matrix()
        m.setRotateY(yaw)
        self.__turretMatrixAnimator.update(m, time)
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isRecording:
            replayCtrl.setTurretYaw(yaw)



    def __updateGunMatrix(self, pitch, time):
        m = Math.Matrix()
        m.setRotateX(pitch)
        self.__gunMatrixAnimator.update(m, time)
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isRecording:
            replayCtrl.setGunPitch(pitch)



    def __onCameraChanged(self, cameraName, currentVehicleId = None):
        if self.__turretRotationSoundEffect is not None:
            self.__turretRotationSoundEffect.enable(_ENABLE_TURRET_ROTATOR_SOUND)
        g__attachToCam = cameraName == 'sniper'




class _MatrixAnimator(object):

    def __init__(self, avatar):
        m = Math.Matrix()
        m.setIdentity()
        self.__animMat = Math.MatrixAnimation()
        self.__animMat.keyframes = ((0.0, m),)



    def destroy(self, avatar):
        self.__animMat = None


    matrix = property(lambda self: self.__animMat)

    def update(self, matrix, time):
        self.__animMat.keyframes = ((0.0, Math.Matrix(self.__animMat)), (time, matrix))
        self.__animMat.time = 0.0




class _PlayerTurretRotationSoundEffect(CallbackDelayer):
    __MIN_ANGLE_TO_ENABLE_MANUAL = math.radians(0.1)
    __MIN_ANGLE_TO_ENABLE_GEAR = math.radians(10.0)
    __GEAR_KEYOFF_PARAM = 'on_off'
    __MANUAL_WAIT_TIME = 0.4
    __GEAR_DELAY_TIME = 0.2
    __GEAR_STOP_DELAY_TIME = 0.2
    __SPEED_IDLE = 0
    __SPEED_SLOW = 1
    __SPEED_PRE_FAST = 2
    __SPEED_FAST = 3

    def __init__(self, updatePeriod = 0.0):
        CallbackDelayer.__init__(self)
        self.__updatePeriod = updatePeriod
        self.__currentSpeedState = self.__SPEED_IDLE
        self.__keyOffCalled = False
        self.__stateTable = ((None,
          self.__startManualSound,
          self.__initHighSpeed,
          None),
         (self.__stopManualSound,
          None,
          self.__initHighSpeed,
          None),
         (self.__stopManualSound,
          self.__startManualSoundFromFast,
          None,
          None),
         (self.__stopGearSoundPlaying,
          self.__startManualSoundFromFast,
          None,
          self.__checkGearSound))



    def init_sound(self):
        if _ENABLE_TURRET_ROTATOR_SOUND:
            self.__manualSound = self.__getTurretSound(BigWorld.player().vehicleTypeDescriptor, 'turretRotatorSoundManual')
            self.__gearSound = self.__getTurretSound(BigWorld.player().vehicleTypeDescriptor, 'turretRotatorSoundGear')



    def destroy(self):
        CallbackDelayer.destroy(self)
        if self.__manualSound is not None:
            self.__manualSound.stop()
        if self.__gearSound is not None:
            self.__gearSound.stop()
        self.__stateTable = None



    def enable(self, enableSound):
        if enableSound:
            self.delayCallback(self.__updatePeriod, self.__update)
        else:
            CallbackDelayer.destroy(self)
            if self.__manualSound is not None:
                self.__manualSound.stop()
            if self.__gearSound is not None:
                self.__gearSound.stop()



    def __getTurretSound(self, vehicleTypDescriptor, soundName):
        event = vehicleTypDescriptor.turret[soundName]
        if event is not None and event != '':
            return SoundGroups.g_instance.FMODgetSound(event)
        else:
            return 



    def __update(self):
        player = BigWorld.player()
        vehicleTypeDescriptor = player.vehicleTypeDescriptor
        gunRotator = player.gunRotator
        turretYaw = gunRotator.turretYaw
        desiredShotPoint = gunRotator.predictLockedTargetShotPoint()
        if desiredShotPoint is None:
            desiredShotPoint = player.inputHandler.getDesiredShotPoint()
        if desiredShotPoint is None:
            desiredShotPoint = gunRotator.markerInfo[0]
        (cameraTurretYaw, _,) = AimingSystems.getTurretYawGunPitch(vehicleTypeDescriptor, player.getOwnVehicleMatrix(), desiredShotPoint, True)
        angleDiff = abs(turretYaw - cameraTurretYaw)
        if angleDiff > math.pi:
            angleDiff = 2 * math.pi - angleDiff
        rotationSpeed = gunRotator.turretRotationSpeed
        if rotationSpeed < 0.0001:
            angleDiff = 0.0
        self.__updateSound(angleDiff)
        return self.__updatePeriod



    def __updateSound(self, angleDiff):
        if self.__manualSound is None:
            return 
        if self.__gearSound is not None and angleDiff >= _PlayerTurretRotationSoundEffect.__MIN_ANGLE_TO_ENABLE_GEAR:
            if self.__currentSpeedState != self.__SPEED_FAST and self.__currentSpeedState != self.__SPEED_PRE_FAST:
                nextSpeedState = self.__SPEED_PRE_FAST
            else:
                nextSpeedState = self.__currentSpeedState
        elif angleDiff >= _PlayerTurretRotationSoundEffect.__MIN_ANGLE_TO_ENABLE_MANUAL:
            nextSpeedState = self.__SPEED_SLOW
        else:
            nextSpeedState = self.__SPEED_IDLE
        stateFn = self.__stateTable[self.__currentSpeedState][nextSpeedState]
        if stateFn is not None:
            stateFn()
        self.__currentSpeedState = nextSpeedState
        if g__attachToCam:
            __p = BigWorld.camera().position
        else:
            __p = BigWorld.player().position
        isTurretAlive = BigWorld.player().deviceStates.get('turretRotator', None) is None
        if self.__gearSound is not None:
            if self.__gearSound.param('turret_damaged'):
                self.__gearSound.param('turret_damaged').value = 0 if isTurretAlive else 1
        if self.__manualSound is not None:
            if self.__manualSound.param('turret_damaged'):
                self.__manualSound.param('turret_damaged').value = 0 if isTurretAlive else 1
        if self.__manualSound is not None:
            self.__manualSound.position = __p
        if self.__gearSound is not None:
            self.__gearSound.position = __p



    def __stopGearByKeyOff(self):
        if self.__gearSound is not None and self.__gearSound.isPlaying:
            param = self.__gearSound.param(_PlayerTurretRotationSoundEffect.__GEAR_KEYOFF_PARAM)
            if param is not None:
                self.__keyOffCalled = True
                param.keyOff()
            else:
                self.__gearSound.stop()



    def __startManualSound(self):
        self.stopCallback(self.__stopManualSoundCallback)
        self.__manualSound.play()



    def __stopManualSound(self):
        if not self.hasDelayedCallback(self.__stopManualSoundCallback) and self.__manualSound.isPlaying:
            self.delayCallback(_PlayerTurretRotationSoundEffect.__MANUAL_WAIT_TIME, self.__stopManualSoundCallback)
        self.__stopGearSoundPlaying()



    def __initHighSpeed(self):
        self.stopCallback(self.__stopGearByKeyOff)
        self.delayCallback(_PlayerTurretRotationSoundEffect.__GEAR_DELAY_TIME, self.__startGearSoundCallback)



    def __startManualSoundFromFast(self):
        self.__manualSound.play()
        self.__stopGearSoundPlaying()



    def __checkGearSound(self):
        if self.__gearSound.isPlaying is False:
            self.__gearSound.play()



    def __stopGearSoundPlaying(self):
        if self.__gearSound is not None:
            self.stopCallback(self.__startGearSoundCallback)
            if self.__gearSound.isPlaying and not self.hasDelayedCallback(self.__stopGearByKeyOff):
                self.delayCallback(_PlayerTurretRotationSoundEffect.__GEAR_STOP_DELAY_TIME, self.__stopGearByKeyOff)



    def __startGearSoundCallback(self):
        self.__currentSpeed = self.__SPEED_FAST
        if self.__manualSound.isPlaying:
            self.__manualSound.stop()
        if self.__keyOffCalled:
            self.__gearSound.stop()
            self.__keyOffCalled = False
        self.__gearSound.play()



    def __stopManualSoundCallback(self):
        self.__manualSound.stop()




+++ okay decompyling vehiclegunrotator.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:32:44 CET
