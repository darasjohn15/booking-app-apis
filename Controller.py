import Models.User
import Models.Event
import DAL.UsersDAL 
import DAL.EventsDAL
from flask import *
import Authentication

# Get the Users Data
usersData = DAL.UsersDAL.UsersDAL("UsersData.json")

#Get Events Data
eventsData = DAL.EventsDAL.EventsDAL("EventsData.json")

def auth(userName, password):
    
    #Get user data based on userName
    user = usersData.getUserByUsername(userName)

    if not user:
        return jsonify({'message' : 'User not found'}), 401

    currentUser = user['id']
    expectedPassword = user['password']

    if Authentication.authenticate(password, expectedPassword):
        token = Authentication.generateJWT(currentUser)
        return jsonify({'token': token })

    return jsonify({'message' : 'Invalid Login' })

def getUsers(token, userId):
    if Authentication.isTokenValid(token, userId):
        data_set = usersData.getUsers()
        return jsonify(data_set)
    
    return jsonify({'message' : 'Invalid Token.'}), 401

def getUser(token, currentUserId, userId):
    if Authentication.isTokenValid(token, currentUserId):
        data_set = usersData.getUserById(userId)
        return jsonify(data_set)
    
    return jsonify({'message' : 'Invalid Token.'}), 401

def createNewUser(token, currentUserId, firstName, lastName, age):
    if Authentication.isTokenValid(token, currentUserId):
        newUser = Models.User.User(firstName, lastName, age)
        usersData.addUser(newUser)
        return jsonify({ 'userName' : newUser.userName, 'password' : newUser.password})
    
    return jsonify({'message' : 'Invalid Token.'}), 401

def deactivateUser(token, currentUserId, userId):
    if Authentication.isTokenValid(token, currentUserId):
        usersData.deactivateUser(userId)
        return jsonify({ 'message' : 'User Deactivated'})
    
    return jsonify({'message' : 'Invalid Token.'})

def getEvents(token, currentUserId):
    if Authentication.isTokenValid(token, currentUserId):
        data_set = eventsData.getAllEvents()
        return jsonify(data_set)
    
    return jsonify({'message' : 'Invalid Token.'})

def getEventsByLocation(token, currentUserId, location):
    if Authentication.isTokenValid(token, currentUserId):
        data_set = eventsData.getEventsByLocation(location)
        return jsonify(data_set)

    return jsonify({'message' : 'Invalid Token.'})

def getEventsByHost(token, currentUserId, host):
    if Authentication.isTokenValid(token, currentUserId):
        data_set = eventsData.getEventsByHost(host)
        return jsonify(data_set)
    
    return jsonify({'message' : 'Invalid Token.'})

def getEventsByDate(token, currentUserId, month, year):
    if Authentication.isTokenValid(token, currentUserId):
        data_set = eventsData.getEventsByDate(month, year)
        return jsonify(data_set)
    
    return jsonify({'message' : 'Invalid Token.'})

def createNewEvent(token, currentUserId, name, date, hostID, location):
    if Authentication.isTokenValid(token, currentUserId):
        newEvent = Models.Event.Event(name, date, hostID, location)
        eventsData.createEvent(newEvent)
        return jsonify({'message' : 'Event Created.'})

    
    return jsonify({'message' : 'Invalid Token.'})

def cancelEvent(token, currentUserId, eventId):
    if Authentication.isTokenValid(token, currentUserId):
        cancelled = eventsData.cancelEvent(eventId)

        if(cancelled):
            return jsonify({'message' : 'Event Cancelled.'})
        else:
            return jsonify({'message': 'Could Not Cancelled'})
        
    return jsonify({'message' : 'Invalid Token.'})

def getEventPerformers(token, currentUserId, eventId):
    if Authentication.isTokenValid(token, currentUserId):

        #Get the list of userIds
        data_set = eventsData.getEventPerformers(eventId)

        #Get each performers info
        results = []
        for performer in data_set:
            performerInfo = usersData.getUser(performer)
            results.append(performerInfo)

        return jsonify(results)
    
    return jsonify({'message' : 'Invalid Token.'})

def getEventRequestedPerformers(token, currentUserId, eventId):
    if Authentication.isTokenValid(token, currentUserId):

        #Get the list of userIds
        data_set = eventsData.getEventRequestedPerformers(eventId)

        #Get each performers info
        results = []
        for performer in data_set:
            performerInfo = usersData.getUserById(performer)
            results.append(performerInfo)

        return jsonify(results)

    return jsonify({'message' : 'Invalid Token.'})

def requestEvent(token, currentUserId, eventId, userId):
    if Authentication.isTokenValid(token, currentUserId):
        requested = eventsData.requestEvent(eventId, userId)

        if (requested):
            return jsonify({'message' : 'Event Requested.'})
        else:
            return jsonify({'message' : 'Cannot request event.'})
    
    return jsonify({'message' : 'Invalid Token.'})

def approvePerformer(token, currentUserId, eventId, performerId):
    if Authentication.isTokenValid(token, currentUserId):
        approved = eventsData.approvePerformer(eventId, performerId)

        if(approved):
            return jsonify({'message' : 'Approved.'})
        else:
            return jsonify({'message' : 'Not Approved.'})
    
    return jsonify({'message' : 'Invalid Token.'})
    
def removePerformer(token, currentUserId, eventId, userId):
    if Authentication.isTokenValid(token, currentUserId):
        removed = eventsData.removePerformer(eventId, userId)

        if(removed):
            return jsonify({'message' : 'Performer Removed.'})
        else:
            return jsonify({'message' : 'Performer Not Found.'})
    
    return jsonify({'message' : 'Invalid Token.'})
    
def denyPerformer(token, currentUserId, eventId, userId):
    if Authentication.isTokenValid(token, currentUserId):
        denied = eventsData.denyPerformer(eventId, userId)

        if (denied):
            return jsonify({'message' : 'Performer Denied.'})
        else:
            return jsonify({'message' : 'Performer Not Found.'})
    
    return jsonify({'message' : 'Invalid Token.'})