from DAL.Database import DatabaseObject
import Helpers.DateHelper

class EventsDAL(DatabaseObject):

    def add_event(self, event):
        self._data.append(event)
        self.save()
        self.reload()

        print('Event Created!')
        print('')
    
    def get_events(self):
        return self._data
    
    def get_event(self, event_id):
        for x in self._data:
            if (x['id'] == event_id):
                return x
      
            
    def add_application(self, event_id, application):
        for x in self._data:
            if (x['id'] == event_id):
                x['applications'].append(application)
                self.save()
                self.reload()

    def approve_application(self, event_id, user_id):
        approved = False

        for x in self._data:
            if (x['id'] == event_id):
                x['performers'].append(user_id)
                approved = True
                
                applications = x['applications']
                for application in applications:
                    if(application['user_id'] == user_id):
                        applications.remove(application)
                        break

                self.save()
                self.reload()
                break

        return approved
    
    def cancelEvent(self, eventID):
        deactivated = False
        found = False
        for x in self._data:
            if (x['id'] == eventID):
                found = True
                print('Events DAL: Event ' + eventID + ' found.')

                x['active'] = False
                deactivated = True
                print('Events DAL: Event ' + eventID + ' cancelled.')

        if (deactivated):
            self.save()
            self.reload()
            print('Events DAL: Database saved and reloaded.')
            return True
        else:
            if (found):
                print('Events DAL: Event ' + eventID + ' could not be cancelled.')
            else:
                print('Events DAL: Event ' + eventID + ' could not found.')
            
            return False

    def activateEvent(self, eventID):
        activated = False
        found = False
        for x in self._data:
            if (x['id'] == eventID):
                found = True
                print('Events DAL: Event ' + eventID + ' found.')

                x['active'] = True
                activated = True
                print('Events DAL: Event ' + eventID + ' activated.')

        if (activated):
            self.save()
            self.reload()
            print('Events DAL: Database saved and reloaded.')
            return True
        else:
            if (found):
                print('Events DAL: Event ' + eventID + ' could not be activated.')
            else:
                print('Events DAL: Event ' + eventID + ' could not found.')
            
            return False
    
    def editEvent(self, eventId, eventName, eventLocation, eventDate):
        for x in self._data:
            if (x['id'] == eventId):
                x['name'] = eventName
                x['location'] = eventLocation
                x['date'] = eventDate
                
                self.save()
                self.reload()

                print('Event Updated!')

    def getEventsByLocation(self, location):
        hasEvents = False
        results = []
        for x in self._data:
            if (x['location'] == location):
                results.append(x)
                hasEvents = True

        if (not hasEvents):
            print('')
            print('No events...')

        return results


    def getEventsByDate(self, month, year):
        results = []
        for x in self._data:
            if (x['active'] == True and Helpers.DateHelper.getMonthFromDate(x['date']) == month and Helpers.DateHelper.getYearFromDate(x['date']) == year):
                results.append(x)
        
        return results
    
    def getAllEvents(self):
        return self._data

    def getActiveEvents(self):
        results = []
        for x in self._data:
            if (x['active'] == True):
                results.append(x)
        
        return results

    
    
    
    
    def getEventPerformers(self, eventId):
        for x in self._data:
            if (x['id'] == eventId):
                return x['performers'] 
            
        return ''
    
    def getEventRequestedPerformers(self, eventId):
        events = self._data
        for event in events:
            if (event['id'] == eventId):
                return event['requestedPerformers']
        
        return ''
    
    def requestEvent(self, eventId, userId):
        events = self._data
        for event in events:
            if (event['id'] == eventId):
                event['requestedPerformers'].append(userId)
                self.save()
                self.reload()
                return True
            
        return False
    

    
    def removePerformer(self, eventId, userId):
        removed = False

        for event in self._data:
            if (event['id'] == eventId):
                event['performers'].remove(userId)
                self.save()
                self.reload()
                removed = True
                break
        
        return removed
    
    def denyPerformer(self, eventId, userId):
        denied = False

        for event in self._data:
            if (event['id'] == eventId):
                event['requestedPerformers'].remove(userId)
                self.save()
                self.reload()
                denied = True
                break
        
        return denied
            
        
            
        