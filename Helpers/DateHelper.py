import datetime

def getMonthFromDate(date):
        return date[:2]

def getYearFromDate(date):
        return date[6:]

def convertIntToDate(dateInMilliseconds):
        return datetime.datetime.fromtimestamp(dateInMilliseconds)

def getTokenExpiration():
        return datetime.datetime.utcnow() + datetime.timedelta(minutes=60)