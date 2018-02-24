//get an iterator of BWUserEntity Type
messenger.proto.bw.ClanListener.usersStorage.getClanMembersIterator()

//function to apply to a BWUserEntity
messenger.proto.bw.clanlistener.BWUserEntity

//get a list of all opened channels
messenger.proto.bw.ChannelsManager.channelsStorage.all()

//add a message to the clan window
messenger.proto.bw.ChannelsManager.channelsStorage.all()[3].addMessage('test')

//to send a message
BigWorld.player().broadcast(idChan, message)

//to get the roster, 1: in line up, 17 reserve
BigWorld.player().prebattle.rosters

//get vehDescriptor
BigWorld.player().prebattle.rosters.values()[0][20552299]['vehCompDescr']

//get vehicle object from Vehicle Descriptor
items.vehicles.VehicleDescr(desc)

items.vehicles.VehicleDescr(BigWorld.player().prebattle.rosters.values()[0][20552299]['vehCompDescr']).name

BigWorld.player().prebattle.rosters[2][]

//refresh CW roster gui
BigWorld.player().prebattle.onTeamStatesReceived()
BigWorld.player().prebattle.onRosterReceived()

//sort list
sorted(roster.items(), key=lambda x: x[1]['time'])

//debugview ?
DebugView.setVisible(true)

//
from clientchat import buildChatActionData
buildChatActionData(action,requestID,channelId,originatorNickname,data,actionResponse)

clientchat.ClientChat.onChatAction
