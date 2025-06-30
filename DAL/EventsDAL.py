from DAL.Database import DatabaseObject
import Helpers.DateHelper
from db import get_db_connection
from psycopg2.extras import RealDictCursor

def get_event(event_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM Event_GET(%s);", (event_id,))
    event = cur.fetchone()
    cur.close()
    conn.close()
    return event

def get_events(host_id=None, active=None, location=None, venue_id=None, date_start=None, date_end=None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM Events_GET(%s, %s, %s, %s, %s, %s);", (host_id, active, location, venue_id, date_start, date_end))
    events = cur.fetchall()
    cur.close()
    conn.close()

    return events

def create_event(host_id, venue_id, title, description, location, date):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM Event_CREATE(%s, %s, %s, %s, %s, %s);", 
                (host_id, venue_id, title, description, location, date))

    new_event = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return new_event

def update_event(event_id, title=None, date=None, venue_id=None, description=None, is_active=None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute(
        "SELECT * FROM Event_UPDATE(%s, %s, %s, %s, %s, %s);",
        (event_id, title, date, venue_id, description, is_active)
    )
    
    updated_event = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    return updated_event


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

    def update_event(self, id, title, date, host_id, venue_id, description, active):
        for x in self._data:
            if (x['id'] == id):
                x['title'] = title or x['title']
                x['date'] = date or x['date']
                x['host_id'] = host_id or x['host_id']
                x['venue_id'] = venue_id or x['venue_id']
                x['description'] = description or x['description']
                x['active'] = active
                
                self.save()
                self.reload()

                print('Event Updated!')
                return True
        return False
            
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
            
        
            
        