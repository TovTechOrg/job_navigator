from pymongo import MongoClient


# Connect to remote database
try:
    client = MongoClient("mongodb+srv://raz:eUpWPQnWTPa3sjqE@cluster0.6d4vc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    job_search_db = client.job_search_db
    CV_db = client.CV_db
    print("Connection to MongoDB successful")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")



def fetchJobs():
    jobs = job_search_db.jobs.find().limit(1)
    return jobs

def fetchCVs():
    cvs = CV_db.CV_collection.find().limit(1)
    return cvs

jobs = fetchJobs()
print("Printing jobs ...")
for job in jobs:
    print(job['title'])

cvs = fetchCVs()
print("Printing cvs ...")
for cv in cvs:
    print(cv['field_of_expertise'])