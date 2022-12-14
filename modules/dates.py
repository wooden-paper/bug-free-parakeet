from .ftp import MyFTP
from datetime import *

"""
------------------------
    DOCUMENTATION
------------------------
Functions: retrieve_dates, get_date
    Explaination: takes two dates and returns files within that range (inclusive) from an FTP server
Parameters: from_date, to_date, myFTP
    Assumption: from_date and to_date are strings of form YYYY-MM-DD 
    e.g. input("What is your start date as YYYY-MM-DD: ") with input 2020-01-01 <- from_date
Returns: requested_dates, invalid
    Explaination: An array of files between the start and end date of form MED_DATE_YYYYMMDDHHMMSS.csv
NB: Requires valid YYYYMMDD to work (e.g. 20200145 would not be accepted and would be in invalid)
"""


def get_date(offset: int = 0):
    timestamp = datetime.today() - timedelta(days=-offset)
    return timestamp.date().isoformat()


def retrieve_dates(ftp: MyFTP, from_date, to_date):
    invalid = []
    data = ftp.get_files_in_current_directory()
    
    # convert formatted data into dates
    dates = []
    for each in data:
        try:
            year = int(each[9:13])
            month = int(each[13:15])
            day = int(each[15:17])
            dates.append(date(year, month, day))
        except ValueError:
            print(year, month, day)
            invalid.append({"name": each, "valid": False})
    # takes request for dates
    starty, startm, startd = [int(i) for i in from_date.split("-")]
    endy, endm, endd = [int(j) for j in to_date.split("-")]
    start = date(starty, startm, startd)
    end = date(endy, endm, endd)
    # finds the filenames for the requested dates
    requested_dates = []
    for k in range(0, len(dates)):
        if start <= dates[k] <= end:
            requested_dates.append(data[k])
    print(requested_dates)
    return requested_dates, invalid
