from modules.validation import validate_csv
from modules.dates import *
from flask import Flask, request, Response
from modules.ftp import MyFTP
from creds import creds
import json
import os

app = Flask(__name__)
ftp = MyFTP(**creds)


@app.route("/api/get/<file_name>")
def getfile(file_name: str):
    try:
        f = open(f"{os.getcwd()}/temp/{file_name}", "wb")
        try:
            ftp.download_local(file_name, f)
            f.close()
        except:
            return (
                Response(
                    json.dumps({"message": "File not found"}),
                    mimetype="application/json",
                ),
                404,
            )

        data = open(f"{os.getcwd()}/temp/{file_name}", "rb").read()
        os.remove(f"{os.getcwd()}/temp/{file_name}")

        return Response(
            data,
            mimetype="text/csv",
            headers={"Content-disposition": f"attachment; filename={file_name}"},
        )
    except:
        return (
            Response(
                json.dumps({"message": "File not found"}), mimetype="application/json"
            ),
            404,
        )


@app.route("/api/validate")
def validate():
    date_from = request.args.get("from", default=get_date(-7), type=str)
    to = request.args.get("to", default=get_date(), type=str)
    file_names, validity = retrieve_dates(ftp, date_from, to)
    print(file_names)
    for file in file_names:
        f = open(f"{os.getcwd()}/temp/{file}", "wb")
        ftp.download_local(file, f)
        f.close()
        validity.append(
            validate_csv(file, open(f"{os.getcwd()}/temp/{file}", "r"))
        )  # format {"valid":bool, "name": str}
        os.remove(f"{os.getcwd()}/temp/{file}")
    valid = [a for a in validity if a["valid"]]
    return Response(json.dumps(validity), mimetype="application/json")
