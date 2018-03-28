# 2015.01.14 22:41:26 CET
from collections import defaultdict
import weakref
import BigWorld
from debug_utils import LOG_CURRENT_EXCEPTION
from messenger.proto.xmpp.jid import ContactJID
from messenger.proto.xmpp.log_output import CLIENT_LOG_AREA, g_logOutput
XmppClient = BigWorld.XmppClient

class PRESENCE(object):
    UNKNOWN = XmppClient.PRESENCE_UNKNOWN
    AVAILABLE = XmppClient.PRESENCE_AVAILABLE
    CHAT = XmppClient.PRESENCE_CHAT
    AWAY = XmppClient.PRESENCE_AWAY
    DND = XmppClient.PRESENCE_DND
    XA = XmppClient.PRESENCE_XA
    UNAVAILABLE = XmppClient.PRESENCE_UNAVAILABLE
    RANGE = (UNKNOWN,
     AVAILABLE,
     CHAT,
     AWAY,
     DND,
     XA,
     UNAVAILABLE)

PRESENCES_ORDER = (PRESENCE.AVAILABLE,
 PRESENCE.CHAT,
 PRESENCE.AWAY,
 PRESENCE.DND,
 PRESENCE.XA,
 PRESENCE.UNAVAILABLE,
 PRESENCE.UNKNOWN)
PRESENCES_NAMES = dict([ (v, k) for (k, v,) in PRESENCE.__dict__.iteritems() if v in PRESENCE.RANGE ])

class SUBSCRIPTION(object):
    OFF = XmppClient.SUBSCRIPTION_OFF
    ON = XmppClient.SUBSCRIPTION_ON
    PENDING = XmppClient.SUBSCRIPTION_PENDING

SUBSCRIPTION_NAMES = dict([ (v, k) for (k, v,) in SUBSCRIPTION.__dict__.iteritems() if not k.startswith('_') ])

class CONNECTION_IMPL_TYPE(object):
    TCP = 1
    BOSH = 2


class CONNECTION_STATE(object):
    DISCONNECTED = XmppClient.STATE_DISCONNECTED
    CONNECTING = XmppClient.STATE_CONNECTING
    AUTHENTICATING = XmppClient.STATE_AUTHENTICATING
    INITIALIZING = XmppClient.STATE_INITIALIZING
    CONNECTED = XmppClient.STATE_CONNECTED


class DISCONNECT_REASON(object):
    BY_REQUEST = XmppClient.DISCONNECT_BY_REQUEST
    AUTHENTICATION = XmppClient.DISCONNECT_AUTHENTICATION
    OTHER_ERROR = XmppClient.DISCONNECT_OTHER_ERROR


class LOG_LEVEL(object):
    DEBUG = XmppClient.LOG_LEVEL_DEBUG
    WARNING = XmppClient.LOG_LEVEL_WARNING
    ERROR = XmppClient.LOG_LEVEL_ERROR


class LOG_SOURCE(object):
    UNKNOWN = 'Unknown source'
    PARSER = 'Parser'
    CLIENT = 'Client'
    CLIENT_BASE = 'Clientbase'
    COMPONENT = 'Component'
    DND = 'Dns'
    USER = 'User'
    CONNECTION_TCP_BASE = 'ConnectionTCPBase'
    CONNECTION_HTTP_PROXY = 'ConnectionHTTPProxy'
    CONNECTION_S5_PROXY = 'ConnectionSOCKS5Proxy'
    CONNECTION_TCP_CLIENT = 'ConnectionTCPClient'
    CONNECTION_TCP_SERVER = 'ConnectionTCPServer'
    CONNECTION_BOSH = 'ConnectionBOSH'
    CONNECTION_TLS = 'ConnectionTLS'
    S5B_MANAGER = 'S5BManager'
    S5_BYTES_STREAM = 'SOCKS5Bytestream'
    XML_INCOMING = 'XmlIncoming'
    XML_OUTGOING = 'XmlOutgoing'
    XML_STREAM = (XML_INCOMING, XML_OUTGOING)


