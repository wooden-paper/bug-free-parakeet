import csv
import os
from os.path import exists
import re
from datetime import datetime
filename = ""
# log why it was invalid in a file
def log(
    message: str, error: bool, invalid: bool, code: int, file_name: str
):  # code 1 and 2 are the same thing (oops)
    # write to a log file with reason
    dt = datetime.now()
    dt = datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")
    if error:
        write_string = f'{dt}\nERROR: Code {code}\nFile: "{file_name}"\n{message}\n\n'
    elif invalid:
        write_string = f'{dt}\nINVLD: Code {code}\nFile: "{file_name}"\n{message}\n\n'
    else:
        write_string = f'{dt}\nLOGGING ERROR: \nCode: N/A\nFile: "{file_name}"\n\n'
    with open("logfile.txt", "a") as log_file:
        log_file.write(str(write_string))
# get csv
def validate_csv(file_name):
    valid_headers = [
        "batch_id",
        "timestamp",
        "reading1",
        "reading2",
        "reading3",
        "reading4",
        "reading5",
        "reading6",
        "reading7",
        "reading8",
        "reading9",
        "reading10",
    ]
    valid = True
    batch_ids = []
    # CHECK FOR INVALID FILENAME (using regex)
    if re.search("^MED_DATA_[0-9]{14}\.csv$", file_name) is None:
        # log: if filename is invalid
        log("filename invalid", True, False, 8, file_name)
        return {"valid": False, "name": file_name}
    # CHECK IF FILE EXISTS (this probably belongs somewhere else but i've put here anyway)
    if not exists(file_name):
        log("file does not exist", True, False, 10, file_name)
        return {"valid": False, "name": file_name}
    # CHECK IF EMPTY
    if os.stat(file_name).st_size == 0:
        valid = False
        # log: & report file is empty (error)
        log("file is empty", True, False, 7, file_name)
        # exit/return here as the rest won't work
        return {"valid": False, "name": file_name}
    # validate whether the actual date is a real one
    try:
        datetime.strptime(str(file_name[9:23]), "%Y%m%d%H%M%S")
        # or date_object = datetime.strptime(DATE, '%Y-%m-%d %H:%M:%S')
        # if you need the actual date object later
    except ValueError:
        log(
            "timestamp is not a real timestamp", False, True, 2, file_name
        )  # handle invalid date
        return {"valid": False, "name": file_name}
    with open(file_name) as csv_file:
        # CHECK FORMATTING HERE
        invalid_value_found = False
        bad_header = False
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        try:
            for row in csv_reader:
                # check if row is the expected length (i.e. data is valid)
                if len(row) != 12:
                    # -log: either a null value was encountered or this row was not the expected length
                    log(
                        "row was not expected length (can be caused by null values)",
                        False,
                        True,
                        1,
                        file_name,
                    )
                    return {"valid": False, "name": file_name}
                # checking data values and headers themselves are okay
                if line_count == 0:  # 1.HEADER LINE
                    row_length = len(row)
                    # ./if headers invalid, it is bad - (i could but) probably won't correct these invalid entries
                    for i in range(row_length):
                        if row[i] != valid_headers[i]:
                            valid = False
                            bad_header = True
                else:  # 2.REST OF LINES
                    # ./make a list of batch ids in this file (check once for loop is done)
                    batch_ids.append(row[0])
                    # ./check for readings above 10 and below 0 (if there is, bad) - also includes timestamp verification
                    for i in range(2, 12):
                        if (
                            not (float(row[i]) >= 0)
                            or not (float(row[i]) < 10)
                            or row[i] == ""
                        ):
                            valid = False
                            invalid_value_found = True
                    # ./check if timestamps don't match filename
                    if float(str(row[1]).replace(":", "")) != float(file_name[17:23]):
                        valid = False
                        log("timestamp does not match data", False, True, 5, file_name)
                line_count = line_count + 1
            # ./check if duplicates exist in the batch ids
            if len(list(set(batch_ids))) != len(batch_ids):
                # -log: duplicate batch ids exist in this file
                log("duplicate batch id", False, True, 6, file_name)
                valid = False
            # if an invalid value was found earlier, log it
            if invalid_value_found:
                # -log: value is bad
                log("a value was out of bounds", False, True, 4, file_name)
            if bad_header:
                # -log: invalid headers
                log("bad header(s)", False, True, 3, file_name)
        except:
            log("file is malformed or unreadable", True, False, 9, file_name)
            valid = False
    # return true or false!!!
    if valid:
        return {"valid": True, "name": file_name}
    return {"valid": False, "name": file_name}
if __name__ == "__main__":  # for testing/running standalone (manually input filename)
    filename = input("\nplease enter filename or path: ")
    print(str(validate_csv(filename)))