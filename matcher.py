from pymongo import MongoClient
from utils import parse_years_of_experience, find_intersection_ignore_case
from bson import ObjectId

class Matcher:

    # Initiate mongo db client
    def __init__(self):
        self.client = MongoClient("mongodb+srv://raz:eUpWPQnWTPa3sjqE@cluster0.6d4vc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    
    def fetch_job(self, job_id):
        job_search_db = self.client.job_search_db
        job_oid = ObjectId(job_id)
        job = job_search_db.jobs.find_one({"_id" : job_oid})
        return job


    # This method fetches all jobs
    def fetch_all_jobs(self):
        job_search_db = self.client.job_search_db
        jobs = job_search_db.jobs.find()
        return jobs

    # This method returns all CV's based on criteria
    def fetch_candidates(self, criteria):
        CV_db = self.client.CV_db
        cvs = CV_db.CV_collection.find(criteria)
        return cvs


    # Returns matching CV's to job based on years of experience 
    def find_matching_candidates(self, job):
        min_years_experience = parse_years_of_experience(job["minimum_experience"])
        criteria = {"years_of_experience": {"$gte": min_years_experience}}
        candidates = self.fetch_candidates(criteria)

        return candidates
    
    # Updates matches collection given job_id, candidate_id and match value
    def score(self, job_id, candidate_id, match):
        job_search_db = self.client.job_search_db
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

    # Creates new matches collection with a match record for each job and candidate (job_id_ candidate_id, False)
    def clean_data(self):
            job_search_db = self.client.job_search_db
            job_search_db.matches.drop()
            matches = job_search_db.matches

            jobs = self.fetch_all_jobs()
        
            # Update table matches (job_id, candidate_id, match)
            for job in jobs:
                candidates = self.fetch_candidates({})
                job_id = ObjectId(job["_id"])
                # print("Job_Id: " + str(job_id))

                for candidate in candidates:
                    candidate_id = ObjectId(candidate['_id']) 
                    # print("Candidate_id: " + str(candidate_id))
                    document = {"job_id": job_id, "candidate_id": candidate_id, "match": False}
                    matches.insert_one(document)

    
    def generate_matches(self):
        # Update collection matches (job_id, candidate_id, False)
        self.clean_data()

        jobs = self.fetch_all_jobs()
        matches = {}

        for job in jobs:
            candidates = self.find_matching_candidates(job)
            job_fields_of_expertise = job["field_of_expertise"].split(",")
            job_education_list = job["education"].split(",")
            job_id = str(job["_id"])

            # print("Job_id: " + job_id)
            # For each candidate that meets minimum experience years
            for candidate in candidates:
                candidate_id = str(candidate['_id'])

                # Verifiy that at least one of cv.field_of_expertise matches at least one jobs.field_of_expertise
                candidate_fields_of_expertise = candidate["field_of_expertise"]
                candidate_education_list = candidate["Education"].split(",")

                common_education_list = find_intersection_ignore_case(job_education_list, candidate_education_list)
                common_fields_of_expertise =  find_intersection_ignore_case(job_fields_of_expertise, candidate_fields_of_expertise)

                if any(common_fields_of_expertise) and any(common_education_list):
                    # print (f"Found a match {job_id}, {candidate_id}")

                    if job_id in matches:
                        matches[job_id].append(candidate)
                    else:
                        matches[job_id] = [candidate]
                    self.score(job_id, candidate_id, True)
        
        return matches