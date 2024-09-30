from pymongo import MongoClient
from utils import parse_years_of_experience

# Connect to remote database
try:
    client = MongoClient("mongodb+srv://raz:eUpWPQnWTPa3sjqE@cluster0.6d4vc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    job_search_db = client.job_search_db
    CV_db = client.CV_db
    print("Connection to MongoDB successful")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")


# Services that fetch data
def fetchJobs():
    jobs = job_search_db.jobs.find().limit(1)
    return jobs

def fetchCVs():
    cvs = CV_db.CV_collection.find().limit(10)
    return cvs

def fetchCVs(criteria):
    cvs = CV_db.CV_collection.find(criteria)
    return cvs

# Matches 
def match(job):
    min_years_experience = parse_years_of_experience(job["minimum_experience"])


    print("Min Years Of Experience: " + str(min_years_experience))
    
    criteria = {"years_of_experience": {"$gte": min_years_experience}}
    candidates = fetchCVs(criteria)

    return candidates


def main():
    jobs = fetchJobs()
    matches = {}

    for job in jobs:
        candidates = match(job)
        job_field_of_expertise = job["field_of_expertise"]
        job_id = job["_id"]


        for candidate in candidates:
            id = candidate['_id']
        
            parse_years_of_experience = str(candidate["years_of_experience"])

            print("id: " + str(id))
            print( "years of experience: " + parse_years_of_experience)

            # Decide if field_of_expertise 
            field_of_expertise = candidate["field_of_expertise"]

            for field in field_of_expertise:
                # Check if field in job.field_of_expertise
                if (field in job_field_of_expertise):
                    matches[job_id].append(candidate)
                    break


if __name__ == "__main__":
    main()

