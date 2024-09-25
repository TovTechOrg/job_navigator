from pymongo import MongoClient


# Connect to remote database
try:
    client = MongoClient("mongodb+srv://raz:eUpWPQnWTPa3sjqE@cluster0.6d4vc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.job_search_db
    print("Connection to MongoDB successful")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")



def fetchJobDescriptions():
    collection = db.jobs.find().limit(10)
    
    return collection



job_descriptions = fetchJobDescriptions()

for js in job_descriptions:
    print(js['title'])