from matcher import Matcher
from utils import find_intersection_ignore_case


matcher = Matcher()
matches = matcher.generate_matches()

for job_id, candidates in matches.items():
    print(f"job_id: {job_id}")

    job = matcher.fetch_job(job_id)
    job_fields_of_expertise = job["field_of_expertise"].split(",")
    job_education_list = job["education"].split(",")
    # print(job_fields_of_expertise)
    

    for candidate in candidates:
        candidate_name = candidate.get("name", "Unknown")
        print(f"\tcandidate_id: {candidate["_id"]}")
        print(f"\tcandidate name: {candidate_name}")
        

        # Verify fields of expertise
        candidate_fields_of_expertise = candidate["field_of_expertise"]
        candidate_education_list = candidate["Education"].split(",")
        # print(candidate_fields_of_expertise)

       
        common_fields_of_expertise = find_intersection_ignore_case(job_fields_of_expertise, candidate_fields_of_expertise)
        common_education = find_intersection_ignore_case(job_education_list, candidate_education_list)

        # for field in common_fields_of_expertise:
        print(f"\tCommon field of expertise: {common_fields_of_expertise}")
        print(f"\tCommon educations: {common_education}")

        # Verify min
        minimum_experience = job["minimum_experience"]
        years_of_experience = candidate["years_of_experience"]

        print(f"\tjob minimum years of experience: {minimum_experience}")
        print(f"\tcandidate years of experience: {years_of_experience}")


        