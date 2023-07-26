import Models.User
import Models.Event
import Models.Message
import DAL.UsersDAL 
import DAL.EventsDAL
from flask import *
import Authentication

# Get the Users Data
usersData = DAL.UsersDAL.UsersDAL("UsersData.json")

#Get Events Data
eventsData = DAL.EventsDAL.EventsDAL("EventsData.json")

def auth(requestBody):
    #Get request values
    userName = requestBody['userName']
    password = requestBody['password']

    #Get user data based on userName
    user = usersData.getUserByUsername(userName)

    if not user:
        return jsonify({'message' : 'User not found'}), 401

    currentUser = user['id']
    expectedPassword = user['password']

    if Authentication.authenticate(password, expectedPassword):
        token = Authentication.generateJWT(currentUser)
        return jsonify({'token': token }), 200

    return jsonify({'message' : 'Invalid Login' }), 401

def getUsers(token, userId):
    if Authentication.isTokenValid(token, userId):
        data_set = usersData.getUsers()
        return jsonify(data_set), 200
    
    return jsonify({'message' : 'Invalid Token.'}), 401

def getUser(token, currentUserId, userId):
    if Authentication.isTokenValid(token, currentUserId):
        data_set = usersData.getUserById(userId)
        return jsonify(data_set), 200
    
    return jsonify({'message' : 'Invalid Token.'}), 401

def createNewUser(requestBody):
    #Get Request Values
    firstName = requestBody['firstName']
    lastName = requestBody['lastName']
    email = requestBody['email']
    userName = requestBody['userName']
    password = requestBody['password']
    age = requestBody['age']

    #Create User
    newUser = Models.User.User(firstName, lastName, email, userName, password, age)
    
    #Save New User to Database
    usersData.addUser(newUser)

    return jsonify({"userName": newUser.userName, "password": newUser.password}), 200

def deactivateUser(token, currentUserId):
    if Authentication.isTokenValid(token, currentUserId):
        usersData.deactivateUser(currentUserId)
        return jsonify({ 'message' : 'User Deactivated'}), 200
    
    return jsonify({'message' : 'Invalid Token.'}), 401

def activateUser(token, currentUserId):
    if Authentication.isTokenValid(token, currentUserId):
        usersData.activateUser(currentUserId)
        return jsonify({ 'message' : 'User Activated'}), 200
    
    return jsonify({'message' : 'Invalid Token.'}), 401

def editUserInfo(token, currentUserId, requestBody):
    if Authentication.isTokenValid(token, currentUserId):
        #Get New Values
        firstName = requestBody['firstName']
        lastName = requestBody['lastName']
        email = requestBody['email']
        age = requestBody['age']

        usersData.editUser(currentUserId, firstName, lastName, email, age)

        return jsonify({ 'message' : 'Info Updated!'}), 200
    
    return jsonify({'message' : 'Invalid Token.'}), 401

def changePassword(token, currentUserId, requestBody):
    if Authentication.isTokenValid(token, currentUserId):
        #Get request values
        requestOldPassword = requestBody['oldPassword']
        requestNewPassword = requestBody['newPassword']

        #Check if old password is correct
        originalPassword = usersData.getPassword(currentUserId)
        if (requestOldPassword != originalPassword):
            return jsonify({'message': 'Invalid Old Password.'}), 400
        
        #Update DB with new password
        usersData.changePassword(currentUserId, requestNewPassword)

        return jsonify({'message': "Password Updated!"}), 200

    return jsonify({'message': 'Invalid Token.'}), 401

def getMessages(token, currentUserId):
    if Authentication.isTokenValid(token, currentUserId):
        data_set = usersData.getMessages(currentUserId)
        return jsonify(data_set)

    return jsonify({'message': 'Invalid Token.'}), 401

def sendMessage(token, currentUserId, requestBody):

    if Authentication.isTokenValid(token, currentUserId):
        #Get Request Values
        recipientUserId = requestBody['userId']
        subject = requestBody['subject']
        message = requestBody['message']

        #Create Message
        newMessage = Models.Message.Message(subject, message, recipientUserId)

        usersData.addMessage(newMessage)
        return jsonify({'message': 'Message Sent!'}), 200

    return jsonify({'message': 'Invalid Token.'}), 401

def getEvents(token, currentUserId):
    if Authentication.isTokenValid(token, currentUserId):
        data_set = eventsData.getAllEvents()
        return jsonify(data_set), 200
    
    return jsonify({'message' : 'Invalid Token.'}), 401

def getActiveEvents(token, currentUserId):
    if Authentication.isTokenValid(token, currentUserId):
        data_set = eventsData.getActiveEvents()
        return jsonify(data_set), 200
    
    return jsonify({'message' : 'Invalid Token.'}), 401

def getEvent(token, currentUserId, eventId):
    if Authentication.isTokenValid(token, currentUserId):
        data_set = eventsData.getEvent(eventId)
        return jsonify(data_set), 200

    return jsonify({'message': 'Invalid Token.'}), 401
    
