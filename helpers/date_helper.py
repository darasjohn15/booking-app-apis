import datetime

def get_month(date):
        return date[:2]

def get_year(date):
        return date[6:]

def covert_to_date(dateInMilliseconds):
        return datetime.datetime.fromtimestamp(dateInMilliseconds)

def get_token_expiration():
        return datetime.datetime.utcnow() + datetime.timedelta(hours=24)