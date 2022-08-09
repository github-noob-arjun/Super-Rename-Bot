import pymongo 
import os

DB_NAME = "Oetdv2_bot_data" #os.environ.get("DB_NAME","")

DB_URL = "mongodb+srv://A:A@cluster0.i6jm9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority" #os.environ.get("DB_URL","")
# urop France DB_URL = "mongodb+srv://A:A@cluster0.bh1tfaq.mongodb.net/?retryWrites=true&w=majority"
#DB_URL = "mongodb+srv://A:A@cluster0.khyoll5.mongodb.net/?retryWrites=true&w=majority"
mongo = pymongo.MongoClient(DB_URL)
db = mongo[DB_NAME]
dbcol = db["user"]

def insert(chat_id):
    user_id = int(chat_id)
    user_det = {"_id": user_id,"file_id": None, "caption": None}
    try:
      dbcol.insert_one(user_det)
    except:
      pass

def addthumb(chat_id, file_id):
    dbcol.update_one({"_id": chat_id},{"$set":{"file_id": file_id}})
	
def delthumb(chat_id): 
    dbcol.update_one({"_id": chat_id},{"$set":{"file_id": None}})

def find(chat_id):
    id =  {"_id":chat_id}
    x = dbcol.find(id)
    for i in x:
         thumb = i["file_id"]
         return [thumb]

def getid():
    values = []
    for key  in dbcol.find():
         id = key["_id"]
         values.append((id)) 
    return values
