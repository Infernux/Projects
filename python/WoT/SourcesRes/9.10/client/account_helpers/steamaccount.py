# 2015.01.14 13:53:29 CET
import BigWorld
import constants
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG
STEAM_IS_DEVELOPMENT = constants.IS_DEVELOPMENT
STEAM_SUPPORT = False

class __SteamAccount(object):
    _GET_USER_INFO_URL = 'https://api.steampowered.com/ISteamMicroTxn/GetUserInfo/V0001/?steamid=%d'
    _STEAM_LOGIN_SUFFIX = '@steam.com'

    def __init__(self):
        self.userInfo = None



    @property
    def isValid(self):
        return STEAM_SUPPORT and BigWorld.wg_isSteamInitialized()



    @property
    def steamID--- This code section failed: ---
0	LOAD_FAST         'self'
3	LOAD_ATTR         'isValid'
6	POP_JUMP_IF_TRUE  '21'
9	LOAD_ASSERT       'AssertionError'
12	LOAD_CONST        'Available only for steam users'
15	CALL_FUNCTION_1   ''
18	RAISE_VARARGS     ''
21	LOAD_GLOBAL       'BigWorld'
24	LOAD_ATTR         'wg_getSteamID'
27	CALL_FUNCTION_0   ''
30	RETURN_VALUE      ''
-1	RETURN_LAST       ''

Syntax error at or near `RETURN_VALUE' token at offset 30

    def getCredentials--- This code section failed: ---
0	LOAD_FAST         'self'
3	LOAD_ATTR         'isValid'
6	POP_JUMP_IF_TRUE  '21'
9	LOAD_ASSERT       'AssertionError'
12	LOAD_CONST        'Available only for steam users'
15	CALL_FUNCTION_1   ''
18	RAISE_VARARGS     ''
21	LOAD_GLOBAL       'STEAM_IS_DEVELOPMENT'
24	POP_JUMP_IF_FALSE '33'
27	LOAD_CONST        '%d@steam.dev'
30	JUMP_FORWARD      '39'
33	LOAD_FAST         'self'
36	LOAD_ATTR         '_STEAM_LOGIN_SUFFIX'
39_0	COME_FROM         '30'
39	LOAD_FAST         'self'
42	LOAD_ATTR         'steamID'
45	BINARY_MODULO     ''
46	STORE_FAST        'user'
49	LOAD_GLOBAL       'STEAM_IS_DEVELOPMENT'
52	POP_JUMP_IF_FALSE '61'
55	LOAD_CONST        ''
58	JUMP_FORWARD      '70'
61	LOAD_GLOBAL       'BigWorld'
64	LOAD_ATTR         'wg_getSteamAuthTicket'
67	CALL_FUNCTION_0   ''
70_0	COME_FROM         '58'
70	STORE_FAST        'password'
73	LOAD_FAST         'user'
76	LOAD_FAST         'password'
79	BUILD_TUPLE_2     ''
82	RETURN_VALUE      ''
-1	RETURN_LAST       ''

Syntax error at or near `RETURN_VALUE' token at offset 82

g_steamAccount = __SteamAccount()

# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2015.01.14 13:53:29 CET
