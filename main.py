from flask import *
from connect import *
import datetime

app = Flask(__name__)

#Connection Funnction
def connection():
    collection = db_connect().mongo_connect()
    return collection

@app.route("/",methods=["GET"])
def sample_api():
    return "sample api showing that it worked"

def cal_fine(start):
    duration = str(datetime.date.today()-start)[0:3]
    return str(int(duration)*2)

@app.route("/book_info",methods=["POST"])
def book_info():
    collection = connection()
    rec_data = request.get_json(force=True)
    for i in collection.find({"id":rec_data["id"]}):
        ins_data = {
            "id": i["id"],
            "student_id": i["student_id"],
            "author": i["author"],
            "fine_rem": cal_fine(i["issue_date"]),
        }
        return ins_data
    return "No match found"

@app.route("/issue",methods=["POST"])
def issue():
    collection = connection()
    rec_data = request.get_json(force = True)
    print(rec_data)
    id = rec_data["id"]
    ins_data = {
                "student_name":rec_data["student_name"],
                "student_id":rec_data["student_id"],
                "issue_date":datetime.date.today(),
                "fine_rem":0,
                "issued_bool":"1"
                }
    for i in collection.find({"id" : id}):
        collection.update_one({"id":rec_data["id"]},{"$set":ins_data})
        return "Done"
    return "This book doesn't exist in database"


if __name__ == "__main__":
    app.run(host="192.168.146.182" , port="8900")

