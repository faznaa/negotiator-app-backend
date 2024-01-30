import openai
import requests
from openai import OpenAI
import os
import json
from setup import *
from prompt import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

uri ="mongodb+srv://user1:fazna@cluster0.rbfdb.mongodb.net/?retryWrites=true&w=majority"
client_mongo = MongoClient(uri, server_api=ServerApi('1'))
try:
    client_mongo.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

except Exception as e:
    print(e)

db = client_mongo["negotiation_app"]  
collection = db["messages"]

openai.api_key = OPEN_AI_API_KEY
os.environ['OPENAI_API_KEY'] = OPEN_AI_API_KEY


client = openai



def get_response_from_openai(prompt_in):
  try:

    client = OpenAI()

    response = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {
          "role": "user",
          "content": prompt_in
        }
      ],
      temperature=1,
      max_tokens=3000,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response.choices[0].message.content
  except Exception as e:
    print(e)



def get_rsponse_from_model(prompt):
        try:
            output = get_response_from_openai(prompt)
            return output
        except Exception as e:
                return "Open ai Error"
        
def get_clean_openai_res(promot_in):
    res=get_response_from_openai(promot_in)
    new_res = json.loads(res)
    return new_res


def format_conversation(conversation):
    conversation_str = ""
    for entry in conversation:
        message = entry['message']
        sender = entry['sender']
        if sender == "student":
            conversation_str += f"Student: {message}\n"
        else:
            conversation_str += f"Seller: {message}\n"
    return conversation_str

def get_sample_conersation(selected_concern, concern_dict):
 
    return concern_dict.get(selected_concern)


 
# def chatInput():

        
#     patient="Sam"
#     patient_data=""
#     query = {"user": patient}

#     documents = collection.find(query).sort("time", 1)

#     conversation_memory = [{"question": doc.get("question", ""), "answer": doc.get("answer", "")} for doc in documents]

#     final_prompt=Prompt_chat.format(patient_data,prompt_swelling,conversation_memory)
#     out=get_rsponse_from_model(final_prompt)
#     print(out)
#     res=input("Enter resposne : ")

#     new_document = {"question": out,"answer":res,
#                         "user":"Sam","time":datetime.now()}  

#     result = db.collection.insert_one(new_document)

#     chatInput()

   

# chatInput()
        


