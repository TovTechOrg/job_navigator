from matcher import Matcher
from utils import find_intersection_ignore_case


matcher = Matcher()
# matcher.clean_data()
candidates = matcher.fetch_matchless_candidates()

print("Total unmatched: " + str(len(candidates)))
matcher.generate_matches()

