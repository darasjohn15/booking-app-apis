import Authentication
import User
import Event
import json
import UsersDatabase
import EventsDatabase
from flask import *

# Get the Users Database data
usersDB = UsersDatabase.UsersDatabase("UsersDatabase.json")

#Get Events Data
eventsDB = EventsDatabase.EventsDatabase("EventsDatabase.json")

def getUsers():
    data_set = usersDB.getUsers()
    json_object = json.dumps(data_set)
    return json_object

def getUser(id):
    data_set = usersDB.getUser(id)
    json_object = json.dumps(data_set)
    return json_object

def createNewUser(firstName, lastName, age):
    newUser = User.User(firstName, lastName, age)
    usersDB.addUser(newUser)
    json_object = json.dumps(newUser, default=lambda o: o.__dict__, indent=4)
    return json_object

def deactivateUser(userId):
    usersDB.deactivateUser(userId)
    return getUser(userId)

def getEvents():
    data_set = eventsDB.getAllEvents()
    json_object = json.dumps(data_set)
    return json_object

def getEventsByLocation(location):
    data_set = eventsDB.getEventsByLocation(location)
    json_object = json.dumps(data_set)
    return json_object

def getEventsByHost(host):
    data_set = eventsDB.getEventsByHost(host)
    json_object = json.dumps(data_set)
    return json_object

def getEventsByDate(month, year):
    data_set = eventsDB.getEventsByDate(month, year)
    json_object = json.dumps(data_set)
    return json_object

def createNewEvent(name, date, hostID, location):
    newEvent = Event.Event(name, date, hostID, location)
    eventsDB.createEvent(newEvent)
    json_object = json.dumps(newEvent, default=lambda o: o.__dict__, indent=4)
    return json_object

def cancelEvent(eventId):
    cancelled = eventsDB.cancelEvent(eventId)

    if(cancelled):
        return 'Cancelled'
    else:
        return 'Could Not Cancelled'

def getEventPerformers(eventId):

    #Get the list of userIds
    data_set = eventsDB.getEventPerformers(eventId)

    #Get each performers info
    results = []
    for performer in data_set:
        performerInfo = usersDB.getUser(performer)
        results.append(performerInfo)

    json_object = json.dumps(results)
    return json_object

def getEventRequestedPerformers(eventId):

    #Get the list of userIds
    data_set = eventsDB.getEventRequestedPerformers(eventId)

    #Get each performers info
    results = []
    for performer in data_set:
        performerInfo = usersDB.getUser(performer)
        results.append(performerInfo)

    json_object = json.dumps(results)
    return json_object

def requestEvent(eventId, userId):
    requested = eventsDB.requestEvent(eventId, userId)

    if (requested):
        return "Requested"
    else:
        return "User Not Found"

def approvePerformer(eventId, performerId):
    approved = eventsDB.approvePerformer(eventId, performerId)

    if(approved):
        return 'Approved'
    else:
        return 'Not Approved'
    
def removePerformer(eventId, userId):
    removed = eventsDB.removePerformer(eventId, userId)

    if(removed):
        return 'Removed'
    else:
        return 'Performer Not Found'
    
def denyPerformer(eventId, userId):
    denied = eventsDB.denyPerformer(eventId, userId)

    if (denied):
        return 'User Denied'
    else:
        return 'User Not Found'