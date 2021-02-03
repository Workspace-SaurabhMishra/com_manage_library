from flask import *
from connect import *
import datetime

app = Flask(__name__)


# Connection Funnction
def connection():
    collection = db_connect().mongo_connect()
    return collection


@app.route("/just_4_test_baby", methods=["GET"])
def sample_api():
    return "<h1>sample api showing that<br>APIs created by saurabh mishra are working</h1>"


def cal_fine(start):
    start = start.split("-")
    diff = datetime.date.today() - datetime.date(int(start[0]), int(start[1]), int(start[2]))
    return str(diff.days * 2)


@app.route("/new_book", methods=["POST"])
def new_books():
    rec_data = request.get_json(force=True)
    collection = connection()
    ins_data = {
        "id": rec_data["id"],
        "price": rec_data["price"],
        "author": rec_data["author"],
        "name": rec_data["name"],
        "student_id": "",
        "student_name": "",
        "issued_date": ""
    }
    collection.insert_one(ins_data)
    return "Registered New Book"


@app.route("/return_", methods=["POST"])
def return_():
    collection = connection()
    rec_data = request.get_json(force=True)
    ins_data = {
        "student_id": "",
        "student_name": "",
        "issued_date": ""
    }
    collection.update_one({"id": rec_data["id"]}, {"$set": ins_data})
    return "Done Bro!!"

@app.route("/book_info", methods=["POST"])
def book_info():
    collection = connection()
    rec_data = request.get_json(force=True)
    for i in collection.find({"id": rec_data["id"]}):
        if i["student_name"] != "":
            ins_data = {
                "id": i["id"],
                "student_id": i["student_id"],
                "student_name":i["student_name"],
                "author": i["author"],
                "fine_rem": cal_fine(i["issued_date"])
            }
            return ins_data
    else:
        return "0"
    return "0"


@app.route("/issue", methods=["POST"])
def issue():
    collection = connection()
    rec_data = request.get_json(force=True)
    id = rec_data["id"]
    ins_data = {
        "student_name": rec_data["student_name"],
        "student_id": rec_data["student_id"],
        "issued_date": str(datetime.date.today())
    }
    x = collection.find({"id": id})
    for i in x:
        if i["student_name"] != "":
            return "Book already issued"
        collection.update_one({"id": rec_data["id"]}, {"$set": ins_data})
        return "Done"
    return "This book doesn't exist in database"


if __name__ == "__main__":
    app.run(host="192.168.43.169", port="8900")