class IQ_TYPE(object):
    GET = XmppClient.IQ_TYPE_GET
    SET = XmppClient.IQ_TYPE_SET
    RESULT = XmppClient.IQ_TYPE_RESULT
    ERROR = XmppClient.IQ_TYPE_ERROR
    INVALID = XmppClient.IQ_TYPE_INVALID


class GLOOX_EVENT(object):
    (CONNECTED, LOGIN, DISCONNECTED, ROSTER_ITEM_SET, ROSTER_ITEM_REMOVED, ROSTER_RESOURCE_ADDED, ROSTER_RESOURCE_REMOVED, SUBSCRIPTION_REQUEST, LOG,) = ALL = range(0, 9)

GLOOX_EVENTS_NAMES = dict([ (v, k) for (k, v,) in GLOOX_EVENT.__dict__.iteritems() if v in GLOOX_EVENT.ALL ])
_GLOOX_EVENTS_LISTENERS = (('onConnect', 'onConnected'),
 ('onReady', 'onLogin'),
 ('onDisconnect', 'onDisconnected'),
 ('onNewRosterItem', 'onRosterItemSet'),
 ('onRosterItemRemove', 'onRosterItemRemoved'),
 ('onNewRosterResource', 'onRosterResourceAdded'),
 ('onRosterResourceRemove', 'onRosterResourceRemoved'),
 ('onSubscribe', 'onSubscriptionRequest'),
 ('onLog', 'onLog'))

