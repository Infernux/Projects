# 2015.01.14 22:41:28 CET
import types
from debug_utils import LOG_ERROR
from messenger.proto.interfaces import IProtoSettings
from messenger.proto.xmpp.gloox_wrapper import CONNECTION_IMPL_TYPE
from messenger.proto.xmpp.jid import JID
import random
_NUMBER_OF_ITEMS_IN_SAMPLE = 2

def _makeSample(*args):
    queue = []
    for seq in args:
        count = min(len(seq), _NUMBER_OF_ITEMS_IN_SAMPLE)
        queue.extend(random.sample(seq, count))

    return queue



def _validateConnection(record):
    result = True
    if len(record) == 2:
        (host, port,) = record
        if not host:
            result = False
        if type(port) is not types.IntType:
            result = False
    else:
        result = False
    return result



class ConnectionsIterator(object):

    def __init__(self, base = None, alt = None, bosh = None):
        super(ConnectionsIterator, self).__init__()
        self.__tcp = _makeSample(base or [], alt or [])
        self.__bosh = _makeSample(bosh or [])



    def __iter__(self):
        return self



    def __len__(self):
        return len(self.__tcp) + len(self.__bosh)



    def clear(self):
        self.__tcp = []
        self.__bosh = []



    def hasNext(self):
        return len(self.__tcp) > 0 or len(self.__bosh) > 0



    def next(self):
        if self.__tcp:
            cType = CONNECTION_IMPL_TYPE.TCP
            (host, port,) = self.__tcp.pop(0)
        elif self.__bosh:
            cType = CONNECTION_IMPL_TYPE.BOSH
            (host, port,) = self.__bosh.pop(0)
        else:
            raise StopIteration
        return (cType, host, port)




class XmppServerSettings(IProtoSettings):
    __slots__ = ('enabled', 'connections', 'domain', 'port', 'resource', 'altConnections', 'boshConnections')

    def __init__(self):
        super(XmppServerSettings, self).__init__()
        self.clear()



    def __repr__(self):
        return 'XmppServerSettings(enabled = {0!r:s}, connections = {1!r:s}, altConnections = {2!r:s}, boshConnections = {3!r:s}, domain = {4:>s}, port = {5:n}, resource = {6:>s})'.format(self.enabled, self.connections, self.altConnections, self.boshConnections, self.domain, self.port, self.resource)



    def update(self, data):
        if 'xmpp_connections' in data:
            self.connections = filter(_validateConnection, data['xmpp_connections'])
        else:
            self.connections = []
        if 'xmpp_alt_connections' in data:
            self.altConnections = filter(_validateConnection, data['xmpp_alt_connections'])
        else:
            self.altConnections = []
        if 'xmpp_bosh_connections' in data:
            self.boshConnections = filter(_validateConnection, data['xmpp_bosh_connections'])
        else:
            self.boshConnections = []
        if 'xmpp_host' in data:
            self.domain = data['xmpp_host']
        else:
            self.domain = ''
        if 'xmpp_port' in data:
            self.port = data['xmpp_port']
        else:
            self.port = -1
        if 'xmpp_resource' in data:
            self.resource = data['xmpp_resource']
        else:
            self.resource = ''
        if 'xmpp_enabled' in data:
            self.enabled = data['xmpp_enabled']
            if self.enabled and not self.connections and not self.altConnections and not self.boshConnections and not self.domain:
                LOG_ERROR('Can not find host to connection. XMPP is disabled', self.connections, self.altConnections, self.domain)
                self.enabled = False
        else:
            self.enabled = False



    def clear(self):
        self.enabled = False
        self.connections = []
        self.altConnections = []
        self.boshConnections = []
        self.domain = None
        self.port = -1
        self.resource = ''



    def isEnabled(self):
        return self.enabled



    def getFullJID--- This code section failed: ---
0	LOAD_FAST         'databaseID'
3	POP_JUMP_IF_TRUE  '18'
6	LOAD_ASSERT       'AssertionError'
9	LOAD_CONST        "Player's databaseID can not be empty"
12	CALL_FUNCTION_1   ''
15	RAISE_VARARGS     ''
18	LOAD_GLOBAL       'JID'
21	CALL_FUNCTION_0   ''
24	STORE_FAST        'jid'
27	LOAD_FAST         'jid'
30	LOAD_ATTR         'setNode'
33	LOAD_FAST         'databaseID'
36	CALL_FUNCTION_1   ''
39	POP_TOP           ''
40	LOAD_FAST         'jid'
43	LOAD_ATTR         'setDomain'
46	LOAD_FAST         'self'
49	LOAD_ATTR         'domain'
52	CALL_FUNCTION_1   ''
55	POP_TOP           ''
56	LOAD_FAST         'jid'
59	LOAD_ATTR         'setResource'
62	LOAD_FAST         'self'
65	LOAD_ATTR         'resource'
68	CALL_FUNCTION_1   ''
71	POP_TOP           ''
72	LOAD_FAST         'jid'
75	RETURN_VALUE      ''
-1	RETURN_LAST       ''

Syntax error at or near `RETURN_VALUE' token at offset 75

    def getConnectionsIterator(self):
        iterator = ConnectionsIterator(self.connections, self.altConnections, self.boshConnections)
        if not iterator.hasNext():
            iterator = ConnectionsIterator([(self.domain, self.port)])
        return iterator




# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2015.01.14 22:41:28 CET
