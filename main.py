from flask import *
from connect import *

app = Flask(__name__)

#Connection Funnction
def connection():
    collection = db_connect().mongo_connect()
    return collection

@app.route("/",methods=["GET"])
def sample_api():
    return "sample api showing that it worked"

@app.route("/scanned",methods=["POST"])
def scanned():
    collection = connection()
    data = request.get_json(force = True)
    id = data["id"]
    print(data,"\n",id)
    for i in collection.find({"id" : id}):
        if int(i["issued_bool"]):
            return "This book is already issued to {0} and the fine amount is {1}".format(i["student_name"],i["fine_rem"])
        else:
            return "This book is not issued"
    return "None"


if __name__ == "__main__":
    app.run(host="192.168.1.7" , port="8900")

