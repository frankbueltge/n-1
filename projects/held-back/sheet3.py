"""Project 15 session 3: draws 20 cleared entries (seed 20261024) for the blind check of the pre-filter (SESSION3.md)."""
import json, random
o = [x for x in json.load(open('filter3.json')) if x['verdict'] == 'cleared']
random.seed(20261024)
pick = random.sample(o, min(20, len(o)))
json.dump([{'n': i + 1, 'treaty': x['treaty'], 'state': x['state']} for i, x in enumerate(pick)], open('sheet3.json', 'w'), indent=0)
