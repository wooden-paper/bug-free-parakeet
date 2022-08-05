from modules.validation import validate_csv
from modules.dates import retrieve_dates
from flask import Flask, request
from modules.ftp import MyFTP
import json

app = Flask(__name__)


@app.route("/api/get/<file_name>")
def hello_world(file_name: str):
    try:
        with open(f"data/{file_name}", "r") as f:
            return f
    except:
        return json.stringify({"message": "File not found"}), 404


@app.route("/api/validate/<file_name>")
def validate(file_name: str):
    date_from = request.args.get("from", default=get_date(-7), type=str)
    to = request.args.get("to", default=get_date(), type=str)
    file_names = get_files(date_from, to)
    validity = []
    for file in file_names:
        validity.append(run_validation(file))  # format {"valid":bool, "name": str}
    valid = [a for a in validity if a["valid"] == True]