class ClientDecorator(object):

    def __init__(self):
        super(ClientDecorator, self).__init__()
        self.__client = BigWorld.XmppClient()
        self.__handlers = defaultdict(set)
        self.__address = None



    def init(self):
        client = self.__client
        ClientHolder._clearClient()
        for (handlerName, listenerName,) in _GLOOX_EVENTS_LISTENERS:
            if not hasattr(client, handlerName):
                g_logOutput.error(CLIENT_LOG_AREA.PY_WRAPPER, 'Handler no is found', handlerName)
                continue
            handler = getattr(client, handlerName)
            if handler:
                g_logOutput.warning(CLIENT_LOG_AREA.PY_WRAPPER, 'Handler already is set', handlerName)
                continue
            listener = getattr(self, listenerName, None)
            if listener is None or not callable(listener):
                g_logOutput.error(CLIENT_LOG_AREA.PY_WRAPPER, 'Listener no is found', listenerName)
                continue
            setattr(client, handlerName, listener)

        ClientEventsHandler._setClient(self)



    def fini(self):
        client = self.__client
        for (handlerName, _,) in _GLOOX_EVENTS_LISTENERS:
            setattr(client, handlerName, None)

        self.__handlers.clear()
        g_logOutput.clear()
        ClientHolder._clearClient()



    def connect(self, jid, host = '', port = -1):
        self.__address = (jid, host, port)
        self.__client.connect(jid, host, port)



    def connectBosh(self, jid, host = '', port = -1, url = ''):
        self.__address = (jid, url)
        self.__client.connectBosh(jid, host, port, url)



    def login(self, password):
        self.__client.login(password)



    def disconnect(self):
        self.__client.disconnect()



    def getConnectionState(self):
        return self.__client.connectionState



    def getConnectionAddress(self):
        return self.__address



    def isConnected(self):
        return self.__client.connectionState == CONNECTION_STATE.CONNECTED



    def isDisconnected(self):
        return self.__client.connectionState == CONNECTION_STATE.DISCONNECTED



    def isConnecting(self):
        state = self.__client.connectionState
        return state in [CONNECTION_STATE.CONNECTING, CONNECTION_STATE.AUTHENTICATING, CONNECTION_STATE.INITIALIZING]



    def getClientPresence(self):
        return self.__client.presence



    def setClientPresence(self, presence):
        if presence not in PRESENCE.RANGE:
            g_logOutput.error(CLIENT_LOG_AREA.PY_WRAPPER, 'Value of presence is invalid', presence)
            return 
        self.__client.presence = presence



    def sendIQ(self, iqType, body):
        return self.__client.sendCustomQuery(iqType, body)



    def setContactToRoster(self, jid, name = '', groups = None):
        if groups is None:
            groups = set()
        self.__client.add(str(jid), name, groups)



    def removeContactFromRoster(self, jid):
        self.__client.remove(str(jid))



    def setSubscribeTo(self, jid, message = ''):
        self.__client.subscribe(str(jid), message)



    def removeSubscribeTo(self, jid):
        self.__client.unsubscribe(str(jid))



    def setSubscribeFrom(self, jid, message = ''):
        self.__client.setSubscribed(str(jid), message)



    def registerHandler(self, event, handler):
        if event in GLOOX_EVENT.ALL:
            handlers = self.__handlers[event]
            if handler in handlers:
                g_logOutput.warning(CLIENT_LOG_AREA.PY_WRAPPER, 'handler already exists', event, handler)
            elif not hasattr(handler, '__self__') or not isinstance(handler.__self__, ClientEventsHandler):
                g_logOutput.error(CLIENT_LOG_AREA.PY_WRAPPER, 'Class of handler is not subclass of ClientEventsHandler', handler)
                return 
            if callable(handler):
                handlers.add(handler)
            else:
                g_logOutput.error(CLIENT_LOG_AREA.PY_WRAPPER, 'Handler is invalid', handler)
        else:
            g_logOutput.error(CLIENT_LOG_AREA.PY_WRAPPER, 'Event is not found', event)



    def unregisterHandler(self, event, handler):
        if event in GLOOX_EVENT.ALL:
            handlers = self.__handlers[event]
            if handler in handlers:
                handlers.remove(handler)
        else:
            g_logOutput.error(CLIENT_LOG_AREA.PY_WRAPPER, 'Event is not found', event)



    def onConnected(self):
        self.__handleEvent(GLOOX_EVENT.CONNECTED)



    def onLogin(self):
        self.__handleEvent(GLOOX_EVENT.LOGIN)



    def onDisconnected(self, reason = DISCONNECT_REASON.BY_REQUEST, description = None):
        if reason != DISCONNECT_REASON.BY_REQUEST:
            self.__address = None
        self.__handleEvent(GLOOX_EVENT.DISCONNECTED, reason, description)



    def onRosterItemSet(self, jid, name, groups, to, from_):
        self.__handleEvent(GLOOX_EVENT.ROSTER_ITEM_SET, ContactJID(jid), name, groups, to, from_)



    def onRosterItemRemoved(self, jid):
        self.__handleEvent(GLOOX_EVENT.ROSTER_ITEM_REMOVED, ContactJID(jid))



    def onRosterResourceAdded(self, jid, priority, status, presence):
        self.__handleEvent(GLOOX_EVENT.ROSTER_RESOURCE_ADDED, ContactJID(jid), priority, status, presence)



    def onRosterResourceRemoved(self, jid):
        self.__handleEvent(GLOOX_EVENT.ROSTER_RESOURCE_REMOVED, ContactJID(jid))



    def onSubscriptionRequest(self, jid, message):
        self.__handleEvent(GLOOX_EVENT.SUBSCRIPTION_REQUEST, ContactJID(jid), message)



    def onLog(self, level, source, message):
        self.__handleEvent(GLOOX_EVENT.LOG, level, source, message)



    def __handleEvent(self, eventName, *args, **kwargs):
        handlers = self.__handlers[eventName]
        for handler in handlers:
            try:
                handler(*args, **kwargs)
            except TypeError:
                g_logOutput.error(CLIENT_LOG_AREA.PY_WRAPPER, ' Handler is invoked with error', handler)
                LOG_CURRENT_EXCEPTION()





class ClientHolder(object):
    _client = None

    @classmethod
    def _setClient(cls, client):
        ClientEventsHandler._client = weakref.proxy(client)



    @classmethod
    def _clearClient(cls):
        cls._client = lambda *args: None



    def client(self):
        return ClientEventsHandler._client




class ClientEventsHandler(ClientHolder):

    def clear(self):
        pass



    def registerHandlers(self):
        raise NotImplementedError



    def unregisterHandlers(self):
        raise NotImplementedError




+++ okay decompyling gloox_wrapper.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:41:27 CET
