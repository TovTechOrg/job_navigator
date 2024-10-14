from pymongo import MongoClient
from utils import parse_years_of_experience, find_intersection_ignore_case
from bson import ObjectId

class Matcher:

    # Initiate mongo db client
    def __init__(self):
        self.client = MongoClient("mongodb+srv://raz:eUpWPQnWTPa3sjqE@cluster0.6d4vc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    
    # Fetch job by job_id
    def fetch_job(self, job_id):
        job_search_db = self.client.job_search_db
        CV_db = self.client.CV_db
        job_oid = ObjectId(job_id)
        job = job_search_db.jobs.find_one({"_id" : job_oid})
        return job


    # This method fetches all jobs
    def fetch_all_jobs(self):
        job_search_db = self.client.job_search_db
        jobs = job_search_db.jobs.find().limit(2)
        return jobs

    # This method returns all candidates
    def fetch_all_candidates(self):
        CV_db = self.client.CV_db
        cvs = CV_db.CV_collection.find()
        return cvs

    # Fetches canidates whom have not been matched yet 
    def fetch_matchless_candidates(self):
        job_search_db = self.client.job_search_db
        matches = job_search_db.matches.find({}, {"candidate_id": 1})
        candidate_ids = set()

        # Create a set containing all candidate_id's found in matches collection
        for match in matches:
            candidate_ids.add(str(match["candidate_id"]))

        # Fetch all candidates in the databse
        candidates = self.fetch_all_candidates()
        
        # Filter out all candidates that have not been matched
        unmatched_candidates = [candidate for candidate in candidates if str(candidate['_id']) not in candidate_ids]
        return unmatched_candidates
        

    # Determine if candidate years of experience is greater or equal to job min years of experience
    def find_years_of_experience_match(self, job, candidate):
        min_years_experience = parse_years_of_experience(job["minimum_experience"])
        candidate_years_of_experience = candidate["years_of_experience"]

        if (candidate_years_of_experience == None):
            candidate_years_of_experience = 0
 
        if (candidate_years_of_experience >= min_years_experience):
            return True
        
        return False

    
    # Updates matches collection using job_id, candidate_id and match value
    def score(self, job_id, candidate_id, match):
        job_search_db = self.client.job_search_db
        matches = job_search_db.matches
        job_id = ObjectId(job_id)
        candidate_id = ObjectId(candidate_id) 

        document = {"job_id": job_id, "candidate_id": candidate_id, "match": match}
        matches.insert_one(document)

    # Creates new matches collection
    def clean_data(self):
            job_search_db = self.client.job_search_db
            job_search_db.matches.drop()


    # Update collection matches with new candidates
    def generate_matches(self):
        jobs = self.fetch_all_jobs()
        candidates = self.fetch_matchless_candidates()
        print("Adding " + str(len(candidates)) + " candidates")

        matches = {}

        for job in jobs:
            job_fields_of_expertise = job["field_of_expertise"].split(",")
            job_education_list = job["education"].split(",")
            job_id = str(job["_id"])
            
            # For each candidate
            for candidate in candidates:
                candidate_id = str(candidate['_id'])
                candidate_fields_of_expertise = candidate["field_of_expertise"]
                candidate_education_list = candidate["Education"].split(",")

                # Test job and candidate against criterias
                common_education_list = find_intersection_ignore_case(job_education_list, candidate_education_list)
                common_fields_of_expertise =  find_intersection_ignore_case(job_fields_of_expertise, candidate_fields_of_expertise)
                min_years_matched = self.find_years_of_experience_match(job, candidate)

                # Determine if candidate matches job criterias
                if any(common_fields_of_expertise) and any(common_education_list) and min_years_matched:
                    self.score(job_id, candidate_id, True)
                else:
                    self.score(job_id, candidate_id, False)
