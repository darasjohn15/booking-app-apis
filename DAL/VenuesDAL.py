from DAL.Database import DatabaseObject

class VenuesDAL(DatabaseObject):
    def get_venues(self):
        return self._data