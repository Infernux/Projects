# 2015.01.18 23:11:03 CET
from constants import QUEUE_TYPE
from debug_utils import LOG_ERROR
from gui.prb_control.context.pre_queue_ctx import LeavePreQueueCtx
from gui.prb_control.factories.ControlFactory import ControlFactory
from gui.prb_control.functional.no_prebattle import NoPreQueueFunctional
from gui.prb_control.functional.not_supported import QueueNotSupportedFunctional
from gui.prb_control.functional.random_queue import RandomQueueFunctional
from gui.prb_control.functional.historical import HistoricalQueueFunctional
from gui.prb_control.functional.historical import HistoricalEntry
from gui.prb_control.functional.event_battles import EventBattlesQueueFunctional
from gui.prb_control.items import FunctionalState
from gui.prb_control.settings import PREBATTLE_ACTION_NAME, CTRL_ENTITY_TYPE, FUNCTIONAL_EXIT
_SUPPORTED_QUEUES = {QUEUE_TYPE.RANDOMS: RandomQueueFunctional,
 QUEUE_TYPE.HISTORICAL: HistoricalQueueFunctional,
 QUEUE_TYPE.EVENT_BATTLES: EventBattlesQueueFunctional}
_SUPPORTED_ENTRY_BY_ACTION = {PREBATTLE_ACTION_NAME.HISTORICAL: (HistoricalEntry, None)}

class PreQueueFactory(ControlFactory):

    def createEntry(self, ctx):
        LOG_ERROR('preQueue functional has not any entries')



    def createEntryByAction(self, action):
        return self._createEntryByAction(action, _SUPPORTED_ENTRY_BY_ACTION)



    def createFunctional--- This code section failed: ---
0	LOAD_FAST         'ctx'
3	LOAD_ATTR         'getCreateParams'
6	CALL_FUNCTION_0   ''
9	STORE_FAST        'createParams'
12	LOAD_CONST        'queueType'
15	LOAD_FAST         'createParams'
18	COMPARE_OP        'in'
21	POP_JUMP_IF_FALSE '37'
24	LOAD_FAST         'createParams'
27	LOAD_CONST        'queueType'
30	BINARY_SUBSCR     ''
31	STORE_FAST        'queueType'
34	JUMP_FORWARD      '43'
37	LOAD_CONST        ''
40	STORE_FAST        'queueType'
43_0	COME_FROM         '34'
43	LOAD_FAST         'queueType'
46	POP_JUMP_IF_FALSE '221'
49	LOAD_FAST         'createParams'
52	LOAD_CONST        'queueType'
55	BINARY_SUBSCR     ''
56	STORE_FAST        'queueType'
59	LOAD_CONST        'settings'
62	LOAD_FAST         'createParams'
65	COMPARE_OP        'in'
68	POP_JUMP_IF_FALSE '96'
71	LOAD_FAST         'createParams'
74	LOAD_CONST        'settings'
77	BINARY_SUBSCR     ''
78	LOAD_ATTR         'get'
81	LOAD_GLOBAL       'CTRL_ENTITY_TYPE'
84	LOAD_ATTR         'PREQUEUE'
87	CALL_FUNCTION_1   ''
90	STORE_FAST        'settings'
93	JUMP_FORWARD      '102'
96	LOAD_CONST        ''
99	STORE_FAST        'settings'
102_0	COME_FROM         '93'
102	LOAD_FAST         'queueType'
105	LOAD_GLOBAL       '_SUPPORTED_QUEUES'
108	COMPARE_OP        'in'
111	POP_JUMP_IF_FALSE '193'
114	LOAD_GLOBAL       '_SUPPORTED_QUEUES'
117	LOAD_FAST         'queueType'
120	BINARY_SUBSCR     ''
121	STORE_FAST        'clazz'
124	LOAD_FAST         'clazz'
127	POP_JUMP_IF_TRUE  '142'
130	LOAD_ASSERT       'AssertionError'
133	LOAD_CONST        'Class is not found, checks settings'
136	CALL_FUNCTION_1   ''
139	RAISE_VARARGS     ''
142	LOAD_FAST         'clazz'
145	LOAD_FAST         'settings'
148	CALL_FUNCTION_1   ''
151	STORE_FAST        'preQueueFunctional'
154	SETUP_LOOP        '218'
157	LOAD_FAST         'dispatcher'
160	LOAD_ATTR         '_globalListeners'
163	GET_ITER          ''
164	FOR_ITER          '189'
167	STORE_FAST        'listener'
170	LOAD_FAST         'preQueueFunctional'
173	LOAD_ATTR         'addListener'
176	LOAD_FAST         'listener'
179	CALL_FUNCTION_0   ''
182	CALL_FUNCTION_1   ''
185	POP_TOP           ''
186	JUMP_BACK         '164'
189	POP_BLOCK         ''
190_0	COME_FROM         '154'
190	JUMP_ABSOLUTE     '230'
193	LOAD_GLOBAL       'LOG_ERROR'
196	LOAD_CONST        'Queue with given type is not supported'
199	LOAD_FAST         'queueType'
202	CALL_FUNCTION_2   ''
205	POP_TOP           ''
206	LOAD_GLOBAL       'QueueNotSupportedFunctional'
209	LOAD_FAST         'queueType'
212	CALL_FUNCTION_1   ''
215	STORE_FAST        'preQueueFunctional'
218	JUMP_FORWARD      '230'
221	LOAD_GLOBAL       'NoPreQueueFunctional'
224	CALL_FUNCTION_0   ''
227	STORE_FAST        'preQueueFunctional'
230_0	COME_FROM         '218'
230	LOAD_FAST         'preQueueFunctional'
233	RETURN_VALUE      ''
-1	RETURN_LAST       ''

Syntax error at or near `RETURN_VALUE' token at offset 233

    def createStateEntity(self, functional):
        return FunctionalState(CTRL_ENTITY_TYPE.PREQUEUE, functional.getQueueType(), True, functional.isInQueue())



    def createLeaveCtx(self, state = None, funcExit = FUNCTIONAL_EXIT.NO_FUNC):
        return LeavePreQueueCtx(waitingID='prebattle/leave')




# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2015.01.18 23:11:03 CET
