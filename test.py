from matcher import Matcher


matcher = Matcher()
matches = matcher.generate_matches()

for job_id, candidates in matches.items():
    print(f"job_id: {job_id}")

    job = matcher.fetch_job(job_id)
    job_fields_of_expertise = job["field_of_expertise"].split(",")

    # print(job_fields_of_expertise)

    for candidate in candidates:
        print(f"\tcandidate_id: {candidate["_id"]}")

        # Verify fields of expertise
        candidate_fields_of_expertise = candidate["field_of_expertise"]
        # print(candidate_fields_of_expertise)

        common_fields = list(set(job_fields_of_expertise) & set(candidate_fields_of_expertise))

        for field in common_fields:
            print(f"\tCommon field of expertise: {field}")

        # Verify min
        minimum_experience = job["minimum_experience"]
        years_of_experience = candidate["years_of_experience"]

        print(f"\tjob minimum years of experience: {minimum_experience}")
        print(f"\tcandidate years of experience: {years_of_experience}")




        