from flask import Flask, jsonify
from flask import request
from flask_cors import CORS,cross_origin
from setup import *
from util import *
from bson.objectid import ObjectId
import random

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def healthcheck():
    return "<p>Backend is running..</p>"

@app.route("/username_available", methods=['POST'])
def username_available():
    recieved_body = request.json
    id = recieved_body['id']
    user = db.users.find_one({"user": id})
    if user is None:
        return "true"
    else:
        return "false"

@app.route("/create_user", methods=['POST'])
def create_user():
    recieved_body = request.json
    id = recieved_body['id']
    user = db.users.find_one({"user": id})
    LISTING_PRICE = random.randint(5, 50) * 100000
    true_value_percentage = random.randint(1, 10)
    true_value_sign = random.choice([-1, 1])
    TRUE_VALUE = LISTING_PRICE + true_value_sign * true_value_percentage/100 * LISTING_PRICE
    TRUE_VALUE = int(TRUE_VALUE/1000 )* 1000
    #  Debt from 0 to 90 in increments of 10
    DEBT = random.randint(0, 9) * 10
    MOTIVATION_LEVEL = random.choice(["Very Motivated", "Somewhat Motivated", "Not Motivated"])

    db.users.insert_one({"user": id,
        "listing_price": LISTING_PRICE,
        "true_value": TRUE_VALUE,
        "debt": DEBT,
        "motivation_level": MOTIVATION_LEVEL,
        "time": datetime.now()})
    return jsonify({"listing_price": LISTING_PRICE, "true_value": TRUE_VALUE, "debt": DEBT, "motivation_level": MOTIVATION_LEVEL})

@app.route("/reply", methods=['POST'])
def reply():
    # LISTING_PRICE = 600000
    # TRUE_VALUE = 550000
    # DEBT = 20
    # MOTIVATION_LEVEL = "Less Motivated"
    recieved_body = request.json
    studentResponse = recieved_body['msg']
    id = recieved_body['id']
    user = db.users.find_one({"user": id})
    LISTING_PRICE = user["listing_price"]
    TRUE_VALUE = user["true_value"]
    DEBT = user["debt"]
    MOTIVATION_LEVEL = user["motivation_level"]
    if user is None:
        db.users.insert_one({"user": id,
                             "listing_price": LISTING_PRICE,
                                "true_value": TRUE_VALUE,
                                "debt": DEBT,
                                "motivation_level": MOTIVATION_LEVEL,
                              "time": datetime.now()})
    documents = db.messages.find({"user": id}).sort("time", 1)
    conversation_memory = [{"message": doc.get("message", ""), "sender": doc.get("sender", "")} for doc in documents]
    conversation_memory.append({"message": studentResponse, "sender": "student"})
    conversation_as_string = format_conversation(conversation_memory)
    final_prompt=prompt_1.format(conversation_as_string, LISTING_PRICE, TRUE_VALUE, DEBT, MOTIVATION_LEVEL)  
    out = get_response_from_openai(final_prompt)

    db.messages.insert_one({
        "message": studentResponse,
        "id": id,
        "sender": "student",
        "time": datetime.now()
    })
    new_document = {
        "message": out,
        "id": id,
        "sender": "seller",
        "time": datetime.now()
    }
    db.messages.insert_one(new_document)
    return out    
    



