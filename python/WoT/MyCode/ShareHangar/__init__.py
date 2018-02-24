XFW_MOD_INFO = {'VERSION': '0.0.1a',
 'URL': 'http://www.modxvm.com/',
 'UPDATE_URL': 'http://www.modxvm.com/en/download-xvm/',
 'GAME_VERSIONS': ['0.9.10']}

import BigWorld
from xfw import *
from xvm_main.python.logger import *
import xvm_main.python.config as config

FIRSTCMD=0

def myActionChat(self, chatActionData):
    from gui import SystemMessages
    from chat_shared import parseCommandMessage
    import Vehicle

    (command,int64,int16,strArg1,strArg2)=parseCommandMessage(chatActionData)
    if int16==FIRSTCMD:
        namelist=[]
        l=list(strArg1)
        for tank in l:
            namelist.append(Vehicle.vehicles.getVehicleType(tank[0]).shortUserString)
        SystemMessages.pushMessage(namelist)
    else:
        SystemMessages.pushMessage(strArg1)

def myOnRosterReceived(self,preBattleId,iterator):
    import messenger
    from chat_shared import buildChatActionData
    from chat_shared import CHAT_COMMANDS
    from chat_shared import parseCommandMessage

    newlist=messenger.MessengerEntry.g_instance.storage.channels.all()
    #TODO
    chan=next((x for x in newlist if x.getName() == '[CPC]'), None)

    com=CHAT_COMMANDS.all()[44]
    com._EnumItem__index=22

    tanklist=gui.shared.g_itemsCache.items.getVehicles(gui.shared.REQ_CRITERIA.INVENTORY)

    p=BigWorld.player()
    p._ClientChat__baseChannelChatCommand(chan.getID(),stringArg1=str(tanklist))

def myparse(self,a,b):
    print "parsing start"
    print a
    print b
    print "parsing end"

def _RegisterEvents():
    from ClientChat import ClientChat
    from ClientPreBattle import ClientPreBattle
    import chat_shared
    print 'import is ok'
    #OverrideMethod(chat_shared, 'parseCommandMessage', myparse)
    RegisterEvent(ClientChat, 'onChatAction', myActionChat)
    RegisterEvent(ClientPreBattle, 'onPrbRosterReceived', myOnRoster)
    print 'registerWorked'

BigWorld.callback(0, _RegisterEvents)
