import Models.User
import Models.Event
import DAL.UsersDAL 
import DAL.EventsDAL
import json
from flask import *

# Get the Users Database data
usersData = DAL.UsersDAL.UsersDAL("UsersData.json")

#Get Events Data
eventsData = DAL.EventsDAL.EventsDAL("EventsData.json")

def getUsers():
    data_set = usersData.getUsers()
    json_object = json.dumps(data_set)
    return json_object

def getUser(id):
    data_set = usersData.getUser(id)
    json_object = json.dumps(data_set)
    return json_object

def createNewUser(firstName, lastName, age):
    newUser = Models.User.User(firstName, lastName, age)
    usersData.addUser(newUser)
    json_object = json.dumps(newUser, default=lambda o: o.__dict__, indent=4)
    return json_object

def deactivateUser(userId):
    usersData.deactivateUser(userId)
    return getUser(userId)

def getEvents():
    data_set = eventsData.getAllEvents()
    json_object = json.dumps(data_set)
    return json_object

def getEventsByLocation(location):
    data_set = eventsData.getEventsByLocation(location)
    json_object = json.dumps(data_set)
    return json_object

def getEventsByHost(host):
    data_set = eventsData.getEventsByHost(host)
    json_object = json.dumps(data_set)
    return json_object

def getEventsByDate(month, year):
    data_set = eventsData.getEventsByDate(month, year)
    json_object = json.dumps(data_set)
    return json_object

def createNewEvent(name, date, hostID, location):
    newEvent = Models.Event.Event(name, date, hostID, location)
    eventsData.createEvent(newEvent)
    json_object = json.dumps(newEvent, default=lambda o: o.__dict__, indent=4)
    return json_object

def cancelEvent(eventId):
    cancelled = eventsData.cancelEvent(eventId)

    if(cancelled):
        return 'Cancelled'
    else:
        return 'Could Not Cancelled'

def getEventPerformers(eventId):

    #Get the list of userIds
    data_set = eventsData.getEventPerformers(eventId)

    #Get each performers info
    results = []
    for performer in data_set:
        performerInfo = usersData.getUser(performer)
        results.append(performerInfo)

    json_object = json.dumps(results)
    return json_object

def getEventRequestedPerformers(eventId):

    #Get the list of userIds
    data_set = eventsData.getEventRequestedPerformers(eventId)

    #Get each performers info
    results = []
    for performer in data_set:
        performerInfo = usersData.getUser(performer)
        results.append(performerInfo)

    json_object = json.dumps(results)
    return json_object

def requestEvent(eventId, userId):
    requested = eventsData.requestEvent(eventId, userId)

    if (requested):
        return "Requested"
    else:
        return "User Not Found"

def approvePerformer(eventId, performerId):
    approved = eventsData.approvePerformer(eventId, performerId)

    if(approved):
        return 'Approved'
    else:
        return 'Not Approved'
    
def removePerformer(eventId, userId):
    removed = eventsData.removePerformer(eventId, userId)

    if(removed):
        return 'Removed'
    else:
        return 'Performer Not Found'
    
def denyPerformer(eventId, userId):
    denied = eventsData.denyPerformer(eventId, userId)

    if (denied):
        return 'User Denied'
    else:
        return 'User Not Found'