def getEventsByLocation(token, currentUserId, location):
    if Authentication.isTokenValid(token, currentUserId):
        data_set = eventsData.getEventsByLocation(location)
        return jsonify(data_set), 200

    return jsonify({'message' : 'Invalid Token.'}), 401

def getEventsByHost(token, currentUserId, host):
    if Authentication.isTokenValid(token, currentUserId):
        data_set = eventsData.getEventsByHost(host)
        return jsonify(data_set), 200
    
    return jsonify({'message' : 'Invalid Token.'}), 401

def getEventsByDate(token, currentUserId, month, year):
    if Authentication.isTokenValid(token, currentUserId):
        data_set = eventsData.getEventsByDate(month, year)
        return jsonify(data_set)
    
    return jsonify({'message' : 'Invalid Token.'}), 401

def createNewEvent(token, currentUserId, requestBody):
    if Authentication.isTokenValid(token, currentUserId):
        # Get request values
        name = requestBody['name']
        date = requestBody['date']
        location = requestBody['location']

        #Create Event Instance
        newEvent = Models.Event.Event(name, date, currentUserId, location)

        #Save to Database
        eventsData.createEvent(newEvent)

        return jsonify({'message' : 'Event Created.'}), 200

    
    return jsonify({'message' : 'Invalid Token.'}), 401

def cancelEvent(token, currentUserId, eventId):
    if Authentication.isTokenValid(token, currentUserId):
        cancelled = eventsData.cancelEvent(eventId)

        if(cancelled):
            return jsonify({'message' : 'Event Cancelled.'}), 200
        else:
            return jsonify({'message': 'Could Not Cancelled'}), 400
        
    return jsonify({'message' : 'Invalid Token.'}), 401

def activateEvent(token, currentUserId, eventId):
    if Authentication.isTokenValid(token, currentUserId):
        activated = eventsData.activateEvent(eventId)

        if(activated):
            return jsonify({'message' : 'Event Activated.'}), 200
        else:
            return jsonify({'message': 'Could Not Activated'}), 400
        
    return jsonify({'message' : 'Invalid Token.'}), 401

def editEvent(token, currentUserId, eventId, requestBody):
    if Authentication.isTokenValid(token, currentUserId):
        # Get Request Values
        eventName = requestBody['name']
        eventLocation = requestBody['location']
        eventDate = requestBody['date']

        #Update Database
        eventsData.editEvent(eventId, eventName, eventLocation, eventDate)

        return jsonify({'message': 'Event Updated!'}), 200

    return jsonify({'message': 'Invalid Token.'}), 401

def getEventPerformers(token, currentUserId, eventId):
    if Authentication.isTokenValid(token, currentUserId):

        #Get the list of userIds
        data_set = eventsData.getEventPerformers(eventId)

        #Get each performers info
        results = []
        for performer in data_set:
            performerInfo = usersData.getUser(performer)
            results.append(performerInfo)

        return jsonify(results), 200
    
    return jsonify({'message' : 'Invalid Token.'}), 401

def getEventRequestedPerformers(token, currentUserId, eventId):
    if Authentication.isTokenValid(token, currentUserId):

        #Get the list of userIds
        data_set = eventsData.getEventRequestedPerformers(eventId)

        #Get each performers info
        results = []
        for performer in data_set:
            performerInfo = usersData.getUserById(performer)
            results.append(performerInfo)

        return jsonify(results), 200

    return jsonify({'message' : 'Invalid Token.'}), 401

def requestEvent(token, currentUserId, eventId):
    if Authentication.isTokenValid(token, currentUserId):
        requested = eventsData.requestEvent(eventId, currentUserId)

        if (requested):
            return jsonify({'message' : 'Event Requested.'}), 200
        else:
            return jsonify({'message' : 'Cannot request event.'}), 400
    
    return jsonify({'message' : 'Invalid Token.'}), 401

def approvePerformer(token, currentUserId, eventId, performerId):
    if Authentication.isTokenValid(token, currentUserId):
        approved = eventsData.approvePerformer(eventId, performerId)

        if(approved):
            return jsonify({'message' : 'Approved.'}), 200
        else:
            return jsonify({'message' : 'Not Approved.'}), 400
    
    return jsonify({'message' : 'Invalid Token.'}), 401
    
def removePerformer(token, currentUserId, eventId, userId):
    if Authentication.isTokenValid(token, currentUserId):
        removed = eventsData.removePerformer(eventId, userId)

        if(removed):
            return jsonify({'message' : 'Performer Removed.'}), 200
        else:
            return jsonify({'message' : 'Performer Not Found.'}), 400
    
    return jsonify({'message' : 'Invalid Token.'}), 401
    
def denyPerformer(token, currentUserId, eventId, userId):
    if Authentication.isTokenValid(token, currentUserId):
        denied = eventsData.denyPerformer(eventId, userId)

        if (denied):
            return jsonify({'message' : 'Performer Denied.'}), 200
        else:
            return jsonify({'message' : 'Performer Not Found.'}), 400
    
    return jsonify({'message' : 'Invalid Token.'}), 401