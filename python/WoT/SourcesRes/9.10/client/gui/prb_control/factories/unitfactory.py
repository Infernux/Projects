# 2015.01.18 23:11:03 CET
from constants import PREBATTLE_TYPE
from debug_utils import LOG_ERROR
from gui import prb_control
from gui.prb_control.context.unit_ctx import LeaveUnitCtx
from gui.prb_control.factories.ControlFactory import ControlFactory
from gui.prb_control.functional.unit import NoUnitFunctional, UnitEntry, UnitIntro, FortBattleEntry
from gui.prb_control.functional.unit import IntroFunctional, UnitFunctional
from gui.prb_control.items import PlayerDecorator, FunctionalState
from gui.prb_control.items.unit_items import SupportedRosterSettings, DynamicRosterSettings
from gui.prb_control.settings import PREBATTLE_ACTION_NAME, CTRL_ENTITY_TYPE, UNIT_MODE_FLAGS, FUNCTIONAL_EXIT
_PAN = PREBATTLE_ACTION_NAME
_SUPPORTED_ENTRY_BY_ACTION = {_PAN.UNIT: (UnitIntro, (PREBATTLE_TYPE.UNIT,)),
 _PAN.FORT: (UnitIntro, (PREBATTLE_TYPE.SORTIE,))}
_SUPPORTED_ENTRY_BY_TYPE = {PREBATTLE_TYPE.UNIT: UnitEntry,
 PREBATTLE_TYPE.SORTIE: UnitEntry,
 PREBATTLE_TYPE.FORT_BATTLE: FortBattleEntry}

class UnitFactory(ControlFactory):

    def createEntry(self, ctx):
        if not ctx.getRequestType():
            entry = UnitIntro(ctx.getPrbType())
        else:
            clazz = _SUPPORTED_ENTRY_BY_TYPE.get(ctx.getPrbType())
            if clazz is not None:
                entry = clazz()
            else:
                entry = None
                LOG_ERROR('Prebattle type is not supported', ctx)
        return entry



    def createEntryByAction(self, action):
        return self._createEntryByAction(action, _SUPPORTED_ENTRY_BY_ACTION)



    def createFunctional(self, dispatcher, ctx):
        unitMrg = prb_control.getClientUnitMgr()
        if unitMrg.id and unitMrg.unitIdx:
            unit = prb_control.getUnit(unitMrg.unitIdx, safe=True)
            prbType = PREBATTLE_TYPE.UNIT
            if unit.isSortie():
                prbType = PREBATTLE_TYPE.SORTIE
            elif unit.isFortBattle():
                prbType = PREBATTLE_TYPE.FORT_BATTLE
            if unit:
                unitFunctional = UnitFunctional(prbType, DynamicRosterSettings(unit))
                for listener in dispatcher._globalListeners:
                    unitFunctional.addListener(listener())

            else:
                LOG_ERROR('Unit is not found in unit manager', unitMrg.unitIdx, unitMrg.units)
                unitMrg.leave()
            unitFunctional = NoUnitFunctional()
        else:
            prbType = ctx.getPrbType()
            if prbType:
                unitFunctional = IntroFunctional(prbType, ctx.getCreateParams().get('modeFlags', UNIT_MODE_FLAGS.UNDEFINED), SupportedRosterSettings.last(prbType))
                for listener in dispatcher._globalListeners:
                    unitFunctional.addListener(listener())

            else:
                unitFunctional = NoUnitFunctional()
        return unitFunctional



    def createPlayerInfo(self, functional):
        info = functional.getPlayerInfo(unitIdx=functional.getUnitIdx())
        return PlayerDecorator(info.isCreator(), info.isReady)



    def createStateEntity(self, functional):
        return FunctionalState(CTRL_ENTITY_TYPE.UNIT, functional.getPrbType(), True, functional.hasLockedState(), isinstance(functional, IntroFunctional))



    def createLeaveCtx(self, funcExit = FUNCTIONAL_EXIT.NO_FUNC):
        return LeaveUnitCtx(waitingID='prebattle/leave', funcExit=funcExit)



    def getLeaveCtxByAction(self, action):
        ctx = None
        if action in (PREBATTLE_ACTION_NAME.UNIT_LEAVE, PREBATTLE_ACTION_NAME.FORT_LEAVE):
            ctx = self.createLeaveCtx()
        return ctx




+++ okay decompyling unitfactory.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.18 23:11:04 CET
