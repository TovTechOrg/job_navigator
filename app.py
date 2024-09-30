from pymongo import MongoClient
from utils import parse_years_of_experience
from bson import ObjectId

# Connect to remote database
try:
    client = MongoClient("mongodb+srv://raz:eUpWPQnWTPa3sjqE@cluster0.6d4vc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    job_search_db = client.job_search_db
    CV_db = client.CV_db
    print("Connection to MongoDB successful")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")


# This method fetches all jobs
def fetchJobs():
    jobs = job_search_db.jobs.find().limit(1)
    return jobs

# This method returns all CV's based on criteria
def fetchCVs(criteria):
    cvs = CV_db.CV_collection.find(criteria)
    return cvs

# Creates new matches collection with a match record for each job and candidate (job_id_ candidate_id, False)
def clean_data():
        job_search_db.matches.drop()
        matches = job_search_db.matches

        jobs = fetchJobs()
    
        # Update table matches (job_id, candidate_id, match)
        for job in jobs:
            candidates = fetchCVs({})
            job_id = ObjectId(job["_id"])
            # print("Job_Id: " + str(job_id))

            for candidate in candidates:
                candidate_id = ObjectId(candidate['_id']) 
                # print("Candidate_id: " + str(candidate_id))
                document = {"job_id": job_id, "candidate_id": candidate_id, "match": False}
                matches.insert_one(document)



# Returns matching CV's to job based on years of experience 
def match(job):
    min_years_experience = parse_years_of_experience(job["minimum_experience"])
    criteria = {"years_of_experience": {"$gte": min_years_experience}}
    candidates = fetchCVs(criteria)

    return candidates

# Updates matches collection given job_id, candidate_id and match value
def score(job_id, candidate_id, match):
    matches = job_search_db.matches
    job_id = ObjectId(job_id)
    candidate_id = ObjectId(candidate_id) 

    filter_query = {
        'job_id': job_id,  # First condition
        'candidate_id': candidate_id   # Second condition
    }

    update_operation = {
        '$set': {'match': match}  # Update or set new values
    }

    matches.update_one(filter_query, update_operation)

# Main method
def main():
    # Update collection matches (job_id, candidate_id, False)
    clean_data()

    jobs = fetchJobs()
    matches = {}

    # For each job fetch candidates that meet criteria 
    # (cv.years_of_experience >= job.minimal_experience_years
    # cv.field_of_expertise in job.field_of_expertise
    for job in jobs:
        candidates = match(job)
        job_field_of_expertise = job["field_of_expertise"]
        job_id = str(job["_id"])


        # For each candidate that meets minimum experience years
        for candidate in candidates:
            candidate_id = str(candidate['_id'])

            # Verifiy that at least one of cv.field_of_expertise matches at least one jobs.field_of_expertise
            fields_of_expertise = candidate["field_of_expertise"]
            # print(fields_of_expertise)

            for field in fields_of_expertise:
                # Check if field in job.field_of_expertise
                if (field in job_field_of_expertise):
                    print (f"Found a match {job_id}, {candidate_id}")
                    if job_id in matches:
                        matches[job_id].append(candidate)
                    else:
                        matches[job_id] = [candidate]
                    score(job_id, candidate_id, True)
                    break


if __name__ == "__main__":
    main()

